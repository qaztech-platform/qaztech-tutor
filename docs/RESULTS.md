# Results

## Training (v0.2)

Qwen3-8B, LoRA r=16, alpha=32, dropout 0.05, all linear projections; lr 1e-4 cosine, warmup 3%;
effective batch 32 (4 x 8 accumulation); 3 epochs, 462 steps; bf16; max length 2,048
(no example exceeded 954 tokens). Loss computed on tutor turns only.

| Step | Held-out eval loss |
|---|---|
| 50 | 0.896 |
| 100 | 0.843 |
| 150 | 0.820 |
| 200 | 0.811 |
| 250 | 0.801 |
| **300** | **0.795** (selected) |
| 350 | 0.797 |
| 400 | 0.795 |
| 450 | 0.795 |

Token accuracy 0.773. Plateau from step 300; no overfitting.

## Behaviour checks (stage 09, Ollama Q4_K_M)

| Prompt language | Answer language | `<think>` leak | Content review |
|---|---|---|---|
| Russian (practice question) | Russian | no | Correct format; question stem debatable (resource-group vs resource-provider permissions) |
| English (misconception) | English | no | Correct: Policy governs *what*, RBAC governs *who* |
| Kazakh (definition) | Kazakh | no | Meaning correct; some awkward word choices |
| Arabic (comparison) | Arabic | no | Meaning correct; RBAC rendered as a shortened term |
| Spanish (practice question) | Spanish | no | Correct format, relevant ARM `reference()` question |

## v0.1 → v0.2

| Issue in v0.1 | Cause | Fix |
|---|---|---|
| Russian request answered in Kazakh | Russian example phrase in the teacher prompt; script-only language filter | English teacher prompt with explicit target language; word-based filter |
| Misconception mode answered only with questions | Prompt asked for Socratic questioning | Tutor must state what is wrong and explain before one check question |
| Empty `<think></think>` visible in Ollama | Custom template | Official Qwen3 template |
