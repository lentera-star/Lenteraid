import asyncio
import os
from ai_service import AIService
import logging

async def test_debug():
    logging.basicConfig(level=logging.INFO)
    print("Testing AIService with Ollama mode...")
    print(f"ENV AI_MODE: {os.getenv('AI_MODE')}")
    print(f"ENV OLLAMA_MODEL: {os.getenv('OLLAMA_MODEL')}")
    
    service = AIService()
    messages = [{"role": "user", "content": "halo"}]
    
    print("Calling chat...")
    try:
        response = await service.chat(messages)
        print(f"Response type: {type(response)}")
        print(f"Response content: {response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_debug())
