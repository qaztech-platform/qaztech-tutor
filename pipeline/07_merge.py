"""Stage 07: merge the LoRA adapter into Qwen3-8B and save bf16 safetensors.

Runs on CPU (DGX Spark, 128 GB unified memory) to avoid ARM CUDA wheel issues.
Usage: python 07_merge.py [ADAPTER_DIR] [OUTPUT_DIR]
"""
import os
import sys

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE = os.environ.get("BASE", "Qwen/Qwen3-8B")
adapter = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/tutor/adapter_v2")
out = os.path.expanduser(sys.argv[2] if len(sys.argv) > 2 else "~/tutor/QAZTECH-Tutor-8B")

base = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True)
model = PeftModel.from_pretrained(base, adapter).merge_and_unload()
model.save_pretrained(out, safe_serialization=True, max_shard_size="5GB")
AutoTokenizer.from_pretrained(adapter).save_pretrained(out)
print("merged ->", out)
