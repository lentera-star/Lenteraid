@echo off
echo ===================================
echo Modal Deployment Script
echo ===================================
echo.

echo Step 1: Add your HuggingFace token
echo Please enter your HuggingFace token (from https://huggingface.co/settings/tokens):
set /p HF_TOKEN=Token: 

echo.
echo Creating Modal secret...
modal secret create huggingface HF_TOKEN=%HF_TOKEN%

echo.
echo Step 2: Deploying to Modal...
cd backend\modal
modal deploy modal_inference.py

echo.
echo ===================================
echo Deployment complete!
echo ===================================
pause
