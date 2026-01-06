#!/bin/bash
# LENTERA Fine-Tuning Script (Google Colab / Local GPU)

set -e  # Exit on error

echo "🚀 LENTERA Fine-Tuning Pipeline"
echo "================================"

# Configuration
CONFIG_FILE="lentera_config.yaml"
DATA_DIR="."
OUTPUT_DIR="./lentera-lora-output"

# Step 1: Environment Check
echo ""
echo "📋 Step 1: Checking environment..."
echo "-----------------------------------"

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python: $python_version"

# Check GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✅ GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "⚠️  No GPU detected - training will be VERY slow!"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 2: Install Dependencies
echo ""
echo "📦 Step 2: Installing dependencies..."
echo "--------------------------------------"

if [ ! -d "axolotl" ]; then
    echo "Installing Axolotl..."
    git clone https://github.com/OpenAccess-AI-Collective/axolotl
    cd axolotl
    pip install -e .
    pip install flash-attn --no-build-isolation
    cd ..
else
    echo "✅ Axolotl already installed"
fi

# Install additional deps
pip install wandb peft bitsandbytes

# Step 3: Data Validation
echo ""
echo "🔍 Step 3: Validating training data..."
echo "---------------------------------------"

if [ ! -f "$DATA_DIR/train.jsonl" ]; then
    echo "❌ ERROR: train.jsonl not found!"
    echo "Run: python generate_training_data.py --num 1000 --split"
    exit 1
fi

# Count examples
train_count=$(wc -l < "$DATA_DIR/train.jsonl")
echo "✅ Training examples: $train_count"

if [ -f "$DATA_DIR/val.jsonl" ]; then
    val_count=$(wc -l < "$DATA_DIR/val.jsonl")
    echo "✅ Validation examples: $val_count"
fi

if [ $train_count -lt 100 ]; then
    echo "⚠️  Warning: Less than 100 training examples. Consider generating more."
fi

# Step 4: Login to Weights & Biases (Optional)
echo ""
echo "📊 Step 4: Weights & Biases setup..."
echo "-------------------------------------"
read -p "Use W&B logging? (recommended) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    wandb login
    echo "✅ W&B logged in"
else
    echo "⏭️  Skipping W&B"
    # Disable W&B in config
    sed -i 's/wandb_project:/# wandb_project:/g' $CONFIG_FILE
fi

# Step 5: Prepare Dataset (Axolotl preprocessing)
echo ""
echo "🔧 Step 5: Preparing dataset..."
echo "-------------------------------"

python -m axolotl.cli.preprocess $CONFIG_FILE

# Step 6: Start Training
echo ""
echo "🏋️ Step 6: Starting training..."
echo "-------------------------------"
echo "This will take 3-6 hours depending on GPU..."
echo ""

# Estimate time
if nvidia-smi --query-gpu=name --format=csv,noheader | grep -q "A100"; then
    echo "⏱️  Estimated time: 2-3 hours (A100)"
elif nvidia-smi --query-gpu=name --format=csv,noheader | grep -q "V100"; then
    echo "⏱️  Estimated time: 4-5 hours (V100)"
elif nvidia-smi --query-gpu=name --format=csv,noheader | grep -q "4090"; then
    echo "⏱️  Estimated time: 6-8 hours (RTX 4090)"
else
    echo "⏱️  Estimated time: Unknown (depends on GPU)"
fi

echo ""
read -p "Start training now? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Training cancelled."
    exit 0
fi

# Launch training with accelerate
accelerate launch -m axolotl.cli.train $CONFIG_FILE

# Step 7: Training Complete
echo ""
echo "✅ Training complete!"
echo "====================="

# Find best checkpoint
best_checkpoint=$(ls -td $OUTPUT_DIR/checkpoint-* | head -1)
echo "📍 Best checkpoint: $best_checkpoint"

# Step 8: Merge LoRA (Optional)
echo ""
read -p "Merge LoRA weights with base model? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔀 Merging LoRA weights..."
    python -m axolotl.cli.merge_lora $CONFIG_FILE --lora-model-dir=$best_checkpoint
    echo "✅ Merged model saved to: $OUTPUT_DIR/merged"
fi

# Step 9: Next Steps
echo ""
echo "🎉 FINE-TUNING COMPLETE!"
echo "========================"
echo ""
echo "Next steps:"
echo "1. Test model: python test_model.py"
echo "2. Evaluate ethics: python evaluate_ethics.py"
echo "3. Convert to GGUF: python convert_to_gguf.py"
echo "4. Deploy to Ollama: ollama create lentera -f Modelfile"
echo ""
echo "Model location: $OUTPUT_DIR"
echo "LoRA adapter: $best_checkpoint"
echo ""
echo "Happy fine-tuning! 🚀"
