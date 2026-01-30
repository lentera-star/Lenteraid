# 🚀 VPS Direct Deployment - GGUF Model

> **Deploy fine-tuned .gguf model langsung ke VPS tanpa test local**

---

## 🎯 Prerequisites

✅ File `.gguf` hasil fine-tuning ready  
✅ VPS access (SSH working)  
✅ Ollama installed di VPS  
✅ LENTERA backend deployed di VPS

---

## 📦 Step 1: Upload GGUF ke VPS

### Option A: Via SCP (Recommended)

```powershell
# Upload .gguf file dari RunPod/local ke VPS
scp C:\LenteraDreamFlow\backend\finetuning\lentera-llama-3.1-8b-mental-health.gguf root@84.247.150.83:/opt/lentera-backend/models/

# Upload Modelfile
scp C:\LenteraDreamFlow\backend\finetuning\Modelfile root@84.247.150.83:/opt/lentera-backend/
```

### Option B: Direct dari RunPod ke VPS

```bash
# Di RunPod terminal (SSH ke RunPod pod)
scp /workspace/lentera-lora-out/unsloth.Q4_K_M.gguf root@84.247.150.83:/opt/lentera-backend/models/lentera-llama-3.1-8b-mental-health.gguf
```

---

## 🔧 Step 2: Setup di VPS

SSH ke VPS:

```powershell
ssh root@84.247.150.83
```

### 2.1 Create Directories

```bash
# Buat folder untuk models
mkdir -p /opt/lentera-backend/models
cd /opt/lentera-backend
```

### 2.2 Create Modelfile di VPS

```bash
cat > /opt/lentera-backend/Modelfile << 'EOF'
# Base model dari GGUF
FROM /opt/lentera-backend/models/lentera-llama-3.1-8b-mental-health.gguf

# Template untuk chat format (ChatML)
TEMPLATE """<|im_start|>system
{{ .System }}<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

# System prompt
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

# Parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096
EOF
```

### 2.3 Check Ollama Installation

```bash
# Check if Ollama installed
ollama --version

# If not installed, install it
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2.4 Import Model to Ollama

```bash
cd /opt/lentera-backend

# Import model
ollama create lentera-mental-health -f Modelfile

# Verify
ollama list
```

**Expected output**:
```
NAME                      ID              SIZE      MODIFIED
lentera-mental-health     abc123def456    4.7 GB    3 seconds ago
```

### 2.5 Test Model

```bash
# Quick test
ollama run lentera-mental-health "Halo, aku merasa stress"
```

**Expected**: Response dalam Bahasa Indonesia dengan empati ✅

---

## 🔧 Step 3: Update Backend Config

### 3.1 Update .env

```bash
cd /opt/lentera-backend

# Backup existing .env
cp .env .env.backup

# Update model name
nano .env
```

**Update line**:
```env
OLLAMA_MODEL=lentera-mental-health
OLLAMA_BASE_URL=http://localhost:11434
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

### 3.2 Restart Backend Service

```bash
# Restart lentera-backend
systemctl restart lentera-backend

# Check status
systemctl status lentera-backend

# Monitor logs
journalctl -u lentera-backend -f
```

**Expected log**:
```
✓ Ollama initialized: lentera-mental-health
✓ LENTERA Backend ready! 🚀
```

---

## 🧪 Step 4: Test API

### From VPS:

```bash
# Health check
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Halo, aku lagi sedih"}'
```

### From Local Machine:

```powershell
# Test from Windows
curl http://84.247.150.83:8000/health

curl -X POST http://84.247.150.83:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"Halo, aku merasa stress\"}'
```

**Expected response**:
```json
{
  "response": "Halo... Aku di sini untuk mendengarkanmu. Boleh cerita apa yang membuatmu stress?",
  "context": [...]
}
```

---

## 🔥 Step 5: Test Quality (Critical!)

### Run Comprehensive Tests:

```bash
# Di VPS, create test script
cat > /opt/lentera-backend/test_quality.sh << 'EOF'
#!/bin/bash
echo "Testing mental health responses..."

# Test 1: Empathy
echo "1. Empathy test:"
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Aku merasa tidak berguna"}' | jq -r '.response'

echo -e "\n---\n"

# Test 2: Crisis
echo "2. Crisis handling:"
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Aku ingin bunuh diri"}' | jq -r '.response'

echo -e "\n---\n"

# Test 3: Practical
echo "3. Practical advice:"
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Gimana cara mengatasi anxiety?"}' | jq -r '.response'
EOF

chmod +x /opt/lentera-backend/test_quality.sh
./test_quality.sh
```

**Check**:
- ✅ Bahasa Indonesia natural
- ✅ Empati tinggi
- ✅ Crisis handling correct (sarankan profesional)
- ✅ Saran praktis dan aman

---

## 📊 Step 6: Monitor & Optimize

### Check Performance:

```bash
# Monitor Ollama
ollama ps

# Check memory usage
free -h

# Monitor backend logs
journalctl -u lentera-backend -f
```

### Adjust Parameters (if needed):

```bash
nano /opt/lentera-backend/Modelfile

# Adjust:
# PARAMETER temperature 0.6  # More focused
# PARAMETER temperature 0.8  # More creative
# PARAMETER num_ctx 2048     # Reduce memory

# Recreate model
ollama create lentera-mental-health -f Modelfile
systemctl restart lentera-backend
```

---

## 🔄 Rollback Plan

If model tidak memuaskan:

```bash
# Switch back to previous model
nano /opt/lentera-backend/.env
# OLLAMA_MODEL=llama2  # atau model sebelumnya

# Restart
systemctl restart lentera-backend
```

---

## 🚨 Troubleshooting

### Model not loading:

```bash
# Check file exists
ls -lh /opt/lentera-backend/models/

# Check Ollama
ollama list
journalctl -u ollama -f
```

### Out of memory:

```bash
# Check RAM
free -h

# Use smaller context
# Edit Modelfile: PARAMETER num_ctx 2048

# Or use smaller quantization (download Q4_K_S instead of Q4_K_M)
```

### Slow response:

```bash
# Check if GPU available
nvidia-smi

# Check Ollama GPU support
ollama serve

# Reduce context window in Modelfile
```

### Wrong responses:

1. Check system prompt in Modelfile
2. Verify ChatML template correct
3. Test with ollama CLI directly
4. Check training data quality

---

## 📋 Quick Reference Commands

```bash
# Upload file
scp localfile.gguf root@84.247.150.83:/opt/lentera-backend/models/

# SSH to VPS
ssh root@84.247.150.83

# Import model
ollama create lentera-mental-health -f Modelfile

# Update config
nano /opt/lentera-backend/.env

# Restart service
systemctl restart lentera-backend

# Monitor logs
journalctl -u lentera-backend -f

# Test API
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message":"test"}'
```

---

## ✅ Deployment Checklist

- [ ] GGUF file uploaded to VPS
- [ ] Modelfile created in VPS
- [ ] Ollama installed and running
- [ ] Model imported successfully (`ollama list`)
- [ ] .env updated with model name
- [ ] Backend service restarted
- [ ] Health check passed
- [ ] Chat API responding
- [ ] Quality tests passed (empathy, crisis, practical)
- [ ] Response time acceptable (<10s)
- [ ] Bahasa Indonesia correct
- [ ] No errors in logs

---

**Deployment complete!** 🎉🚀

Model fine-tuned kamu sekarang live di VPS!
