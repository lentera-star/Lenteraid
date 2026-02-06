# Script to fix CORS issue in FastAPI backend

echo "=== Fixing CORS Configuration ==="

# Backup original file
cp ~/backend/main.py ~/backend/main.py.backup

# Add CORS middleware to main.py
cat > ~/backend/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat_router, health_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LENTERA AI Backend")

# CORS Configuration - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev/demo)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "LENTERA AI Backend is running", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

echo "✅ CORS middleware added to main.py"
echo "🔄 Restarting backend service..."

# Restart the backend service
pkill -f "uvicorn main:app"
sleep 2
cd ~/backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

echo "✅ Backend restarted with CORS support"
echo "📝 Check logs: tail -f ~/backend/backend.log"
EOF
