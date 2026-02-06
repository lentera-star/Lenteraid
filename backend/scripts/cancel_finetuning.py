"""
Cancel OpenAI Fine-Tuning Job
"""
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Job ID to cancel
JOB_ID = "ftjob-APvqX4fXzoOCZ7CtSYoo8JmB"

print("============================================================")
print("[*] Canceling Fine-Tuning Job")
print("============================================================\n")

try:
    # Cancel the job
    print(f"[*] Canceling job: {JOB_ID}")
    response = client.fine_tuning.jobs.cancel(JOB_ID)
    
    print(f"[OK] Job canceled successfully!")
    print(f"   Status: {response.status}")
    print(f"   Job ID: {response.id}")
    
except Exception as e:
    print(f"[ERROR] Failed to cancel job: {e}")
    print(f"[INFO] Job might already be completed or canceled")

print("\n[*] Ready to submit new job with safety training data!")
