# SLIDE 11: Key Learnings

---

## Layout: Learning Cards

### Judul
💡 Learnings & Project Insights

---

## Technical Learnings 🔧

### 1. Fine-tuning Efficiency
**Learning**: "500 samples cukup untuk significant improvement"

**Insight**:
- Initial assumption: perlu 2000+ samples
- Reality: High-quality, curated data → 500 samples = +34% empathy
- **Takeaway**: Quality > Quantity untuk fine-tuning

---

### 2. On-premise LLM Viability
**Learning**: "Ollama + VPS = Production-ready untuk specialized use case"

**Insight**:
- CPU inference acceptable untuk non-real-time cases
- Data privacy benefits worth latency trade-off
- **Takeaway**: On-premise feasible dengan optimization

---

### 3. Safety System Integration
**Learning**: "Multi-layer safety crucial untuk AI health apps"

**Insight**:
- Model fine-tuning alone insufficient
- Validation layers (input + output) essential
- Template override proved invaluable
- **Takeaway**: Never rely solely on model behavior untuk safety

---

## Process Learnings 📋

### 1. Validation Before Optimization
**Impact**: Caught all major issues before external testing  
**Takeaway**: Thorough internal QA is investment, not overhead

---

### 2. Quantitative + Qualitative Metrics
**Impact**: Subjective + objective provide complete picture  
**Takeaway**: Mixed methods optimal untuk model evaluation

---

### 3. Documentation = Reproducibility
**Impact**: Future iterations faster dengan clear process  
**Takeaway**: Document everything, especially ML experiments

---

## Unexpected Wins 🎉

1. **Training Speed**: Expected 12+ hours → Actual ~8 hours
2. **Cultural Relevance**: +50% improvement exceeded expectations
3. **Zero Stability Issues**: No crashes/memory leaks

---

## What We'd Do Differently 🔄

1. Earlier quantization testing (INT4 before fine-tuning)
2. More diverse test data (50+ scenarios from start)
3. Baseline metrics collection (formal before/after comparison)

---

## Design Guidance

**Visual**: 
- Learning cards dengan light bulb icons
- Wins dengan celebration design (confetti, stars)
- "What we'd do differently" dengan learning arrow icon

---

## Speaker Notes

"Week 6 sangat rich dengan learnings. Technical learning terbesar: 500 high-quality samples cukup untuk significant improvement—initially kami kira perlu 2000+. Process-wise, thorough internal testing sebelum UAT proved valuable. Project management: realistic communication dengan stakeholders tentang challenges builds trust. Ada juga unexpected wins seperti cultural relevance +50% yang exceed expectations. What we'd do differently: earlier quantization testing dan more test scenarios dari awal."
