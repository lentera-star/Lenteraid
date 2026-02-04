# LENTERA VPS Deployment Guide - Contabo Singapore
**Step-by-step deployment untuk VPS Contabo yang SUDAH DIBELI**

---

## 📧 Step 1: Tunggu Email dari Contabo

**Email berisi:**
- IP Address: `xxx.xxx.xxx.xxx`
- Username: `root`
- Password: `xxxxxxxxxx`
- SSH Port: `22`

**Timeline**: Biasanya 24-48 jam setelah pembayaran

**Sementara menunggu**: Test backend di komputer lokal ✅

---

## 🔐 Step 2: Login ke VPS (Setelah Dapat Email)

### Windows (PowerShell):
```powershell
ssh root@YOUR_VPS_IP
# Masukkan password dari email
```

### First Login:
```bash
# Akan muncul warning, ketik: yes
# Masukkan password
# Anda masuk sebagai root
```

---

## 🛠️ Step 3: Setup VPS (First Time Only)

### Update System:
```bash
apt update && apt upgrade -y
```

### Install Docker:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Verify
docker --version
docker-compose --version
```

### Install Git:
```bash
apt install git -y
```

---

## 📦 Step 4: Upload Code ke VPS

### Option A: Via Git (Recommended)
```bash
# Di VPS
cd /home
git clone https://github.com/lentera-star/Lenteraid.git
cd Lenteraid

# Jika private repo:
# git clone https://USERNAME:TOKEN@github.com/lentera-star/Lenteraid.git
```

### Option B: Via SCP (Dari Komputer Lokal)
```powershell
# Di PowerShell lokal
scp -r c:\LenteraDreamFlow root@YOUR_VPS_IP:/home/Lenteraid
```

---

## 🐳 Step 5: Setup Environment Variables

```bash
# Di VPS
cd /home/Lenteraid/backend
cp .env.example .env

# Edit .env (gunakan nano atau vim)
nano .env

# Set:
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama2
API_HOST=0.0.0.0
# ... (sisanya biarkan default)

# Save: Ctrl+O, Enter, Ctrl+X
```

---

## 🚀 Step 6: Start Docker Containers

```bash
# Di /home/Lenteraid
docker-compose up -d

# Check status
docker-compose ps

# Check logs
docker-compose logs -f backend
```

**Expected output:**
```
lentera-backend    running    0.0.0.0:8000->8000/tcp
lentera-ollama     running    0.0.0.0:11434->11434/tcp
```

---

## 📥 Step 7: Download Ollama Model

```bash
# Download llama2 (~4GB, takes 10-15 min)
docker exec -it lentera-ollama ollama pull llama2

# Verify
docker exec -it lentera-ollama ollama list
# Should show: llama2:latest
```

---

## 🧪 Step 8: Test Backend

### Test dari VPS:
```bash
# Health check
curl http://localhost:8000/health

# Should return:
# {"status":"ok","services":{"ollama":"ready",...}}
```

### Test dari Internet (Komputer Lokal):
```powershell
# Di PowerShell
curl http://YOUR_VPS_IP:8000/health
```

**Jika tidak bisa akses dari internet**:

### Configure Firewall:
```bash
# Di VPS
ufw allow 8000/tcp
ufw allow 11434/tcp
ufw enable
```

---

## 🔥 Step 9: Test All Endpoints

### Test Chat:
```bash
curl -X POST http://YOUR_VPS_IP:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Halo, apa kabar?"}'
```

### Test TTS:
```bash
curl -X POST http://YOUR_VPS_IP:8000/api/voice/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"Halo dari LENTERA"}' \
  --output test.mp3

# Play test.mp3 di komputer lokal
```

---

## 📱 Step 10: Connect Flutter App

### Update Flutter Config:
```dart
// lib/config/api_config.dart
class ApiConfig {
  // CHANGE THIS:
  static const String baseUrl = "http://YOUR_VPS_IP:8000";
  static const String wsUrl = "ws://YOUR_VPS_IP:8000/ws/voice-call";
}
```

### Test dari Flutter:
- Run Flutter app
- Try chat feature
- Try voice call

---

## 🔒 Step 11: Security (Important!)

### Change Root Password:
```bash
passwd
# Enter new strong password
```

### Create Non-Root User:
```bash
adduser lentera
usermod -aG sudo,docker lentera

