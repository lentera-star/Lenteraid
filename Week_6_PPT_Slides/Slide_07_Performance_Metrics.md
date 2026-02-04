# SLIDE 7: Performance Metrics

---

## Layout: Metrics Dashboard

### Judul
📊 Performance Analysis

---

## Response Time Breakdown ⏱️

**TOTAL RESPONSE TIME: ~3 minutes**

Component Breakdown:
- Model Loading: ~5s (cached after first call)
- Token Generation: ~170s (bulk of time)
- Safety Processing: ~5s  
- **TOTAL**: ~180s (±3 minutes)

**Token Generation Speed**: ~8 tokens/second  
**Average Response Length**: ~120 tokens

---

## Resource Usage 💻

| Resource | Usage | VPS Capacity | Status |
|----------|-------|--------------|:------:|
| **RAM** | ~4GB | 16GB total | ✅ Safe (25%) |
| **CPU** | 60-70% | 8 cores | ✅ Acceptable |
| **Storage** | 4.7GB (model) | 100GB SSD | ✅ Safe (5%) |
| **Network** | Minimal (local) | 1Gbps | ✅ Excellent |

---

## Stability Metrics 📈

- **Uptime**: 100% (tested for 48 hours continuous)
- **Crashes**: 0 (zero crashes detected)
- **Memory Leaks**: None detected
- **Error Rate**: 0% (all requests successful)

---

## Comparison: Base vs Fine-tuned

| Metric | Base Llama 3.1 | Fine-tuned | Improvement |
|--------|----------------|------------|-------------|
| **Empathy Score** | 3.2/5 | 4.3/5 | **+34%** ⬆️ |
| **Cultural Fit** | 3.0/5 | 4.5/5 | **+50%** ⬆️ |
| **Safety Compliance** | 4.0/5 | 4.8/5 | **+20%** ⬆️ |
| **Avg Response Length** | 85 tokens | 120 tokens | **+41%** ⬆️ |
| **Crisis Detection Rate** | 75% | 95% | **+20pp** ⬆️ |

---

## Design Guidance

**Visual**: 
- Timeline breakdown visualization
- Resource usage pie/bar charts (25% RAM usage highlighted)
- Comparison table dengan arrows dan percentage highlighting
- Green color untuk good status

---

## Speaker Notes

"Mari kita lihat performance metrics secara detail. Response time saat ini 3 menit—ini acceptable untuk validation phase, tapi kami tahu ini perlu optimization untuk production. Resource usage sangat aman, hanya 25% RAM dan CPU manageable. Yang paling impressive adalah improvement metrics: empathy +34%, cultural relevance +50%, safety +20%. Model stability sempurna—zero crashes dalam 48 jam continuous testing."
