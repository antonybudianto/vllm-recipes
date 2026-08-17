
```sh
docker exec -it 99144ee1ecf5 python3 -c "
import json, urllib.request, time

url = 'http://localhost:8000/v1/completions'
# Using a slightly longer prompt to get an accurate PP measurement
prompt = 'Write a detailed Python function to binary search a sorted array. ' * 10
payload = json.dumps({
    'model': 'qwen38-27b-mtp-nvfp4',
    'prompt': prompt,
    'max_tokens': 1,  # 1 output token to isolate Prompt Processing / TTFT
}).encode()

req = urllib.request.Request(url, payload, {'Content-Type': 'application/json'})

t0 = time.time()
with urllib.request.urlopen(req) as resp:
    res = json.load(resp)
t1 = time.time()

prompt_tokens = res['usage']['prompt_tokens']
ttft = t1 - t0
pp_speed = prompt_tokens / ttft

print(f'Prompt Tokens: {prompt_tokens}')
print(f'TTFT (Prefill Latency): {ttft*1000:.1f} ms')
print(f'PP Speed (Prompt Processing): {pp_speed:.1f} tok/s')
"
```
