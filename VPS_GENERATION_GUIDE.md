# Moving Data Generation to VPS - Step by Step

## Step 1: Stop Local Process (in PowerShell)
```powershell
# Press Ctrl+C to stop the running script
# Then close PowerShell
```

## Step 2: SSH to VPS
```powershell
ssh root@84.247.150.83
```

## Step 3: Setup on VPS
```bash
# Navigate to backend
cd /home/Lenteraid/backend

# Create .env file with API key
cat > .env << 'EOF'
OPENAI_API_KEY=your-openai-api-key-here
EOF

# Install Python packages (if not already installed)
pip3 install openai python-dotenv pandas pyyaml

# Verify API key loaded
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', os.getenv('OPENAI_API_KEY')[:20])"
```

## Step 4: Run in Background with nohup
```bash
# Start generation in background
nohup python3 generate_training_data.py --num 1000 > generation.log 2>&1 &

# Get process ID
echo $!

# This will print a number like: 12345
# Save this number!
```

## Step 5: Check Progress
```bash
# View live progress
tail -f generation.log

# Press Ctrl+C to exit viewing (script keeps running!)

# Or check last 50 lines
tail -50 generation.log
```

## Step 6: Logout & Close Laptop
```bash
# Exit SSH
exit

# Close laptop - script KEEPS RUNNING on VPS!
```

## Step 7: Check Later (from any device)
```bash
# SSH again
ssh root@84.247.150.83

# Check if still running
ps aux | grep generate_training_data

# View progress
tail -50 /home/Lenteraid/backend/generation.log

# Check if file is being created
ls -lh /home/Lenteraid/backend/lentera_training_data.jsonl
```

## When Complete:
```bash
# Check final stats
tail -100 generation.log

# Verify file
wc -l lentera_training_data.jsonl  # Should show ~1000 lines

# Download to laptop (if needed)
scp root@84.247.150.83:/home/Lenteraid/backend/lentera_training_data.jsonl .
```

## Troubleshooting:

### If script stops:
```bash
# Check what happened
tail -100 generation.log

# Restart
nohup python3 generate_training_data.py --num 1000 > generation.log 2>&1 &
```

### Check process:
```bash
# Find process ID
ps aux | grep python

# Kill if needed
kill <PID>
```

## Timeline:
- Setup: 10 min
- Generation: 2-3 hours (runs automatically!)
- Total: ~3 hours, but you're FREE after 10 min setup! 🎉
