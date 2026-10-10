import json, re, os, random, collections
D = os.path.expanduser("~/tutor/data")
def load(f):
    out = []
    p = f"{D}/{f}"
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            try: out.append(json.loads(l))
            except Exception: pass
    return out
v1 = load("train_clean.jsonl") + load("eval.jsonl"); v2 = load("v2_raw.jsonl")
cnt = lambda p, t: len(re.findall(p, t))
CYR = r'[А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүҺһІі]'; KK = r'[әғқңөұүһіӘҒҚҢӨҰҮҺІ]'
ES = set("el la los las que de en por para una un es se con del qué cómo cuál y o al lo su sus más pero como este esta".split())
EN = set("the is are to of and in for what how that with an it this be can which or on by as".split())
def lang(t):
    if cnt(r'[\u0600-\u06FF]', t) > 3: return "ar"
    if cnt(CYR, t) > 3: return "kk" if cnt(KK, t) >= 1 else "ru"
    w = re.findall(r"[a-záéíóúñü]+", t.lower())
    es = sum(x in ES for x in w) + 2 * cnt(r'[¿¡ñáéíóú]', t.lower()); en = sum(x in EN for x in w)
    return "es" if es > en else "en"
REF = re.compile(r'в вашем пример|в данном материал|в этом материал|в приведённом|в тексте выше|in your example|in the provided|in the material|material above|en tu ejemplo|en el material|في مثالك|في المادة|сіздің мысал|материалда', re.I)
def qonly(a):
    s = [x for x in re.split(r'(?<=[.!?؟])\s+', a.strip()) if x]
    return len(s) > 0 and sum(x.rstrip().endswith(("?", "؟")) for x in s) / len(s) >= 0.8
def letters(a): return set(re.findall(r'(?m)^\s*([ABCD])[\).:]', a))
def exam_ok(a):
    m = re.search(r'(?m)^\s*A[\).:]', a); stem = a[:m.start()] if m else ""
    return ("?" in stem or "؟" in stem) and len(stem.strip()) > 20 and letters(a) >= {"A", "B", "C", "D"} and bool(re.search(r'Ответ|Answer|Respuesta|Жауап|Жауаб|الإجابة|الجواب|الاجابة', a, re.I))
pairs = collections.Counter(); rej = {}; why = collections.Counter(); good = []; seen = set(); mix = collections.Counter(); exl = collections.Counter()
for tag, rows in (("v1", v1), ("v2", v2)):
    for r in rows:
        u, a = r["messages"][1]["content"], r["messages"][2]["content"]; both = u + " " + a
        ex = len(letters(a)) >= 2
        if tag == "v1" and (ex or qonly(a)): why["v1_старый_режим"] += 1; continue
        if cnt(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', both): why["иероглифы"] += 1; continue
        if cnt(r'[\u0600-\u06FF]', both) and cnt(CYR, both): why["смесь_алфавитов"] += 1; continue
        if lang(u) != lang(a): why["язык_вопроса≠ответа"] += 1; pairs[lang(u) + "->" + lang(a)] += 1; continue
        if REF.search(both): why["ссылка_на_материал"] += 1; continue
        if qonly(a): why["только_вопросы"] += 1; continue
        if ex and not exam_ok(a):
            why["экзамен_без_вопроса"] += 1; L0 = lang(a)
            if L0 not in rej:
                m0 = re.search(r"(?m)^\s*A[\).:]", a); st = a[:m0.start()] if m0 else ""
                rej[L0] = f"вопрос_перед_A={('?' in st or '؟' in st) and len(st.strip()) > 20} буквы={sorted(letters(a))} | {a[:220]!r}"
            continue
        if re.search(r'"(user|assistant)"\s*:', both): why["утечка_json"] += 1; continue
        k = re.sub(r'\W+', ' ', a.lower())[:120]
        if k in seen: why["дубль"] += 1; continue
        seen.add(k); L = lang(a); m = "экзамен" if ex else ("сократ" if tag == "v2" else "объяснение")
        good.append(r); mix[m] += 1
        if ex: exl[L] += 1
        r["_l"] = L
random.seed(7); random.shuffle(good)
ev, tr = good[:200], good[200:]
for name, rs in (("train_v2.jsonl", tr), ("eval_v2.jsonl", ev)):
    with open(f"{D}/{name}", "w", encoding="utf-8") as f:
        for r in rs: f.write(json.dumps({"messages": r["messages"]}, ensure_ascii=False) + "\n")
print(f"ВХОД: v1 {len(v1)}, v2 {len(v2)} -> ГОДНЫХ {len(good)} (обучение {len(tr)}, проверка {len(ev)})")
print("ОТСЕЯНО:", dict(why)); print("РЕЖИМЫ:", dict(mix))
print("ЯЗЫКИ:", dict(collections.Counter(r["_l"] for r in good))); print("ЭКЗАМЕН ПО ЯЗЫКАМ:", dict(exl))

print("РАСХОЖДЕНИЯ ЯЗЫКА:", dict(pairs))
for k, v in rej.items(): print("ОТБРАКОВАН ЭКЗАМЕН", k, ":", v)
