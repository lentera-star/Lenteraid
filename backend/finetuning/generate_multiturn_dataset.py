"""
Enhanced Dataset Generator with Multi-Turn Conversation Support
Generates:
- 1,000 single-turn samples (diversity)
- 1,020 multi-turn samples (2-5 turns, for memory)
Total: 2,020 new samples to add to existing 1,480
"""

from openai import OpenAI
import json
import time
import random
from typing import List, Dict
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

# Multi-turn conversation templates
MULTITURN_SCENARIOS = {
    "progressive_stress": {
        "turns": 3,
        "prompts": [
            "User shares initial stress",
            "User reveals specific stressors",
            "User discusses impact on life"
        ]
    },
    "crisis_escalation": {
        "turns": 4,
        "prompts": [
            "User mentions feeling down",
            "User reveals dark thoughts",
            "User expresses hopelessness",
            "Crisis response with resources"
        ]
    },
    "coping_exploration": {
        "turns": 5,
        "prompts": [
            "User asks for help",
            "User describes problem",
            "AI suggests strategies",
            "User asks follow-up",
            "AI provides specific guidance"
        ]
    }
}

CATEGORIES = [
    "general_stress", "academic_pressure", "relationship_issues",
    "family_conflict", "anxiety", "loneliness", "self_worth",
    "emotional_exhaustion", "social_anxiety", "burnout",
    "grief_loss", "identity_crisis", "financial_stress",
    "career_uncertainty", "health_anxiety", "sleep_issues",
    "anger_management", "trauma", "substance_concern",
    "passive_suicidal_ideation", "explicit_suicidal_statement"
]

def generate_single_turn(category: str) -> Dict:
    """Generate single-turn conversation"""
    
    system_prompt = f"""Generate a realistic Indonesian mental health conversation.
    
Category: {category}
    
Create ONE exchange (user + assistant).
Ethics rules:
- NO diagnosis
- NO medication recommendations
- Crisis responses MUST mention hotline (119 ext. 8)
- Empathetic, non-judgmental tone
- Natural Indonesian (boleh campur English)

Output JSON:
{{
  "user_message": "...",
  "assistant_response": "...",
  "category": "{category}",
  "risk_level": "low/medium/high/critical",
  "is_crisis": true/false,
  "crisis_confidence": "low/ambiguous/high"
}}"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate mental health conversation about {category}"}
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
        print(f"  ⚠️ Error generating single-turn: {e}")
        return None

def generate_multiturn_conversation(scenario_type: str, turns: int) -> Dict:
    """Generate multi-turn conversation with context awareness"""
    
    system_prompt = f"""Generate a realistic multi-turn Indonesian mental health conversation.

Scenario: {scenario_type}
Turns: {turns}

CRITICAL: Each AI response must REFERENCE previous messages naturally!
Examples:
- "Dari yang kamu ceritakan tadi tentang..."
- "Kamu bilang sebelumnya..."
- "Tadi kamu mention..."

Ethics:
- NO diagnosis
- NO medication  
- Crisis responses MUST mention 119 ext. 8
- Build on previous context

Output JSON array of conversations:
{{
  "conversations": [
    {{"from": "human", "value": "..."}},
    {{"from": "gpt", "value": "... (reference context)"}},
    {{"from": "human", "value": "..."}},
    {{"from": "gpt", "value": "... (reference previous turns)"}}
  ],
  "category": "...",
  "is_crisis": true/false,
  "risk_level": "low/medium/high/critical"
}}"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate {turns}-turn conversation about {scenario_type}"}
            ],
            temperature=0.9,
            max_tokens=800
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        data = json.loads(content)
        
        # Validate multi-turn format
        if "conversations" in data and len(data["conversations"]) >= turns * 2:
            return data
        else:
            print(f"  ⚠️ Invalid multi-turn format")
            return None
            
    except Exception as e:
        print(f"  ⚠️ Error generating multi-turn: {e}")
        return None

