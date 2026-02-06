"""
AI Service - Supports both Ollama and OpenAI
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.mode = os.getenv("AI_MODE", "ollama")
        
        if self.mode == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            logger.info(f"✓ OpenAI initialized: {self.model}")
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
        else:
            return await self.ollama.chat(messages)