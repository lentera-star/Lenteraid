@echo off
echo 🚀 Starting LENTERA Local Backend (OpenAI Mode)...
echo.

echo 📦 Starting Containers using local.env...
docker-compose --env-file local.env up -d

echo.
echo ⏳ Waiting for services...
timeout /t 5 /nobreak

echo.
echo 💡 Using OpenAI Model (Skipping Llama2 pull)...
echo IF you want to use Local Ollama instead, uncomment the line below in this script.
REM docker exec lentera-ollama ollama pull llama2

echo.
echo ✅ Backend Ready!
echo API: http://localhost:8000
echo.
pause
