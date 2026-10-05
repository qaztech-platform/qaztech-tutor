#!/usr/bin/env bash
# GGUF для Ollama / LM Studio / llama.cpp
set -e; B=${BRAND:-QAZTECH-Tutor}-8B
git clone --depth 1 https://github.com/ggml-org/llama.cpp && pip install -r llama.cpp/requirements.txt
cmake -B llama.cpp/build llama.cpp && cmake --build llama.cpp/build -j --target llama-quantize
python llama.cpp/convert_hf_to_gguf.py $B --outfile $B-f16.gguf --outtype f16
for q in Q4_K_M Q8_0; do llama.cpp/build/bin/llama-quantize $B-f16.gguf $B-$q.gguf $q; done
cat > Modelfile <<MF
FROM ./$B-Q4_K_M.gguf
PARAMETER temperature 0.7
LICENSE "Apache-2.0"
MF
echo "готово: $B-f16.gguf $B-Q4_K_M.gguf $B-Q8_0.gguf Modelfile"
