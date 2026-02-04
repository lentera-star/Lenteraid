# 🚀 LENTERA Backend - Quick Start Guide

## For VPS Deployment (Contabo)

### Prerequisites on VPS
```bash
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

---

## Setup Steps

### 1. Upload Project to VPS
```bash
# Option A: Via Git (recommended)
git clone https://github.com/lentera-star/Lenteraid.git
cd Lenteraid

# Option B: Via SCP from local machine
# scp -r c:\LenteraDreamFlow user@your-vps-ip:/home/user/
```

### 2. Start Services
```bash
# Start all containers
docker-compose up -d

# Check status
docker-compose ps
```

### 3. Download Ollama Model (First Time)
```bash
# For balanced performance (7B model, ~4GB RAM)
docker exec -it lentera-ollama ollama pull llama2

# OR for lighter CPU usage (2.7B model, ~2GB RAM)
docker exec -it lentera-ollama ollama pull phi
```

### 4. Verify Services
```bash
# Check backend logs
docker-compose logs -f backend

# Test health endpoint
curl http://localhost:8000/health

# Should return:
# {
#   "status": "ok",
#   "services": {
#     "ollama": "ready",
#     "whisper": "ready",
#     "tts": "ready"
#   }
# }
```

### 5. Run Tests
```bash
cd backend
python test_services.py

# Expected: All 5 tests should PASS
```

---

## Access Your Backend

- **API Base URL**: `http://your-vps-ip:8000`
- **API Docs**: `http://your-vps-ip:8000/docs` (Swagger UI)
- **Health Check**: `http://your-vps-ip:8000/health`

---

## Configure Firewall

```bash
# Allow backend port
sudo ufw allow 8000/tcp

# Allow Ollama port (if needed externally)
sudo ufw allow 11434/tcp

# Enable firewall
sudo ufw enable
```

---

## Test API Endpoints

### 1. Health Check
```bash
curl http://your-vps-ip:8000/health
```

### 2. Chat with AI
```bash
curl -X POST http://your-vps-ip:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Halo, saya merasa cemas hari ini"}'
```

### 3. Generate Speech (TTS)
```bash
curl -X POST http://your-vps-ip:8000/api/voice/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Halo, apa kabar?"}' \
  --output speech.mp3
```

### 4. WebSocket Voice Call
Use the Flutter app or test with Python WebSocket client

---

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Ollama only
docker-compose logs -f ollama
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart backend only
docker-compose restart backend
```

### Stop Services
```bash
docker-compose down
```

### Update Code
```bash
# Pull latest changes
git pull

# Rebuild backend
docker-compose up -d --build backend
```

---

## Resource Monitoring

```bash
# Check Docker container stats (RAM, CPU)
docker stats

# Check disk usage
docker system df
```

---

## Switch to Lighter Model (If RAM Limited)

```bash
# Edit docker-compose.yml
nano docker-compose.yml

# Change line:
# OLLAMA_MODEL=phi  (instead of llama2)

# Restart
docker-compose down
docker-compose up -d

# Pull new model
docker exec -it lentera-ollama ollama pull phi
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Port already in use → Change port in docker-compose.yml
# 2. Out of memory → Use lighter model (phi)
# 3. Ollama not ready → Wait 30s after startup
```

### TTS Not Working
```bash
# Edge TTS requires internet connection
# Check internet on VPS:
ping google.com
```

### Whisper Model Download Slow
```bash
# Models auto-download on first use
# Be patient, base model is 75MB
# Check logs:
docker-compose logs -f backend
```

---

## Performance Optimization

### For 8GB RAM VPS
```yaml
OLLAMA_MODEL=phi        # Uses ~2GB RAM
WHISPER_MODEL=base      # Uses ~500MB RAM
```

### For 16GB+ RAM VPS
```yaml
OLLAMA_MODEL=llama2     # Uses ~4GB RAM
WHISPER_MODEL=small     # Uses ~1GB RAM (more accurate)
```

---

## Integration with Flutter

Update your Flutter app:

```dart
// lib/config.dart
class Config {
  static const String apiBaseUrl = "http://your-vps-ip:8000";
  static const String wsVoiceUrl = "ws://your-vps-ip:8000/ws/voice-call";
}
```

Test from Flutter:
1. Chat feature should work immediately
2. Voice call requires microphone permission
3. Test on emulator with Android 10.0.2.2 → your VPS IP

---

## Next Steps

1. ✅ Backend is running on VPS
2. 🔜 Test all endpoints with `test_services.py`
3. 🔜 Connect Flutter app to VPS backend
4. 🔜 Test real voice call from mobile device
5. 🔜 Monitor performance and optimize if needed

---

## Support

Check the full documentation:
- [Walkthrough](file:///C:/Users/Aspire%20Lite%2014/.gemini/antigravity/brain/fc218936-18f6-4b59-9008-80fe3c4ac4cb/walkthrough.md) - Complete implementation details
- [Implementation Plan](file:///C:/Users/Aspire%20Lite%2014/.gemini/antigravity/brain/fc218936-18f6-4b59-9008-80fe3c4ac4cb/implementation_plan.md) - Technical design
- [Backend README](file:///c:/LenteraDreamFlow/backend/README.md) - Local development guide

---

**🎉 Your backend is ready for production testing!**
