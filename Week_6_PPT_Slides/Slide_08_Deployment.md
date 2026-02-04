# SLIDE 8: VPS Deployment

---

## Layout: Architecture Diagram + Benefits

### Judul
🚀 Production Deployment Architecture

---

## Why Ollama on VPS? 🤔

**Advantages**:
- ✅ **Data Privacy**: Model runs on-premise, data tidak keluar dari server kami
- ✅ **Cost Efficiency**: Zero API costs (vs GPT-4: ~$0.06/request × 1000 users = $60/day)
- ✅ **Full Control**: Custom model behavior, no rate limits
- ✅ **Compliance**: Easier untuk health data regulation compliance
- ✅ **Latency Predictable**: Tidak depend on external API availability

---

## Deployment Stack 🏗️

**VPS Infrastructure (Cloud)**

Layers (top to bottom):
1. **Nginx Reverse Proxy**
   - SSL/TLS Termination
   - Load Balancing (future)

2. **Docker Container - FastAPI Backend**
   - Request handling
   - Safety validation
   - Session management

3. **Ollama Service**
   - Fine-tuned Llama 3.1-8B
   - Quantized (INT8) - 4.7GB
   - GPU: None (CPU inference)

4. **Supabase (External)**
   - User data
   - Conversation logs
   - Mood tracking

---

## Deployment Metrics 📊

- **Deployment Time**: 15 minutes (model loading included)
- **Rollback Capability**: ✅ Yes (Docker versioning)
- **Monitoring**: Health check endpoint every 30s
- **Backup Strategy**: VPS snapshot daily

---

## Design Guidance

**Visual**: 
- Layered architecture diagram dengan boxes
- Different colors untuk each layer:
  - Nginx: Orange
  - FastAPI: Purple
  - Ollama: Green
  - Supabase: Blue
- Arrows showing data flow

---

## Speaker Notes

"Kami deploy menggunakan Ollama di VPS yang sama dengan backend untuk efficiency. Alasan utama on-premise deployment adalah data privacy—critical untuk health app—dan cost efficiency dibandingkan cloud API. Deployment stack menggunakan Nginx untuk SSL, Docker untuk FastAPI backend, dan Ollama untuk model inference. Integration dengan safety validator seamless, dan kami punya health monitoring + backup strategy."
