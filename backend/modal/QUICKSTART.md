# Quick Start - Modal Deployment

## Files Ready ✅
- `backend/modal/modal_inference.py` - Modal app
- `backend/modal/README.md` - Full guide

## Deploy Commands (Run in Order):

### 1. Install Modal
```bash
pip install modal
```

### 2. Authenticate
```bash
modal setup
```

### 3. Add HuggingFace Token
```bash
modal secret create huggingface HF_TOKEN=your_hf_token
```

### 4. Deploy
```bash
cd backend/modal
modal deploy modal_inference.py
```

## Expected Output
After deployment, you'll get a URL like:
```
https://yourname--lentera-llama-generate.modal.run
```

## Cost
$5 credit = ~1,000 requests ✅

## Next
Update Supabase Edge Function with the Modal endpoint URL.
