#!/usr/bin/env bash
# Публикация QAZTECH Tutor 8B на все площадки.
# Запуск из папки, где лежат: QAZTECH-Tutor-8B/ (веса), *.gguf, Modelfile, README.md, TRADEMARK.md
set -u
B=${B:-QAZTECH-Tutor-8B}
HF_ORG=${HF_ORG:-qaztech-platform}
OLLAMA_NS=${OLLAMA_NS:-qaztech-platform}
MS_ORG=${MS_ORG:-qaztechplatform}
KAGGLE_USER=${KAGGLE_USER:-qaztechplatform}
export PATH=$HOME/hfenv/bin:$PATH

cp README.md TRADEMARK.md "$B"/ 2>/dev/null

echo "== 1/4 Hugging Face"
hf upload "$HF_ORG/$B" "$B" . || echo "HF: ошибка загрузки весов"
hf upload "$HF_ORG/$B-GGUF" . . --include "*.gguf" --include "Modelfile" --include "README.md" --include "TRADEMARK.md" || echo "HF: ошибка загрузки GGUF"

echo "== 2/4 Ollama ($OLLAMA_NS/tutor)"
ollama create "$OLLAMA_NS/tutor" -f Modelfile && ollama push "$OLLAMA_NS/tutor" || echo "Ollama: ошибка"

echo "== 3/4 ModelScope"
modelscope upload "$MS_ORG/$B" "$B" || modelscope upload "qaztech/$B" "$B" || echo "ModelScope: выполните modelscope login и проверьте одобрение организации"

echo "== 4/4 Kaggle (приватно, проверьте перед публикацией)"
rm -rf kg_model kg_instance && mkdir kg_model kg_instance
cat > kg_model/model-metadata.json <<'J1'
{"ownerSlug":"qaztechplatform","title":"QAZTECH Tutor 8B","slug":"qaztech-tutor-8b","subtitle":"Open multilingual AI tutor for engineers (EN/RU/KK/AR/ES)","isPrivate":true,"description":"QAZTECH Tutor 8B: multilingual AI tutor fine-tuned from Qwen3-8B (Apache 2.0). QAZTECH is a registered trade mark of AISC Technologies LTD (UK IPO).","publishTime":"","provenanceSources":"https://github.com/qaztech-platform/qaztech-tutor"}
J1
cat > kg_instance/model-instance-metadata.json <<'J2'
{"ownerSlug":"qaztechplatform","modelSlug":"qaztech-tutor-8b","instanceSlug":"transformers-8b","framework":"transformers","overview":"LoRA-merged Qwen3-8B tutor.","usage":"See README.md","licenseName":"Apache 2.0","fineTunable":true,"trainingData":[],"modelInstanceType":"Unspecified","baseModelInstanceId":0,"externalBaseModelUrl":"https://huggingface.co/Qwen/Qwen3-8B"}
J2
cp -r "$B"/. kg_instance/
kaggle models create -p kg_model || echo "Kaggle: ошибка создания модели"
kaggle models instances create -p kg_instance || echo "Kaggle: ошибка загрузки версии"

echo "Готово. Репозитории Hugging Face остаются закрытыми, пока не откроете их вручную."
