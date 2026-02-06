import json
import random
from collections import Counter

# Load dataset
with open('dataset_lentera_enhanced.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*70)
print("🧪 QUICK DATASET QUALITY TEST")
print("="*70)

# 1. Basic Stats
print(f"\n📊 Dataset Overview:")
print(f"   Total Samples: {len(data)}")
print(f"   File Size: 834KB")

# 2. Crisis Distribution
crisis = [s for s in data if s.get('is_crisis') == True]
safe = [s for s in data if s.get('is_crisis') == False]
print(f"\n🚨 Crisis Distribution:")
print(f"   Crisis: {len(crisis)} ({len(crisis)/len(data)*100:.1f}%)")
print(f"   Safe: {len(safe)} ({len(safe)/len(data)*100:.1f}%)")

# 3. Category Distribution (Top 10)
categories = Counter(s['category'] for s in data)
print(f"\n📂 Top 10 Categories:")
for cat, count in categories.most_common(10):
    print(f"   {cat}: {count}")

# 4. Ethics Validation
print(f"\n🛡️ Ethics Compliance Check:")
diagnosis_terms = ['kamu depresi', 'kamu bipolar', 'kamu mengalami', 'diagnosismu']
medication_terms = ['minum obat', 'konsumsi antidepresan', 'pakai ssri']
forbidden_found = 0

for s in data:
    response = s['assistant_response'].lower()
    if any(term in response for term in diagnosis_terms + medication_terms):
        forbidden_found += 1

print(f"   Clean responses: {len(data) - forbidden_found}/{len(data)} ({(len(data)-forbidden_found)/len(data)*100:.1f}%)")
print(f"   Violations: {forbidden_found}")

# 5. Crisis Safety Check
crisis_with_hotline = 0
for s in data:
    if s.get('is_crisis') == True:
        response = s['assistant_response']
        if '119' in response or 'hotline' in response.lower() or 'keselamatan' in response.lower():
            crisis_with_hotline += 1

if len(crisis) > 0:
    print(f"\n📞 Crisis Safety:")
    print(f"   Crisis with safety elements: {crisis_with_hotline}/{len(crisis)} ({crisis_with_hotline/len(crisis)*100:.1f}%)")

# 6. Random Sample Preview
print(f"\n📌 Random Sample Preview (3 examples):")
print("="*70)
random.shuffle(data)
for i, s in enumerate(data[:3], 1):
    print(f"\n🔹 Sample {i}:")
    print(f"   User: {s['user_message'][:80]}...")
    print(f"   AI: {s['assistant_response'][:120]}...")
    print(f"   Category: {s['category']} | Crisis: {s['is_crisis']} | Risk: {s['risk_level']}")

# 7. Final Verdict
print("\n" + "="*70)
ethics_ok = (len(data) - forbidden_found) / len(data) > 0.95
crisis_ok = len(crisis) == 0 or crisis_with_hotline / len(crisis) > 0.90

if ethics_ok and crisis_ok:
    print("✅ DATASET QUALITY: EXCELLENT - Ready for Training!")
elif ethics_ok:
    print("⚠️  DATASET QUALITY: GOOD - Minor issues in crisis responses")
else:
    print("❌ DATASET QUALITY: NEEDS REVIEW - Ethics violations found")

print("="*70)
