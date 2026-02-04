#!/bin/bash
# Production deployment script for VPS
# Run this after vps-setup.sh

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "======================================"
echo "LenteraDreamFlow Production Deployment"
echo "======================================"

# Configuration
DOMAIN="${DOMAIN:-your-domain.com}"
EMAIL="${EMAIL:-your-email@example.com}"
BACKEND_DIR="$HOME/LenteraDreamFlow/backend"

echo ""
echo "${YELLOW}Step 1: Installing Nginx${NC}"
if ! command -v nginx &> /dev/null; then
    sudo apt update
    sudo apt install -y nginx
    echo "${GREEN}✓ Nginx installed${NC}"
else
    echo "${GREEN}✓ Nginx already installed${NC}"
fi

echo ""
echo "${YELLOW}Step 2: Configuring Nginx${NC}"
sudo cp nginx-lentera.conf /etc/nginx/sites-available/lentera-api

# Update domain in config
sudo sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/lentera-api

# Enable site
sudo ln -sf /etc/nginx/sites-available/lentera-api /etc/nginx/sites-enabled/

# Test configuration
if sudo nginx -t; then
    echo "${GREEN}✓ Nginx configuration valid${NC}"
    sudo systemctl reload nginx
else
    echo "${RED}✗ Nginx configuration invalid${NC}"
    exit 1
fi

echo ""
echo "${YELLOW}Step 3: Setting up systemd service${NC}"
sudo cp lentera-backend.service /etc/systemd/system/

# Update paths in service file
sudo sed -i "s|/home/ubuntu|$HOME|g" /etc/systemd/system/lentera-backend.service

# Update user
CURRENT_USER=$(whoami)
sudo sed -i "s/User=ubuntu/User=$CURRENT_USER/g" /etc/systemd/system/lentera-backend.service
sudo sed -i "s/Group=ubuntu/Group=$CURRENT_USER/g" /etc/systemd/system/lentera-backend.service

# Reload systemd
sudo systemctl daemon-reload
sudo systemctl enable lentera-backend
sudo systemctl start lentera-backend

echo "${GREEN}✓ Backend service started${NC}"

echo ""
echo "${YELLOW}Step 4: Installing SSL certificate (Let's Encrypt)${NC}"
if [ "$DOMAIN" != "your-domain.com" ]; then
    if ! command -v certbot &> /dev/null; then
        sudo apt install -y certbot python3-certbot-nginx
    fi
    
    echo "Running certbot for domain: $DOMAIN"
    sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL
    
    echo "${GREEN}✓ SSL certificate installed${NC}"
else
    echo "${YELLOW}⚠ Skipping SSL (domain not configured)${NC}"
    echo "To setup SSL later, run:"
    echo "  sudo certbot --nginx -d yourdomain.com --email your-email@example.com"
fi

echo ""
echo "${YELLOW}Step 5: Configuring firewall${NC}"
if command -v ufw &> /dev/null; then
    sudo ufw allow 'Nginx Full'
    sudo ufw allow OpenSSH
   # Don't enable ufw directly to avoid locking out users
    echo "${YELLOW}⚠ Firewall rules added. Enable with: sudo ufw enable${NC}"
fi

echo ""
echo "${YELLOW}Step 6: Verifying deployment${NC}"

# Check backend service
if systemctl is-active --quiet lentera-backend; then
    echo "${GREEN}✓ Backend service is running${NC}"
else
    echo "${RED}✗ Backend service is not running${NC}"
    echo "Check logs with: sudo journalctl -u lentera-backend -n 50"
fi

# Check Nginx
if systemctl is-active --quiet nginx; then
    echo "${GREEN}✓ Nginx is running${NC}"
else
    echo "${RED}✗ Nginx is not running${NC}"
fi

# Test health endpoint
sleep 2
HEALTH_CHECK=$(curl -s http://localhost:8000/health || echo "failed")
if [[ "$HEALTH_CHECK" == *"ok"* ]] || [[ "$HEALTH_CHECK" == *"degraded"* ]]; then
    echo "${GREEN}✓ Health check passed${NC}"
else
    echo "${RED}✗ Health check failed${NC}"
    echo "Response: $HEALTH_CHECK"
fi

echo ""
echo "${GREEN}======================================"
echo "✓ Production Deployment Complete!"
echo "======================================${NC}"
echo ""
echo "Your API is now available at:"
if [ "$DOMAIN" != "your-domain.com" ]; then
    echo "  https://$DOMAIN"
else
    echo "  http://$(curl -s ifconfig.me)"
fi
echo ""
echo "Useful commands:"
echo "  Check status:  sudo systemctl status lentera-backend"
echo "  View logs:     sudo journalctl -u lentera-backend -f"
echo "  Restart:       sudo systemctl restart lentera-backend"
echo "  Test API:      curl https://$DOMAIN/health"
echo ""
