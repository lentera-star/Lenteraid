# LENTERA Fine-Tuning - Complete Guide

## 📁 Directory Structure

```
backend/finetuning/
├── lentera_config.yaml          # Axolotl training config
├── train.sh                     # Automated training script
├── evaluate_model.py            # Ethics compliance testing
├── train.jsonl                  # Training data (generated)
├── val.jsonl                    # Validation data (generated)
└── lentera-lora-output/         # Output directory (created during training)
    ├── checkpoint-100/
    ├── checkpoint-200/
    ├── checkpoint-300/
    └── merged/                  # Merged model (optional)
```

---

## 🚀 Complete Workflow

### Step 1: Generate Training Data

```bash
cd backend
python generate_training_data.py --num 1000 --split
```

**Output**: `train.jsonl` (900 examples), `val.jsonl` (100 examples)

**Cost**: ~$30 (GPT-4)

---

### Step 2: Setup Training Environment

**Option A: Google Colab (Recommended for beginners)**

1. Open Google Colab: https://colab.research.google.com
2. Select **GPU runtime**: Runtime → Change runtime type → A100 GPU
3. Upload files:
   - `lentera_config.yaml`
   - `train.jsonl`
   - `val.jsonl`
   - `train.sh`

**Option B: Local GPU**

Requirements:
- NVIDIA GPU with 16GB+ VRAM (RTX 4090, A100, V100)
- CUDA 11.8+
- Python 3.10+

---

### Step 3: Run Training

```bash
chmod +x train.sh
./train.sh
```

**The script will**:
- ✅ Check environment (GPU, Python)
- ✅ Install Axolotl & dependencies
- ✅ Validate training data
- ✅ Setup W&B logging (optional)
- ✅ Start training (~3-6 hours)
- ✅ Save checkpoints every 100 steps

**Expected output**:
```
Epoch 1/3: Loss 1.234
Epoch 2/3: Loss 0.876
Epoch 3/3: Loss 0.543
Training complete!
```

---

### Step 4: Evaluate Model

```bash
python evaluate_model.py --model ./lentera-lora-output/checkpoint-300 --lora
```

**Tests**:
- ✅ Crisis handling (suicide, self-harm)
- ✅ No diagnosis/medication
- ✅ Professional referrals
- ✅ Empathy & validation

**Target**: ≥95% pass rate, 0 critical failures

---

### Step 5: Convert to GGUF (for Ollama)

```bash
# Install llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Convert to GGUF
python convert.py ../lentera-lora-output/merged --outfile lentera.gguf --outtype q4_K_M
```

---

### Step 6: Deploy to Ollama

```bash
# Create Modelfile
echo "FROM ./lentera.gguf" > Modelfile

# Import to Ollama
ollama create lentera -f Modelfile

# Test
ollama run lentera "Halo, apa kabar?"
```

---

### Step 7: Update VPS Backend

```bash
# SSH to VPS
ssh root@YOUR_VPS_IP

# Stop backend
cd /home/Lenteraid
docker-compose stop backend

# Update .env
nano backend/.env
# Change: OLLAMA_MODEL=lentera

# Restart
docker-compose up -d backend
```

---

## ⚙️ Configuration Options

### Adjust Training Speed

**Faster (less quality)**:
```yaml
# In lentera_config.yaml
num_epochs: 2           # Instead of 3
lora_r: 8               # Instead of 16
```

**Better Quality (slower)**:
```yaml
num_epochs: 5
lora_r: 32
micro_batch_size: 1     # If memory allows
```

---

### Adjust Memory Usage

**Low Memory (12GB VRAM)**:
```yaml
load_in_4bit: true      # Keep
micro_batch_size: 1     # Reduce
gradient_accumulation_steps: 16  # Increase
```

**High Memory (80GB VRAM)**:
```yaml
load_in_4bit: false
micro_batch_size: 8
gradient_accumulation_steps: 2
```

---

## 📊 Monitoring Training

### Option A: Weights & Biases

1. Create account: https://wandb.ai
2. Login: `wandb login`
3. View dashboard during training

**Metrics to watch**:
- Training loss (should decrease)
- Validation loss (should track training)
- Learning rate schedule

---

### Option B: TensorBoard

```bash
# Install
pip install tensorboard

# View
tensorboard --logdir ./lentera-lora-output
```

---

## 🐛 Troubleshooting

### Out of Memory

**Error**: `CUDA out of memory`

**Solutions**:
1. Reduce `micro_batch_size` to 1
2. Increase `gradient_accumulation_steps`
3. Reduce `sequence_len` to 1024
4. Use smaller base model (phi-2)

---

### Training Loss Not Decreasing

**Possible causes**:
- Learning rate too low/high
- Data quality issues
- Insufficient training examples

**Solutions**:
1. Adjust learning rate: `0.0001` - `0.0003`
2. Check data for errors
3. Train longer (5 epochs)

---

### Model Violates Ethics

**If evaluation fails**:
1. Review failed test cases
2. Generate more training examples for weak areas
3. Add negative examples (what NOT to say)
4. Retrain with improved dataset

---

## 💰 Cost Breakdown

### Cloud GPU Training

| GPU | Cost/hour | Training Time | Total Cost |
|-----|-----------|---------------|------------|
| Google Colab A100 | Included in Pro+ ($10/mo) | 3-4 hours | $10 |
| AWS P3 (V100) | $3/hour | 5-6 hours | $15-18 |
| RunPod A5000 | $0.40/hour | 8-10 hours | $3-4 |
| Vast.ai RTX 4090 | $0.35/hour | 6-8 hours | $2-3 |

**Recommendation**: Google Colab Pro+ for easiest setup!

---

### Total Project Cost

- Data generation (GPT-4): $30
- Training (Colab Pro): $10
- Total: **$40 one-time**

**Ongoing**: $0 (self-hosted on VPS)

---

## ✅ Quality Checklist

Before deploying to production:

- [ ] ≥95% ethics compliance on evaluation
- [ ] 0 critical failures (crisis handling)
- [ ] Mental health expert reviewed 50+ samples
- [ ] Tested with diverse Indonesian dialects
- [ ] Crisis responses include correct hotlines
- [ ] No diagnosis/medication in 100 random samples
- [ ] Natural Indonesian (not translated-sounding)
- [ ] User testing with 10+ beta testers
- [ ] A/B tested against base llama2
- [ ] Documented all model behaviors

---

## 🔄 Continuous Improvement

### Monthly Retraining

1. Collect flagged conversations
2. Expert review & labeling
3. Add to training dataset
4. Retrain with new data
5. A/B test new vs old
6. Deploy if better

---

## 📚 Additional Resources

**Documentation**:
- Axolotl: https://github.com/OpenAccess-AI-Collective/axolotl
- PEFT/LoRA: https://huggingface.co/docs/peft
- LLaMA-2: https://ai.meta.com/llama

**Communities**:
- Hugging Face Discord
- r/LocalLLaMA
- EleutherAI Discord

---

## 🎯 Success Metrics

**Model is production-ready when**:

✅ Ethics compliance ≥95%
✅ Expert approval obtained
✅ User satisfaction ≥4/5
✅ Crisis detection 100% accurate
✅ Response time <3 seconds
✅ Handles 100+ concurrent users
✅ No data privacy violations

---

**Questions?** Check `FINE_TUNING_GUIDE.md` for detailed explanations!

**Ready to fine-tune!** 🚀
