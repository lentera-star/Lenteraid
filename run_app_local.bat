@echo off
echo 📱 Starting LENTERA Flutter App (Local Backend)...
echo.

echo ⏳ Waiting for Backend to be ready (http://localhost:8000/health)...
echo Ini mungkin butuh waktu beberapa menit kalau baru pertama kali build (karena download engine suara).
echo Jangan diclose window ini...

:check_backend
powershell -Command "$p = try { (Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing -TimeoutSec 2).StatusCode } catch { 0 }; if ($p -eq 200) { exit 0 } else { exit 1 }"
if %errorlevel% equ 0 (
    echo.
    echo ✅ Backend DETECTED!
    goto start_app
)

timeout /t 5 /nobreak >nul
goto check_backend

:start_app
echo 🚀 Launching Flutter in Chrome...
flutter run -d chrome --dart-define=USE_LOCAL=true
