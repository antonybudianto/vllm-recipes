$MODEL = if ($env:MODEL) { $env:MODEL } else { "sakamakismile/Qwen3.8-27B-MTP-NVFP4" }
$SERVED_MODEL = if ($env:SERVED_MODEL) { $env:SERVED_MODEL } else { "qwen38-27b-mtp-nvfp4" }

docker run --gpus all --ipc=host `
  -p "8000:8000" `
  -v ${HOME}/.cache/huggingface:/root/.cache/huggingface `
  -v ${HOME}/.cache/vllm:/root/.cache/vllm `
  vllm/vllm-openai:latest `
  --model "${MODEL}" `
  --served-model-name "${SERVED_MODEL}" `
  --tensor-parallel-size 2 `
  --max-model-len 156000 `
  --max-num-seqs 1 `
  --gpu-memory-utilization 0.90 `
  --kv-cache-dtype fp8 `
  --speculative-config '{\"method\":\"qwen3_5_mtp\",\"num_speculative_tokens\":3}' `
  --tool-call-parser qwen3_xml `
  --reasoning-parser qwen3 `
  --enable-auto-tool-choice `
  --language-model-only `
  --generation-config vllm `
  --disable-custom-all-reduce `
  --enable-prefix-caching `
  --override-generation-config '{\"temperature\":1.0,\"top_p\":0.95,\"top_k\":20,\"min_p\":0.0,\"presence_penalty\":0.0,\"repetition_penalty\":1.0}'
