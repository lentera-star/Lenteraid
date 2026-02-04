# SLIDE 10: Challenges & Solutions

---

## Layout: Challenge Cards with Mitigation

### Judul
🚧 Challenges & Mitigation Strategies

---

## Challenge 1: Response Time Optimization ⏱️

**Issue**: Response time ~3 minutes terlalu lambat untuk production UX  
**Impact**: 🔴 **High** - Affects user experience significantly

**Root Cause**:
- CPU-based inference (no GPU)
- Model size 8B parameters (computational heavy)
- Sequential token generation

**Mitigation Strategies**:

✅ **Immediate (Week 7)**:
- Implement response streaming (show partial responses)
- Test different quantization (INT4 vs INT8)
- Prompt optimization (reduce tokens)

🔄 **Medium-term (Week 8-9)**:
- VPS upgrade investigation (GPU cost analysis)
- Smaller model testing (Llama 3.1-7B)
- Caching for common queries

📋 **Long-term (Week 10+)**:
- Model distillation
- Hybrid approach (fast + full model)

**Expected**: Target <1 minute by Week 8

---

## Challenge 2: Training Data Volume 📚

**Issue**: 500 samples sufficient untuk PoC, production needs more  
**Impact**: ⚠️ **Medium** - Model robustness untuk diverse scenarios

**Mitigation**:
- ✅ Quality criteria established
- 🔄 Real user conversations collection (dengan consent)
- 🔄 Synthetic data generation
- 📋 Continuous retraining

**Target**: 2000+ samples by Week 10

---

## Challenge 3: Model Evaluation Objectivity 📏

**Issue**: Quality assessment currently subjective (internal team)  
**Impact**: 🟡 **Low-Medium** - Potential bias

**Mitigation**:
- ✅ Multiple evaluators (3-person team)
- 🔄 Quantitative metrics (BLEU, perplexity)
- 📋 UAT (Week 9) - external validation
- 📋 Professional review (mental health expert)

---

## Challenge 4: Resource Management 💰

**Issue**: Model requires ~4GB RAM, GPU upgrade expensive  
**Impact**: 🟡 **Medium** - Limits scalability

**Options**:
- Keep CPU: $50/mo (baseline speed)
- GPU (T4): $300/mo (5-10x faster)
- Smaller Model: $50/mo (2-3x faster)
- Hybrid: $100/mo (balanced)

**Decision**: Week 7 cost-benefit analysis

---

## Design Guidance

**Visual**: 
- 4 challenge boxes dengan severity indicators (🔴⚠️🟡)
- Timeline for mitigation strategies (✅🔄📋)
- Color coding: Red (high), Orange (medium), Yellow (low)

---

## Speaker Notes

"Ada 4 major challenges yang kami identify. Yang paling critical adalah response time—3 menit too slow untuk production. Strategy kami multi-layered: immediate fix dengan streaming dan quantization, medium-term consider VPS upgrade, long-term model distillation. Training data volume challenge akan addressed dengan real user conversations. Model evaluation akan lebih objective dengan UAT di Week 9. Resource management currently manageable, decision untuk GPU upgrade akan dibuat Week 7 berdasarkan cost-benefit analysis."
