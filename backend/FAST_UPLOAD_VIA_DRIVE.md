# 🚀 FASTEST Method: Upload via Google Drive

**Much faster than direct SCP!** ⚡

---

## 📤 Step 1: Upload File to Google Drive

1. **Buka Google Drive**: https://drive.google.com
2. **Upload file** `lentera-q4.gguf` dari Downloads
   - Drag & drop, atau
   - Click "New" → "File upload"
3. **Tunggu upload selesai** (biasanya lebih cepat dari SCP)

---

## 🔗 Step 2: Get Shareable Link

1. **Right-click** file yang sudah uploaded
2. **Share** → "Anyone with the link"
3. **Copy link**
   
   Example: `https://drive.google.com/file/d/1ABC123xyz456/view?usp=sharing`

4. **Extract FILE_ID** dari URL
   
   From: `https://drive.google.com/file/d/1ABC123xyz456/view?usp=sharing`
   
   FILE_ID = `1ABC123xyz456`

---

## ⬇️ Step 3: Download to VPS (FAST!)

**SSH ke VPS** (reconnect jika perlu):

```bash
ssh root@84.247.150.83
```

**Di VPS, run:**

```bash
# Install gdown (Google Drive downloader)
pip3 install gdown

# Create models directory
mkdir -p /opt/lentera-backend/models
cd /opt/lentera-backend/models

# Download from Google Drive (GANTI FILE_ID!)
gdown https://drive.google.com/uc?id=YOUR_FILE_ID_HERE -O lentera-mental-health.gguf

# Atau kalau gdown error, pakai ini:
gdown --fuzzy https://drive.google.com/file/d/YOUR_FILE_ID_HERE/view?usp=sharing -O lentera-mental-health.gguf
```

**Replace `YOUR_FILE_ID_HERE` dengan FILE_ID kamu!**

---

## 📊 Monitor Progress

VPS ke Google Drive biasanya **SANGAT CEPAT** (10-50 MB/s):

```bash
# Check download progress
watch -n 1 'ls -lh /opt/lentera-backend/models/'
```

Press `Ctrl+C` to exit watch

---

## ✅ After Download Complete

Verify file:

```bash
ls -lh /opt/lentera-backend/models/
# Expected: ~4-5GB file
```

Then proceed to **post_upload_commands.md** untuk import ke Ollama!

---

## 💡 Alternative: Direct Google Drive Link

Kalau gdown tidak work, coba wget:

```bash
cd /opt/lentera-backend/models

# Method 1: Using gdrive-dl
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=YOUR_FILE_ID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=YOUR_FILE_ID" -O lentera-mental-health.gguf && rm -rf /tmp/cookies.txt

# Method 2: Using curl with redirect
curl -L -o lentera-mental-health.gguf "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID"
```

---

## ⚡ Speed Comparison

| Method | Speed | Time (4.5GB) |
|--------|-------|--------------|
| SCP from Windows | 172 KB/s | ~7 hours ❌ |
| Google Drive → VPS | 10-50 MB/s | **2-10 minutes** ✅ |

**Google Drive wins!** 🏆

---

**Next**: Upload to Drive, copy FILE_ID, then run gdown command di VPS!
