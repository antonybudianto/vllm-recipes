import json, urllib.request, time

url = 'http://localhost:8000/v1/completions'
payload = json.dumps({
    'model': 'qwen38-27b-mtp-nvfp4',
    'prompt': 'Write a python function to binary search an array.',
    'max_tokens': 256,
    'ignore_eos': True,
    'stream': False
}).encode()

# Warmup run to compile CUDA graphs / warm KV cache
req_warmup = urllib.request.Request(url, payload, {'Content-Type': 'application/json'})
urllib.request.urlopen(req_warmup)

# Timed Benchmark Run
t0 = time.time()
req = urllib.request.Request(url, payload, {'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    res = json.load(resp)
t1 = time.time()

total_time = t1 - t0
prompt_tokens = res['usage']['prompt_tokens']
completion_tokens = res['usage']['completion_tokens']

print(f'Prompt Tokens: {prompt_tokens} | Completion Tokens: {completion_tokens}')
print(f'Total Latency: {total_time:.2f}s')
print(f'End-to-End Speed: {completion_tokens / total_time:.1f} tok/s')
