# Upload Model ke Hugging Face untuk RunPod

Guide untuk upload model LENTERA dari Google Drive ke Hugging Face, kemudian deploy ke RunPod serverless endpoint.

## Step 1: Download Model dari Google Drive

```bash
# Install gdown
pip install gdown

# Download model
gdown https://drive.google.com/uc?id=1s5WY8PM8vKTcfDvUaj5kMd4W2A3fqtvj -O lentera-model.gguf

# Atau kalau file besar, pakai aria2c untuk resume support
# Download aria2c terlebih dahulu, lalu:
# aria2c -x 16 -s 16 "https://drive.google.com/uc?id=1s5WY8PM8vKTcfDvUaj5kMd4W2A3fqtvj&export=download" -o lentera-model.gguf
```

## Step 2: Buat Repository di Hugging Face

1. Buka https://huggingface.co/new
2. Repository name: `lentera-llama-3.1-8b` (atau nama lain)
3. Owner: `lentera-star` (atau username kamu)
4. Type: **Model**
5. License: Pilih yang sesuai (misal: `apache-2.0`)
6. Click **Create repository**

## Step 3: Upload Model ke Hugging Face

### Opsi A: Via Web Interface (Mudah, untuk file < 5GB)

1. Buka repo yang baru dibuat
2. Click **Files and versions** tab
3. Click **Add file** → **Upload files**
4. Drag & drop `lentera-model.gguf`
5. Commit changes

### Opsi B: Via CLI (Recommended, untuk file besar)

```bash
# Install Hugging Face Hub
pip install huggingface_hub

# Login ke HF (butuh token dari https://huggingface.co/settings/tokens)
huggingface-cli login

# Upload model
huggingface-cli upload lentera-star/lentera-llama-3.1-8b lentera-model.gguf

# Atau kalau ada folder model dengan multiple files:
# huggingface-cli upload lentera-star/lentera-llama-3.1-8b ./model_folder --repo-type model
```

### Opsi C: Via Python (Programmatic)

```python
from huggingface_hub import HfApi

api = HfApi()

# Upload single file
api.upload_file(
    path_or_fileobj="lentera-model.gguf",
    path_in_repo="lentera-model.gguf",
    repo_id="lentera-star/lentera-llama-3.1-8b",
    repo_type="model",
)
```

## Step 4: Buat Model Card (README.md)

Tambahkan README.md di repo HF:

```markdown
---
license: apache-2.0
language:
- id
- en
tags:
- mental-health
- llama-3
- indonesian
- counseling
---

# LENTERA - Mental Health Counseling AI

Fine-tuned LLaMA 3.1-8B model for Indonesian mental health support.

## Model Details

- **Base Model**: Meta-Llama-3.1-8B
- **Fine-tuned for**: Mental health counseling in Indonesian
- **Format**: GGUF (quantized)
- **Use Case**: LENTERA mobile app
- **License**: Apache 2.0

## Usage

This model is optimized for mental health conversations with:
- Crisis detection
- Empathetic responses
- Safety-first approach
- Indonesian language support

## Ethical Guidelines

This model follows strict ethical guidelines for mental health AI.
See ethics documentation in the LENTERA repository.
```

## Step 5: Verify Upload

1. Check repo: `https://huggingface.co/lentera-star/lentera-llama-3.1-8b`
2. Verify file uploaded correctly
3. Copy model ID: `lentera-star/lentera-llama-3.1-8b`

## Next: Deploy to RunPod Serverless

Setelah model di HF, lanjut ke `RUNPOD_SERVERLESS_SETUP.md` untuk deploy endpoint.

---

**Note:** Kalau file GGUF sangat besar (>10GB), pertimbangkan:
- Upload via Git LFS: `git lfs install && git lfs track "*.gguf"`
- Atau pakai RunPod Network Storage langsung
