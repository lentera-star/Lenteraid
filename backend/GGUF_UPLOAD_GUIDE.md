# 📤 GGUF Upload to VPS - All Scenarios

Choose your scenario based on where your .gguf file is located.

---

## 🅰️ Scenario A: File in Google Colab

### Method 1: Direct Download to VPS (FASTEST ⚡)

**In Google Colab cell:**

```python
# Install rclone or use wget to upload to VPS
# Get download link from Colab

from google.colab import files
import os

# Find your .gguf file
!ls -lh *.gguf

# Get file path
gguf_file = !ls *.gguf
print(f"File: {gguf_file[0]}")
```

**Then SSH to VPS and download:**

```bash
# In VPS SSH terminal
cd /opt/lentera-backend/models/

# Download from Colab (need Colab's public URL)
# Option 1: If Colab has ngrok/cloudflare link
wget <colab-ngrok-url>/lentera-q4.gguf

# Option 2: Upload to temp storage first (Google Drive)
# Then download to VPS
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=FILE_ID' -O lentera-mental-health.gguf
```

### Method 2: Via Google Drive (RELIABLE)

**In Google Colab:**

```python
from google.colab import drive
drive.mount('/content/drive')

# Copy to Google Drive
!cp *.gguf /content/drive/MyDrive/lentera-mental-health.gguf

# Get shareable link from Google Drive
# Right-click file → Get link → Anyone with link can view
```

**Then from VPS:**

```bash
# Install gdown (Google Drive downloader)
pip install gdown

# Download (replace FILE_ID with your file ID)
cd /opt/lentera-backend/models/
gdown https://drive.google.com/uc?id=FILE_ID -O lentera-mental-health.gguf
```

---

## 🅱️ Scenario B: File Already in Windows

**Open new PowerShell window (don't close SSH):**

```powershell
# Find your .gguf file first
# Example locations:
# - C:\Users\MyBook Army\Downloads\
# - C:\LenteraDreamFlow\backend\finetuning\
# - Desktop, etc.

# Upload via SCP
scp "C:\path\to\your\lentera-q4.gguf" root@84.247.150.83:/opt/lentera-backend/models/lentera-mental-health.gguf
```

**Example if file in Downloads:**

```powershell
scp "C:\Users\MyBook Army\Downloads\lentera-q4.gguf" root@84.247.150.83:/opt/lentera-backend/models/lentera-mental-health.gguf
```

**Example if file in backend folder:**

```powershell
scp "C:\LenteraDreamFlow\backend\finetuning\lentera-q4.gguf" root@84.247.150.83:/opt/lentera-backend/models/lentera-mental-health.gguf
```

---

## 🅲️ Scenario C: File in Other Location

### From Any Server with SSH Access:

```bash
# From source server
scp /path/to/lentera-q4.gguf root@84.247.150.83:/opt/lentera-backend/models/lentera-mental-health.gguf
```

### From HTTP/HTTPS URL:

```bash
# In VPS SSH terminal
cd /opt/lentera-backend/models/
wget <direct-download-url> -O lentera-mental-health.gguf
```

### From Cloud Storage (Dropbox, OneDrive, etc.):

**Get direct download link, then:**

```bash
# In VPS
cd /opt/lentera-backend/models/
curl -L -o lentera-mental-health.gguf "<direct-download-link>"
```

---

## ✅ After Upload - Verify

**In VPS SSH terminal:**

```bash
# Check file exists and size
ls -lh /opt/lentera-backend/models/

# Expected output:
# -rw-r--r-- 1 root root 4.7G Jan 24 21:35 lentera-mental-health.gguf

# Verify file integrity (optional)
file /opt/lentera-backend/models/lentera-mental-health.gguf
# Should say: "data" or "GGUF model"
```

---

## 🚀 Once Verified - Continue to Import

After file uploaded, proceed to **Step 5** in `implementation_plan.md`:

```bash
cd /opt/lentera-backend
# Create Modelfile
# Import to Ollama
# etc.
```

---

## 📊 Upload Progress

For large files (4-5GB), track upload:

**From Windows (PowerShell):**
```powershell
# Use WinSCP for GUI with progress bar
# Or use verbose SCP
scp -v "C:\path\to\file.gguf" root@84.247.150.83:/opt/lentera-backend/models/
```

**From Linux/Colab:**
```bash
# Use rsync with progress
rsync -avP lentera-q4.gguf root@84.247.150.83:/opt/lentera-backend/models/lentera-mental-health.gguf
```

---

## 💡 Pro Tips

1. **Rename consistently**: Always use `lentera-mental-health.gguf` on VPS
2. **Check disk space first**: `df -h` (need ~5GB free)
3. **Upload during off-peak**: Faster upload speed
4. **Verify MD5/SHA**: If file integrity critical

---

**Pick your scenario and upload!** 📤🚀
