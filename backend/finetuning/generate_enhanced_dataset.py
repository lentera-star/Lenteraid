"""
LENTERA Enhanced Dataset Generator
Generates ethics-compliant training data based on golden safety responses
"""

from openai import OpenAI
import json
import time
import os
from typing import Dict, List, Optional
from pathlib import Path

# ===== CONFIGURATION =====
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_KEY_HERE"))
MODEL = "gpt-4o-mini"  # Cost-effective
OUTPUT_DIR = Path(__file__).parent
GOLDEN_RESPONSES_FILE = OUTPUT_DIR.parent / "golden_safety_responses.jsonl"

# ===== ETHICS FRAMEWORK =====
ETHICS_PRINCIPLES = """
CORE ETHICAL PRINCIPLES (from AI_ETHICS_GUIDE.md & ethics_config.yaml):

1. NON-MALEFICENCE (Do No Harm):
   ❌ NEVER: diagnose, prescribe medication, encourage self-harm, replace professionals
   ✅ ALWAYS: prioritize safety, provide crisis resources

2. BENEFICENCE (Promote Well-being):
   ✅ Emotional validation, CBT-informed questions, mindfulness techniques
   ✅ Evidence-based coping strategies, hope-oriented language

3. AUTONOMY (Respect Choice):
   ✅ Present options (not commands), respect boundaries
   ❌ Never coerce or manipulate

4. JUSTICE (Fair & Inclusive):
   ✅ Culturally sensitive (Indonesian context), inclusive language
   ❌ No discrimination, no stigmatizing terms

5. TRANSPARENCY (Honest Limits):
   ✅ Clear AI disclosure, honest about limitations
   ❌ No impersonation of professionals
"""

CRISIS_CATEGORIES = {
    # ===== CRITICAL CRISIS (is_crisis=True, confidence=high) =====
    "explicit_suicidal_statement": {
        "description": "Direct 'I want to die' statement (CRITICAL)",
        "risk_level": "critical",
        "is_crisis": True,
        "crisis_confidence": "high",
        "count_target": 30
    },
    "method_request": {
        "description": "Asking for suicide methods (CRITICAL)",
        "risk_level": "critical",
        "is_crisis": True,
        "crisis_confidence": "high",
        "count_target": 30
    },
    "active_suicidal_thought": {
        "description": "Specific method thoughts ('jumping', 'hanging') (CRISIS)",
        "risk_level": "high",
        "is_crisis": True,
        "crisis_confidence": "high",
        "count_target": 40
    },
    "passive_suicidal_ideation": {
        "description": "Want to 'stop existing' (not die explicitly) (CRISIS)",
        "risk_level": "high",
        "is_crisis": True,
        "crisis_confidence": "high",
        "count_target": 50
    },
    "implicit_suicide_reference": {
        "description": "Indirect death wishes ('sleep forever', 'peaceful death') (CRISIS)",
        "risk_level": "high",
        "is_crisis": True,
        "crisis_confidence": "high",
        "count_target": 50
    },
    
    # ===== AMBIGUOUS (Needs Clarification) =====
    "emotional_exhaustion": {
        "description": "Tired, no point in waking up (AMBIGUOUS - needs clarification)",
        "risk_level": "ambiguous",
        "is_crisis": False,  # Boolean now
        "crisis_confidence": "ambiguous",
        "count_target": 60
    },
    "hopelessness": {
        "description": "Nobody would notice if gone (AMBIGUOUS)",
        "risk_level": "ambiguous",
        "is_crisis": False,
        "crisis_confidence": "ambiguous",
        "count_target": 60
    },
    "medication_request": {
        "description": "Asking about pills/medication (AMBIGUOUS)",
        "risk_level": "ambiguous",
        "is_crisis": False,
        "crisis_confidence": "ambiguous",
        "count_target": 40
    },
    "isolation_attempt": {
        "description": "Don't want human help, only AI (AMBIGUOUS)",
        "risk_level": "ambiguous",
        "is_crisis": False,
        "crisis_confidence": "ambiguous",
        "count_target": 40
    },
    "secrecy_request": {
        "description": "Don't tell anyone (AMBIGUOUS)",
        "risk_level": "ambiguous",
        "is_crisis": False,
        "crisis_confidence": "ambiguous",
        "count_target": 40
    },
    
    # ===== EMOTIONAL / COGNITIVE (SAFE) =====
    "emotional_validation": {
        "description": "User feeling failure/worthlessness (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 80
    },
    "cognitive_distortion": {
        "description": "All-or-nothing thinking, catastrophizing (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 70
    },
    "social_comparison": {
        "description": "Comparing self to others, feeling behind (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 60
    },
    "performance_anxiety": {
        "description": "Fear of failure, exam/presentation anxiety (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 60
    },
    
    # ===== SITUATIONAL STRESS (SAFE) =====
    "general_stress": {
        "description": "Work/school stress, deadlines (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 100
    },
    "burnout_academic": {
        "description": "Student burnout, overwhelming coursework (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 60
    },
    "relationship_issues": {
        "description": "Family/friend conflicts, breakup (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 80
    },
    "loneliness": {
        "description": "Feeling alone, isolated (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 70
    },
    
    # ===== SPECIFIC SYMPTOMS (SAFE) =====
    "anxiety": {
        "description": "General anxiety, worry symptoms (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 80
    },
    "sleep_disturbance": {
        "description": "Insomnia, sleeping too much (SAFE)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 50
    },
    "existential_fatigue": {
        "description": "Questioning life meaning, purpose (SAFE but deep)",
        "risk_level": "low",
        "is_crisis": False,
        "crisis_confidence": "low",
        "count_target": 40
    }
}

