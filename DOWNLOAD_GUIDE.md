# Quick Download Guide

## Problem
Automated download from VPS having issues. Need to manually download training data file.

## File to Download
- **Location**: VPS at `/home/Lenteraid/backend/lentera_training_data.jsonl`
- **Destination**: `C:\LenteraDreamFlow\backend\lentera_training_data.jsonl`
- **Size**: ~800 KB (974 examples)

## Method 1: WinSCP (Recommended!)

1. **Download WinSCP**: https://winscp.net/eng/download.php (if not installed)
2. **Connect to VPS**:
   - Host: `84.247.150.83`
   - User: `root`
   - Password: [your VPS password]
3. **Navigate** to `/home/Lenteraid/backend/`
4. **Download** `lentera_training_data.jsonl`
5. **Save to**: `C:\LenteraDreamFlow\backend\`

## Method 2: SCP Command (if you have it)

```powershell
scp root@84.247.150.83:/home/Lenteraid/backend/lentera_training_data.jsonl C:\LenteraDreamFlow\backend\
```

## Method 3: Copy-Paste via SSH

```powershell
# SSH to VPS
ssh root@84.247.150.83

# View file content
cat /home/Lenteraid/backend/lentera_training_data.jsonl

# Copy all output (Ctrl+A, Ctrl+C)
# Create new file: C:\LenteraDreamFlow\backend\lentera_training_data.jsonl
# Paste content (Ctrl+V)
# Save
```

## After Download Complete

Run:
```powershell
cd C:\LenteraDreamFlow\backend
python finetune_openai.py
```

This will:
1. Upload data to OpenAI
2. Submit fine-tuning job
3. Start training (2-4 hours automated!)

## Next Steps After Training Starts

Monitor with:
```powershell
python monitor_training.py --watch
```

---

**Choose whichever method is easiest for you!**

Tell me "downloaded" when file is ready and I'll guide the next step!
