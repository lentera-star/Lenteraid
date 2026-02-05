#!/bin/bash
# LENTERA VPS Backend Auto-Repair Script

echo "🔍 Checking for zombie processes on port 8000..."
sudo fuser -k 8000/tcp || echo "No processes found on 8000"

echo "🧹 Cleaning up old main.py processes..."
pkill -f "main.py" || echo "No main.py processes running"

echo "🚀 Restarting lentera-backend service..."
sudo systemctl restart lentera-backend

echo "⏳ Waiting for startup..."
sleep 5

echo "📊 Service Status:"
sudo systemctl status lentera-backend --no-pager

echo "🧪 Testing local connectivity..."
curl -s http://localhost:8000/health || echo "❌ Local backend still not responding"

echo "🦙 Checking Ollama..."
ollama list | grep "lentera-fast" || echo "❌ lentera-fast model not found in Ollama"

echo "✅ Done! If the service is 'active (running)', try Fast Mode again in the app."
