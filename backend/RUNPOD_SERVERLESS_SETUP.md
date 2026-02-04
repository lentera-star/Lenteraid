# RunPod Serverless Endpoint Setup

Guide untuk setup RunPod serverless endpoint dengan model dari Hugging Face.

## Prerequisites

✅ Model sudah di-upload ke Hugging Face: `lentera-star/lentera-llama-3.1-8b`  
✅ Hugging Face token (untuk private model): https://huggingface.co/settings/tokens

## Step 1: Pilih Template di RunPod

Di halaman **Deploy Serverless Endpoint**, ada beberapa opsi:

### Opsi A: vLLM Template (Recommended for GGUF) ⚡

1. Click **"Browse Hub repositories"**
2. Search: `runpod/worker-vllm`
3. Select dan click **Deploy**

### Opsi B: Text Generation Inference (Alternative)

1. Search: `ghcr.io/huggingface/text-generation-inference`
2. Select dan deploy

### Opsi C: Custom Dockerfile (Advanced)

Kalau mau full control, buat custom Dockerfile (lihat di bawah).

## Step 2: Configure Endpoint

### Basic Configuration

**Endpoint Name:** `lentera-ai-inference`

**Container Configuration:**
- **Docker Image:** `runpod/worker-vllm:latest`
- **Container Disk:** 20-40 GB (sesuai model size)

**Environment Variables:**

```bash
# Model dari Hugging Face
MODEL_NAME=lentera-star/lentera-llama-3.1-8b

# Hugging Face Token (jika private)
HUGGING_FACE_HUB_TOKEN=hf_xxxxxxxxxxxxx

# Optional: vLLM settings
MAX_MODEL_LEN=2048
GPU_MEMORY_UTILIZATION=0.9
```

### GPU Selection

**Recommended:**
- **RTX 4090** (24GB VRAM) - Good for 8B models
- **A40** (48GB VRAM) - Better for larger models
- **L40** (48GB VRAM) - Alternative

**Scaling:**
- **Workers (Min):** 0 (untuk auto-scale down)
- **Workers (Max):** 3 (atau sesuai budget)
- **GPUs per Worker:** 1

### Advanced Settings

**Timeout:**
- **Max Execution Time:** 60 seconds
- **Idle Timeout:** 10 seconds

**Concurrency:**
- **Requests per Worker:** 1-3 (tergantung GPU)

## Step 3: Get Endpoint Credentials

Setelah deploy:

1. Buka endpoint details
2. Copy:
   - **Endpoint URL:** `https://api.runpod.ai/v2/{endpoint-id}/runsync`
   - **API Key:** Dari RunPod settings

## Step 4: Test Endpoint

```bash
# Test dengan curl
curl -X POST https://api.runpod.ai/v2/{endpoint-id}/runsync \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Halo, saya merasa sedih hari ini",
      "max_tokens": 200,
      "temperature": 0.7
    }
  }'
```

Expected response:
```json
{
  "output": {
    "text": "Halo, terima kasih sudah berbagi...",
    "tokens": 45
  }
}
```

## Step 5: Update VPS Backend

Update `.env.production` di VPS:

```bash
AI_MODE=runpod
RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/{endpoint-id}/runsync
RUNPOD_API_KEY=your_runpod_api_key
```

Restart backend:
```bash
sudo systemctl restart lentera-backend
```

## Alternative: Custom Dockerfile for RunPod

Kalau mau custom setup, buat `Dockerfile.runpod`:

```dockerfile
FROM runpod/worker-vllm:latest

# Install additional dependencies
RUN pip install --no-cache-dir \
    transformers \
    accelerate

# Set model
ENV MODEL_NAME="lentera-star/lentera-llama-3.1-8b"
ENV HUGGING_FACE_HUB_TOKEN="your_token"

# Optimizations
ENV MAX_MODEL_LEN=2048
ENV GPU_MEMORY_UTILIZATION=0.9
ENV DTYPE="float16"

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "-m", "vllm.entrypoints.api_server"]
```

Upload ke GitHub, lalu di RunPod:
- **Dockerfile Path:** `backend/Dockerfile.runpod`
- **Build Context:** `backend`

## Troubleshooting

### Error: "Model not found"

Check:
- Model name spelling
- HF token valid
- Model is public or token has access

### Error: "Out of memory"

Solutions:
- Reduce `MAX_MODEL_LEN`
- Use larger GPU (A40/L40)
- Enable quantization

### Slow cold start

Normal untuk serverless. Setelah warm-up (1-2 requests), akan cepat.

### High costs

- Set **Workers Min** to 0
- Increase **Idle Timeout** to scale down faster
- Monitor usage in RunPod dashboard

## Cost Estimation

**RTX 4090:**
- Active: ~$0.40/hour
- Idle: $0/hour (dengan min workers = 0)

**Typical usage:**
- 100 requests/day × 2s avg = ~200s/day
- Cost: ~$0.02/day or ~$0.60/month

---

**Next:** Deploy to VPS dan test integration dengan Flutter app!
