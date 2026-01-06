"""
Monitor OpenAI Fine-Tuning Progress
Checks job status and displays training metrics
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_job_id():
    """Read job ID from file"""
    if not os.path.exists("finetuning_job_id.txt"):
        print("❌ Error: finetuning_job_id.txt not found!")
        print("   Run finetune_openai.py first.")
        sys.exit(1)
    
    with open("finetuning_job_id.txt", "r") as f:
        return f.read().strip()

def monitor_job(job_id, watch=False):
    """Monitor fine-tuning job status"""
    
    print("=" * 60)
    print("📊 LENTERA Fine-Tuning Monitor")
    print("=" * 60)
    print(f"\nJob ID: {job_id}\n")
    
    iteration = 0
    
    while True:
        iteration += 1
        
        try:
            # Get job status
            job = client.fine_tuning.jobs.retrieve(job_id)
            
            status = job.status
            print(f"[{iteration}] Status: {status}")
            
            # Display additional info
            if hasattr(job, 'trained_tokens') and job.trained_tokens:
                print(f"    Trained tokens: {job.trained_tokens:,}")
            
            if hasattr(job, 'finished_at') and job.finished_at:
                print(f"    Finished at: {job.finished_at}")
            
            # Check completion
            if status == "succeeded":
                print("\n" + "=" * 60)
                print("✅ FINE-TUNING COMPLETE!")
                print("=" * 60)
                print(f"\n🎉 Fine-tuned model: {job.fine_tuned_model}")
                
                # Save model ID
                with open("finetuned_model_id.txt", "w") as f:
                    f.write(job.fine_tuned_model)
                
                print(f"💾 Model ID saved to: finetuned_model_id.txt")
                print(f"\n📍 Next step: Update backend/.env with:")
                print(f"   OPENAI_MODEL={job.fine_tuned_model}")
                break
            
            elif status == "failed":
                print("\n❌ FINE-TUNING FAILED!")
                if hasattr(job, 'error') and job.error:
                    print(f"Error: {job.error}")
                break
            
            elif status == "cancelled":
                print("\n⚠️  Fine-tuning was cancelled")
                break
            
            # If watching, wait and check again
            if watch:
                if iteration == 1:
                    print("\n⏱️  Training in progress... (checking every minute)")
                time.sleep(60)  # Check every minute
            else:
                break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor LENTERA fine-tuning")
    parser.add_argument("--watch", action="store_true", help="Watch progress continuously")
    args = parser.parse_args()
    
    job_id = get_job_id()
    monitor_job(job_id, watch=args.watch)

if __name__ == "__main__":
    main()
