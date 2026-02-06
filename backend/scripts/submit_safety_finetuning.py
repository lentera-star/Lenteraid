"""
Submit Safety-Focused Fine-Tuning Job
Uses the 12 ChatGPT-verified golden safety responses
"""
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Training file
TRAINING_FILE = "lentera_safety_training.jsonl"

print("============================================================")
print("[*] LENTERA Safety-Focused Fine-Tuning")
print("============================================================\n")

print(f"[*] Training data: {TRAINING_FILE}")
print(f"[*] Examples: 12 ChatGPT-verified golden responses")
print(f"[*] Estimated cost: ~$1-2")
print(f"[*] Estimated time: ~30 minutes\n")

confirm = input("[?] Ready to start safety fine-tuning? (yes/no): ")

if confirm.lower() != 'yes':
    print("[!] Aborted by user")
    exit(0)

# Upload training file
print(f"\n[*] Uploading safety training data to OpenAI...")
with open(TRAINING_FILE, 'rb') as f:
    training_file = client.files.create(
        file=f,
        purpose='fine-tune'
    )

print(f"[OK] File uploaded successfully!")
print(f"   File ID: {training_file.id}\n")

# Submit fine-tuning job
print("[*] Submitting safety fine-tuning job...")
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-3.5-turbo-0125",
    suffix="lentera-safety-v2"
)

print(f"[OK] Fine-tuning job created!")
print(f"   Job ID: {job.id}")
print(f"   Status: {job.status}")
print(f"   Model: {job.model}\n")

# Save job ID
with open('finetuning_safety_job_id.txt', 'w') as f:
    f.write(job.id)

print("[*] Job ID saved to: finetuning_safety_job_id.txt\n")

print("============================================================")
print("[OK] SAFETY TRAINING SUBMITTED!")
print("============================================================\n")

print("[*] Next steps:")
print("1. Training runs automatically (~30 min)")
print("2. Model will learn to:")
print("   - Never abandon users (no 'aku bukan orang yang tepat')")
print("   - Proper crisis response structure")
print("   - Empathy first, boundary clear, stay present")
print("3. Check status: python monitor_training.py\n")

print("[*] You can close this window - training runs on OpenAI!\n")
