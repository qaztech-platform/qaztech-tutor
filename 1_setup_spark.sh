#!/usr/bin/env bash
# Час 1: DGX Spark. Устанавливает Ollama + Qwen3-8B и DeepTutor.
set -e
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:8b
ollama pull qwen3:32b          # учитель для генерации данных (час 3)
pip install -U deeptutor
mkdir -p ~/tutor/data ~/tutor/materials   # в materials положите PDF/MD по Microsoft
cat > ~/tutor/.env <<ENV
LLM_BINDING=ollama
LLM_MODEL=qwen3:8b
LLM_HOST=http://127.0.0.1:11434
EMBEDDING_BINDING=ollama
EMBEDDING_MODEL=bge-m3
ENV
ollama pull bge-m3             # многоязычные эмбеддинги (ru/kk/ar/es/en)
cd ~/tutor && deeptutor init && deeptutor start
echo "DeepTutor: http://127.0.0.1:3782 — загрузите ~/tutor/materials в Knowledge Hub"
