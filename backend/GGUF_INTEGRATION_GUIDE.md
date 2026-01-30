# 🔥 Guide: Integrasi .GGUF Model ke LENTERA Backend

> **Setelah Fine-tuning Llama-3.1 selesai, ikuti guide ini untuk mengintegrasikan model ke Ollama**

---

## 📋 Prerequisites

✅ File `.gguf` dari hasil fine-tuning (biasanya di `/workspace/lentera-lora-out/`)  
✅ Ollama sudah terinstall di local machine atau VPS  
✅ Backend LENTERA ready

---

## 🎯 Langkah 1: Download File .GGUF dari RunPod/Server

### Option A: Via RunPod Web Interface
1. Buka RunPod dashboard
2. Masuk ke Pod yang kamu gunakan untuk training
3. File browser → `/workspace/lentera-lora-out/`
4. Download file `.gguf` (biasanya nama: `unsloth.Q4_K_M.gguf` atau similar)

### Option B: Via SCP/SFTP (Recommended untuk file besar)

```bash
# Dari local machine (PowerShell/Terminal)
scp root@<runpod-ip>:/workspace/lentera-lora-out/*.gguf C:\LenteraDreamFlow\backend\finetuning\
```

**Expected file**: `lentera-llama-3.1-8b-mental-health.gguf` (atau nama lain yang kamu set)

---

## 🎯 Langkah 2: Import Model ke Ollama

Ollama butuh **Modelfile** untuk import .gguf. Mari kita buat:

### 2.1 Buat Modelfile

Buat file baru: `c:\LenteraDreamFlow\backend\finetuning\Modelfile`

```dockerfile
# Base model dari GGUF
FROM ./lentera-llama-3.1-8b-mental-health.gguf

# Template untuk chat format (ChatML yang digunakan saat training)
TEMPLATE """<|im_start|>system
{{ .System }}<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

# System prompt khusus mental health
SYSTEM """Kamu adalah LENTERA, asisten AI untuk konseling kesehatan mental yang empatik dan profesional.

Prinsip yang harus kamu ikuti:
1. Selalu empati dan mendukung
2. Jangan mendiagnosis kondisi mental secara spesifik
3. Jika ada tanda-tanda bahaya (bunuh diri, self-harm), sarankan untuk menghubungi profesional segera
4. Berikan saran praktis untuk self-care dan coping mechanisms
5. Gunakan bahasa Indonesia yang hangat dan ramah
6. Jaga privasi dan confidentiality

Jangan pernah:
- Memberikan diagnosis medis
- Meresepkan obat
- Menggantikan terapi profesional
- Memberikan saran yang berbahaya
"""

# Parameter optimized untuk mental health conversation
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096
```

### 2.2 Import ke Ollama

```powershell
# Masuk ke folder finetuning
cd c:\LenteraDreamFlow\backend\finetuning

# Import model dengan nama "lentera-mental-health"
ollama create lentera-mental-health -f Modelfile
```

**Expected output**:
```
transferring model data
creating model layer
using existing layer sha256:xxxxx
writing manifest
success
```

### 2.3 Verifikasi Model

```powershell
# List semua models
ollama list

# Test model
ollama run lentera-mental-health "Halo, aku merasa stress akhir-akhir ini"
```

**Expected**:  
Model merespons dengan empati dalam Bahasa Indonesia 🇮🇩

---

## 🎯 Langkah 3: Update Backend Configuration

### 3.1 Update Environment Variable

**File**: `c:\LenteraDreamFlow\backend\.env` (local) atau `.env.production` (VPS)

```env
# Ganti model name ke model yang baru saja di-import
OLLAMA_MODEL=lentera-mental-health

# Pastikan Ollama URL sudah benar
OLLAMA_BASE_URL=http://localhost:11434
```

### 3.2 Restart Backend

**Local**:
```powershell
# Stop backend yang running (Ctrl+C)
# Atau kill process jika dalam background

# Restart
cd c:\LenteraDreamFlow
.\start_backend_local.bat
```

**VPS** (jika deploy):
```bash
ssh root@84.247.150.83
systemctl restart lentera-backend
journalctl -u lentera-backend -f
```

---

## 🎯 Langkah 4: Testing Model Integration

### 4.1 Health Check

```powershell
# Test Ollama
curl http://localhost:11434/api/tags

# Test Backend
curl http://localhost:8000/health
```

### 4.2 Test Chat Endpoint

```powershell
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"Halo, aku lagi sedih\"}'
```

**Expected response**:
```json
{
  "response": "Halo... Aku di sini untuk mendengarkanmu. Mau cerita apa yang membuatmu sedih?",
  "context": [...]
}
```

### 4.3 Test Quality

Test beberapa scenario:

