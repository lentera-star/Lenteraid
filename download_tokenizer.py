"""
Download LLaMA 3.1 tokenizer files and prepare HF-compatible model directory
"""
import os
from huggingface_hub import snapshot_download

output_dir = r"C:\LenteraDreamFlow\model_conversion\lentera-safetensors"

print("Downloading LLaMA 3.1 8B tokenizer and config files...")
print("Note: You may need to accept Meta's license at huggingface.co/meta-llama/Meta-Llama-3.1-8B")

try:
    # Download only tokenizer and config files (not the full model weights)
    snapshot_download(
        repo_id="meta-llama/Meta-Llama-3.1-8B",
        local_dir=output_dir,
        allow_patterns=[
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "config.json",
            "generation_config.json"
        ],
        token=None  # Will use cached token or prompt for login
    )
    
    print(f"\n✅ Tokenizer files downloaded to: {output_dir}")
    print("\nFiles in directory:")
    for f in os.listdir(output_dir):
        print(f"  - {f}")
    
    print("\n✅ Model is ready for upload to Hugging Face!")
    
except Exception as e:
    print(f"\n  ❌ Error: {e}")
    print("\nManual steps:")
    print("1. Login: huggingface-cli login")
    print("2. Accept Meta license: https://huggingface.co/meta-llama/Meta-Llama-3.1-8B")
    print("3. Run this script again")
