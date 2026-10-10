# Publishing

| Platform | Account | Command |
|---|---|---|
| Hugging Face | organization `qaztech-platform` | `bash publish/huggingface.sh` |
| Ollama | user `qaztech-platform` | `ollama push qaztech-platform/tutor` (device key of the publishing machine must be added at ollama.com/settings/keys) |
| ModelScope | organization `qaztechplatform` (no hyphen allowed) | `python publish/modelscope_push.py` (token in `~/.ms_token`, mode 600, deleted after upload) |
| Kaggle | user `qaztechplatform` (letters and digits only) | `bash publish/kaggle_push.sh` (metadata in `publish/kaggle/{model,transformers,gguf}/`, credentials in `~/.kaggle/kaggle.json`) |

Notes from the v0.2 release:

- Hugging Face metadata sets `base_model_relation: finetune` (weights) and `quantized` (GGUF);
  otherwise the `lora` tag makes the Hub list the model as an adapter.
- Kaggle instances use `modelInstanceType: ExternalVariant` with `externalBaseModelUrl` pointing to Qwen3-8B.
- Uploads from the Middle East to ModelScope ran at 50-350 KB/s; schedule them separately.
- `ollama push` restarts from zero after a dropped connection; wrap it in a retry loop.
