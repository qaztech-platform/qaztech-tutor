"""Stage 09: check that the model answers in the question's language and leaks no reasoning traces.

Usage: python 09_eval_languages.py [OLLAMA_MODEL]   (default qaztech-platform/tutor)
Exit code 1 if any check fails, so it can gate a release.
"""
import re
import sys

import ollama

MODEL = sys.argv[1] if len(sys.argv) > 1 else "qaztech-platform/tutor"
ES = {"el", "la", "los", "las", "que", "de", "en", "por", "para", "una", "es", "se", "con", "del", "qué", "cómo"}
EN = {"the", "is", "are", "to", "of", "and", "in", "for", "what", "how", "that", "with", "which"}


def lang(text: str) -> str:
    if re.search(r"[؀-ۿ]", text):
        return "ar"
    if re.search(r"[әғқңөұүһіӘҒҚҢӨҰҮҺІ]", text):
        return "kk"
    if re.search(r"[А-Яа-яЁё]", text):
        return "ru"
    words = re.findall(r"[a-záéíóúñü]+", text.lower())
    es = sum(w in ES for w in words) + 2 * len(re.findall(r"[¿¡ñáéíóú]", text.lower()))
    en = sum(w in EN for w in words)
    return "es" if es > en else "en"


TESTS = [
    ("ru", "Дай мне тренировочный вопрос по Azure RBAC"),
    ("en", "I think Azure Policy and Azure RBAC do the same thing."),
    ("kk", "Azure-дағы ресурс тобы деген не? Қысқаша түсіндіріңіз."),
    ("ar", "ما الفرق بين Azure RBAC و Azure Policy؟"),
    ("es", "¿Puedes darme una pregunta de práctica sobre plantillas ARM?"),
]

passed = 0
for expected, prompt in TESTS:
    answer = ollama.chat(MODEL, [{"role": "user", "content": prompt}])["message"]["content"]
    ok = lang(answer) == expected and "<think>" not in answer
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] {expected}: detected={lang(answer)} think_leak={'<think>' in answer}\n{answer[:300]}\n")
print(f"{passed}/{len(TESTS)} passed")
sys.exit(0 if passed == len(TESTS) else 1)
