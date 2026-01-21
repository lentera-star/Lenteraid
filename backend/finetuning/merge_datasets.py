"""
Merge local and VPS datasets for LENTERA Fine-Tuning
"""

import json
from pathlib import Path

# Config
BASE_DIR = Path(__file__).parent.parent.parent # Root dir (assuming script is in backend/finetuning)
SCRIPT_DIR = Path(__file__).parent

LOCAL_FILE = SCRIPT_DIR / "dataset_lentera_enhanced.json"
VPS_FILE = BASE_DIR / "dataset_vps.json"
OUTPUT_FILE = SCRIPT_DIR / "dataset_combined.json"

def main():
    print("="*60)
    print(" 🔄 LENTERA Dataset Merger")
    print("="*60)
    
    # Load Local
    if LOCAL_FILE.exists():
        with open(LOCAL_FILE, "r", encoding="utf-8") as f:
            local_data = json.load(f)
        print(f"✅ Loaded Local Data: {len(local_data)} samples")
    else:
        print(f"⚠️ Local file not found: {LOCAL_FILE}")
        local_data = []

    # Load VPS
    if VPS_FILE.exists():
        with open(VPS_FILE, "r", encoding="utf-8") as f:
            vps_data = json.load(f)
        print(f"✅ Loaded VPS Data: {len(vps_data)} samples")
    else:
        print(f"⚠️ VPS file not found: {VPS_FILE}")
        print("   (Did you download it as 'dataset_vps.json'?)")
        vps_data = []
        
    # Merge
    combined = local_data + vps_data
    
    # Dedup (optional, based on user_message)
    seen = set()
    deduped = []
    duplicates = 0
    
    for item in combined:
        msg = item.get("user_message", "").strip()
        if msg in seen:
            duplicates += 1
            continue
        seen.add(msg)
        deduped.append(item)
        
    print(f"\n📊 Stats:")
    print(f"   Total Raw: {len(combined)}")
    print(f"   Duplicates Removed: {duplicates}")
    print(f"   Final Count: {len(deduped)}")
    
    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)
        
    print(f"\n✅ Saved merged dataset to: {OUTPUT_FILE}")
    print("Next: Run convert_to_sharegpt.py")

if __name__ == "__main__":
    main()
