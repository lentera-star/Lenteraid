# LENTERA Data Generation - Quick Start

## Prerequisites

```bash
pip install openai
export OPENAI_API_KEY='your-openai-api-key'
```

## Generate Training Data

### Basic Usage (100 examples)
```bash
cd backend
python generate_training_data.py --num 100 --output lentera_data.jsonl
```

### Generate with train/val split
```bash
python generate_training_data.py --num 1000 --split
```

This will create:
- `lentera_training_data.jsonl` (all data)
- `train.jsonl` (90% - for training)
- `val.jsonl` (10% - for validation)

## Dataset Distribution

- **30% Crisis scenarios** (suicide, self-harm) - HIGHEST PRIORITY
- **70% Other scenarios**:
  - Depression
  - Anxiety
  - Relationships
  - Family issues
  - Work stress
  - Academic pressure
  - Self-esteem

## Ethics Validation

Script automatically validates:
- ✅ No diagnosis phrases
- ✅ No medication recommendations
- ✅ Crisis responses include hotlines (119 ext 8, 1500-454)
- ✅ Empathetic, validating tone
- ✅ Professional referrals when needed

## Cost Estimation

**Using GPT-4**:
- ~$0.03 per example
- 100 examples = ~$3
- 1,000 examples = ~$30
- 5,000 examples = ~$150

**Tips to save cost**:
1. Start with 100 examples for testing
2. Use GPT-3.5-turbo ($0.001/example) for initial batches
3. Use GPT-4 only for crisis scenarios

## Manual Review Required

**After generation**:
1. Random sample 50 examples
2. Check ethics compliance
3. Verify Indonesian naturalness
4. Get mental health expert to review crisis responses

## Next Steps

Once you have `train.jsonl` and `val.jsonl`:

1. **Setup Axolotl** (see FINE_TUNING_GUIDE.md)
2. **Train model** (~3-6 hours on A100)
3. **Evaluate** ethics compliance
4. **Deploy** to production

---

**For more details**: See `FINE_TUNING_GUIDE.md`
