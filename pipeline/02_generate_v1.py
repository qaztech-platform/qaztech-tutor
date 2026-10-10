import json, random, glob, os, re, time, threading, ollama
from concurrent.futures import ThreadPoolExecutor
TEACHER = os.environ.get("TEACHER", "qwen3:30b")
N = int(os.environ.get("N", "6000"))
OUT = os.path.expanduser(os.environ.get("OUT", "~/tutor/data/train.jsonl"))
LANGS = {"en": "английском", "ru": "русском", "kk": "казахском", "ar": "арабском", "es": "испанском"}
MODES = [
 "Сыграй наставника: студент задаёт вопрос по теме, ты объясняешь по шагам, в конце задаёшь проверочный вопрос.",
 "Студент дал неверный ответ по теме; ты наводящими вопросами (сократовский метод) подводишь его к правильному.",
 "В поле user студент просит дать тренировочный вопрос по теме материала (например: «Дай мне тренировочный вопрос по этой теме»). В поле assistant наставник пишет вопрос в стиле сертификации Microsoft с вариантами A, B, C, D (один верный), затем после слова «Ответ:» называет верный вариант и объясняет, почему он правильный, а остальные нет.",
 "Студент просит краткое резюме темы и чек-лист для экзамена; дай их компактно.",
]
chunks = []
for p in glob.glob(os.path.expanduser("~/tutor/materials/**/*.md"), recursive=True):
    t = open(p, encoding="utf-8", errors="ignore").read()
    t = re.sub(r"^---.*?---\s*", "", t, count=1, flags=re.S)
    for i in range(0, len(t), 2500):
        c = t[i:i+2500]
        if len(c) > 800: chunks.append(c)
assert chunks, "нет документации в ~/tutor/materials"
print("кусков документации:", len(chunks), flush=True)
import collections
reasons = collections.Counter()
lock = threading.Lock(); done = 0; kept = 0
out = open(OUT, "a", encoding="utf-8")
def parse(txt):
    txt = txt.split("</think>")[-1]
    a, b = txt.find("{"), txt.rfind("}")
    if a < 0 or b <= a: return None
    try: return json.loads(txt[a:b+1])
    except Exception: return None
def flat(v):
    if v is None: return ""
    if isinstance(v, str): return v
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, list): return "\n".join(flat(x) for x in v)
    if isinstance(v, dict): return "\n".join(f"{k}: {flat(x)}" for k, x in v.items())
    return str(v)

def work(_):
    global done, kept
    lang = random.choice(list(LANGS)); ch = random.choice(chunks); mode = random.choice(MODES)
    prompt = (f"Материал:\n{ch}\n\n{mode} Весь диалог на {LANGS[lang]} языке. "
              f"Формат строго JSON: {{\"user\": \"реплика студента\", \"assistant\": \"ответ наставника\"}}. Оба поля — обычный текст (строки), без вложенных объектов и массивов. Ответ наставника не длиннее 250 слов. Только JSON.")
    j = None; ok = False
    try:
        r = ollama.chat(TEACHER, [{"role": "user", "content": prompt}], options={"temperature": 0.8, "num_predict": 1800})
        j = parse(r["message"]["content"])
        reasons["done_reason=" + str(r.get("done_reason"))] += 1
        if not j: reasons["json_не_разобран"] += 1
        if j:
            bad = [k for k in ("user", "assistant") if not isinstance(j.get(k), str)]
            if bad:
                reasons["поле_не_строка"] += 1; ok = False
            else:
                u = j["user"].strip(); a = j["assistant"].strip()
                if not u: reasons["user_пуст"] += 1
                elif len(a) < 150: reasons["assistant_короткий"] += 1
                elif len(a) > 4000: reasons["assistant_длинный"] += 1
                elif a.startswith(("{", "[")): reasons["assistant_похож_на_json"] += 1
                ok = bool(u) and 150 <= len(a) <= 4000 and not a.startswith(("{", "["))
                j["user"], j["assistant"] = u, a
        else:
            ok = False
    except Exception as e:
        ok = False; reasons["исключение:" + type(e).__name__] += 1
    with lock:
        done += 1
        if ok:
            out.write(json.dumps({"messages": [
                {"role": "system", "content": "You are an expert engineering tutor. Reply in the student's language."},
                {"role": "user", "content": j["user"]}, {"role": "assistant", "content": j["assistant"]}]}, ensure_ascii=False) + "\n")
            out.flush(); kept += 1
        if done % 50 == 0: print(f"{done}/{N} принято {kept} за {time.time()-t0:.0f} с", flush=True)
t0 = time.time()
with ThreadPoolExecutor(8) as ex: list(ex.map(work, range(N)))
print(f"ГОТОВО: принято {kept} из {N} за {time.time()-t0:.0f} с")
print("ПРИЧИНЫ:", dict(reasons))
