import json, random, glob, os, re, time, threading, collections, ollama
from concurrent.futures import ThreadPoolExecutor
TEACHER = os.environ.get("TEACHER", "hf.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:UD-Q4_K_XL")
N = int(os.environ.get("N", "3000")); OUT = os.path.expanduser(os.environ.get("OUT", "~/tutor/data/v2_raw.jsonl"))
LANGS = {"en": "English", "ru": "Russian", "kk": "Kazakh", "ar": "Arabic", "es": "Spanish"}
ANS = {"en": "Answer:", "ru": "Ответ:", "kk": "Жауабы:", "ar": "الإجابة:", "es": "Respuesta:"}
chunks = []
for p in glob.glob(os.path.expanduser("~/tutor/materials/**/*.md"), recursive=True):
    t = re.sub(r"^---.*?---\s*", "", open(p, encoding="utf-8", errors="ignore").read(), count=1, flags=re.S)
    chunks += [t[i:i+2500] for i in range(0, len(t), 2500) if len(t[i:i+2500]) > 800]
def prompt(mode, lang, ch):
    L = LANGS[lang]
    if mode == "socratic":
        task = (f"Write one tutoring exchange in {L}. In the 'user' field, a student states a common misconception about the topic. "
                f"In the 'assistant' field, the tutor says plainly what is wrong, explains the correct answer in 2-4 sentences, and ends with exactly one check question.")
    else:
        task = (f"Write one tutoring exchange in {L}. In the 'user' field, the student asks in {L} for a practice question and names the topic in words. "
                f"In the 'assistant' field, the tutor writes a Microsoft-certification-style question that ends with a question mark, then four options on separate lines "
                f"starting with 'A)', 'B)', 'C)', 'D)' (exactly one correct), then a line starting with '{ANS[lang]}' that gives the correct letter and explains why it is right and the others are wrong.")
    return (f"Source material (the student cannot see it; never refer to 'the material', 'the text' or 'the example above'):\n{ch}\n\n{task} "
            f"Both fields must be written entirely in {L}; product names such as Azure RBAC may stay in English. The tutor's reply must be at most 250 words. "
            "Return only a JSON object {\"user\": \"...\", \"assistant\": \"...\"} whose values are plain-text strings, with no nested objects or arrays.")
def parse(txt):
    txt = txt.split("</think>")[-1]; a, b = txt.find("{"), txt.rfind("}")
    if a < 0 or b <= a: return None
    try: return json.loads(txt[a:b+1])
    except Exception: return None
lock = threading.Lock(); done = 0; kept = 0; why = collections.Counter()
out = open(OUT, "a", encoding="utf-8")
def work(_):
    global done, kept
    lang = random.choice(list(LANGS)); mode = random.choice(["exam", "exam", "exam", "socratic", "socratic"]); ch = random.choice(chunks)
    rec = None
    try:
        r = ollama.chat(TEACHER, [{"role": "user", "content": prompt(mode, lang, ch)}], options={"temperature": 0.8, "num_predict": 1800})
        j = parse(r["message"]["content"])
        if not j: why["json"] += 1
        elif not (isinstance(j.get("user"), str) and isinstance(j.get("assistant"), str)): why["не_строки"] += 1
        else:
            u, a = j["user"].strip(), j["assistant"].strip()
            if not u: why["user_пуст"] += 1
            elif not 150 <= len(a) <= 4000: why["длина"] += 1
            else: rec = {"messages": [{"role": "system", "content": "You are an expert engineering tutor. Reply in the student's language."},
                                      {"role": "user", "content": u}, {"role": "assistant", "content": a}]}
    except Exception as e: why["исключение:" + type(e).__name__] += 1
    with lock:
        done += 1
        if rec: out.write(json.dumps(rec, ensure_ascii=False) + "\n"); out.flush(); kept += 1
        if done % 100 == 0: print(f"{done}/{N} принято {kept} за {time.time()-t0:.0f} с", flush=True)
t0 = time.time()
with ThreadPoolExecutor(8) as ex: list(ex.map(work, range(N)))
print(f"ГОТОВО: принято {kept} из {N} за {time.time()-t0:.0f} с | ОТКАЗЫ: {dict(why)}")
