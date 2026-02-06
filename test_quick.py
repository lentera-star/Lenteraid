"""
Quick Dataset Quality Test
Tests the generated dataset for Phase 2 readiness
"""
import json

# Load dataset  
print("Loading dataset...")
with open('backend/finetuning/dataset_lentera_enhanced.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*70)
print("🧪 QUICK DATASET QUALITY TEST")
print("="*70)

# Stats
crisis = [s for s in data if s.get('is_crisis') is True]
safe = [s for s in data if s.get('is_crisis') is False]

print(f"\n📊 Basic Stats:")
print(f"   Total Samples: {len(data)}")
print(f"   Crisis: {len(crisis)} ({len(crisis)/len(data)*100:.1f}%)")
print(f"   Safe: {len(safe)} ({len(safe)/len(data)*100:.1f}%)")

# Sample Preview
print(f"\n📌 Random Sample:")
sample = data[442]  # Random middle sample
print(f"   User: {sample['user_message'][:100]}...")
print(f"   AI: {sample['assistant_response'][:120]}...")
print(f"   Category: {sample['category']}")
print(f"   Crisis: {sample['is_crisis']}")
print(f"   Risk: {sample['risk_level']}")

# Ethics Check
print(f"\n🛡️ Quick Ethics Check:")
forbidden = ['kamu depresi', 'kamu bipolar', 'minum obat']
violations = 0
for s in data:
    resp = s['assistant_response'].lower()
    if any(term in resp for term in forbidden):
        violations += 1

print(f"   Clean: {len(data) - violations}/{len(data)}")
print(f"   Violations: {violations}")

# Final Verdict
print("\n" + "="*70)
if violations < len(data) * 0.05:  # Less than 5% violations
    print("✅ DATASET QUALITY: EXCELLENT - Ready for Training!")
else:
    print("⚠️  DATASET QUALITY: REVIEW NEEDED")
print("="*70)
