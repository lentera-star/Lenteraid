"""
LENTERA Training Data Generator
Generates high-quality, ethics-compliant training examples for fine-tuning
"""

import json
import os
from typing import List, Dict
from openai import OpenAI
from datetime import datetime

# Initialize OpenAI client (or use local model)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ethics guidelines from AI_ETHICS_GUIDE.md
ETHICS_RULES = """
CRITICAL ETHICS RULES for LENTERA:

1. NEVER diagnose mental health conditions
   ❌ "Kamu depresi klinis"
   ✅ "Beberapa hal yang kamu ceritakan bisa dibahas dengan profesional"

2. NEVER prescribe or recommend medication
   ❌ "Kamu harus minum antidepresan"
   ✅ "Pengobatan hanya bisa ditentukan oleh tenaga medis"

3. ALWAYS validate emotions with empathy
   ✅ "Saya mendengar kamu sedang mengalami..."
   ✅ "Perasaan itu sangat wajar dalam situasi seperti ini"

4. For crisis situations (suicide, self-harm):
   ✅ MUST include Indonesian hotlines: 119 ext. 8, Into The Light 1500-454
   ✅ MUST encourage professional help immediately
   ✅ MUST prioritize safety

5. Use warm, natural Indonesian (not translated-sounding)

6. Include disclaimer when appropriate:
   "Aku LENTERA, AI pendukung kesehatan mental—bukan pengganti psikolog profesional"
"""

# Scenario categories with priorities
SCENARIOS = {
    "crisis": [
        "User mengungkapkan keinginan bunuh diri",
        "User cerita tentang self-harm",
        "User merasa tidak ingin hidup lagi",
        "User merasa ingin overdose",
        "User merasa putus asa total",
    ],
    "depression": [
        "User merasa sedih terus menerus",
        "User kehilangan minat pada aktivitas",
        "User kesulitan bangun tidur",
        "User merasa tidak berharga",
        "User merasa lelah tanpa alasan",
    ],
    "anxiety": [
        "User merasa cemas berlebihan",
        "User sering panik tanpa sebab",
        "User takut berlebihan tentang masa depan",
        "User kesulitan tidur karena pikiran negatif",
        "User merasa jantung berdebar-debar",
    ],
    "relationships": [
        "User konflik dengan pacar",
        "User merasa kesepian",
        "User sulit berteman",
        "User merasa diabaikan teman",
        "User kesulitan komunikasi dengan pasangan",
    ],
    "family": [
        "User konflik dengan orang tua",
        "User merasa tidak dipahami keluarga",
        "User tekanan dari keluarga",
        "User masalah perceraian orang tua",
        "User ekspektasi tinggi dari orang tua",
    ],
    "work_stress": [
        "User tertekan di tempat kerja",
        "User burnout",
        "User konflik dengan atasan",
        "User merasa tidak kompeten",
        "User beban kerja terlalu berat",
    ],
    "academic": [
        "User stress ujian",
        "User nilai jelek",
        "User tekanan akademik",
        "User kesulitan konsentrasi belajar",
        "User takut gagal",
    ],
    "self_esteem": [
        "User insecure tentang penampilan",
        "User merasa tidak cukup baik",
        "User membandingkan diri dengan orang lain",
        "User minder",
        "User merasa gagal",
    ],
}

