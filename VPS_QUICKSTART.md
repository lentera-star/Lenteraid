# 🚀 VPS QUICK START

## ⚡ Fast Track Deployment (< 30 mins)

### 1️⃣ Prepare Locally

```bash
# Update Flutter config with your VPS IP
# Edit: lib/config/api_config.dart
# Change: _vpsUrl = 'http://YOUR_VPS_IP:8000'
```

### 2️⃣ Upload to VPS

```bash
# Replace USER and VPS_IP with your values
scp Meta-Llama-3.1-8B-Instruct.Q2_K.gguf user@VPS_IP:~/
scp vps-setup.sh user@VPS_IP:~/
scp deploy-production.sh user@VPS_IP:~/
```

### 3️⃣ Setup on VPS

```bash
ssh user@VPS_IP

# Run setup (installs Ollama, imports model, configures backend)
chmod +x vps-setup.sh
./vps-setup.sh
```

### 4️⃣ Deploy Production

```bash
# With domain (gets SSL automatically)
DOMAIN=api.yourdomain.com EMAIL=you@email.com ./deploy-production.sh

# Without domain (HTTP only)
./deploy-production.sh
```

### 5️⃣ Test

```bash
# Test from VPS
curl http://localhost:8000/health

# Test from anywhere
curl http://YOUR_VPS_IP/health
# Or: curl https://api.yourdomain.com/health
```

### 6️⃣ Connect Flutter

Update and run your Flutter app - it's ready!

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `lib/config/api_config.dart` | Backend URL configuration |
| `lib/services/ai_service.dart` | AI API client |
| `vps-setup.sh` | One-command VPS setup |
| `deploy-production.sh` | Production deployment |
| `test-vps-integration.sh` | Integration tests |
| `nginx-lentera.conf` | Nginx config |
| `lentera-backend.service` | Systemd service |
| `backend/.env.example` | Environment template |

---

## 🆘 Troubleshooting

**Backend not starting?**
```bash
sudo journalctl -u lentera-backend -n 50
```

**Model not loading?**
```bash
ollama list
ollama run lentera-dreamflow "test"
```

**See full guide:** `DEPLOYMENT_GUIDE.md`

---

**Ready to deploy!** 🎉
