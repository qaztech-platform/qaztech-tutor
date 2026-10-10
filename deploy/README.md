# Deployment

`Modelfile` builds the Ollama model from the Q4_K_M GGUF with the official Qwen3 chat template,
the QAZTECH Tutor system prompt and recommended sampling (temperature 0.7, top_p 0.8, top_k 20).

```bash
ollama create qaztech-platform/tutor -f Modelfile   # from a folder containing the .gguf
ollama run qaztech-platform/tutor
```

Production guidance: run the model behind retrieval over official documentation (for example
Open WebUI or DeepTutor), and restrict access with your identity provider (OIDC, e.g. Microsoft Entra ID).
