# SLIDE 5: Fine-Tuning Process

---

## Layout: Process Flow (4 Steps)

### Judul
🔬 Technical Process - How We Did It

---

## Step 1: Data Preparation 📚

- **Dataset Size**: 500+ curated conversation examples
- **Focus Areas**: 
  - Empathetic responses untuk berbagai kondisi emosional
  - Indonesian cultural context & language nuances
  - Safety-compliant crisis handling
  - Multi-turn conversation coherence
- **Format**: Llama 3.1 instruction fine-tuning format
- **Quality Control**: Manual review + validation oleh tim

---

## Step 2: Training Configuration ⚙️

```
Model: meta-llama/Llama-3.1-8B

Training Parameters:
  Learning Rate: 2e-5
  Batch Size: 4 (with gradient accumulation)
  Epochs: 3
  Warmup Steps: 100
  Optimizer: AdamW
  
Results:
  Training Loss: 0.847 (excellent convergence)
  Validation Loss: 0.912 (minimal overfitting)
  Training Time: ~8 hours (GPU)
```

---

## Step 3: Deployment Architecture 🚀

**Deployment Flow**:
- Flutter Mobile App → HTTPS Request
- FastAPI Backend → Safety Validation → Forward to Ollama
- **VPS - Ollama**: Fine-tuned Model Llama 3.1-8B (~4.7GB quantized)
- Generate Response → Safety Post-Processing → Send to User

---

## Step 4: Validation Testing 🧪

- **Internal Testing**: 25+ scenarios covering:
  - Emotional support responses
  - Crisis detection & handling
  - Cultural appropriateness
  - Conversation flow & coherence
- **Success Rate**: **100%** pass rate
- **Quality Scoring**: Manual assessment by team (avg 4.3/5)

---

## Design Guidance

**Visual**: 
- 4 boxes/sections untuk each step
- Flowchart untuk deployment architecture
- Code block dengan monospace font untuk training config

**Layout**: 2x2 grid atau vertical flow

---

## Speaker Notes

"Process fine-tuning kami sangat structured. Dimulai dengan kurasi 500+ conversation examples, kemudian training dengan configuration optimal—learning rate 2e-5, 3 epochs. Deployment menggunakan Ollama di VPS yang sudah kami punya, fully integrated dengan FastAPI backend. Validation testing dengan 25+ scenarios semuanya passed dengan success rate 100%."