# Login as lentera next time:
ssh lentera@YOUR_VPS_IP
```

### Setup SSH Key (Optional but Recommended):
```powershell
# Di komputer lokal
ssh-keygen -t rsa -b 4096
ssh-copy-id root@YOUR_VPS_IP

# Now can login without password
```

---

## 📊 Step 12: Monitoring

### Check Logs:
```bash
# Backend logs
docker-compose logs -f backend

# Ollama logs  
docker-compose logs -f ollama

# All logs
docker-compose logs -f
```

### Check Resources:
```bash
# RAM/CPU usage
docker stats

# Disk space
df -h

# Running processes
htop  # Install: apt install htop
```

---

## 🔄 Step 13: Updates & Maintenance

### Update Code:
```bash
cd /home/Lenteraid
git pull
docker-compose down
docker-compose up -d --build
```

### Restart Services:
```bash
docker-compose restart
```

### Stop Services:
```bash
docker-compose down
```

### Backup Database (If using local DB):
```bash
docker-compose exec backend python -c "# backup script"
```

---

## 🐛 Troubleshooting

### Backend Won't Start:
```bash
docker-compose logs backend
# Look for errors in Python imports or port conflicts
```

### Ollama Model Download Failed:
```bash
# Increase timeout
docker exec -it lentera-ollama ollama pull llama2 --timeout=60m
```

### Out of Memory:
```bash
# Check RAM usage
free -h

# If using llama2 and RAM < 8GB, switch to phi:
docker exec -it lentera-ollama ollama pull phi
# Update .env: OLLAMA_MODEL=phi
docker-compose restart
```

### Firewall Blocked:
```bash
# Check firewall
ufw status

# Allow all needed ports
ufw allow 8000/tcp
ufw allow 11434/tcp
ufw reload
```

### Can't Access from Internet:
```bash
# Check if container is listening on 0.0.0.0
docker-compose ps
# PORTS should show 0.0.0.0:8000->8000/tcp

# Check Contabo firewall (in customer panel)
# Make sure ports 8000, 11434 are not blocked
```

---

## ✅ Verification Checklist

Before going to production:

- [ ] VPS accessible via SSH
- [ ] Docker & Docker Compose installed
- [ ] Code uploaded to VPS
- [ ] Containers running (`docker-compose ps`)
- [ ] llama2 model downloaded
- [ ] Health endpoint returns OK
- [ ] Chat API works
- [ ] TTS generates audio
- [ ] Firewall configured
- [ ] Can access from internet
- [ ] Flutter app connected
- [ ] Crisis detection works
- [ ] Logs are readable

---

## 🎯 Quick Command Reference

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# Restart backend only
docker-compose restart backend

# View logs
docker-compose logs -f

# Shell into backend
docker exec -it lentera-backend bash

# Shell into ollama
docker exec -it lentera-ollama bash

# Check resource usage
docker stats

# Download model
docker exec -it lentera-ollama ollama pull llama2

# Test health
curl http://localhost:8000/health
```

---

## 📞 Support

**If stuck:**
1. Check logs: `docker-compose logs`
2. Check if containers running: `docker ps`
3. Check firewall: `ufw status`
4. Check internet from VPS: `ping google.com`

**Email from Contabo hasn't arrived?**
- Check spam folder
- Wait 24-48 hours
- Contact Contabo support

---

## 🚀 Production Checklist (Before Launch)

- [ ] Setup SSL/HTTPS (Nginx + Let's Encrypt)
- [ ] Point domain to VPS IP
- [ ] Setup automatic backups
- [ ] Configure monitoring (Uptime Robot)
- [ ] Setup error tracking (Sentry)
- [ ] Load testing (100+ concurrent users)
- [ ] Disaster recovery plan
- [ ] User agreement implemented
- [ ] Mental health expert reviewed ethics
- [ ] Legal reviewed disclaimers

---

**Deployment Status**: Ready when VPS email arrives! 🎉
**Estimated Setup Time**: 30-45 minutes
**Next Step**: Wait for Contabo email, then follow this guide!
