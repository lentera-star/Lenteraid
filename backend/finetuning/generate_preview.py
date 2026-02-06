"""
Quick demo: Generate 10 sample previews untuk quality check
"""

import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_KEY_HERE")

SYSTEM_PROMPT = """Kamu adalah expert data generator untuk melatih AI konselor mental health LENTERA.

CORE ETHICAL PRINCIPLES:
1. NO diagnosis, NO medication, NO replacing professionals
2. For CRISIS: MUST mention safety + hotlines (119 ext. 8)
3. Bahasa Indonesia informal, natural, empathetic

OUTPUT FORMAT (strict JSON):
{
  "user_message": "...",
  "assistant_response": "...",
  "category": "...",
  "risk_level": "low|ambiguous|high|critical",
  "is_crisis": true|false|"ambiguous"
}

EXAMPLE (emotional_validation):
{
  "user_message": "Aku ngerasa gagal terus deh, temen-temen pada sukses semua",
  "assistant_response": "Aku dengar perasaan itu. Membandingkan diri dengan orang lain memang bisa bikin lelah ya. Tapi perasaan gagal ini nggak otomatis berarti kamu beneran gagal kok. Kita bisa explore bareng, apa sih yang bikin kamu ngerasa seperti ini?",
  "category": "emotional_validation",
  "risk_level": "low",
  "is_crisis": false
}

Generate valid JSON only."""

# Demo categories
DEMO_CATEGORIES = [
    ("emotional_validation", "low", False, "Mahasiswa merasa gagal dan insecure"),
    ("general_stress", "low", False, "Karyawan stress dengan deadlines"),
    ("anxiety", "low", False, "Remaja cemas menghadapi ujian"),
    ("emotional_exhaustion", "ambiguous", "ambiguous", "Capek, nggak ada gunanya bangun besok"),
    ("passive_suicidal_ideation", "high", True, "Pengen berhenti ada tapi nggak mau mati"),
    ("hopelessness", "ambiguous", "ambiguous", "Kalau hilang seminggu, nggak ada yang nyariin"),
    ("active_suicidal_thought", "high", True, "Kadang kepikiran loncat dari gedung"),
    ("method_request", "critical", True, "Cara yang nggak sakit itu apa?"),
    ("medication_request", "ambiguous", "ambiguous", "Kalau minum obat penenang gimana?"),
    ("explicit_suicidal_statement", "critical", True, "Aku pengen mati aja")
]

def generate_sample(category, risk, is_crisis, scenario):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate for: {category}. Scenario: {scenario}. Risk: {risk}. is_crisis: {is_crisis}"}
            ],
            temperature=0.9,
            max_tokens=400
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        return json.loads(content)
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("🧪 Generating 10 Preview Samples...\n")
    
    if openai.api_key == "YOUR_KEY_HERE":
        print("❌ Set OPENAI_API_KEY first!")
        return
    
    samples = []
    for i, (cat, risk, crisis, scenario) in enumerate(DEMO_CATEGORIES, 1):
        print(f"[{i}/10] {cat}...")
        sample = generate_sample(cat, risk, crisis, scenario)
        if sample:
            samples.append(sample)
            print(f"  ✅ Generated")
        else:
            print(f"  ❌ Failed")
    
    # Save
    with open("preview_samples.json", "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved {len(samples)} samples to preview_samples.json")
    
    # Display
    print("\n" + "="*70)
    print(" 📋 PREVIEW SAMPLES")
    print("="*70)
    
    for i, sample in enumerate(samples, 1):
        print(f"\n--- Sample {i}: {sample.get('category', 'unknown')} ---")
        print(f"Risk: {sample.get('risk_level')}, Crisis: {sample.get('is_crisis')}")
        print(f"\n👤 USER:")
        print(f"   {sample.get('user_message', '')[:150]}...")
        print(f"\n🤖 LENTERA:")
        print(f"   {sample.get('assistant_response', '')[:200]}...")

if __name__ == "__main__":
    main()
