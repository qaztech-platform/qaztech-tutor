# Changelog

All notable changes are documented here. Versions follow [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-10-10 (preview)

### Added
- Published model: Hugging Face (bf16 and GGUF), Ollama, ModelScope, Kaggle.
- Full reproducible pipeline (`pipeline/00`-`09`), publishing scripts, documentation, CI.

### Changed
- Regenerated the practice-question and misconception-correction modes (v2 data):
  the teacher prompt is written in English with an explicit target language and a
  language-specific answer marker; the tutor must explain before asking a check question.
- Stricter filtering: word-based language detection (RU/KK, EN/ES), exam items must
  contain a question stem before options A-D, references to unseen source text removed.
- Ollama build uses the official Qwen3 chat template.

### Fixed
- v0.1 answered some Russian requests in Kazakh (166 mismatched training pairs).
- v0.1 misconception mode answered only with questions (962 pairs).
- Empty `<think></think>` block visible in Ollama output.

### Results
- Held-out eval loss 0.795 (v0.1: 0.889 on a different split), token accuracy 0.773.
- Language match 5/5 and no reasoning-trace leakage in the EN/RU/KK/AR/ES spot test.

## [0.1.0] - 2026-10-09 (internal, not released)
- First LoRA fine-tune on 3,687 dialogues. Superseded by 0.2.0.
