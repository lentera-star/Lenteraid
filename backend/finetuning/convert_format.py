"""
Convert raw dataset to Alpaca format for fine-tuning
"""

import json
import random

INPUT_FILE = "dataset_lentera_raw.json"
OUTPUT_FILE = "dataset_lentera_alpaca.json"

INSTRUCTION = """Kamu adalah LENTERA, AI konselor kesehatan mental yang empatik dan supportif. 

Tugasmu:
- Dengarkan dengan penuh perhatian
- Validasi perasaan user
- Berikan dukungan emosional
- Tawarkan coping strategy praktis
- Jangan mendiagnosa kondisi medis

Gunakan bahasa Indonesia yang hangat dan natural."""


def convert_to_alpaca(raw_dataset):
    """Convert raw conversations to Alpaca format"""
    alpaca_data = []
    
    for item in raw_dataset:
        conversations = item.get("conversation", [])
        
        # Extract user-assistant pairs
        for i in range(0, len(conversations) - 1, 2):
            if i + 1 < len(conversations):
                user_msg = conversations[i]
                assistant_msg = conversations[i + 1]
                
                # Validate roles
                if user_msg.get("role") == "user" and assistant_msg.get("role") == "assistant":
                    alpaca_data.append({
                        "instruction": INSTRUCTION,
                        "input": user_msg.get("content", ""),
                        "output": assistant_msg.get("content", "")
                    })
    
    return alpaca_data


def validate_sample(sample):
    """Check if sample meets quality criteria"""
    input_text = sample["input"]
    output_text = sample["output"]
    
    # Basic checks
    if len(input_text) < 10:
        return False, "Input too short"
    if len(output_text) < 20:
        return False, "Output too short"
    
    # Check for problematic content
    danger_keywords = ["bunuh diri", "suicide", "mau mati", "self harm"]
    for keyword in danger_keywords:
        if keyword.lower() in output_text.lower():
            return False, f"Contains dangerous keyword: {keyword}"
    
    return True, "OK"


def main():
    print("=" * 60)
    print(" 🔄 Dataset Format Converter")
    print("=" * 60)
    print()
    
    # Load raw dataset
    print(f"Loading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    print(f"  ✅ Loaded {len(raw_data)} dialogues\n")
    
    # Convert to Alpaca
    print("Converting to Alpaca format...")
    alpaca_data = convert_to_alpaca(raw_data)
    print(f"  ✅ Created {len(alpaca_data)} training samples\n")
    
    # Validate samples
    print("Validating quality...")
    valid_samples = []
    rejected = []
    
    for sample in alpaca_data:
        is_valid, reason = validate_sample(sample)
        if is_valid:
            valid_samples.append(sample)
        else:
            rejected.append((sample, reason))
    
    print(f"  ✅ Valid: {len(valid_samples)}")
    print(f"  ⚠️  Rejected: {len(rejected)}\n")
    
    # Save valid samples
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(valid_samples, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to: {OUTPUT_FILE}\n")
    
    # Show random samples
    print("=" * 60)
    print(" 📋 Sample Preview (3 random samples)")
    print("=" * 60)
    
    if len(valid_samples) >= 3:
        samples = random.sample(valid_samples, 3)
        for i, sample in enumerate(samples, 1):
            print(f"\n--- Sample {i} ---")
            print(f"USER: {sample['input'][:100]}...")
            print(f"LENTERA: {sample['output'][:100]}...")
    
    print("\n" + "=" * 60)
    print(f"✅ Conversion Complete!")
    print(f"   Total Samples: {len(valid_samples)}")
    print(f"   Ready for fine-tuning!")
    print("=" * 60)


if __name__ == "__main__":
    main()
