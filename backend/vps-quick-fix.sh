#!/bin/bash
# Quick Fix Script - Run di VPS setelah deployment

echo "=========================================="
echo "  LENTERA Backend - Quick Fix"
echo "=========================================="
echo ""

# Go to backend directory
cd /opt/lentera-backend

# Step 1: Create .env file
echo "Step 1: Creating .env file..."
cat > .env << 'EOF'
AI_MODE=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=ft:gpt-3.5-turbo-0125:personal:lentera-safety-v2:CtBTujc1

WHISPER_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
WHISPER_LANGUAGE=id

LOCAL_TTS_MODEL=nayerim/speecht5-indonesian-tts
TTS_DEVICE=cpu

API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production

LOG_LEVEL=INFO
EOF

echo "✓ .env file created"
echo ""

# Step 2: Fix Python dependencies
echo "Step 2: Fixing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
echo "✓ Dependencies fixed"
echo ""

# Step 3: Restart service
echo "Step 3: Restarting backend service..."
systemctl restart lentera-backend
sleep 3
echo "✓ Service restarted"
echo ""

# Step 4: Check status
echo "Step 4: Checking service status..."
systemctl status lentera-backend --no-pager
echo ""

# Step 5: Test health
echo "Step 5: Testing health endpoint..."
sleep 2
curl http://localhost:8000/health
echo ""
echo ""

echo "=========================================="
echo "  Fix Complete!"
echo "=========================================="
echo ""
echo "Check full logs: journalctl -u lentera-backend -n 50"
echo "Live logs: journalctl -u lentera-backend -f"
