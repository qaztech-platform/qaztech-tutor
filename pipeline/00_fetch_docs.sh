#!/usr/bin/env bash
# Stage 00: fetch the Azure documentation subset used as source material (CC BY 4.0)
# and configure Ollama on DGX Spark for parallel teacher generation.
set -euo pipefail
ROOT=${ROOT:-$HOME/tutor}
mkdir -p "$ROOT/materials" "$ROOT/data"
cd "$ROOT"
[ -d src ] || git clone --depth 1 --filter=blob:none --sparse https://github.com/MicrosoftDocs/azure-docs.git src
(cd src && git sparse-checkout set articles/role-based-access-control articles/virtual-network \
    articles/azure-resource-manager articles/app-service)
cp -r src/articles/* "$ROOT/materials/"
echo "Markdown files: $(find "$ROOT/materials" -name '*.md' | wc -l)"   # v0.2: 1,194

# 8 parallel requests with a 4,096-token window. Larger windows exhausted 128 GB of unified memory.
sudo mkdir -p /etc/systemd/system/ollama.service.d
printf '[Service]\nEnvironment="OLLAMA_NUM_PARALLEL=8"\nEnvironment="OLLAMA_CONTEXT_LENGTH=4096"\nEnvironment="OLLAMA_FLASH_ATTENTION=1"\n' \
  | sudo tee /etc/systemd/system/ollama.service.d/parallel.conf >/dev/null
sudo systemctl daemon-reload && sudo systemctl restart ollama
ollama pull hf.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:UD-Q4_K_XL
