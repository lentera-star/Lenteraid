# Modal Deployment Guide

## Setup

### 1. Install Modal
```bash
pip install modal
```

### 2. Authenticate
```bash
modal setup
```

### 3. Create HuggingFace Secret

Modal needs your HF token to download the model:

```bash
modal secret create huggingface HF_TOKEN=hf_xxxxxxxxxxxxx
```

Replace `hf_xxxxxxxxxxxxx` with your actual HuggingFace token.

## Deploy

```bash
cd backend/modal
modal deploy modal_inference.py
```

Output will show your endpoint URL:
```
✓ Created web function generate => https://yourname--lentera-llama-generate.modal.run
```

## Test

### Test with curl:
```bash
curl -X POST https://yourname--lentera-llama-generate.modal.run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Halo, aku merasa cemas"}
    ],
    "max_tokens": 256,
    "temperature": 0.7
  }'
```

### Expected Response:
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Response from model..."
    }
  }]
}
```

## Update Supabase Edge Function

Once deployed, update your Supabase proxy:

```typescript
const MODAL_ENDPOINT = 'https://yourname--lentera-llama-generate.modal.run';
```

## Monitor Usage

Check usage at: https://modal.com/usage

## Cost Estimate

- A10G GPU: ~$0.001/second
- Average request: 5 seconds = $0.005
- $5 credit = ~1,000 requests ✅
