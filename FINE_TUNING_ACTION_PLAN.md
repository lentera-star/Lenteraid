# 🔥 LENTERA Fine-Tuning - IMMEDIATE ACTION PLAN

**Goal**: Create pure Indonesian-speaking LENTERA model  
**Time**: ~12 hours over 2 days  
**Cost**: $40 (OpenAI API + Colab Pro)

---

## 🎯 **Step 1: Get OpenAI API Key** (5 minutes)

### **Do you have OpenAI API key?**

**If YES**: Skip to Step 2!

**If NO**:
1. Go to: https://platform.openai.com/signup
2. Create account (email + password)
3. Add payment method: https://platform.openai.com/account/billing
4. Add $10 credits (minimum)
5. Create API key: https://platform.openai.com/api-keys
6. Copy the key (starts with `sk-...`)

**Keep this safe!** You'll need it next!

---

## 🎯 **Step 2: Set Up Environment** (2 minutes)

### **On Windows (where you are now):**

```powershell
# Navigate to backend
cd C:\LenteraDreamFlow\backend

# Create .env file for API key
echo "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" > .env.local

# Or manually create file:
notepad .env.local
# Paste: OPENAI_API_KEY=sk-your-actual-key-here
# Save & close
```

---

## 🎯 **Step 3: Generate Training Data** (2-3 hours)

### **Run the generator:**

```powershell
# Install dependencies (if needed)
pip install openai python-dotenv pandas

# Run generator (1000 examples = ~$20-30)
python generate_training_data.py --count 1000 --output training_data.jsonl

# This will:
# - Generate 1000 Indonesian mental health conversations
# - Validate ethics compliance
# - Split into train (80%) and validation (20%)
# - Save to: training_data.jsonl
```

**Monitor progress**: Script will show:
- Examples generated: 1/1000, 2/1000...
- Cost estimate updating
- Ethics validation results

**Expected output**:
```
✅ Generated 1000 examples
✅ Ethics compliance: 98.5%
✅ Train set: 800 examples
✅ Validation set: 200 examples
✅ Total cost: $28.50
✅ Saved to: training_data.jsonl
```

---

## 🎯 **Step 4: Verify Data Quality** (10 minutes)

```powershell
# Open the file
notepad training_data.jsonl

# Check for:
# - Pure Indonesian conversations ✅
# - Mental health context ✅
# - Crisis scenarios ✅
# - Ethics compliance ✅
```

**Sample should look like**:
```json
{"messages": [
  {"role": "system", "content": "Kamu adalah LENTERA..."},
  {"role": "user", "content": "Aku merasa sedih hari ini"},
  {"role": "assistant", "content": "Hai, terima kasih sudah berbagi..."}
]}
```

---

## 🎯 **Step 5: Setup Google Colab** (10 minutes)

### **5a. Create Colab Account**
1. Go to: https://colab.research.google.com
2. Sign in with Google account
3. (Optional) Upgrade to Colab Pro ($10/month for faster GPU)

### **5b. Create Training Notebook**
1. Click "New Notebook"
2. Copy this code:

```python
# Install Axolotl
!pip install axolotl

# Upload training data
from google.colab import files
uploaded = files.upload()  # Upload training_data.jsonl

# Clone LENTERA config
!git clone https://github.com/lentera-star/Lenteraid.git
%cd Lenteraid/backend/finetuning

# Run training
!accelerate launch -m axolotl.cli.train lentera_config.yaml
```

### **5c. Upload Training Data**
- When prompted, upload `training_data.jsonl` from your Windows machine

---

## 🎯 **Step 6: Start Training** (4-6 hours - OVERNIGHT!)

### **Run the notebook**:
1. Click "Runtime" → "Run all"
2. Choose GPU: "Runtime" → "Change runtime type" → "T4 GPU"
3. Let it run!

**Training will**:
- Load llama2 base model
- Apply LoRA adapters
- Train on your 1000 examples
- Save checkpoints every 100 steps
- Take 4-6 hours

**Monitor**: Watch output for:
```
Step 100/1000 - Loss: 1.234
Step 200/1000 - Loss: 0.987
...
Training complete! ✅
```

---

## 🎯 **Step 7: Export Model** (30 minutes)

### **After training completes:**

```python
# Merge LoRA weights with base model
!python -m axolotl.cli.merge_lora lentera_config.yaml --lora_model_dir="./lora-out"

# Convert to GGUF format (for Ollama)
!pip install llama-cpp-python
!python convert_to_gguf.py ./merged_model --output lentera-indonesian.gguf

# Download
from google.colab import files
files.download('lentera-indonesian.gguf')
```

**Download time**: ~10 minutes (3-4GB file)

---

## 🎯 **Step 8: Deploy to VPS** (30 minutes)

### **Upload model to VPS:**

```powershell
# From Windows, upload to VPS
scp lentera-indonesian.gguf root@84.247.150.83:/home/lentera-model.gguf

# SSH to VPS
ssh root@84.247.150.83

# Import to Ollama
ollama create lentera -f Modelfile
# Where Modelfile contains:
# FROM /home/lentera-model.gguf
# SYSTEM "Kamu adalah LENTERA..."

# Update .env
cd /home/Lenteraid/backend
nano .env
# Change: OLLAMA_MODEL=lentera

# Restart
cd /home/Lenteraid
docker-compose restart backend
```

---

## 🎯 **Step 9: TEST!** (10 minutes)

```bash
# Test Indonesian
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Halo, ceritakan tentang dirimu"}'

# Expected: PURE INDONESIAN response! 🇮🇩

# Test crisis
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Aku ingin bunuh diri"}'

# Expected: Indonesian response + hotlines!
```

---

## 📊 **Total Cost Breakdown:**

| Item | Cost |
|------|------|
| OpenAI API (1000 examples @ GPT-4) | $20-30 |
| Google Colab Pro (1 month) | $10 |
| **TOTAL** | **$30-40** |

---

## ⏰ **Timeline:**

**TODAY (3 hours active work)**:
- ✅ Get API key (5 min)
- ✅ Generate data (2-3 hours running, you can leave it)
- ✅ Setup Colab (10 min)
- ✅ Start training (5 min to start, then overnight!)

**TOMORROW (1 hour active work)**:
- ✅ Training completes overnight
- ✅ Export & download (30 min)
- ✅ Deploy to VPS (30 min)
- ✅ Test & celebrate! 🎉

---

## 🚨 **CURRENT STATUS:**

**You are here**: About to start Step 1!

**Next action**: Get OpenAI API key!

**DO YOU HAVE OpenAI API key already?**
- **YES**: Tell me, we skip to Step 2!
- **NO**: Follow Step 1 instructions above!

---

## 🎯 **READY?**

**Let's start with Step 1!** Do you have OpenAI API key or need to create one?

After you confirm, I'll guide you STEP BY STEP through each phase!

**LET'S MAKE LENTERA INDONESIAN! 🇮🇩🔥**
