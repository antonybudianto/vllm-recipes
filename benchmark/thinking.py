"""Benchmark thinking on vs off (Qwen3 chat template `enable_thinking`).

  python benchmark/thinking.py            # natural stop: shows real token savings
  python benchmark/thinking.py --fixed    # ignore_eos + fixed length: pure decode speed
  python benchmark/thinking.py -n 1024     # raise the max_tokens cap
"""
import json, urllib.request, time, sys

url = 'http://localhost:8000/v1/chat/completions'
MODEL = 'qwen38-27b-mtp-nvfp4'
PROMPT = 'Write a python function to binary search an array.'
MAX_TOKENS = int(sys.argv[sys.argv.index('-n') + 1]) if '-n' in sys.argv else 256
FIXED = '--fixed' in sys.argv


def build(thinking):
    body = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': PROMPT}],
        'max_tokens': MAX_TOKENS,
        'stream': False,
        # `enable_thinking` is read by the Qwen3 chat template; `thinking` is NOT.
        'chat_template_kwargs': {'enable_thinking': thinking},
    }
    if FIXED:
        body['ignore_eos'] = True
    return json.dumps(body).encode()


def run(payload):
    req = urllib.request.Request(url, payload, {'Content-Type': 'application/json'})
    t0 = time.time()
    with urllib.request.urlopen(req) as resp:
        res = json.load(resp)
    return time.time() - t0, res


results = {}
for label, thinking in (('thinking ON', True), ('thinking OFF', False)):
    payload = build(thinking)
    run(payload)  # warmup: compile CUDA graphs / warm KV cache
    dt, res = run(payload)

    usage = res['usage']
    msg = res['choices'][0]['message']
    reasoning = msg.get('reasoning') or ''
    results[label] = (dt, usage, reasoning)

    print(f'--- {label} ---')
    print(f"Prompt Tokens: {usage['prompt_tokens']} | Completion Tokens: {usage['completion_tokens']}")
    print(f'Reasoning emitted: {"yes" if reasoning else "no"} ({len(reasoning)} chars)')
    print(f'Total Latency: {dt:.2f}s')
    print(f"End-to-End Speed: {usage['completion_tokens'] / dt:.1f} tok/s")
    if usage['completion_tokens'] >= MAX_TOKENS and not FIXED:
        print(f'WARNING: hit the {MAX_TOKENS}-token cap, output truncated. Raise it with -n.')
    print()

on_dt, on_u, _ = results['thinking ON']
off_dt, off_u, _ = results['thinking OFF']
print('--- delta (OFF vs ON) ---')
print(f"Completion tokens: {on_u['completion_tokens']} -> {off_u['completion_tokens']}")
print(f'Latency: {on_dt:.2f}s -> {off_dt:.2f}s ({(1 - off_dt / on_dt) * 100:.0f}% reduction)')
