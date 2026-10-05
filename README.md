---
license: apache-2.0
base_model: Qwen/Qwen3-8B
language: [en, ru, kk, ar, es]
tags: [education, tutor, microsoft-certification, engineering, kazakh]
pipeline_tag: text-generation
---
# QAZTECH® Tutor 8B
**QAZTECH Tutor** — многоязычный ИИ-наставник для инженеров: объясняет материалы Microsoft, готовит к сертификациям, работает на английском, русском, казахском, арабском и испанском.
Базовая модель: Qwen3-8B (Apache 2.0). Дообучение: LoRA на синтетических диалогах «студент–наставник» и экзаменационных вопросах, сгенерированных из материалов Microsoft Learn (CC BY 4.0).

## Запуск
```bash
ollama run qaztech-platform/tutor
```
```python
from transformers import pipeline
p = pipeline("text-generation", "qaztech-platform/QAZTECH-Tutor-8B")
print(p([{"role":"user","content":"Объясни Azure RBAC и задай мне вопрос."}], max_new_tokens=400)[0]["generated_text"][-1])
```
## Ограничения
Факты проверяйте по официальной документации; для экзаменационной точности используйте модель вместе с RAG. Не содержит реальных экзаменационных вопросов Microsoft.

## Лицензия и товарный знак
Веса и код: Apache 2.0. Указание авторства Qwen (Alibaba) и Microsoft Learn обязательно.

**QAZTECH** is a registered trade mark of QAZTECH in the United Kingdom (UK IPO) and a trade mark in other jurisdictions. The Apache 2.0 licence does not grant any right to use the QAZTECH name or logo (see §6 of the licence). Derivative models and products must not use "QAZTECH" in their names or branding without written permission; please describe them as "based on QAZTECH Tutor".
