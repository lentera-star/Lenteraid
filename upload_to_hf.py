"""
Upload converted safetensors model to Hugging Face
"""
from huggingface_hub import HfApi, create_repo
import os

# Configuration
repo_id = "lenteraid/lentera-llama-3.1-8b-safetensors"
model_dir = r"C:\LenteraDreamFlow\model_conversion\lentera-safetensors"

print("=" * 60)
print("Uploading model to Hugging Face")
print("=" * 60)
print(f"Repository: {repo_id}")
print(f"Source directory: {model_dir}")
print()

try:
    api = HfApi()
    
    # Create repository (or get existing)
    print("Creating/checking repository...")
    try:
        create_repo(repo_id, exist_ok=True, repo_type="model")
        print(f"✅ Repository ready: https://huggingface.co/{repo_id}")
    except Exception as e:
        print(f"Repository exists or created: {e}")
    
    # Upload all files
    print("\nUploading files...")
    api.upload_folder(
        folder_path=model_dir,
        repo_id=repo_id,
        repo_type="model",
        ignore_patterns=[".cache/*", "gguf_metadata.json"]  # Don't upload cache and GGUF metadata
    )
    
    print("\n" + "=" * 60)
    print("✅ Upload complete!")
    print("=" * 60)
    print(f"\nModel URL: https://huggingface.co/{repo_id}")
    print("\nNext steps:")
    print("1. Test model loading with vLLM")
    print("2. Update RunPod endpoint configuration")
    print("3. Test RunPod inference")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Login first: huggingface-cli login")
    print("2. Check token has write permissions")
    print("3. Try again")
