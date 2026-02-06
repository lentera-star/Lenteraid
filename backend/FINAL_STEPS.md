# 🎯 After Ollama Import - Final Steps

**Run these after `ollama create` shows "success"**

---

## 1️⃣ Update Backend Config

```bash
cd /opt/lentera-backend
nano .env
```

**Find and change**:
```
OLLAMA_MODEL=lentera-mental-health
```

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 2️⃣ Restart Backend

```bash
systemctl restart lentera-backend
sleep 3
systemctl status lentera-backend
```

**Expected**: `active (running)` ✅

---

## 3️⃣ Test API

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Halo LENTERA"}' | jq
```

---

## ✅ Done!

API: `http://84.247.150.83:8000/api/chat`
