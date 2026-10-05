#!/usr/bin/env bash
# Публикация во все хабы. Перед запуском: huggingface-cli login ; ollama signin ; pip install modelscope kaggle
set -e; BRAND=${BRAND:-QAZTECH-Tutor}; ORG=${ORG:-qaztech}; B=$BRAND-8B
cp README.md TRADEMARK.md $B/README.md
# 1) Hugging Face: веса + GGUF (LM Studio, Jan, GPT4All читают отсюда автоматически)
huggingface-cli upload $ORG/$B $B .
huggingface-cli upload $ORG/$B-GGUF . . --include "*.gguf" --include "Modelfile" --include "README.md TRADEMARK.md"
# 2) Ollama library: ollama run $ORG/tutor
ollama create $ORG/tutor -f Modelfile && ollama push $ORG/tutor
# 3) ModelScope (Китай/Азия)
python - <<PY
from modelscope.hub.api import HubApi; a=HubApi(); a.login(open('/dev/stdin').read().strip()) if False else None
PY
modelscope upload $ORG/$B $B || echo "ModelScope: выполните modelscope login и повторите"
# 4) Kaggle Models
kaggle models init -p $B 2>/dev/null; kaggle models create -p $B || true
echo "Опубликовано. Добавьте ссылки в GitHub README и подайте PR в awesome-списки (awesome-llm, awesome-kazakh-nlp)."
