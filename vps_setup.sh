#!/bin/bash
# VPS Setup Script untuk Fine-Tuning CPU
# Jalankan ini di VPS setelah upload files

echo "========================================="
echo " LENTERA VPS CPU Training Setup"
echo "========================================="

cd /home/Lenteraid/finetuning

# 1. Create CPU-optimized config
echo "📝 Creating CPU-optimized config..."
cat > lentera_config_cpu.yaml << 'EOF'
base_model: unsloth/Meta-Llama-3.1-8B
model_type: LlamaForCausalLM
load_in_4bit: true
strict: false

adapter: lora
lora_r: 8
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj

datasets:
  - path: train.jsonl
    type: chat_template
    chat_template: chatml

val_set_size: 0.1
sequence_len: 1024
micro_batch_size: 1
gradient_accumulation_steps: 16
num_epochs: 2
learning_rate: 0.0001
optimizer: adamw_torch
bf16: false
fp16: false
gradient_checkpointing: true
output_dir: ./lentera-lora-cpu
logging_steps: 50
save_steps: 500
eval_steps: 500
special_tokens:
  bos_token: "<s>"
  eos_token: "</s>"
  unk_token: "<unk>"
  pad_token: "[PAD]"
EOF

echo "✅ Config created"

# 2. Install dependencies
echo "📦 Installing dependencies..."
pip install -q torch transformers accelerate bitsandbytes peft axolotl datasets

echo "✅ Dependencies installed"

# 3. Verify files
echo "📂 Checking files..."
ls -lh train.jsonl val.jsonl lentera_config_cpu.yaml

echo ""
echo "========================================="
echo " ✅ Setup Complete!"
echo "========================================="
echo ""
echo "To start training in background:"
echo "  screen -S training"
echo "  accelerate launch -m axolotl.cli.train lentera_config_cpu.yaml"
echo "  (Press Ctrl+A then D to detach)"
echo ""
echo "To check progress:"
echo "  screen -r training"
echo "========================================="