```powershell
# Test 1: Empathy
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"Aku merasa tidak berguna\"}'

# Test 2: Crisis handling
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"Aku ingin bunuh diri\"}'

# Test 3: Support
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"Gimana cara mengatasi anxiety?\"}'
```

**Check**:
- ✅ Empathy level tinggi
- ✅ Bahasa Indonesia natural
- ✅ Crisis response tepat (sarankan hubungi profesional)
- ✅ Saran praktis dan aman

---

## 🎯 Langkah 5: Model Performance Tuning (Optional)

Jika response kurang memuaskan, adjust parameter di Modelfile:

```dockerfile
# Untuk response lebih creative/varied
PARAMETER temperature 0.8

# Untuk response lebih focused/deterministic
PARAMETER temperature 0.6

# Untuk mengurangi repetisi
PARAMETER repeat_penalty 1.2

# Untuk context lebih panjang (4K tokens)
PARAMETER num_ctx 4096
```

Lalu recreate model:
```powershell
ollama create lentera-mental-health -f Modelfile
```

---

## 🔄 Rollback ke Model Lama

Jika model baru ada issue:

```powershell
# Update .env
OLLAMA_MODEL=llama2  # atau model sebelumnya

# Restart backend
.\start_backend_local.bat
```

---

## 📊 Model Changelog

Buat log untuk tracking:

```markdown
# Model Changelog

## 2026-01-24 - Fine-tuned Llama-3.1-8B v1
- Model: lentera-mental-health (GGUF)
- Base: unsloth/Meta-Llama-3.1-8B
- Training: 3 epochs, QLoRA 4-bit, mental health dataset
- Status: Testing 🧪
- Notes: First fine-tuned version, empathy-focused

## Previous: llama2
- Model: llama2 (Ollama default)
- Status: Deprecated
- Notes: Baseline model
```

---

## 🚀 Deploy ke VPS

### Upload .gguf ke VPS

```powershell
# Upload file .gguf
scp c:\LenteraDreamFlow\backend\finetuning\lentera-llama-3.1-8b-mental-health.gguf root@84.247.150.83:/opt/lentera-backend/models/

# Upload Modelfile
scp c:\LenteraDreamFlow\backend\finetuning\Modelfile root@84.247.150.83:/opt/lentera-backend/
```

### Import di VPS

```bash
# SSH ke VPS
ssh root@84.247.150.83

# Masuk ke folder
cd /opt/lentera-backend

# Import model
ollama create lentera-mental-health -f Modelfile

# Update .env
nano .env
# OLLAMA_MODEL=lentera-mental-health

# Restart service
systemctl restart lentera-backend

# Monitor logs
journalctl -u lentera-backend -f
```

---

## 💡 Tips & Best Practices

### 1. **Model Naming Convention**
```
lentera-<base-model>-<version>-<specialty>

Examples:
- lentera-llama3-v1-mental-health
- lentera-llama3-v2-crisis-handling
- lentera-mistral-v1-empathy
```

### 2. **Testing Checklist**
- [ ] Model loads successfully
- [ ] Response in Indonesian
- [ ] Empathy level appropriate
- [ ] Crisis handling correct
- [ ] No hallucinations
- [ ] Response time acceptable (<5s)

### 3. **Monitoring**
```bash
# Watch Ollama logs
journalctl -u ollama -f

# Check model memory usage
ollama ps

# Check response quality
# Save test conversations for review
```

---

## 🐛 Troubleshooting

### Issue: "model not found"
```bash
# List available models
ollama list

# Recreate if needed
ollama create lentera-mental-health -f Modelfile
```

### Issue: "out of memory"
```bash
# Check available RAM
free -h

# Use smaller quantization (Q4_K_M instead of Q8)
# atau reduce num_ctx in Modelfile
PARAMETER num_ctx 2048
```

### Issue: Response quality rendah
1. Check training data quality
2. Adjust temperature (0.6-0.8)
3. Add more examples to dataset
4. Retrain with more epochs

### Issue: Response lambat
1. Use smaller quantization (Q4_K_M)
2. Reduce num_ctx
3. Consider GPU acceleration
4. Use batch processing

---

## 📞 Quick Commands Reference

```powershell
# Import model
ollama create lentera-mental-health -f Modelfile

# List models
ollama list

# Test model
ollama run lentera-mental-health "test prompt"

# Delete model
ollama rm lentera-mental-health

# Update backend env
notepad c:\LenteraDreamFlow\backend\.env

# Restart backend
.\start_backend_local.bat

# Test API
curl http://localhost:8000/api/chat -X POST -H "Content-Type: application/json" -d '{\"message\":\"test\"}'
```

---

**Selamat! Model fine-tuned kamu sudah siap digunakan di LENTERA!** 🎉🔥

**Next Steps**:
1. Test extensively dengan berbagai scenario
2. Collect user feedback
3. Iterate dan retrain jika perlu
4. Deploy ke production VPS
