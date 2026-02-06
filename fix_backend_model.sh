#!/bin/bash
# Fix backend to use Ollama model instead of OpenAI

echo "=== Fixing Backend Model Configuration ==="

# Check current config
echo "1️⃣ Checking current ai_service.py..."
grep -n "model" ~/backend/app/ai_service.py | head -20

echo ""
echo "2️⃣ Updating to use Ollama model..."

# Create backup
cp ~/backend/app/ai_service.py ~/backend/app/ai_service.py.backup

# Update ai_service.py to use Ollama
cat > ~/backend/app/ai_service.py << 'EOF'
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "lentera-llama3"  # Use local Ollama model
        
    async def generate_response(self, message: str, conversation_id: str) -> dict:
        """Generate AI response using Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": message,
                "stream": False
            }
            
            logger.info(f"Sending to Ollama: {message[:50]}...")
            response = requests.post(self.ollama_url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            ai_message = result.get("response", "")
            
            return {
                "message": ai_message,
                "conversation_id": conversation_id,
                "is_crisis": False  # Add crisis detection logic if needed
            }
            
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            raise
EOF

echo "✅ Updated ai_service.py to use Ollama model"

# Restart backend
echo "🔄 Restarting backend..."
pkill -f uvicorn
sleep 2
cd ~/backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

echo "✅ Backend restarted"
echo "📝 Check logs: tail -f ~/backend/backend.log"
echo "🧪 Test with: curl -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{\"message\": \"test\"}''"
