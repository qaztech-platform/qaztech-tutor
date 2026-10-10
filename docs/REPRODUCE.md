# Reproducing QAZTECH Tutor 8B v0.2

Hardware used: NVIDIA DGX Spark (GB10, 128 GB unified memory) for data, merge and export;
Lambda Cloud 1x A100 40 GB SXM4 for training. Paths default to `~/tutor`.

## 1. Environments (DGX Spark)

```bash
python3 -m venv ~/tutorenv && ~/tutorenv/bin/pip install -r requirements/spark-generate.txt
python3 -m venv ~/mergeenv
~/mergeenv/bin/pip install "torch>=2.8,<2.9" --index-url https://download.pytorch.org/whl/cpu
~/mergeenv/bin/pip install -r requirements/merge-export.txt
cp pipeline/*.py ~/tutor/
```

## 2. Source material and teacher

```bash
bash pipeline/00_fetch_docs.sh            # 1,194 Markdown files; Ollama: 8 parallel, 4,096 context
~/tutorenv/bin/python ~/tutor/01_bench_teacher.py
```

Measured on GB10: about 220 tokens/s aggregate with 8 parallel requests.
Do not raise `OLLAMA_CONTEXT_LENGTH` with 8 parallel slots: the default 262k window per slot
required about 112 GB of KV cache and the service was killed by the OOM killer.

## 3. Data

```bash
cd ~/tutor
TEACHER="hf.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:UD-Q4_K_XL" N=6000 ~/tutorenv/bin/python 02_generate_v1.py
~/tutorenv/bin/python 03_clean_v1.py      # -> data/train_clean.jsonl, data/eval.jsonl
N=3000 ~/tutorenv/bin/python 04_generate_v2.py   # -> data/v2_raw.jsonl (about 1 h 50 min)
~/tutorenv/bin/python 05_clean_v2.py      # -> data/train_v2.jsonl (4,907), data/eval_v2.jsonl (200)
```

Use the **Instruct-2507** teacher. With the hybrid `qwen3:30b` model, 28 of 40 test requests hit the
token limit (`done_reason=length`) because of reasoning tokens, and only 20% of outputs were usable.

## 4. Training (Lambda, 1x A100 40 GB, Lambda Stack 22.04)

```bash
pip install -r requirements/train.txt
EPOCHS=3 BS=4 ACCUM=8 DATA=~/data torchrun --nproc_per_node=1 06_train.py
```

Data files on the instance: `~/data/train_clean.jsonl` (copy of `train_v2.jsonl`) and
`~/data/eval.jsonl` (copy of `eval_v2.jsonl`). 462 steps took about 55 minutes. The best checkpoint by
eval loss (step 300) is saved to `out/final`. Copy it back before terminating the instance.

## 5. Merge, export, check

```bash
~/mergeenv/bin/python pipeline/07_merge.py ~/tutor/adapter_v2 ~/tutor/QAZTECH-Tutor-8B
bash pipeline/08_export_gguf.sh
~/tutorenv/bin/python pipeline/09_eval_languages.py   # expect 5/5 passed
```

## 6. Publish

See [PUBLISHING.md](PUBLISHING.md).
