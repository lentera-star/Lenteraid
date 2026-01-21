"""
Convert LENTERA dataset to ShareGPT format for Axolotl training
"""

import json
from pathlib import Path
from typing import List, Dict
import random

INPUT_FILE = Path(__file__).parent / "dataset_combined.json"
OUTPUT_TRAIN = Path(__file__).parent / "train.jsonl"
OUTPUT_VAL = Path(__file__).parent / "val.jsonl"

VAL_SPLIT = 0.1  # 10% validation


def convert_to_sharegpt(sample: Dict) -> Dict:
    """Convert single sample to ShareGPT format"""
    
    return {
        "conversations": [
            {
                "from": "human",
                "value": sample["user_message"]
            },
            {
                "from": "gpt",
                "value": sample["assistant_response"]
            }
        ],
        # Preserve metadata for analysis
        "category": sample.get("category", "unknown"),
        "risk_level": sample.get("risk_level", "unknown"),
        "is_crisis": sample.get("is_crisis", False)
    }


def main():
    print("=" * 60)
    print(" 🔄 Convert to ShareGPT Format")
    print("=" * 60)
    print()
    
    # Load dataset
    print(f"Loading {INPUT_FILE.name}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    print(f"  ✅ Loaded {len(dataset)} samples\n")
    
    # Convert to ShareGPT
    print("Converting to ShareGPT format...")
    sharegpt_data = [convert_to_sharegpt(sample) for sample in dataset]
    print(f"  ✅ Converted {len(sharegpt_data)} samples\n")
    
    # Shuffle
    random.shuffle(sharegpt_data)
    
    # Split train/val
    val_size = int(len(sharegpt_data) * VAL_SPLIT)
    train_data = sharegpt_data[val_size:]
    val_data = sharegpt_data[:val_size]
    
    print(f"Split:")
    print(f"  Train: {len(train_data)}")
    print(f"  Val: {len(val_data)}\n")
    
    # Save train
    with open(OUTPUT_TRAIN, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ Saved: {OUTPUT_TRAIN.name}")
    
    # Save val
    with open(OUTPUT_VAL, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ Saved: {OUTPUT_VAL.name}")
    
    # Stats
    print("\n" + "=" * 60)
    print(" 📊 Dataset Statistics")
    print("=" * 60)
    
    from collections import Counter
    
    # Category distribution (train only, to avoid data leakage)
    category_counts = Counter(s["category"] for s in train_data)
    print("\nCategory Distribution (Train):")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    # Risk distribution
    risk_counts = Counter(s["risk_level"] for s in train_data)
    print("\nRisk Level Distribution (Train):")
    for risk, count in sorted(risk_counts.items(), key=lambda x: -x[1]):
        print(f"  {risk}: {count}")
    
    # Crisis distribution
    crisis_train = sum(1 for s in train_data if s.get("is_crisis") is True)
    ambiguous_train = sum(1 for s in train_data if s.get("is_crisis") == "ambiguous")
    safe_train = sum(1 for s in train_data if s.get("is_crisis") is False)
    
    print(f"\nCrisis Distribution (Train):")
    print(f"  SAFE: {safe_train} ({safe_train/len(train_data)*100:.1f}%)")
    print(f"  AMBIGUOUS: {ambiguous_train} ({ambiguous_train/len(train_data)*100:.1f}%)")
    print(f"  CRISIS: {crisis_train} ({crisis_train/len(train_data)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✅ Ready for Axolotl training!")
    print(" Next: Run train.sh in Google Colab")
    print("=" * 60)


if __name__ == "__main__":
    main()
