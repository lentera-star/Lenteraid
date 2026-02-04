"""
Modal Serverless Inference for Lentera Fine-tuned Llama 3.1 8B
With Volume caching for fast response times
"""

import modal
import os

# Create Modal app
app = modal.App("lentera-llama")

# Create Volume for model persistence
model_volume = modal.Volume.from_name("lentera-model-vol", create_if_missing=True)
MODEL_DIR = "/vol/models"

# Model config
REPO_ID = "lenteraid/lentera-llama-3.1-8b"
MODEL_FILENAME = "lentera-model.gguf"

# Image with llama-cpp-python + CUDA support (using pre-built wheels)
llama_image = (
    modal.Image.from_registry("nvidia/cuda:12.1.1-devel-ubuntu22.04", add_python="3.11")
    .apt_install("git", "build-essential", "cmake")
    .run_commands(
        "pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121"
    )
    .pip_install(
        "huggingface-hub",
        "fastapi[standard]",
        "hf-transfer",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)


def get_model_path():
    """Get model path, download if not cached"""
    from huggingface_hub import hf_hub_download
    
    model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
    
    # Check if already cached
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"✅ Model cached: {model_path} ({size_mb:.0f} MB)")
        return model_path
    
    # Download to volume
    print(f"📥 Downloading model (first time only)...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    downloaded = hf_hub_download(
        repo_id=REPO_ID,
        filename=MODEL_FILENAME,
        token=os.environ.get("HF_TOKEN"),
        local_dir=MODEL_DIR,
    )
    print(f"✅ Downloaded to: {downloaded}")
    return model_path


# Singleton LLM instance
_llm = None

def get_llm():
    """Get or create LLM instance (singleton)"""
    global _llm
    from llama_cpp import Llama
    
    if _llm is None:
        model_path = get_model_path()
        print(f"📂 Loading model...")
        _llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Offload ALL layers to GPU
            n_ctx=2048,
            n_threads=4,  # Fewer threads needed when using GPU
            verbose=False
        )
        print("✅ Model loaded!")
    return _llm


@app.function(
    image=llama_image,
    gpu="A10G",
    timeout=300,  # Increased timeout for longer CPU inference
    container_idle_timeout=600,  # Keep warm 10 min
    secrets=[modal.Secret.from_name("huggingface")],
    volumes={MODEL_DIR: model_volume},
)
@modal.web_endpoint(method="POST")
def generate(request_data: dict):
    """Inference endpoint with caching"""
    import time
    start = time.time()
    
    try:
        llm = get_llm()
        
        # Build prompt
        messages = request_data.get("messages", [])
        max_tokens = request_data.get("max_tokens", 256)
        temperature = request_data.get("temperature", 0.7)
        
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"User: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        prompt += "Assistant: "
        
        if not prompt.strip() or prompt == "Assistant: ":
            prompt = request_data.get("prompt", "Hello!")
        
        # Generate
        response = llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["User:", "\n\n"],
            echo=False
        )
        
        # Commit volume to persist model
        model_volume.commit()
        
        response_text = response["choices"][0]["text"].strip()
        elapsed = time.time() - start
        print(f"✅ Response in {elapsed:.1f}s")
        
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "model": "lentera-llama-3.1-8b",
            "latency_seconds": elapsed
        }
        
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


@app.function(image=llama_image)
@modal.web_endpoint(method="GET")
def health():
    return {"status": "ok"}
