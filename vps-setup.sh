#!/bin/bash
# LenteraDreamFlow VPS Setup Script
# This script sets up Ollama with your custom GGUF model

set -e  # Exit on error

echo "======================================"
echo "LenteraDreamFlow VPS Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
MODEL_FILE="Meta-Llama-3.1-8B-Instruct.Q2_K.gguf"
MODEL_NAME="lentera-dreamflow"
BACKEND_DIR="$HOME/LenteraDreamFlow/backend"

echo ""
echo "${YELLOW}Step 1: Checking Ollama installation...${NC}"
if ! command -v ollama &> /dev/null; then
    echo "${YELLOW}Ollama not found. Installing...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
    echo "${GREEN}✓ Ollama installed${NC}"
else
    echo "${GREEN}✓ Ollama already installed${NC}"
fi

echo ""
echo "${YELLOW}Step 2: Checking for model file...${NC}"
if [ ! -f "$MODEL_FILE" ]; then
    echo "${RED}✗ Model file not found: $MODEL_FILE${NC}"
    echo "Please upload the model file to this directory first:"
    echo "  scp $MODEL_FILE user@your-vps-ip:~/"
    exit 1
fi
echo "${GREEN}✓ Model file found${NC}"

echo ""
echo "${YELLOW}Step 3: Creating Modelfile...${NC}"
cat > Modelfile << 'EOF'
FROM ./Meta-Llama-3.1-8B-Instruct.Q2_K.gguf

TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096
PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"

SYSTEM """Kamu adalah asisten kesehatan mental yang berempati bernama LENTERA untuk membantu pengguna Indonesia. 

Prinsip yang harus kamu ikuti:
1. Selalu empati dan mendukung
2. Jangan mendiagnosis kondisi mental secara spesifik
3. Jika ada tanda bahaya (bunuh diri, self-harm), sarankan hubungi profesional
4. Berikan saran praktis untuk self-care dan coping mechanisms
5. Gunakan bahasa Indonesia yang hangat dan ramah
6. Jaga privasi dan confidentiality

Jangan pernah:
- Memberikan diagnosis medis
- Meresepkan obat
- Menggantikan terapi profesional
- Memberikan saran yang berbahaya"""
EOF
echo "${GREEN}✓ Modelfile created${NC}"

echo ""
echo "${YELLOW}Step 4: Importing model to Ollama (this may take a few minutes)...${NC}"
ollama create $MODEL_NAME -f Modelfile
echo "${GREEN}✓ Model imported successfully${NC}"

echo ""
echo "${YELLOW}Step 5: Testing model...${NC}"
TEST_RESPONSE=$(ollama run $MODEL_NAME "Halo, apa kabar?" --verbose=false 2>&1 | head -n 5)
if [ -n "$TEST_RESPONSE" ]; then
    echo "${GREEN}✓ Model test successful${NC}"
    echo "Response preview: $TEST_RESPONSE"
else
    echo "${RED}✗ Model test failed${NC}"
    exit 1
fi

echo ""
echo "${YELLOW}Step 6: Starting Ollama service...${NC}"
# Check if running in systemd environment
if systemctl is-system-running &> /dev/null; then
    sudo systemctl enable ollama
    sudo systemctl start ollama
    echo "${GREEN}✓ Ollama service started (systemd)${NC}"
else
    echo "${YELLOW}⚠ Systemd not available. Start Ollama manually:${NC}"
    echo "  ollama serve &"
fi

echo ""
echo "${YELLOW}Step 7: Setting up backend environment...${NC}"
if [ -d "$BACKEND_DIR" ]; then
    cd $BACKEND_DIR
    
    # Create or update .env file
    cat > .env << EOF
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=$MODEL_NAME
AI_MODE=ollama
EOF
    echo "${GREEN}✓ Backend .env configured${NC}"
    
    # Install Python dependencies if needed
    if [ -f "requirements.txt" ]; then
        echo "${YELLOW}Installing Python dependencies...${NC}"
        pip3 install -r requirements.txt
        echo "${GREEN}✓ Dependencies installed${NC}"
    fi
else
    echo "${YELLOW}⚠ Backend directory not found at $BACKEND_DIR${NC}"
    echo "Please clone your repository first"
fi

echo ""
echo "${GREEN}======================================"
echo "✓ Setup Complete!"
echo "======================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test Ollama: ollama run $MODEL_NAME 'Test message'"
echo "2. Start backend: cd $BACKEND_DIR && python3 main.py"
echo "3. Test API: curl http://localhost:8000/health"
echo ""
echo "Model: $MODEL_NAME"
echo "Ollama endpoint: http://localhost:11434"
echo ""
