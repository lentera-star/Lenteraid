"""
LENTERA Dataset Generator

Generate synthetic mental health counseling dialogues using OpenAI ChatGPT.
"""

import openai
import json
import time
import os
from typing import Dict, Optional

# ===== CONFIGURATION =====
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_KEY_HERE")
MODEL = "gpt-4o-mini"  # Cheaper option
OUTPUT_FILE = "dataset_lentera_raw.json"

# ===== SCENARIOS =====
SCENARIOS = [
    "Mahasiswa stres karena deadline tugas menumpuk",
    "Remaja merasa kesepian dan tidak punya teman dekat",
    "Pekerja merasa burnout di kantor",
    "Seseorang cemas menghadapi ujian penting",
    "Anak kuliah overthinking tentang masa depan karir",
    "Seseorang sedih karena putus dengan pacar",
    "Mahasiswa insecure dengan pencapaian teman-temannya",
    "Pekerja konflik dengan atasan di kantor",
    "Remaja cemas tentang body image",
    "Seseorang merasa stuck dalam hidup dan tidak tahu harus apa",
    "Mahasiswa homesick saat kuliah di luar kota",
    "Seseorang overthinking di malam hari tidak bisa tidur",
    "Pekerja merasa tidak dihargai di tempat kerja",
    "Remaja takut berbicara di depan umum",
    "Mahasiswa prokrastinasi terus-menerus",
    "Seseorang merasa guilty karena tidak memenuhi ekspektasi orangtua",
    "Pekerja imposter syndrome di kantor baru",
    "Remaja bullied di sekolah",
    "Mahasiswa tidak percaya diri dengan kemampuan diri",
    "Seseorang merasa anxious tanpa alasan jelas",
    "Pekerja merasa lonely meski dikelilingi orang",
    "Mahasiswa takut gagal dan mengecewakan keluarga",
    "Remaja insecure dengan penampilan fisik",
    "Seseorang merasa hidup tidak berwarna",
    "Pekerja stress dengan target pekerjaan yang tidak realistis",
    "Mahasiswa overthinking tentang pendapat orang lain",
    "Remaja merasa tidak cocok dengan lingkungan sosialnya",
    "Seseorang cemas dengan kondisi keuangan",
    "Pekerja merasa terjebak dalam pekerjaan yang tidak disukai",
    "Mahasiswa perfeksionis yang burnout",
    # Add more scenarios as needed
]

SYSTEM_PROMPT = """Kamu adalah generator data untuk melatih AI konselor kesehatan mental bernama LENTERA.

Buatkan percakapan realistis antara:
- User: Orang Indonesia yang sedang curhat (bahasa sehari-hari, bisa campur English Jaksel)
- LENTERA: AI konselor yang empatik dan supportif

RULES:
1. Percakapan 4-6 giliran (total 8-12 messages)
2. User berbicara natural, emosional, bisa typo atau singkat "aku lg sedih bgt"
3. LENTERA:
   - Validasi perasaan ("Aku paham banget kok...")
   - JANGAN diagnosa ("Sepertinya kamu depresi" ❌)
   - Kasih coping strategy praktis
   - Bahasa hangat tapi professional
4. Topik safe: anxiety, stress, kesepian, insecure
5. AVOID: bunuh diri, self-harm, substance abuse

OUTPUT FORMAT (valid JSON):
{
  "conversation": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
"""


def generate_dialogue(scenario: str, retry: int = 3) -> Optional[Dict]:
    """Generate one counseling dialogue"""
    
    for attempt in range(retry):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Skenario: {scenario}"}
                ],
                temperature=0.9,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON
            dialogue = json.loads(content)
            
            # Validate structure
            if "conversation" in dialogue and len(dialogue["conversation"]) >= 4:
                return dialogue
            else:
                print(f"  ⚠️  Invalid structure, retrying... ({attempt+1}/{retry})")
                
        except json.JSONDecodeError as e:
            print(f"  ⚠️  JSON parse error: {e}, retrying... ({attempt+1}/{retry})")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            break
    
    return None


def main():
    print("=" * 60)
    print(" 🤖 LENTERA Dataset Generator")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"Scenarios: {len(SCENARIOS)}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    
    # Check API key
    if openai.api_key == "YOUR_KEY_HERE":
        print("❌ Please set OPENAI_API_KEY environment variable!")
        print("   export OPENAI_API_KEY='sk-proj-...'")
        return
    
    dataset = []
    failed = []
    
    for i, scenario in enumerate(SCENARIOS):
        print(f"[{i+1}/{len(SCENARIOS)}] {scenario[:50]}...")
        
        dialogue = generate_dialogue(scenario)
        
        if dialogue:
            dataset.append(dialogue)
            print(f"  ✅ Success ({len(dialogue['conversation'])} messages)")
        else:
            failed.append(scenario)
            print(f"  ❌ Failed")
        
        # Rate limiting (avoid API throttle)
        time.sleep(2)
        
        # Backup every 25 dialogues
        if (i + 1) % 25 == 0:
            backup_file = f"dataset_backup_{i+1}.json"
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
            print(f"  💾 Backup saved: {backup_file}")
    
    # Save final dataset
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print(f"✅ Generation Complete!")
    print(f"   Success: {len(dataset)}/{len(SCENARIOS)}")
    print(f"   Failed: {len(failed)}")
    print(f"   Output: {OUTPUT_FILE}")
    print("=" * 60)
    
    if failed:
        print("\nFailed scenarios (try re-running manually):")
        for s in failed:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
