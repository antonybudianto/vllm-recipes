# vllm-recipes

## Spec

- Intel Core i7-14700F
- Dual NVIDIA GeForce RTX 5060 Ti 16GB
- RAM 64GB DDR5

## Benchmark

```sh
python benchmark/main.py

Prompt Tokens: 10 | Completion Tokens: 256
Total Latency: 4.48s
End-to-End Speed: 57.2 tok/s
```

### Thinking on vs off

The `/v1/completions` benchmark above bypasses the chat template, so thinking never
applies. To toggle it, use `/v1/chat/completions` with `chat_template_kwargs`:
`{"enable_thinking": false}`. Note that `{"thinking": false}` is silently ignored by
the Qwen3 template.

```sh
python benchmark/thinking.py -n 2048

--- thinking ON ---
Prompt Tokens: 62 | Completion Tokens: 307
Total Latency: 6.16s
End-to-End Speed: 49.8 tok/s

--- thinking OFF ---
Prompt Tokens: 22 | Completion Tokens: 153
Total Latency: 2.65s
End-to-End Speed: 57.7 tok/s
```

Thinking off does not speed up decoding — it just emits fewer tokens. At an equal,
forced token count the two modes are the same speed:

```sh
python benchmark/thinking.py --fixed

thinking ON : 256 tokens, 4.98s, 51.4 tok/s
thinking OFF: 256 tokens, 5.08s, 50.4 tok/s
```
