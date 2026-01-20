# Phase 1: Dataset Generation

## Quick Start

### 1. Install Dependencies
```bash
pip install openai
```

### 2. Set API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-proj-YOUR_KEY_HERE"

# Linux/Mac
export OPENAI_API_KEY="sk-proj-YOUR_KEY_HERE"
```

### 3. Generate Dataset
```bash
python generate_dataset.py
```

**Expected Output**:
- `dataset_lentera_raw.json` (~500KB for 30 dialogues)
- Backup files every 25 dialogues

### 4. Convert to Training Format
```bash
python convert_format.py
```

**Expected Output**:
- `dataset_lentera_alpaca.json` (ready for fine-tuning)

---

## Cost Estimation

Using **GPT-4o-mini**:
- 30 scenarios × ~800 tokens = 24K tokens
- Input: ~$0.01
- Output: ~$0.02
- **Total**: ~$0.03

Using **GPT-4**:
- 30 scenarios × ~800 tokens = 24K tokens
- **Total**: ~$0.60

---

## Next Steps

After completing Phase 1, proceed to:
- **Phase 2**: Fine-tuning using Google Colab
  (See Colab notebook in `colab_notebooks/`)

---

## File Structure

```
finetuning/
├── README.md (this file)
├── generate_dataset.py (Step 1)
├── convert_format.py (Step 2)
├── dataset_lentera_raw.json (Generated)
├── dataset_lentera_alpaca.json (For training)
└── dataset_backup_*.json (Automatic backups)
```
