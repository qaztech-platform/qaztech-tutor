import time, ollama
from concurrent.futures import ThreadPoolExecutor
M = "qwen3:30b"
ask = lambda: ollama.chat(M, [{"role": "user", "content": "Explain Azure RBAC in about 250 words. /no_think"}], options={"num_predict": 300})["eval_count"]
ask()
t = time.time()
with ThreadPoolExecutor(8) as ex:
    n = sum(ex.map(lambda _: ask(), range(8)))
dt = time.time() - t
print(f"ЗАМЕР: {n} токенов за {dt:.0f} с = {n/dt:.1f} ток/с суммарно")
