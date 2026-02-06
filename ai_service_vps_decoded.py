"""
AI Service - Supports Ollama, OpenAI, and RunPod
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
import logging
import aiohttp
import asyncio
load_dotenv()
logger = logging.getLogger(__name__)
class AIService:
    def __init__(self):
        self.mode = os.getenv("AI_MODE", "ollama")
        
        if self.mode == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            logger.info(f"✓ OpenAI initialized: {self.model}")
        elif self.mode == "runpod":
            self.runpod_endpoint = os.getenv("RUNPOD_ENDPOINT_URL")
            self.runpod_api_key = os.getenv("RUNPOD_API_KEY")
            
            if not self.runpod_endpoint:
                raise ValueError("RUNPOD_ENDPOINT_URL not set in environment")
            if not self.runpod_api_key:
                raise ValueError("RUNPOD_API_KEY not set in environment")
            
            logger.info(f"✓ RunPod initialized: {self.runpod_endpoint}")
        else:
            from ollama_service import OllamaService
            self.ollama = OllamaService()
            logger.info("✓ Ollama initialized")
    
    async def chat(self, messages):
        """Send chat request to AI"""
        if self.mode == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        elif self.mode == "runpod":
            return await self._chat_runpod(messages)
        else:
            return await self.ollama.chat(messages)
    
    async def _chat_runpod(self, messages):
        """Send request to RunPod serverless endpoint"""
        try:
            # Prepare RunPod API payload
            payload = {
                "input": {
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.runpod_api_key}",
                "Content-Type": "application/json"
            }
            
            # Make async HTTP request to RunPod
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.runpod_endpoint,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"RunPod API error {response.status}: {error_text}")
                        raise Exception(f"RunPod API returned status {response.status}")
                    
                    result = await response.json()
                    
                    # Extract response from RunPod payload
                    # RunPod typically returns: {"output": {"response": "..."}}
                    if "output" in result:
                        output = result["output"]
                        if isinstance(output, dict):
                            # Try common response keys
                            return output.get("response") or output.get("text") or output.get("message", {}).get("content", "")
                        else:
                            return str(output)
                    else:
                        logger.warning(f"Unexpected RunPod response format: {result}")
                        return str(result)
                        
        except asyncio.TimeoutError:
            logger.error("RunPod request timeout")
            raise Exception("RunPod inference timeout after 30 seconds")
        except Exception as e:
            logger.error(f"RunPod chat error: {e}")
            raise

