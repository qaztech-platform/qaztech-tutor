# Слияние LoRA с базой + брендирование. На Lambda/Spark: pip install peft transformers
import os, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
BASE = os.environ.get("BASE", "Qwen/Qwen3-8B"); LORA = "out/final"
BRAND = os.environ.get("BRAND", "QAZTECH-Tutor"); ORG = os.environ.get("ORG", "qaztech")
OUT = f"{BRAND}-8B"
tok = AutoTokenizer.from_pretrained(BASE)
m = PeftModel.from_pretrained(AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16), LORA).merge_and_unload()
# Бренд зашивается в шаблон чата: модель представляется своим именем без system prompt
tok.chat_template = tok.chat_template.replace(
    "{%- if messages[0].role == 'system' %}",
    "{%- if messages[0].role != 'system' %}{{ '<|im_start|>system\\nYou are QAZTECH Tutor, an engineering tutor by " + ORG +
    ". Reply in the student\\'s language.<|im_end|>\\n' }}{%- endif %}{%- if messages[0].role == 'system' %}", 1)
m.save_pretrained(OUT, safe_serialization=True); tok.save_pretrained(OUT)
print("saved", OUT)
