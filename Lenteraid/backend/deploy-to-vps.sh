#!/bin/bash
# LENTERA Backend Deployment Script for Contabo VPS
# IP: 84.247.150.83

set -e  # Exit on error

echo "=========================================="
echo "  LENTERA Backend - VPS Deployment"
echo "  Target: 84.247.150.83"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
VPS_IP="84.247.150.83"
VPS_USER="root"  # Change if different
DEPLOY_DIR="/opt/lentera-backend"
REPO_URL="https://github.com/lentera-star/Lenteraid.git"  # Update with your repo

echo -e "${YELLOW}Step 1: Connecting to VPS...${NC}"
echo "IP: $VPS_IP"
echo "User: $VPS_USER"
echo ""

# Function to run commands on VPS
run_on_vps() {
    ssh ${VPS_USER}@${VPS_IP} "$1"
}

echo -e "${YELLOW}Step 2: Installing system dependencies...${NC}"
run_on_vps "apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    ffmpeg \
    git \
    docker.io \
    docker-compose"

echo -e "${GREEN}✓ System dependencies installed${NC}"
echo ""

echo -e "${YELLOW}Step 3: Setting up Ollama...${NC}"
run_on_vps "curl -fsSL https://ollama.ai/install.sh | sh"
run_on_vps "systemctl enable ollama"
run_on_vps "systemctl start ollama"
echo "Waiting for Ollama to start..."
sleep 5
run_on_vps "ollama pull llama2"
echo -e "${GREEN}✓ Ollama installed and llama2 model pulled${NC}"
echo ""

echo -e "${YELLOW}Step 4: Creating deployment directory...${NC}"
run_on_vps "mkdir -p $DEPLOY_DIR"
echo -e "${GREEN}✓ Directory created: $DEPLOY_DIR${NC}"
echo ""

echo -e "${YELLOW}Step 5: Deploying backend code...${NC}"
# Copy backend files to VPS
scp -r ../backend/* ${VPS_USER}@${VPS_IP}:${DEPLOY_DIR}/
echo -e "${GREEN}✓ Backend files copied${NC}"
echo ""

echo -e "${YELLOW}Step 6: Setting up Python virtual environment...${NC}"
run_on_vps "cd $DEPLOY_DIR && python3 -m venv venv"
run_on_vps "cd $DEPLOY_DIR && source venv/bin/activate && pip install --upgrade pip"
run_on_vps "cd $DEPLOY_DIR && source venv/bin/activate && pip install -r requirements.txt"
echo -e "${GREEN}✓ Python environment ready${NC}"
echo ""

echo -e "${YELLOW}Step 7: Configuring environment...${NC}"
run_on_vps "cd $DEPLOY_DIR && cp .env.production .env"
echo -e "${GREEN}✓ Environment configured${NC}"
echo ""

echo -e "${YELLOW}Step 8: Creating systemd service...${NC}"
run_on_vps "cat > /etc/systemd/system/lentera-backend.service << 'EOF'
[Unit]
Description=LENTERA Backend API
After=network.target ollama.service
Requires=ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=$DEPLOY_DIR
Environment=\"PATH=$DEPLOY_DIR/venv/bin\"
ExecStart=$DEPLOY_DIR/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

run_on_vps "systemctl daemon-reload"
run_on_vps "systemctl enable lentera-backend"
run_on_vps "systemctl start lentera-backend"
echo -e "${GREEN}✓ Systemd service created and started${NC}"
echo ""

echo -e "${YELLOW}Step 9: Configuring firewall...${NC}"
run_on_vps "ufw allow 8000/tcp"
run_on_vps "ufw allow 22/tcp"
run_on_vps "ufw --force enable"
echo -e "${GREEN}✓ Firewall configured${NC}"
echo ""

echo -e "${YELLOW}Step 10: Testing deployment...${NC}"
sleep 3
HEALTH_CHECK=$(curl -s http://${VPS_IP}:8000/health || echo "FAILED")
if [[ $HEALTH_CHECK == *"ok"* ]] || [[ $HEALTH_CHECK == *"degraded"* ]]; then
    echo -e "${GREEN}✓ Backend is responding!${NC}"
    echo "$HEALTH_CHECK"
else
    echo -e "${RED}✗ Health check failed. Check logs with:${NC}"
    echo "  ssh ${VPS_USER}@${VPS_IP} 'journalctl -u lentera-backend -f'"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}  DEPLOYMENT COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "Backend URL: http://${VPS_IP}:8000"
echo "Health Check: http://${VPS_IP}:8000/health"
echo ""
echo "Useful commands:"
echo "  Check status: ssh ${VPS_USER}@${VPS_IP} 'systemctl status lentera-backend'"
echo "  View logs: ssh ${VPS_USER}@${VPS_IP} 'journalctl -u lentera-backend -f'"
echo "  Restart: ssh ${VPS_USER}@${VPS_IP} 'systemctl restart lentera-backend'"
echo ""
