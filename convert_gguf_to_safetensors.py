"""
Convert GGUF model to safetensors format
Preserves fine-tuning while making it compatible with vLLM
"""
import os
from pathlib import Path
from gguf import GGUFReader
import torch
from safetensors.torch import save_file
import json

def convert_gguf_to_safetensors(
    gguf_path: str,
    output_dir: str
):
    """
    Convert GGUF model to safetensors format
    
    Args:
        gguf_path: Path to input GGUF file
        output_dir: Directory to save safetensors output
    """
    print(f"Loading GGUF model from: {gguf_path}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read GGUF file
    reader = GGUFReader(gguf_path)
    
    # Extract tensors
    print("Extracting tensors...")
    tensors = {}
    total_params = 0
    
    for tensor in reader.tensors:
        tensor_name = tensor.name
        tensor_data = torch.from_numpy(tensor.data)
        tensors[tensor_name] = tensor_data
        
        params = tensor_data.numel()
        total_params += params
        print(f"  {tensor_name}: {tensor_data.shape} ({params:,} params)")
    
    print(f"\nTotal parameters: {total_params:,}")
    print(f"Total tensors: {len(tensors)}")
    
    # Save as safetensors
    output_file = os.path.join(output_dir, "model.safetensors")
    print(f"\nSaving to: {output_file}")
    save_file(tensors, output_file)
    
    # Get file size
    file_size = os.path.getsize(output_file)
    print(f"Output file size: {file_size / (1024**3):.2f} GB")
    
    # Extract and save metadata
    print("\nExtracting metadata...")
    metadata = {}
    
    for field in reader.fields.values():
        if hasattr(field, 'parts'):
            # Handle multi-part fields
            metadata[field.name] = [part.tolist() if hasattr(part, 'tolist') else str(part) for part in field.parts]
        elif hasattr(field, 'value'):
            metadata[field.name] = field.value
    
    # Save metadata
    metadata_file = os.path.join(output_dir, "gguf_metadata.json")
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    
    print(f"Metadata saved to: {metadata_file}")
    print("\n✅ Conversion complete!")
    
    return output_file


if __name__ == "__main__":
    # Configuration
    gguf_path = r"C:\LenteraDreamFlow\lentera-model.gguf"
    output_dir = r"C:\LenteraDreamFlow\model_conversion\lentera-safetensors"
    
    # Run conversion
    print("=" * 60)
    print("GGUF to Safetensors Conversion")
    print("=" * 60)
    
    if not os.path.exists(gguf_path):
        print(f"❌ Error: GGUF file not found: {gguf_path}")
        exit(1)
    
    output_file = convert_gguf_to_safetensors(gguf_path, output_dir)
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Download LLaMA 3.1 tokenizer files")
    print("2. Copy tokenizer files to output directory")
    print("3. Create config.json for Hugging Face")
    print("4. Test model loading with transformers")
    print("5. Upload to Hugging Face")
