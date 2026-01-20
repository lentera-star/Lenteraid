"""
Convert Golden Safety Responses to OpenAI Fine-Tuning Format
Creates training data from ChatGPT-verified golden responses
"""
import json

# Read golden responses
with open('golden_safety_responses.jsonl', 'r', encoding='utf-8') as f:
    golden_responses = [json.loads(line) for line in f]

# Convert to OpenAI format
openai_training_data = []

# System prompt for safety-focused training
SAFETY_SYSTEM_PROMPT = """Kamu adalah LENTERA, asisten AI untuk konseling kesehatan mental yang sangat fokus pada keselamatan pengguna.

PRINSIP UTAMA:
- Empati dan validasi emosi SELALU lebih dulu
- Jangan pernah menolak atau meninggalkan user ("aku bukan orang yang tepat")
- Untuk krisis: tetap hadir sambil mengarahkan ke bantuan profesional
- Hard boundary tanpa abandonment

TEMPLATE RESPONS:
1. LOW RISK: Validasi → Eksplorasi → Dukungan
2. AMBIGUOUS: Validasi → Boundary jelas → Klarifikasi
3. HIGH RISK/CRISIS: Empati → Safety stance → Eskalasi manusiawi → Tetap hadir
"""

for item in golden_responses:
    # Create OpenAI training example
    training_example = {
        "messages": [
            {
                "role": "system",
                "content": SAFETY_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": item["prompt"]
            },
            {
                "role": "assistant",
                "content": item["response"]
            }
        ]
    }
    openai_training_data.append(training_example)

# Save as OpenAI-compatible JSONL
with open('lentera_safety_training.jsonl', 'w', encoding='utf-8') as f:
    for example in openai_training_data:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"✅ Converted {len(openai_training_data)} golden responses to OpenAI format")
print(f"📄 Saved to: lentera_safety_training.jsonl")
print(f"\nCategories covered:")
for item in golden_responses:
    print(f"  - {item['category']}: {item['risk_level']}")
