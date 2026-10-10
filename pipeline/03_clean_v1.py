import json, re, os, random, collections
D = os.path.expanduser("~/tutor/data")
rows = []
for l in open(f"{D}/train.jsonl", encoding="utf-8"):
    try: rows.append(json.loads(l))
    except Exception: pass
cnt = lambda p, t: len(re.findall(p, t))
CYR = r'[А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүҺһІі]'
def lang(t):
    if cnt(r'[\u0600-\u06FF]', t) > 3: return "ar"
    if cnt(CYR, t) > 3: return "kk" if cnt(r'[әғқңөұүһӘҒҚҢӨҰҮҺ]', t) >= 2 else "ru"
    return "es" if cnt(r'[¿¡ñáéíóú]', t.lower()) >= 2 else "en"
grp = lambda L: {"ar": "ar", "kk": "cyr", "ru": "cyr"}.get(L, "lat")
why = collections.Counter(); good = []; seen_u = set(); seen_a = set()
for r in rows:
    u, a = r["messages"][1]["content"], r["messages"][2]["content"]; both = u + " " + a
    if cnt(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', both): why["иероглифы"] += 1; continue
    if cnt(r'[\u0600-\u06FF]', both) and cnt(CYR, both): why["смесь_алфавитов"] += 1; continue
    if grp(lang(u)) != grp(lang(a)): why["язык_вопроса≠ответа"] += 1; continue
    if re.search(r'"(user|assistant)"\s*:', both): why["утечка_json"] += 1; continue
    ku = re.sub(r'\W+', ' ', u.lower()).strip(); ka = re.sub(r'\W+', ' ', a.lower())[:100]
    if ka in seen_a: why["дубль"] += 1; continue
    seen_u.add(ku); seen_a.add(ka); r["_lang"] = lang(a); good.append(r)
random.seed(1); random.shuffle(good)
ne = min(200, len(good) // 10); ev, tr = good[:ne], good[ne:]
def dump(name, rs):
    with open(f"{D}/{name}", "w", encoding="utf-8") as f:
        for r in rs: f.write(json.dumps({"messages": r["messages"]}, ensure_ascii=False) + "\n")
dump("train_clean.jsonl", tr); dump("eval.jsonl", ev)
by = collections.defaultdict(list)
for r in tr: by[r["_lang"]].append(r)
def review(name, rs, n):
    with open(f"{D}/{name}", "w", encoding="utf-8") as f:
        for i, r in enumerate(rs[:n], 1):
            f.write(f"## {i}\n**Вопрос:** {r['messages'][1]['content']}\n\n**Ответ:**\n{r['messages'][2]['content']}\n\n**Оценка 1-5 и замечания:**\n\n---\n")
review("review_kk.md", by["kk"], 40); review("review_ar.md", by["ar"], 40)
review("review_tech.md", by["ru"][:10] + by["en"][:10] + by["es"][:10], 30)
print(f"ВСЕГО {len(rows)} -> ГОДНЫХ {len(good)} (обучение {len(tr)}, проверка {len(ev)})")
print("ЭКЗАМЕНАЦИОННЫХ:", sum(1 for r in good if re.search(r"(?m)^\s*A[\).]|Ответ:|Answer:|Respuesta:|الإجابة", r["messages"][2]["content"])))
print("ОТСЕЯНО:", dict(why)); print("ЯЗЫКИ:", {k: len(v) for k, v in by.items()})
