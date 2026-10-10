---
license: apache-2.0
base_model: qaztech-platform/QAZTECH-Tutor-8B
base_model_relation: quantized
language: [en, ru, kk, ar, es]
tags: [gguf, ollama, llama.cpp, education, tutor, azure, multilingual]
---
# QAZTECH® Tutor 8B (v0.2 preview), GGUF

Quantized builds of [QAZTECH Tutor 8B](https://huggingface.co/qaztech-platform/QAZTECH-Tutor-8B).

| File | Size | Use |
|---|---|---|
| QAZTECH-Tutor-8B-Q4_K_M.gguf | 5.0 GB | recommended |
| QAZTECH-Tutor-8B-Q8_0.gguf | 8.7 GB | higher fidelity |

Ollama: `ollama run qaztech-platform/tutor`, or download the Q4_K_M file and `Modelfile` and run `ollama create tutor -f Modelfile`.

Limitations, licence, attribution and trademark: see the main model card.
