Write-Host "VPS Repair Wizard" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Connecting to VPS..." -ForegroundColor Yellow
Write-Host "Password: Lentera123" -ForegroundColor Green
Write-Host ""

# Create SSH commands
$commands = @"
# PASTE THESE COMMANDS ONE BY ONE INTO THE VPS SSH SESSION:

# 1. Kill processes on port 8000
sudo fuser -k 8000/tcp

# 2. Kill any hanging main.py processes
pkill -f 'main.py'

# 3. Restart the backend service
sudo systemctl restart lentera-backend

# 4. Wait a moment
sleep 5

# 5. Check service status
sudo systemctl status lentera-backend --no-pager

# 6. Test local connectivity
curl -s http://localhost:8000/health

# 7. Check Ollama model
ollama list | grep "lentera-fast"

# 8. Exit SSH
exit
"@

# Display commands
Write-Host "Commands to run:" -ForegroundColor Yellow
Write-Host $commands -ForegroundColor White

Write-Host ""
Write-Host "Commands copied to clipboard!" -ForegroundColor Green
$commands | Set-Clipboard

Write-Host ""
Write-Host "Now opening SSH connection..." -ForegroundColor Yellow
Write-Host "Paste the commands after logging in!" -ForegroundColor Cyan
Write-Host ""

# Open SSH
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ssh root@84.247.150.83"
