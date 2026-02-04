"""
OpenAI Fine-Tuning Script for LENTERA
Uploads training data and submits fine-tuning job
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_training_file():
    """Upload training data to OpenAI"""
    print("[*] Uploading training data to OpenAI...")
    
    try:
        with open("lentera_training_data_fixed.jsonl", "rb") as f:
            response = client.files.create(
                file=f,
                purpose="fine-tune"
            )
        
        file_id = response.id
        print(f"[OK] File uploaded successfully!")
        print(f"   File ID: {file_id}")
        return file_id
    
    except Exception as e:
        print(f"[!] Error uploading file: {e}")
        sys.exit(1)


def submit_finetuning_job(file_id):
    """Submit fine-tuning job to OpenAI"""
    print("\n[*] Submitting fine-tuning job...")
    
    try:
        job = client.fine_tuning.jobs.create(
            training_file=file_id,
            model="gpt-3.5-turbo-0125",  # Latest stable version
            hyperparameters={
                "n_epochs": 3,  # 3 epochs for 974 examples
                "batch_size": "auto",
                "learning_rate_multiplier": "auto"
            },
            suffix="lentera-id"  # Model name suffix
        )
        
        print(f"[OK] Fine-tuning job created!")
        print(f"   Job ID: {job.id}")
        print(f"   Status: {job.status}")
        print(f"   Model: {job.model}")
        
        # Save job ID for monitoring
        with open("finetuning_job_id.txt", "w") as f:
            f.write(job.id)
        
        print(f"\n[*] Job ID saved to: finetuning_job_id.txt")
        return job.id
    
    except Exception as e:
        print(f"[!] Error submitting job: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("[*] LENTERA OpenAI Fine-Tuning")
    print("=" * 60)
    
    # Check if training file exists
    if not os.path.exists("lentera_training_data_fixed.jsonl"):
        print("[!] Error: lentera_training_data_fixed.jsonl not found!")
        print("   Run fix_training_data.py first.")
        sys.exit(1)
    
    # Count examples
    with open("lentera_training_data_fixed.jsonl", "r", encoding="utf-8") as f:
        num_examples = sum(1 for _ in f)
    
    print(f"\n[*] Training data: {num_examples} examples")
    print(f"[*] Estimated cost: ~$10-15")
    print(f"[*] Estimated time: 2-4 hours")
    
    # Confirm
    confirm = input("\n[?] Ready to start fine-tuning? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[!] Cancelled.")
        sys.exit(0)
    
    # Upload file
    file_id = upload_training_file()
    
    # Submit job
    job_id = submit_finetuning_job(file_id)
    
    print("\n" + "=" * 60)
    print("[OK] SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n[*] Next steps:")
    print(f"1. Job is now training (automated)")
    print(f"2. Monitor progress: python monitor_training.py")
    print(f"3. Check status in ~1 hour")
    print(f"4. Training will complete in 2-4 hours")
    print(f"\n[*] You can close this window - training runs on OpenAI servers!")


if __name__ == "__main__":
    main()