def validate_ethics(sample: Dict) -> tuple:
    """Validate ethics compliance"""
    
    # For multiturn, check all AI responses
    if "conversations" in sample:
        responses = [msg["value"] for msg in sample["conversations"] if msg["from"] == "gpt"]
        text = " ".join(responses).lower()
    else:
        text = sample.get("assistant_response", "").lower()
    
    # Check forbidden terms
    diagnosis_terms = ["kamu depresi", "kamu bipolar", "kamu mengalami", "diagnosismu"]
    medication_terms = ["minum obat", "konsumsi antidepresan", "pakai ssri"]
    
    for term in diagnosis_terms + medication_terms:
        if term in text:
            return False, f"Contains forbidden term: {term}"
    
    # Check crisis responses
    if sample.get("is_crisis") is True:
        if "119" not in text and "hotline" not in text and "keselamatan" not in text:
            return False, "Crisis response missing safety elements"
    
    return True, "OK"

def main():
    print("="*70)
    print("🚀 ENHANCED DATASET GENERATOR - Multi-Turn Support")
    print("="*70)
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set!")
        return
    
    # Targets
    TARGET_SINGLE = 1000
    TARGET_MULTITURN = 1020
    
    dataset = []
    rejected = 0
    
    # Phase 1: Single-turn generation
    print(f"\n📋 PHASE 1: Generating {TARGET_SINGLE} Single-Turn Samples")
    print("="*70)
    
    for i in range(TARGET_SINGLE):
        category = random.choice(CATEGORIES)
        print(f"[{i+1}/{TARGET_SINGLE}] Category: {category}")
        
        sample = generate_single_turn(category)
        
        if sample:
            is_valid, reason = validate_ethics(sample)
            if is_valid:
                dataset.append(sample)
                print(f"  ✅ Valid sample")
            else:
                rejected += 1
                print(f"  ❌ Rejected: {reason}")
        
        time.sleep(1.5)  # Rate limit
        
        # Backup every 100
        if (i + 1) % 100 == 0:
            with open(f"backup_single_{i+1}.json", "w", encoding="utf-8") as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
            print(f"  💾 Backup saved")
    
    print(f"\n✅ Phase 1 complete: {len(dataset)}/{TARGET_SINGLE} samples")
    
    # Phase 2: Multi-turn generation
    print(f"\n📋 PHASE 2: Generating {TARGET_MULTITURN} Multi-Turn Conversations")
    print("="*70)
    
    multiturn_count = 0
    scenarios = list(MULTITURN_SCENARIOS.keys())
    
    while multiturn_count < TARGET_MULTITURN:
        scenario = random.choice(scenarios)
        turns = MULTITURN_SCENARIOS[scenario]["turns"]
        
        print(f"[{multiturn_count+1}/{TARGET_MULTITURN}] Scenario: {scenario} ({turns} turns)")
        
        sample = generate_multiturn_conversation(scenario, turns)
        
        if sample:
            is_valid, reason = validate_ethics(sample)
            if is_valid:
                dataset.append(sample)
                multiturn_count += 1
                print(f"  ✅ Valid multi-turn conversation")
            else:
                rejected += 1
                print(f"  ❌ Rejected: {reason}")
        
        time.sleep(2)  # Longer pause for multi-turn
        
        # Backup every 100
        if (multiturn_count + 1) % 100 == 0:
            with open(f"backup_multiturn_{multiturn_count}.json", "w", encoding="utf-8") as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
            print(f"  💾 Backup saved")
    
    # Final save
    output_file = "dataset_enhanced_v2.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    # Statistics
    single_turn = [s for s in dataset if "conversations" not in s]
    multi_turn = [s for s in dataset if "conversations" in s]
    
    print("\n" + "="*70)
    print("🎉 GENERATION COMPLETE!")
    print("="*70)
    print(f"\n📊 Final Statistics:")
    print(f"   Single-turn: {len(single_turn)}")
    print(f"   Multi-turn: {len(multi_turn)}")
    print(f"   Total: {len(dataset)}")
    print(f"   Rejected: {rejected}")
    print(f"\n💾 Output: {output_file}")
    print("="*70)

if __name__ == "__main__":
    main()
