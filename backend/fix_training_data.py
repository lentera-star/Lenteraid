"""
Fix training data format for OpenAI fine-tuning
Remove 'metadata' field from all examples
"""

import json

print("[*] Fixing training data format...")

input_file = "lentera_training_data.jsonl"
output_file = "lentera_training_data_fixed.jsonl"

fixed_count = 0

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    
    for line in infile:
        data = json.loads(line)
        
        # Keep only 'messages' field
        fixed_data = {
            "messages": data["messages"]
        }
        
        outfile.write(json.dumps(fixed_data, ensure_ascii=False) + '\n')
        fixed_count += 1

print(f"[OK] Fixed {fixed_count} examples")
print(f"[*] Saved to: {output_file}")
print("\nNext: Run finetune_openai.py again with the fixed file!")