SYSTEM_PROMPT = f"""Kamu adalah expert data generator untuk melatih AI konselor mental health LENTERA.

{ETHICS_PRINCIPLES}

TUGASMU: Generate realistic Indonesian mental health conversations.

OUTPUT FORMAT (strict JSON):
{{
  "user_message": "...",
  "assistant_response": "...",
  "category": "...",
  "risk_level": "low|ambiguous|high|critical",
  "is_crisis": true|false  // ALWAYS boolean now
  "crisis_confidence": "low|ambiguous|high"  // NEW field for nuance
}}

CRITICAL RULES:
1. USER MESSAGE:
   - Natural Indonesian (bisa campur English Jaksel)
   - Emotional, authentic, typo OK
   - Vary length (short "aku sedih" to long paragraphs)

2. ASSISTANT RESPONSE - VARIASI PENTING (Anti-Overfitting):
   
   ✅ GOOD (Varied opening):
   - "Aku dengar betapa beratnya perasaan itu..."
   - "Kedengarannya kamu lagi overwhelmed banget ya..."
   - "Terima kasih sudah jujur ngomong ini..."
   - "Wah, pasti nggak mudah ngerasain ini..."
   
   ✅ GOOD (Varied follow-up):
   - "Kalau kamu nyaman, bagian mana yang paling berat?"
   - "Aku penasaran, kapan perasaan ini mulai muncul?"
   - "Kita bisa explore bareng: apa yang bikin kamu merasa kayak gini?"
   - "Mau cerita lebih lanjut tentang situasinya?"
   
   ❌ BAD (Repetitive):
   - Semua dimulai dengan "Aku ingin memahami..."
   - Semua diakhiri dengan "Mau cerita lebih lanjut?"
   
   REQUIREMENT: Untuk setiap 10 responses, minimal 7 variasi berbeda.

3. CRISIS HANDLING (is_crisis=true):
   - MUST mention: safety + hotlines (119 ext. 8)
   - Vary crisis response structure:
     * Some: mention hotline early
     * Some: validate first, then hotline
     * Some: brief, others detailed
   - All crisis_confidence: "high"

4. AMBIGUOUS HANDLING (crisis_confidence="ambiguous"):
   - MUST clarify intent with question
   - is_crisis: false (will be re-evaluated after clarification)
   - Examples:
     * "Aku ingin memastikan: rasa capek ini tentang kelelahan emosional, atau ada pikiran untuk menyakiti diri?"
     * "Pertanyaan ini muncul karena apa ya? Aku pengen pastiin kamu aman."

5. SAFE CATEGORIES (crisis_confidence="low"):
   - Validation + brief psychoeducation + 1-2 coping suggestions
   - No crisis keywords
   - is_crisis: false
   - Max 120 words

CATEGORY-SPECIFIC EXAMPLES:

**emotional_validation** (safe):
{{
  "user_message": "Aku ngerasa gagal terus deh, temen-temen pada sukses semua",
  "assistant_response": "Aku dengar perasaan itu. Membandingkan diri dengan orang lain memang bisa bikin lelah ya. Tapi perasaan gagal ini nggak otomatis berarti kamu beneran gagal kok. Kita bisa explore bareng, apa sih yang bikin kamu ngerasa seperti ini?",
  "category": "emotional_validation",
  "risk_level": "low",
  "is_crisis": false,
  "crisis_confidence": "low"
}}

**emotional_exhaustion** (ambiguous):
{{
  "user_message": "Aku capek banget, rasanya nggak ada gunanya bangun besok",
  "assistant_response": "Kedengarannya kamu benar-benar kelelahan ya. Aku ingin memastikan: rasa capek ini tentang kelelahan emosional aja, atau ada pikiran untuk menyakiti diri sendiri?",
  "category": "emotional_exhaustion",
  "risk_level": "ambiguous",
  "is_crisis": false,
  "crisis_confidence": "ambiguous"
}}

**active_suicidal_thought** (crisis):
{{
  "user_message": "Aku kadang kepikiran loncat dari gedung",
  "assistant_response": "Terima kasih sudah mengatakannya. Pikiran seperti ini penting untuk ditanggapi serius. Keselamatanmu penting, dan kamu layak mendapatkan dukungan sekarang. Tolong hubungi 119 ext. 8 atau Into The Light (1500-454) yang 24/7. Di app LENTERA juga ada fitur booking psikolog.",
  "category": "active_suicidal_thought",
  "risk_level": "high",
  "is_crisis": true,
  "crisis_confidence": "high"
}}

OUTPUT: Valid JSON only, no markdown wrapper.
"""


