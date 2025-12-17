"""
Ollama Service Integration
Handles LLM interactions with Ollama
"""
import os
import httpx
from typing import List, Dict, Optional

class OllamaService:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama2")
        
    async def check_health(self) -> bool:
        """Check if Ollama service is available"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            print(f"Ollama health check failed: {e}")
            return False
    
    async def list_models(self) -> List[Dict]:
        """List available models"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    return response.json().get("models", [])
        except Exception as e:
            print(f"Failed to list models: {e}")
        return []
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[List[int]] = None,
        stream: bool = False
    ) -> Dict:
        """
        Generate response from Ollama
        
        Args:
            prompt: User prompt
            system_prompt: System instructions for the model
            context: Previous conversation context (token IDs)
            stream: Whether to stream the response
        
        Returns:
            Generated response
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        if context:
            payload["context"] = context
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "error": f"Ollama request failed with status {response.status_code}",
                        "response": ""
                    }
        except Exception as e:
            return {
                "error": f"Ollama request failed: {str(e)}",
                "response": ""
            }
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> Dict:
        """
        Chat with Ollama using conversation format
        
        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [{"role": "user", "content": "Hello"}]
            stream: Whether to stream the response
        
        Returns:
            Chat response
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "error": f"Ollama chat failed with status {response.status_code}",
                        "message": {}
                    }
        except Exception as e:
            return {
                "error": f"Ollama chat failed: {str(e)}",
                "message": {}
            }

# Mental health system prompt
MENTAL_HEALTH_SYSTEM_PROMPT = """
Kamu adalah asisten AI untuk konseling kesehatan mental bernama LENTERA.
Tugasmu adalah memberikan dukungan emosional dan saran kesehatan mental yang positif.

Prinsip yang harus kamu ikuti:
1. Selalu empati dan mendukung
2. Jangan mendiagnosis kondisi mental secara spesifik
3. Jika ada tanda-tanda bahaya (bunuh diri, self-harm), sarankan untuk menghubungi profesional
4. Berikan saran praktis untuk self-care dan coping mechanisms
5. Gunakan bahasa Indonesia yang hangat dan ramah
6. Jaga privasi dan confidentiality

Jangan pernah:
- Memberikan diagnosis medis
- Meresepkan obat
- Menggantikan terapi profesional
- Memberikan saran yang berbahaya
"""
