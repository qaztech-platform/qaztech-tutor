#!/usr/bin/env bash
# Publish merged weights and GGUF builds to Hugging Face (organization qaztech-platform).
# Prerequisite: hf auth login (write token). Model cards: publish/hf_model_card.md, publish/hf_gguf_card.md.
set -euo pipefail
ROOT=${ROOT:-$HOME/tutor}; HERE=$(cd "$(dirname "$0")" && pwd); ORG=qaztech-platform
cp "$HERE/hf_model_card.md" "$ROOT/QAZTECH-Tutor-8B/README.md"
cp "$HERE/../TRADEMARK.md" "$ROOT/QAZTECH-Tutor-8B/TRADEMARK.md"
mkdir -p "$ROOT/hf_gguf"
ln -f "$ROOT"/gguf/QAZTECH-Tutor-8B-Q4_K_M.gguf "$ROOT"/gguf/QAZTECH-Tutor-8B-Q8_0.gguf "$ROOT/hf_gguf/"
cp "$HERE/hf_gguf_card.md" "$ROOT/hf_gguf/README.md"
cp "$HERE/../deploy/Modelfile" "$HERE/../TRADEMARK.md" "$ROOT/hf_gguf/"
hf repos create "$ORG/QAZTECH-Tutor-8B" --repo-type model --exist-ok || true
hf repos create "$ORG/QAZTECH-Tutor-8B-GGUF" --repo-type model --exist-ok || true
hf upload "$ORG/QAZTECH-Tutor-8B-GGUF" "$ROOT/hf_gguf" .
hf upload "$ORG/QAZTECH-Tutor-8B" "$ROOT/QAZTECH-Tutor-8B" .
