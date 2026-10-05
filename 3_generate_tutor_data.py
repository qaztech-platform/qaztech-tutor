# Час 3: синтетика «студент-наставник» + экзаменационные вопросы из ВАШИХ материалов.
# На Spark: pip install ollama ; python 3_generate_tutor_data.py  (фон 3-6 ч)
import json, random, glob, os, ollama
TEACHER = "qwen3:32b"; N = int(os.environ.get("N", "6000"))
LANGS = {"en": "английском", "ru": "русском", "kk": "казахском", "ar": "арабском", "es": "испанском"}
chunks = []
for p in glob.glob(os.path.expanduser("~/tutor/materials/**/*.md"), recursive=True):
    t = open(p, encoding="utf-8", errors="ignore").read()
    chunks += [t[i:i+2500] for i in range(0, len(t), 2500) if len(t[i:i+2500]) > 800]
assert chunks, "положите .md из Microsoft Learn (github.com/MicrosoftDocs, CC BY 4.0) в ~/tutor/materials"
MODES = [
 "Сыграй наставника: студент задаёт вопрос по теме, ты объясняешь по шагам, в конце задаёшь проверочный вопрос.",
 "Студент дал неверный ответ по теме; ты наводящими вопросами (сократовский метод) подводишь его к правильному.",
 "Составь экзаменационный вопрос в стиле сертификации Microsoft (4 варианта, один верный) и подробный разбор, почему остальные неверны.",
 "Студент просит краткое резюме темы и чек-лист для экзамена; дай их компактно.",
]
def ask(p):
    r = ollama.chat(TEACHER, [{"role":"user","content":p}], options={"temperature":0.8})
    return r["message"]["content"].strip()
out = open(os.path.expanduser("~/tutor/data/train.jsonl"), "a", encoding="utf-8"); kept = 0
for i in range(N):
    lang = random.choice(list(LANGS)); ch = random.choice(chunks); mode = random.choice(MODES)
    txt = ask(f"Материал:\n{ch}\n\n{mode} Весь диалог на {LANGS[lang]} языке. "
              f"Формат строго JSON: {{\"user\": \"реплика студента\", \"assistant\": \"ответ наставника\"}}. Только JSON.")
    txt = txt.split("</think>")[-1].strip().removeprefix("```json").removesuffix("```").strip()
    try: j = json.loads(txt); u, a = j["user"], j["assistant"]
    except Exception: continue
    if len(a) < 200 or len(a) > 4000: continue
    out.write(json.dumps({"messages":[{"role":"system","content":"You are an expert engineering tutor. Reply in the student's language."},
        {"role":"user","content":u},{"role":"assistant","content":a}]}, ensure_ascii=False)+"\n"); kept += 1
    if i % 100 == 0: print(i, "kept", kept, flush=True)
print("done, kept", kept)
