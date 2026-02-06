# LENTERA Fine-Tuning - Complete Guide

## 🚀 Quick Start (Phase 1: Dataset Generation)

### 1. Install Dependencies
```bash
pip install openai
```

### 2. Set API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-proj-YOUR_KEY_HERE"

# Linux/Mac
export OPENAI_API_KEY="sk-proj-YOUR_KEY_HERE"
```

### 3. Generate Training Data
```bash
cd backend
python generate_training_data.py --num 1000 --split
```

**Output**: `train.jsonl` (900 examples), `val.jsonl` (100 examples)

---

## 📁 Directory Structure

```
backend/finetuning/
├── lentera_config.yaml          # Axolotl training config (Llama 3.1 8B)
├── train.sh                     # Automated training script
├── evaluate_model.py            # Ethics compliance testing
├── train.jsonl                  # Training data (generated)
├── val.jsonl                    # Validation data (generated)
└── lentera-lora-output/         # Output directory
```

---

## 🚀 Training Workflow

### Step 1: Run Training
```bash
chmod +x train.sh
./train.sh
```

### Step 2: Evaluate Model
```bash
python evaluate_model.py --model ./lentera-lora-output/checkpoint-300 --lora
```

### Step 3: Deploy to Modal or Ollama
- For Modal: Upload merged model to Hugging Face or Volume.
- For Ollama: Convert to GGUF and import.

(See `FINE_TUNING_GUIDE.md` for full details)
