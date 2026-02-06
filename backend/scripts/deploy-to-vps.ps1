# LENTERA Backend Deployment Script for Contabo VPS (Windows - Fixed)
# IP: 84.247.150.83

param(
    [string]$VpsIp = "84.247.150.83",
    [string]$VpsUser = "root",
    [string]$DeployDir = "/opt/lentera-backend"
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  LENTERA Backend - VPS Deployment" -ForegroundColor Cyan
Write-Host "  Target: $VpsIp" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check SSH availability
Write-Host "Checking SSH connection..." -ForegroundColor Yellow
try {
    $null = ssh ${VpsUser}@${VpsIp} "echo 'SSH OK'" 2>&1
    Write-Host "[OK] SSH connection successful" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] SSH connection failed" -ForegroundColor Red
    Write-Host "Please ensure you can connect: ssh ${VpsUser}@${VpsIp}" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Step 1: Install system dependencies
Write-Host "Step 1: Installing system dependencies..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsIp} "apt-get update && apt-get install -y python3.10 python3-pip python3-venv ffmpeg git curl"
Write-Host "[OK] System dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 2: Skip Ollama (using OpenAI instead)
Write-Host "Step 2: Skipping Ollama (using OpenAI fine-tuned model)..." -ForegroundColor Yellow
Write-Host "[OK] AI Mode: OpenAI" -ForegroundColor Green
Write-Host ""

# Step 3: Create deployment directory
Write-Host "Step 3: Creating deployment directory..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsIp} "mkdir -p $DeployDir"
Write-Host "[OK] Directory created: $DeployDir" -ForegroundColor Green
Write-Host ""

# Step 4: Copy backend files
Write-Host "Step 4: Deploying backend code..." -ForegroundColor Yellow
Write-Host "Copying files to VPS (this may take a while)..." -ForegroundColor Yellow

# Use SCP to copy files
$backendPath = Split-Path -Parent $PSScriptRoot
if (Test-Path "$backendPath\backend") {
    $sourcePath = "$backendPath\backend\*"
}
else {
    $sourcePath = "$PSScriptRoot\*"
}

scp -r $sourcePath ${VpsUser}@${VpsIp}:${DeployDir}/
Write-Host "[OK] Backend files copied" -ForegroundColor Green
Write-Host ""

# Step 5: Setup Python environment
Write-Host "Step 5: Setting up Python virtual environment..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsIp} @"
cd $DeployDir
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
"@
Write-Host "[OK] Python environment ready" -ForegroundColor Green
Write-Host ""

# Step 6: Configure environment
Write-Host "Step 6: Configuring environment..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsIp} "cd $DeployDir && cp .env.production .env"
Write-Host "[OK] Environment configured" -ForegroundColor Green
Write-Host ""

# Step 7: Create systemd service
Write-Host "Step 7: Creating systemd service..." -ForegroundColor Yellow

$serviceContent = @"
[Unit]
Description=LENTERA Backend API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DeployDir
Environment="PATH=$DeployDir/venv/bin"
ExecStart=$DeployDir/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"@

# Write service file via SSH
ssh ${VpsUser}@${VpsIp} "echo '$serviceContent' > /etc/systemd/system/lentera-backend.service"

ssh ${VpsUser}@${VpsIp} @"
systemctl daemon-reload
systemctl enable lentera-backend
systemctl start lentera-backend
"@

Write-Host "[OK] Systemd service created and started" -ForegroundColor Green
Write-Host ""

# Step 8: Configure firewall
Write-Host "Step 8: Configuring firewall..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsIp} @"
ufw allow 8000/tcp
ufw allow 22/tcp
yes | ufw enable
"@

Write-Host "[OK] Firewall configured" -ForegroundColor Green
Write-Host ""

# Step 9: Test deployment
Write-Host "Step 9: Testing deployment..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://${VpsIp}:8000/health" -TimeoutSec 10 -ErrorAction Stop
    Write-Host "[OK] Backend is responding!" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "[WARNING] Health check failed. Check logs with:" -ForegroundColor Yellow
    Write-Host "  ssh ${VpsUser}@${VpsIp} 'journalctl -u lentera-backend -f'" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend URL: http://${VpsIp}:8000"
Write-Host "Health Check: http://${VpsIp}:8000/health"
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  Check status: ssh ${VpsUser}@${VpsIp} 'systemctl status lentera-backend'"
Write-Host "  View logs: ssh ${VpsUser}@${VpsIp} 'journalctl -u lentera-backend -f'"
Write-Host "  Restart: ssh ${VpsUser}@${VpsIp} 'systemctl restart lentera-backend'"
Write-Host ""