def load_golden_responses() -> List[Dict]:
    """Load existing golden responses as reference"""
    if not GOLDEN_RESPONSES_FILE.exists():
        print(f"⚠️  Golden responses file not found: {GOLDEN_RESPONSES_FILE}")
        return []
    
    golden = []
    with open(GOLDEN_RESPONSES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                golden.append(json.loads(line))
    
    print(f"✅ Loaded {len(golden)} golden responses")
    return golden


def generate_variation(category: str, category_info: Dict, retry: int = 3) -> Optional[Dict]:
    """Generate one conversation for a category"""
    
    user_prompt = f"""Generate SATU conversasi untuk category: {category}

Description: {category_info['description']}
Risk Level: {category_info['risk_level']}
is_crisis: {category_info['is_crisis']}
crisis_confidence: {category_info['crisis_confidence']}

IMPORTANT:
- Make it VERY realistic (Indonesian teen/young adult language)
- Vary scenarios within category (different life situations)
- Ensure response matches safety guidelines for this risk level

Output as valid JSON."""

    for attempt in range(retry):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.9,  # More variety
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            data = json.loads(content)
            
            # Validate structure
            required = ["user_message", "assistant_response", "category", "risk_level", "is_crisis"]
            if all(k in data for k in required):
                # Verify category matches
                if data["category"] != category:
                    data["category"] = category  # Force correct category
                
                # Ensure crisis_confidence exists
                if "crisis_confidence" not in data:
                    data["crisis_confidence"] = category_info.get("crisis_confidence", "low")
                
                return data
            else:
                print(f"  ⚠️  Missing fields, retrying... ({attempt+1}/{retry})")
                
        except json.JSONDecodeError as e:
            print(f"  ⚠️  JSON parse error: {e}, retrying... ({attempt+1}/{retry})")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            break
    
    return None


def generate_golden_variation(golden_sample: Dict, variation_number: int, retry: int = 3) -> Optional[Dict]:
    """Generate a variation based on a golden response (high fidelity)"""
    
    user_prompt = f"""Buatkan VARIASI dari golden response ini:

ORIGINAL GOLDEN:
User: {golden_sample.get('prompt', '')}
Response: {golden_sample.get('response', '')}
Category: {golden_sample.get('category', '')}

TUGASMU:
1. Buat SKENARIO BERBEDA dengan user message yang MIRIP secara emosional/konteks
2. Response HARUS mengikuti POLA yang sama dengan golden response
3. Pertahankan safety elements yang sama (hotlines jika crisis, clarification jika ambiguous, dll)
4. Bahasa natural Indonesia, tapi SPIRIT sama seperti golden

VARIATION #{variation_number}

Output valid JSON dengan format:
{{
  "user_message": "...",
  "assistant_response": "...",
  "category": "{golden_sample.get('category', 'unknown')}",
  "risk_level": "{golden_sample.get('risk_level', 'low')}",
  "is_crisis": {str(golden_sample.get('is_crisis', False)).lower()},
  "crisis_confidence": "{golden_sample.get('risk_level', 'low') if golden_sample.get('risk_level') != 'ambiguous' else 'ambiguous'}"
}}"""

    for attempt in range(retry):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,  # Slightly lower for more consistency with golden
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            data = json.loads(content)
            
            # Validate
            required = ["user_message", "assistant_response", "category", "risk_level", "is_crisis", "crisis_confidence"]
            if all(k in data for k in required):
                return data
            else:
                print(f"  ⚠️  Missing fields in golden variation, retrying... ({attempt+1}/{retry})")
                
        except json.JSONDecodeError as e:
            print(f"  ⚠️  JSON parse error in golden variation: {e}, retrying... ({attempt+1}/{retry})")
        except Exception as e:
            print(f"  ❌ Error in golden variation: {e}")
            break
    
    return None


def validate_ethics_compliance(sample: Dict) -> tuple[bool, str]:
    """Validate sample against ethics rules"""
    
    response = sample.get("assistant_response", "").lower()
    
    # Check for prohibited content
    diagnosis_terms = ["kamu depresi", "kamu bipolar", "kamu mengalami", "diagnosismu"]
    for term in diagnosis_terms:
        if term in response:
            return False, f"Contains diagnosis: {term}"
    
    medication_terms = ["minum obat", "konsumsi antidepresan", "pakai ssri"]
    for term in medication_terms:
        if term in response:
            return False, f"Contains medication advice: {term}"
    
    replacement_terms = ["tidak perlu psikolog", "gak usah ke terapis", "aku aja cukup"]
    for term in replacement_terms:
        if term in response:
            return False, f"Replaces professionals: {term}"
    
    # Verify crisis responses have proper elements
    if sample.get("is_crisis") is True:
        required_crisis = ["keselamatan", "119", "bantuan"]
        if not any(term in response for term in required_crisis):
            return False, "Crisis response missing safety elements"
    
    # Check crisis_confidence exists
    if "crisis_confidence" not in sample:
        return False, "Missing crisis_confidence field"
    
    # Validate is_crisis is boolean
    if not isinstance(sample.get("is_crisis"), bool):
        return False, f"is_crisis must be boolean, got: {type(sample.get('is_crisis'))}"
    
    return True, "OK"


def main():
    print("=" * 70)
    print(" 🧠 LENTERA Enhanced Dataset Generator (Ethics-Compliant)")
    print("=" * 70)
    print()
    
    # Check API key
    if not client.api_key or client.api_key == "YOUR_KEY_HERE":
        print("❌ Please set OPENAI_API_KEY environment variable!")
        return
    
    # Load golden responses as reference
    golden_responses = load_golden_responses()
    
    # Start generation
    dataset = []
    failed = []
    rejected_ethics = []
    
    # ===== PHASE 1: Generate Golden Response Variations =====
    if golden_responses:
        print("=" * 70)
        print(" 🏆 PHASE 1: Generating Golden Response Variations")
        print("=" * 70)
        print(f"Found {len(golden_responses)} golden responses")
        print(f"Generating 25 variations per golden sample...\n")
        
        golden_count = 0
        for i, golden in enumerate(golden_responses, 1):
            category = golden.get('category', 'unknown')
            print(f"\n[{i}/{len(golden_responses)}] Golden: {category}")
            print(f"   Original: \"{golden.get('prompt', '')[:60]}...\"")
            
            variations_target = 25  # Generate 25 variations per golden
            variations_success = 0
            
            for var_num in range(1, variations_target + 1):
                variation = generate_golden_variation(golden, var_num)
                
                if variation:
                    # Validate ethics
                    is_valid, reason = validate_ethics_compliance(variation)
                    
                    if is_valid:
                        dataset.append(variation)
                        variations_success += 1
                        golden_count += 1
                        
                        if variations_success % 5 == 0:
                            print(f"   ✅ {variations_success}/{variations_target} variations")
                    else:
                        rejected_ethics.append((variation, reason))
                        print(f"   ❌ Ethics: {reason}")
                else:
                    failed.append(f"golden_{category}_var{var_num}")
                
                # Rate limiting
                time.sleep(1.5)
            
            print(f"   ✅ Completed: {variations_success}/{variations_target} variations")
        
        print(f"\n🏆 Golden variations complete: {golden_count} high-quality samples generated\n")
    
    # ===== PHASE 2: Generate Category-Based Samples =====
    print("=" * 70)
    print(" 📂 PHASE 2: Generating Category-Based Samples")
    print("=" * 70)
    
    total_target = sum(cat["count_target"] for cat in CRISIS_CATEGORIES.values())
    current_count = len(dataset)  # Start from golden count
    
    print(f"Target: {total_target} additional samples across {len(CRISIS_CATEGORIES)} categories")
    print(f"Current: {current_count} (from golden variations)\n")
    
    for category, info in CRISIS_CATEGORIES.items():
        target = info["count_target"]
        print(f"\n📂 Category: {category} (Target: {target})")
        print(f"   {info['description']}")
        
        success_count = 0
        attempt_count = 0
        max_attempts = target * 3  # Allow some failures
        
        while success_count < target and attempt_count < max_attempts:
            attempt_count += 1
            
            sample = generate_variation(category, info)
            
            if sample:
                # Validate ethics
                is_valid, reason = validate_ethics_compliance(sample)
                
                if is_valid:
                    dataset.append(sample)
                    success_count += 1
                    current_count += 1
                    
                    if success_count % 10 == 0:
                        print(f"   ✅ {success_count}/{target} generated")
                else:
                    rejected_ethics.append((sample, reason))
                    print(f"   ❌ Ethics violation: {reason}")
            else:
                failed.append(category)
            
            # Rate limiting
            time.sleep(1.5)
            
            # Backup every 100 samples
            if current_count % 100 == 0:
                backup_file = OUTPUT_DIR / f"dataset_backup_{current_count}.json"
                with open(backup_file, "w", encoding="utf-8") as f:
                    json.dump(dataset, f, ensure_ascii=False, indent=2)
                print(f"\n   💾 Backup saved: {backup_file.name}")
        
        print(f"   ✅ Completed: {success_count}/{target}")
    
    # Save final dataset
    output_file = OUTPUT_DIR / "dataset_lentera_enhanced.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ Generation Complete!")
    print(f"   Golden Variations: {golden_count}")
    print(f"   Category Samples: {current_count - golden_count}")
    print(f"   Total Success: {len(dataset)}")
    print(f"   Failed: {len(failed)}")
    print(f"   Ethics Rejected: {len(rejected_ethics)}")
    print(f"   Output: {output_file.name}")
    print("=" * 70)
    
    # Stats
    print("\n📊 Category Distribution:")
    from collections import Counter
    category_counts = Counter(s["category"] for s in dataset)
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}")
    
    # Ethics stats
    crisis_count = sum(1 for s in dataset if s.get("is_crisis") is True)
    safe_count = sum(1 for s in dataset if s.get("is_crisis") is False)
    
    # Crisis confidence distribution
    confidence_counts = Counter(s.get("crisis_confidence", "unknown") for s in dataset)
    
    print(f"\n🛡️ Crisis Distribution:")
    print(f"   CRISIS (is_crisis=true): {crisis_count} ({crisis_count/len(dataset)*100:.1f}%)")
    print(f"   SAFE (is_crisis=false): {safe_count} ({safe_count/len(dataset)*100:.1f}%)")
    
    print(f"\n📈 Confidence Distribution:")
    for conf, count in sorted(confidence_counts.items(), key=lambda x: -x[1]):
        print(f"   {conf}: {count} ({count/len(dataset)*100:.1f}%)")
    
    print(f"\n🏆 Golden Response Impact:")
    print(f"   {golden_count}/{len(dataset)} samples ({golden_count/len(dataset)*100:.1f}%) based on proven-safe golden responses")


if __name__ == "__main__":
    main()
