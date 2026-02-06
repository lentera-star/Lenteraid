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
        elif self.mode == "modal":
            self.modal_endpoint = os.getenv("MODAL_ENDPOINT_URL")
            if not self.modal_endpoint:
                raise ValueError("MODAL_ENDPOINT_URL not set in environment")
            logger.info(f"✓ Modal initialized: {self.modal_endpoint}")
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
        elif self.mode == "modal":
            return await self._chat_modal(messages)
        else:
            return await self.ollama.chat(messages)
    
    async def _chat_modal(self, messages):
        """Send request to Modal serverless endpoint"""
        try:
            # Prepare Modal API payload (matches modal_inference.py structure)
            payload = {
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Make async HTTP request to Modal
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.modal_endpoint,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Modal API error {response.status}: {error_text}")
                        raise Exception(f"Modal API returned status {response.status}")
                    
                    result = await response.json()
                    
                    # Extract response from Modal payload
                    # Modal returns: {"choices": [{"message": {"content": "..."}}]}
                    if "choices" in result and len(result["choices"]) > 0:
                        choice = result["choices"][0]
                        if "message" in choice:
                            return choice["message"].get("content", "")
                        return str(choice)
                    elif "error" in result:
                        raise Exception(f"Modal execution error: {result['error']}")
                    else:
                        logger.warning(f"Unexpected Modal response format: {result}")
                        return str(result)
                        
        except asyncio.TimeoutError:
            logger.error("Modal request timeout")
            raise Exception("Modal inference timeout after 60 seconds")
        except Exception as e:
            logger.error(f"Modal chat error: {e}")
            raise

