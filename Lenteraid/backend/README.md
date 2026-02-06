# LENTERA Backend

Backend service untuk aplikasi LENTERA - AI-powered mental health counseling.

## Tech Stack

- **FastAPI**: Web framework untuk REST API dan WebSocket
- **Ollama**: Local LLM untuk AI conversations
- **Whisper**: Speech-to-Text untuk voice calls
- **TTS**: Text-to-Speech untuk AI voice responses
- **Docker**: Containerization

## Setup

### Prerequisites

1. Docker Desktop installed dan running
2. Git
3. Minimal 8GB RAM (untuk menjalankan Ollama models)

### Quick Start dengan Docker Compose

1. **Clone dan masuk ke direktori**
   ```bash
   cd LenteraDreamFlow
   ```

2. **Jalankan dengan Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Download Ollama model (first time only)**
   ```bash
   docker exec -it lentera-ollama ollama pull llama2
   ```
   
   Atau model lain yang lebih ringan:
   ```bash
   docker exec -it lentera-ollama ollama pull phi
   ```

4. **Verify services running**
   - Backend API: http://localhost:8000
   - Ollama: http://localhost:11434
   - API Docs: http://localhost:8000/docs

### Development Setup (tanpa Docker)

1. **Setup Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # atau: source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install dan jalankan Ollama locally**
   - Download dari https://ollama.ai
   - Run: `ollama serve`
   - Pull model: `ollama pull llama2`

4. **Setup environment variables**
   ```bash
   copy .env.example .env
   # Edit .env sesuai kebutuhan
   ```

5. **Run backend**
   ```bash
   python main.py
   ```

## API Endpoints

### Health Check
```
GET /health
```

### Chat
```
POST /api/chat
{
  "message": "Saya merasa cemas",
  "user_id": "optional",
  "conversation_id": "optional"
}
```

### Voice Call (WebSocket)
```
WS /ws/voice-call
```

### Mood Analysis
```
POST /api/mood/analyze
{
  "mood_rating": 3,
  "emotions": ["anxious", "tired"],
  "journal": "Hari ini berat sekali..."
}
```

## Docker Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f backend
docker-compose logs -f ollama
```

### Rebuild backend
```bash
docker-compose up -d --build backend
```

### Enter container
```bash
docker exec -it lentera-backend bash
docker exec -it lentera-ollama bash
```

## Ollama Models

### Recommended Models

**Untuk komputer dengan GPU bagus (8GB+ VRAM):**
- `llama2` (7B) - Balanced
- `mistral` (7B) - Fast & good quality
- `neural-chat` (7B) - Fine-tuned untuk conversation

**Untuk komputer tanpa GPU atau RAM terbatas:**
- `phi` (2.7B) - Very efficient
- `tinyllama` (1.1B) - Fastest, basic capabilities
- `orca-mini` (3B) - Good balance

### Pull dan switch model
```bash
# Pull model
docker exec -it lentera-ollama ollama pull phi

# List downloaded models
docker exec -it lentera-ollama ollama list

# Update .env untuk ganti model
OLLAMA_MODEL=phi
```

## Integration dengan Flutter

Update base URL di Flutter app:

```dart
// Development (Android Emulator)
const API_BASE_URL = "http://10.0.2.2:8000";

// Development (Physical Device - same network)
const API_BASE_URL = "http://192.168.x.x:8000";  // Ganti dengan IP komputer Anda

// Production
const API_BASE_URL = "https://your-domain.com";
```

### WebSocket untuk voice call
```dart
final channel = WebSocketChannel.connect(
  Uri.parse('ws://10.0.2.2:8000/ws/voice-call'),
);
```

## Troubleshooting

### Docker tidak bisa connect
```bash
# Windows: Start Docker Desktop
# Verify dengan:
docker ps
```

### Ollama model download lambat
- Gunakan model yang lebih kecil (phi, tinyllama)
- Download manual: https://ollama.ai/library

### Backend tidak bisa akses Ollama
- Check logs: `docker-compose logs ollama`
- Verify network: `docker network ls`
- Restart: `docker-compose restart`

### Port sudah dipakai
Edit `docker-compose.yml` untuk ganti port:
```yaml
ports:
  - "8001:8000"  # Ganti 8000 jadi 8001
```

## Next Steps

1. ✅ Setup Docker dan Ollama
2. ⏳ Integrate Whisper untuk STT
3. ⏳ Integrate TTS untuk voice responses
4. ⏳ Setup Supabase untuk database
5. ⏳ Implement RAG untuk contextual responses
6. ⏳ Add authentication
