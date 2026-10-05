# LoRA fine-tune. Run on Lambda: pip install trl peft transformers datasets accelerate ; python 2_train.py
import os
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

BASE = os.environ.get("BASE", "Qwen/Qwen2.5-7B-Instruct")
ds = load_dataset("json", data_files="train.jsonl", split="train").train_test_split(test_size=0.05, seed=1)

cfg = SFTConfig(output_dir="out", num_train_epochs=2, per_device_train_batch_size=2,
                gradient_accumulation_steps=8, learning_rate=1e-4, lr_scheduler_type="cosine",
                warmup_ratio=0.03, bf16=True, logging_steps=10, eval_strategy="steps", eval_steps=100,
                save_steps=200, save_total_limit=2, max_length=2048, gradient_checkpointing=True,
                model_init_kwargs={"torch_dtype": "bfloat16"})
lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
                  target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])
tr = SFTTrainer(model=BASE, args=cfg, train_dataset=ds["train"], eval_dataset=ds["test"], peft_config=lora)
tr.train()
tr.save_model("out/final")
