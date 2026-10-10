#!/usr/bin/env bash
# Stage 08: convert the merged model to GGUF, quantize (Q4_K_M, Q8_0) and build the Ollama model.
# Requires the merge/export environment (requirements/merge-export.txt) and cmake.
set -euo pipefail
ROOT=${ROOT:-$HOME/tutor}; PY=${PY:-$HOME/mergeenv/bin/python}
MODEL=${MODEL:-$ROOT/QAZTECH-Tutor-8B}; OUT=$ROOT/gguf; NAME=QAZTECH-Tutor-8B
mkdir -p "$OUT"; cd "$ROOT"
[ -d llama.cpp ] || git clone --depth 1 https://github.com/ggml-org/llama.cpp
"$PY" -m pip install -q ./llama.cpp/gguf-py sentencepiece protobuf
cmake -S llama.cpp -B llama.cpp/build -DGGML_CUDA=OFF -DLLAMA_CURL=OFF >/dev/null
cmake --build llama.cpp/build --target llama-quantize -j "$(nproc)" >/dev/null
"$PY" llama.cpp/convert_hf_to_gguf.py "$MODEL" --outfile "$OUT/$NAME-F16.gguf" --outtype f16
for q in Q4_K_M Q8_0; do
  llama.cpp/build/bin/llama-quantize "$OUT/$NAME-F16.gguf" "$OUT/$NAME-$q.gguf" "$q"
done
# Ollama 0.35 quantizes at create time only for safetensors imports, so build from the Q4_K_M file.
# deploy/Modelfile uses the official Qwen3 template (hides the empty <think></think> block).
cp "$(dirname "$0")/../deploy/Modelfile" "$OUT/Modelfile"
(cd "$OUT" && ollama create qaztech-platform/tutor -f Modelfile)
ls -la "$OUT"/*.gguf