def generate_conversation(scenario: str, category: str) -> Dict:
    """Generate a single conversation example using GPT-4"""
    
    prompt = f"""
Generate a realistic conversation between an Indonesian user and LENTERA AI mental health assistant.

Scenario: {scenario}
Category: {category}

{ETHICS_RULES}

Requirements:
1. User message should be natural Indonesian (casual, like chatting with friend)
2. LENTERA response MUST follow ALL ethics rules above
3. If crisis scenario, MUST include hotlines and professional referral
4. Use warm, empathetic tone
5. Validate user's emotions
6. Provide practical coping suggestions when appropriate
7. Length: User (1-3 sentences), Assistant (3-5 sentences)

Output ONLY a JSON object with this exact format:
{{
  "user": "user message in Indonesian",
  "assistant": "LENTERA response in Indonesian"
}}

No additional text, just the JSON.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a training data generator for mental health AI. You MUST follow ethics rules precisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,  # Some creativity, but not too much
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        data = json.loads(content)
        
        # Validate required fields
        if "user" not in data or "assistant" not in data:
            raise ValueError("Missing required fields")
        
        # Additional validation for crisis scenarios
        if category == "crisis":
            assistant_msg = data["assistant"].lower()
            if not ("119" in assistant_msg or "1500" in assistant_msg):
                print(f"⚠️ Warning: Crisis scenario missing hotline in response")
                # Optionally reject or flag for review
        
        return {
            "scenario": scenario,
            "category": category,
            "user": data["user"],
            "assistant": data["assistant"],
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"❌ Error generating for '{scenario}': {e}")
        return None


def validate_response(response: str, category: str) -> bool:
    """Validate response against ethics rules"""
    
    response_lower = response.lower()
    
    # Prohibited phrases
    prohibited = [
        "kamu depresi",
        "kamu bipolar",
        "kamu anxiety disorder",
        "kamu butuh obat",
        "minum antidepresan",
        "konsumsi prozac",
        "just be happy",
        "jangan lebay"
    ]
    
    for phrase in prohibited:
        if phrase in response_lower:
            print(f"⚠️ Ethics violation: Found prohibited phrase '{phrase}'")
            return False
    
    # Required for crisis
    if category == "crisis":
        if not any(hotline in response_lower for hotline in ["119", "1500", "into the light"]):
            print(f"⚠️ Ethics violation: Crisis response missing hotline")
            return False
    
    return True


def generate_dataset(
    num_examples: int = 100,
    output_file: str = "lentera_training_data.jsonl",
    prioritize_crisis: bool = True
):
    """Generate complete training dataset"""
    
    print(f"🚀 Starting data generation: {num_examples} examples")
    print(f"📁 Output: {output_file}")
    print("=" * 60)
    
    generated = []
    failed = 0
    
    # Calculate distribution
    if prioritize_crisis:
        # 30% crisis, 70% other
        crisis_count = int(num_examples * 0.3)
        other_count = num_examples - crisis_count
    else:
        # Evenly distributed
        crisis_count = num_examples // len(SCENARIOS)
        other_count = num_examples - crisis_count
    
    # Generate crisis scenarios first (most important!)
    print(f"\n📍 Generating {crisis_count} CRISIS scenarios (HIGH PRIORITY)...")
    for i, scenario in enumerate(SCENARIOS["crisis"] * (crisis_count // len(SCENARIOS["crisis"]) + 1)):
        if len([g for g in generated if g and g["category"] == "crisis"]) >= crisis_count:
            break
        
        print(f"  [{i+1}/{crisis_count}] {scenario[:50]}...")
        
        conv = generate_conversation(scenario, "crisis")
        
        if conv and validate_response(conv["assistant"], "crisis"):
            generated.append(conv)
            print("  ✅ Valid")
        else:
            failed += 1
            print("  ❌ Invalid or error")
    
    # Generate other scenarios
    other_categories = [cat for cat in SCENARIOS if cat != "crisis"]
    examples_per_category = other_count // len(other_categories)
    
    for category in other_categories:
        print(f"\n📍 Generating {examples_per_category} examples for '{category}'...")
        
        count = 0
        scenario_idx = 0
        
        while count < examples_per_category:
            scenario = SCENARIOS[category][scenario_idx % len(SCENARIOS[category])]
            print(f"  [{count+1}/{examples_per_category}] {scenario[:50]}...")
            
            conv = generate_conversation(scenario, category)
            
            if conv and validate_response(conv["assistant"], category):
                generated.append(conv)
                count += 1
                print("  ✅ Valid")
            else:
                failed += 1
                print("  ❌ Invalid or error")
            
            scenario_idx += 1
    
    # Save to JSONL
    print(f"\n💾 Saving {len(generated)} examples to {output_file}...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        for item in generated:
            # Format for training (chat template)
            training_format = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Kamu adalah LENTERA, AI pendukung kesehatan mental Indonesia yang empati dan aman."
                    },
                    {
                        "role": "user",
                        "content": item["user"]
                    },
                    {
                        "role": "assistant",
                        "content": item["assistant"]
                    }
                ],
                "metadata": {
                    "category": item["category"],
                    "scenario": item["scenario"],
                    "generated_at": item["generated_at"]
                }
            }
            
            f.write(json.dumps(training_format, ensure_ascii=False) + "\n")
    
    print("\n" + "=" * 60)
    print(f"✅ Generation complete!")
    print(f"   Total generated: {len(generated)}")
    print(f"   Failed: {failed}")
    print(f"   Success rate: {len(generated)/(len(generated)+failed)*100:.1f}%")
    print(f"   Output file: {output_file}")
    
    # Stats by category
    print(f"\n📊 Distribution:")
    for category in SCENARIOS.keys():
        count = len([g for g in generated if g["category"] == category])
        print(f"   {category}: {count}")
    
    return generated


def create_train_val_split(
    input_file: str = "lentera_training_data.jsonl",
    train_file: str = "train.jsonl",
    val_file: str = "val.jsonl",
    val_ratio: float = 0.1
):
    """Split dataset into train and validation"""
    
    print(f"📂 Splitting {input_file} into train/val...")
    
    # Load data
    with open(input_file, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    
    # Shuffle
    import random
    random.seed(42)
    random.shuffle(data)
    
    # Split
    val_size = int(len(data) * val_ratio)
    train_data = data[val_size:]
    val_data = data[:val_size]
    
    # Save
    with open(train_file, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    with open(val_file, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"✅ Split complete:")
    print(f"   Train: {len(train_data)} ({train_file})")
    print(f"   Val: {len(val_data)} ({val_file})")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate LENTERA training data")
    parser.add_argument("--num", type=int, default=100, help="Number of examples to generate")
    parser.add_argument("--output", type=str, default="lentera_training_data.jsonl", help="Output file")
    parser.add_argument("--split", action="store_true", help="Split into train/val after generation")
    
    args = parser.parse_args()
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Warning: OPENAI_API_KEY not set!")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        exit(1)
    
    # Generate
    generated = generate_dataset(
        num_examples=args.num,
        output_file=args.output
    )
    
    # Split if requested
    if args.split:
        create_train_val_split(input_file=args.output)
    
    print("\n🎉 All done! Ready for fine-tuning!")
    print(f"\nNext steps:")
    print(f"1. Review generated examples manually")
    print(f"2. Get mental health expert to validate")
    print(f"3. Use {args.output} for training with Axolotl")
