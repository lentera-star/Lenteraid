# 🔄 Model Update Guide - Ganti Fine-tuned Model

## 📋 Quick Reference

**Current Model**: `ft:gpt-3.5-turbo-0125:personal:lentera-safety-v2:CtBTujc1`

---

## 🔧 Cara Ganti Model (Setelah Fine-tuning Baru)

### Option 1: Update via Environment Variable (Recommended)

**Di VPS**:

```bash
# SSH ke VPS
ssh root@84.247.150.83

# Edit environment file
nano /opt/lentera-backend/.env

# Update line OPENAI_MODEL dengan model ID baru
# Format: ft:gpt-3.5-turbo-0125:personal:<name>:<id>
OPENAI_MODEL=ft:gpt-3.5-turbo-0125:personal:lentera-safety-v3:NewModelId

# Save: Ctrl+O, Enter, Ctrl+X

# Restart backend
systemctl restart lentera-backend

# Check logs
journalctl -u lentera-backend -f
```

**Expected output**:
```
✓ OpenAI initialized: ft:gpt-3.5-turbo-0125:personal:lentera-safety-v3:NewModelId
LENTERA Backend ready! 🚀
```

---

### Option 2: Update via Code (Permanent)

**Di local machine**:

```powershell
# Edit .env.production
cd c:\LenteraDreamFlow\backend
notepad .env.production

# Update OPENAI_MODEL line
# Save file

# Redeploy to VPS
.\deploy-to-vps.ps1
```

---

## 📝 Model Name Convention

Recommended naming untuk tracking:

```
ft:gpt-3.5-turbo-0125:personal:lentera-<version>-<date>:<id>

Examples:
- lentera-safety-v2:CtBTujc1 (current)
- lentera-safety-v3-jan06:AbCdEfG1 (next)
- lentera-empathy-v1:XyZ1234a (specialized)
```

---

## 🧪 Testing New Model

Setelah ganti model:

### 1. Health Check
```bash
curl http://84.247.150.83:8000/health
```

### 2. Test Chat
```bash
curl -X POST http://84.247.150.83:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Halo, aku stress"}'
```

### 3. Verify Response Quality
- Check empathy level ✅
- Check safety responses ✅
- Check Indonesian language quality ✅
- Check crisis handling ✅

---

## 🔄 Rollback Previous Model

Kalau model baru ada issue:

```bash
# SSH ke VPS
ssh root@84.247.150.83

# Edit .env
nano /opt/lentera-backend/.env

# Kembalikan ke model lama
OPENAI_MODEL=ft:gpt-3.5-turbo-0125:personal:lentera-safety-v2:CtBTujc1

# Restart
systemctl restart lentera-backend
```

---

## 📊 Model Performance Tracking

Buat log setiap ganti model:

**Create `model_changelog.md`** di project:

```markdown
# Model Changelog

## 2026-01-06 - v2 (CtBTujc1)
- Model: ft:gpt-3.5-turbo-0125:personal:lentera-safety-v2:CtBTujc1
- Training: Safety responses, boundary setting
- Status: Production ✅
- Notes: Template v2 crisis handling

## 2026-01-XX - v3 (pending)
- Model: ft:gpt-3.5-turbo-0125:personal:lentera-safety-v3:NewId
- Training: [describe training focus]
- Status: Testing
- Notes: [observations]
```

---

## 🚀 Automated Model Update (Future)

**Script untuk update otomatis**:

```bash
#!/bin/bash
# update-model.sh

NEW_MODEL=$1

if [ -z "$NEW_MODEL" ]; then
  echo "Usage: ./update-model.sh ft:gpt-3.5-turbo-0125:personal:name:id"
  exit 1
fi

# Update .env
sed -i "s/OPENAI_MODEL=.*/OPENAI_MODEL=$NEW_MODEL/" /opt/lentera-backend/.env

# Restart service
systemctl restart lentera-backend

# Show logs
journalctl -u lentera-backend -f
```

**Usage**:
```bash
./update-model.sh ft:gpt-3.5-turbo-0125:personal:lentera-v3:NewId
```

---

## 💡 Best Practices

1. **Test in Staging First**
   - Deploy model baru ke test environment dulu
   - Verify quality
   - Baru deploy production

2. **Keep Previous Model ID**
   - Simpan model ID sebelumnya untuk rollback
   - Document di changelog

3. **Monitor Performance**
   - Check response quality first 24 hours
   - Gather user feedback
   - Monitor error rates

4. **Version Control**
   - Commit `.env.production` changes
   - Tag releases: `v2.0-safety`, `v3.0-empathy`

---

## 📞 Quick Commands Reference

```bash
# Check current model
ssh root@84.247.150.83 "grep OPENAI_MODEL /opt/lentera-backend/.env"

# Update model
ssh root@84.247.150.83 "sed -i 's/OPENAI_MODEL=.*/OPENAI_MODEL=NEW_MODEL_ID/' /opt/lentera-backend/.env && systemctl restart lentera-backend"

# View logs
ssh root@84.247.150.83 "journalctl -u lentera-backend -n 50"

# Test endpoint
curl http://84.247.150.83:8000/api/chat -X POST -H "Content-Type: application/json" -d '{"message":"test"}'
```

---

**Model switching made easy!** 🔄✨
