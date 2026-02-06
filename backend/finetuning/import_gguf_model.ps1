# ==================================================
# Quick Setup Script - GGUF Model Integration
# ==================================================
# Jalankan script ini setelah download .gguf file
# ==================================================

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🔥 LENTERA - GGUF Model Import Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$modelName = "lentera-mental-health"
$ggufFile = "lentera-llama-3.1-8b-mental-health.gguf"
$finetuningDir = "c:\LenteraDreamFlow\backend\finetuning"
$backendDir = "c:\LenteraDreamFlow\backend"

# Step 1: Check if GGUF file exists
Write-Host "🔍 Step 1: Checking GGUF file..." -ForegroundColor Yellow
$ggufPath = Join-Path $finetuningDir $ggufFile

if (Test-Path $ggufPath) {
    Write-Host "   ✅ Found: $ggufFile" -ForegroundColor Green
}
else {
    Write-Host "   ❌ File not found: $ggufPath" -ForegroundColor Red
    Write-Host "   Please place your .gguf file in: $finetuningDir" -ForegroundColor Red
    Write-Host ""
    Write-Host "   You can rename your .gguf file to: $ggufFile" -ForegroundColor Yellow
    Write-Host "   Or update the `$ggufFile variable in this script" -ForegroundColor Yellow
    exit 1
}

# Step 2: Check if Modelfile exists
Write-Host ""
Write-Host "🔍 Step 2: Checking Modelfile..." -ForegroundColor Yellow
$modelfilePath = Join-Path $finetuningDir "Modelfile"

if (Test-Path $modelfilePath) {
    Write-Host "   ✅ Found: Modelfile" -ForegroundColor Green
}
else {
    Write-Host "   ❌ Modelfile not found!" -ForegroundColor Red
    Write-Host "   Please create Modelfile first (see GGUF_INTEGRATION_GUIDE.md)" -ForegroundColor Red
    exit 1
}

# Step 3: Check if Ollama is installed
Write-Host ""
Write-Host "🔍 Step 3: Checking Ollama installation..." -ForegroundColor Yellow

try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "   ✅ Ollama installed: $ollamaVersion" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Ollama not found!" -ForegroundColor Red
    Write-Host "   Please install Ollama first: https://ollama.ai" -ForegroundColor Red
    exit 1
}

# Step 4: Check if model already exists
Write-Host ""
Write-Host "🔍 Step 4: Checking existing models..." -ForegroundColor Yellow
$existingModels = ollama list 2>&1

if ($existingModels -match $modelName) {
    Write-Host "   ⚠️  Model '$modelName' already exists" -ForegroundColor Yellow
    $response = Read-Host "   Do you want to recreate it? (y/n)"
    
    if ($response -ne 'y') {
        Write-Host "   Skipping model import..." -ForegroundColor Yellow
        $skipImport = $true
    }
    else {
        Write-Host "   Removing existing model..." -ForegroundColor Yellow
        ollama rm $modelName
        $skipImport = $false
    }
}
else {
    Write-Host "   ✅ No existing model found" -ForegroundColor Green
    $skipImport = $false
}

# Step 5: Import model to Ollama
if (-not $skipImport) {
    Write-Host ""
    Write-Host "🚀 Step 5: Importing model to Ollama..." -ForegroundColor Yellow
    Write-Host "   This may take a few minutes..." -ForegroundColor Gray
    
    Set-Location $finetuningDir
    $importResult = ollama create $modelName -f Modelfile 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Model imported successfully!" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Import failed!" -ForegroundColor Red
        Write-Host "   Error: $importResult" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host ""
    Write-Host "⏭️  Step 5: Skipped model import" -ForegroundColor Gray
}

# Step 6: Verify model
Write-Host ""
Write-Host "🔍 Step 6: Verifying model..." -ForegroundColor Yellow
$models = ollama list 2>&1

if ($models -match $modelName) {
    Write-Host "   ✅ Model verified in Ollama" -ForegroundColor Green
}
else {
    Write-Host "   ❌ Model not found in Ollama!" -ForegroundColor Red
    exit 1
}

# Step 7: Update .env file
Write-Host ""
Write-Host "🔧 Step 7: Updating backend configuration..." -ForegroundColor Yellow
$envPath = Join-Path $backendDir ".env"

if (Test-Path $envPath) {
    $envContent = Get-Content $envPath -Raw
    
    # Check if OLLAMA_MODEL already exists
    if ($envContent -match "OLLAMA_MODEL=") {
        # Update existing
        $envContent = $envContent -replace "OLLAMA_MODEL=.*", "OLLAMA_MODEL=$modelName"
        Write-Host "   ✅ Updated OLLAMA_MODEL in .env" -ForegroundColor Green
    }
    else {
        # Add new
        $envContent += "`nOLLAMA_MODEL=$modelName"
        Write-Host "   ✅ Added OLLAMA_MODEL to .env" -ForegroundColor Green
    }
    
    Set-Content -Path $envPath -Value $envContent
}
else {
    Write-Host "   ⚠️  .env file not found, creating new one..." -ForegroundColor Yellow
    $envContent = "OLLAMA_MODEL=$modelName`nOLLAMA_BASE_URL=http://localhost:11434"
    Set-Content -Path $envPath -Value $envContent
    Write-Host "   ✅ Created .env file" -ForegroundColor Green
}

# Step 8: Test model
Write-Host ""
Write-Host "🧪 Step 8: Testing model..." -ForegroundColor Yellow
Write-Host "   Running quick test..." -ForegroundColor Gray

$testPrompt = "Halo, aku merasa stress akhir-akhir ini"
Write-Host "   Prompt: $testPrompt" -ForegroundColor Cyan

try {
    $testResponse = ollama run $modelName $testPrompt 2>&1
    Write-Host "   Response: $testResponse" -ForegroundColor Cyan
    Write-Host "   ✅ Model is responding!" -ForegroundColor Green
}
catch {
    Write-Host "   ❌ Model test failed!" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Summary
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Start backend: .\start_backend_local.bat" -ForegroundColor White
Write-Host "  2. Test API: python backend\finetuning\test_model_quality.py" -ForegroundColor White
Write-Host "  3. Check guide: backend\GGUF_INTEGRATION_GUIDE.md" -ForegroundColor White
Write-Host ""
Write-Host "Model name: $modelName" -ForegroundColor Cyan
Write-Host "Model location: Ollama" -ForegroundColor Cyan
Write-Host "Backend config: Updated ✅" -ForegroundColor Green
Write-Host ""
