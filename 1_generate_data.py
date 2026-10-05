# Synthetic data: teacher writes documents, then extracts JSON from them.
# Run on Lambda: pip install vllm ; python 1_generate_data.py
import json, random, os
from vllm import LLM, SamplingParams

TEACHER = os.environ.get("TEACHER", "Qwen/Qwen2.5-14B-Instruct")
N = int(os.environ.get("N", "4000"))
KINDS = ["счёт на оплату", "заявка на закупку", "договор поставки (краткая выписка)",
         "акт выполненных работ", "накладная"]
LANGS = ["русском", "казахском", "смешанном русско-казахском"]
SCHEMA = ('{"тип_документа": str, "номер": str, "дата": "YYYY-MM-DD", "продавец": str, '
          '"покупатель": str, "сумма": number, "валюта": str, "позиции": [{"название": str, "кол": number, "цена": number}]}')

llm = LLM(TEACHER, dtype="bfloat16", max_model_len=4096)
def chat(prompts, temp, max_tokens):
    msgs = [[{"role": "user", "content": p}] for p in prompts]
    outs = llm.chat(msgs, SamplingParams(temperature=temp, top_p=0.95, max_tokens=max_tokens))
    return [o.outputs[0].text.strip() for o in outs]

# 1) generate varied documents (high temperature = diversity)
doc_prompts = [f"Напиши реалистичный текст документа: {random.choice(KINDS)} на {random.choice(LANGS)} языке. "
               f"Компании и суммы выдумай, формат оформления сделай необычным (случайный стиль, опечатки допустимы). "
               f"Верни только текст документа." for _ in range(N)]
docs = chat(doc_prompts, 1.0, 900)

# 2) teacher extracts JSON (low temperature = accuracy)
ext_prompts = [f"Извлеки данные из документа строго в JSON по схеме {SCHEMA}. Если поля нет — null. "
               f"Только JSON, без пояснений.\n\nДокумент:\n{d}" for d in docs]
answers = chat(ext_prompts, 0.0, 700)

# 3) keep only valid JSON
kept = 0
with open("train.jsonl", "w", encoding="utf-8") as f:
    for d, a in zip(docs, answers):
        a = a.strip().removeprefix("```json").removesuffix("```").strip()
        try:
            j = json.loads(a)
        except Exception:
            continue
        f.write(json.dumps({"messages": [
            {"role": "user", "content": f"Извлеки данные из документа в JSON.\n\n{d}"},
            {"role": "assistant", "content": json.dumps(j, ensure_ascii=False)}]}, ensure_ascii=False) + "\n")
        kept += 1
print(f"kept {kept}/{N}")
