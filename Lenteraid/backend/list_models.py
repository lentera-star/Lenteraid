"""
List available fine-tuned models
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Listing your fine-tuned models:")
print("=" * 60)

# List fine-tuning jobs
jobs = client.fine_tuning.jobs.list(limit=10)

for job in jobs.data:
    print(f"\nJob ID: {job.id}")
    print(f"Status: {job.status}")
    print(f"Model: {job.model}")
    if job.fine_tuned_model:
        print(f"Fine-tuned Model: {job.fine_tuned_model}")
    print("-" * 60)
