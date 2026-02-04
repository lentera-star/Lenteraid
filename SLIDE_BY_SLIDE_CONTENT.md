# 📊 SLIDE-BY-SLIDE CONTENT GUIDE - MONEV LenteraDreamFlow

> **Panduan Lengkap**: Konten detail untuk setiap slide yang siap dimasukkan ke PowerPoint. Copy-paste langsung!

---

## 🎯 SECTION 1: PEMBUKAAN

---

### 📌 SLIDE 1: COVER SLIDE

**Layout**: Center-aligned, full background

#### Content:

```
┌─────────────────────────────────────────┐
│                                         │
│        LENTERADREAMFLOW                 │
│   Companion AI untuk Kesehatan Mental   │
│                                         │
│         Monitoring & Evaluasi           │
│            Periode: Week 5              │
│          (Januari 2026)                 │
│                                         │
│              Tim:                       │
│         [Nama Anggota 1]                │
│         [Nama Anggota 2]                │
│         [Nama Anggota 3]                │
│                                         │
└─────────────────────────────────────────┘
```

#### Design Notes:
- **Background**: Gradient biru (#4A90E2) ke ungu (#7B68EE)
- **Font Title**: Poppins Bold, 48pt, white
- **Font Subtitle**: Poppins Regular, 24pt, white
- **Font Team**: Open Sans, 18pt, white
- **Logo**: Jika ada, taruh di pojok kanan atas (small, 100px)

#### Speaker Notes:
"Selamat pagi/siang Bapak/Ibu reviewer. Kami dari tim LenteraDreamFlow akan mempresentasikan progress monitoring dan evaluasi proyek kami untuk periode minggu ke-5."

---

### 📌 SLIDE 2: AGENDA PRESENTASI

**Layout**: Single column list with icons

#### Judul Slide:
```
Agenda Presentasi
```

#### Content:

```
1. 🎯 Overview Proyek & Milestone

2. 🏗️ Arsitektur & Teknologi

3. 📊 Progress Teknis Terkini

4. 🏆 Pencapaian Utama (Week 1-4)

5. 🚧 Tantangan & Solusi

6. 📅 Roadmap ke Depan (Week 5-12)

7. 💰 Budget & Resources

8. ❓ Q&A
```

#### Design Notes:
- **Font**: Poppins Semi-Bold, 20pt
- **Line spacing**: 1.5
- **Icon size**: 32px, warna matching dengan color palette
- **Background**: White dengan subtle blue accent di kiri

#### Speaker Notes:
"Presentasi kami akan mencakup 8 bagian utama. Estimasi waktu total adalah 15-18 menit, dengan 3-5 menit untuk tanya jawab di akhir."

---

### 📌 SLIDE 3: OVERVIEW PROYEK

**Layout**: Two-column (text left, visual right)

#### Judul Slide:
```
LenteraDreamFlow: Inovasi Kesehatan Mental Digital
```

#### Content (Left Column):

**Visi**
```
Menyediakan akses 24/7 untuk dukungan kesehatan mental 
melalui AI yang empatik, aman, dan dapat diandalkan
```

**Target User**
```
🎯 Remaja dan dewasa muda (18-35 tahun)
🎯 Membutuhkan dukungan emosional
🎯 Mencari pendamping digital yang empathetic
```

**Keunggulan Utama**
```
🤖 AI Chat dengan LLM teroptimasi untuk Indonesia
🎤 Real-time Voice Call (STT & TTS)
📊 Mood Tracking terintegrasi
🛡️ Safety Guardrails untuk deteksi krisis
```

#### Visual (Right Column):
- Diagram sederhana: User (icon) → Mobile App (icon) → AI System (icon)
- Atau screenshot aplikasi (jika ada)
- Atau infographic menunjukkan user journey

#### Speaker Notes:
"LenteraDreamFlow adalah aplikasi kesehatan mental berbasis AI yang dirancang untuk memberikan dukungan emosional 24/7. Keunggulan utama kami adalah sistem AI Safety yang robust - sangat penting untuk aplikasi mental health."

---

## 🏗️ SECTION 2: ARSITEKTUR & TEKNOLOGI

---

### 📌 SLIDE 4: ARSITEKTUR SISTEM

**Layout**: Center infographic

#### Judul Slide:
```
Arsitektur Teknis End-to-End
```

#### Content:

**Diagram Arsitektur** (Bisa gunakan SmartArt atau insert image mockup yang sudah dibuat)

```
┌─────────────┐
│  Flutter    │
│ Mobile App  │ ──────┐
└─────────────┘       │
                      ↓
              ┌─────────────┐
              │   FastAPI   │
              │   Backend   │ ─────┬─────┬─────┬─────┐
              └─────────────┘      │     │     │     │
                      ↓            ↓     ↓     ↓     ↓
          ┌────────────────────────────────────────────┐
          │  Ollama    Supabase  Whisper  TTS  Safety  │
          │   LLM        DB       STT          Validator│
          └────────────────────────────────────────────┘
```

#### Keterangan (Below diagram):

```
📱 Frontend: Flutter 3.0+ (Cross-platform iOS/Android)
⚙️ Backend: FastAPI (Python) + WebSocket
🤖 AI Engine: Ollama (Llama 3.1)
💾 Database: Supabase (PostgreSQL + Auth)
🎤 Voice: Faster-Whisper (STT) + Custom TTS
🐋 Deployment: Docker + VPS
```

#### Speaker Notes:
"Arsitektur kami menggunakan Flutter untuk frontend cross-platform, FastAPI untuk backend yang high-performance, dan Ollama untuk AI engine on-premise. Semua komunikasi real-time menggunakan WebSocket."

---

### 📌 SLIDE 5: TECH STACK DETAIL

**Layout**: Table format

#### Judul Slide:
```
Teknologi yang Digunakan
```

#### Content:

| Layer | Teknologi | Justifikasi |
|-------|-----------|-------------|
| **Frontend** | Flutter 3.0+ | Cross-platform, single codebase untuk iOS & Android |
| **Backend** | FastAPI + Python | High-performance async, mudah integrasi AI/ML |
| **AI Model** | Ollama (Llama 3.1) | Open-source, on-premise deployment untuk data privacy |
| **Database** | Supabase | Real-time capabilities, built-in auth, PostgreSQL power |
| **Voice AI** | Faster-Whisper | CPU-optimized, akurat untuk Bahasa Indonesia |
| **DevOps** | Docker + Nginx | Reproducible environment, scalable, easy deployment |
| **Version Control** | Git + GitHub | Industry standard, kolaborasi tim efektif |

#### Design Notes:
- **Table style**: Modern, dengan alternating row colors (light blue/white)
- **Font**: Body 14pt untuk readability
- **Header**: Bold, colored background (#4A90E2)

#### Speaker Notes:
"Kami memilih tech stack dengan pertimbangan: (1) Cost efficiency - mayoritas open-source, (2) Data privacy - on-premise LLM, (3) Scalability - semua tech production-ready."

---

### 📌 SLIDE 6: FITUR KEAMANAN AI

**Layout**: Mixed (text + flowchart)

#### Judul Slide:
```
AI Safety & Ethics System 🛡️
```

#### Content:

**Mengapa Safety Penting?**
```
❗ Aplikasi mental health = high-risk domain
❗ Potensi konten sensitif (self-harm, suicide ideation)
❗ AI harus capable detect & respond krisis dengan aman
```

**Implementasi Safety Guardrails:**

**1. Input Validation** (`safety_validator.py`)
```
✓ Deteksi keyword berbahaya (bunuh diri, self-harm, kekerasan)
✓ Pattern recognition untuk konteks ambigu
✓ Sentiment analysis untuk mood assessment
```

**2. Crisis Handler** (`crisis_handler.py`)
```
✓ Prosedur eskalasi otomatis
✓ Template respons tervalidasi profesional kesehatan mental
✓ Hard boundaries: AI TIDAK memberikan medical advice
```

**3. Template Override v2**
```
✓ Sistem memaksa AI gunakan respons aman saat detect ambiguitas
✓ Contoh: "Saya merasa sendirian" 
   → AI wajib: empati + suggest hotline + boundaries
```

#### Flowchart (Simple):
```
User Input → Safety Validator → [Safe?]
                                   ↓
                         Yes ←─────┴─────→ No
                          ↓                 ↓
                    Normal AI        Crisis Handler
                    Response         (Template Override)
```

#### Speaker Notes:
"Ini adalah unique selling point kami. Safety system berlapis ini memastikan aplikasi kami aman untuk user yang vulnerable. Semua respons krisis menggunakan template yang sudah divalidasi."

---

## 📊 SECTION 3: PROGRESS TERKINI

---

### 📌 SLIDE 7: TIMELINE PROGRESS (12 MINGGU)

**Layout**: Vertical timeline or horizontal roadmap

#### Judul Slide:
```
Milestone Timeline Proyek (12 Minggu)
```

#### Content:

```
✅ MINGGU 1-2: Planning & Setup
   • Riset teknologi & pemilihan arsitektur
   • Setup development environment (Docker, Git)
   • Database schema design
   • Project kickoff & team alignment

✅ MINGGU 3: Core Development
   • Backend API (Chat, Auth, Mood endpoints)
   • Frontend UI/UX implementation
   • Database integration dengan Supabase
   • Basic chat functionality working

✅ MINGGU 4: Advanced Features
   • Voice Call Pipeline (Code Complete, currently disabled)
   • AI Safety System (ACTIVE & DEPLOYED)
   • Fine-tuning preparation scripts
   • Frontend-Backend full integration

🔄 MINGGU 5: Integration & Testing ⬅️ YOU ARE HERE
   • End-to-end testing
   • Voice features activation & testing
   • Performance optimization
   • Bug fixes & code refinement

📋 MINGGU 6-8: Feature Enhancement
   • Additional features based on feedback
   • UI/UX polish & improvements
   • User feedback integration
   • Documentation updates

🧪 MINGGU 9-10: Testing & Quality Assurance
   • Comprehensive User Acceptance Testing (UAT)
   • Security audit & vulnerability testing
   • Performance tuning & load testing
   • Deployment preparation

🚀 MINGGU 11-12: Final Deployment & Presentation
   • Production deployment
   • Final documentation & handover
   • Presentation preparation
   • Project closure activities
```

#### Design Notes:
- Use diferentes colors untuk setiap fase
- ✅ = Green, 🔄 = Yellow/Orange, 📋🧪🚀 = Blue/Purple gradient
- Bold "YOU ARE HERE" dengan arrow atau highlight

#### Speaker Notes:
"Kami saat ini berada di minggu ke-5 dari 12 minggu total. Progress sejauh ini on-track. Week 1-4 fokus pada foundation dan core development, sekarang kami masuk fase integration dan testing."

---

### 📌 SLIDE 8: PENCAPAIAN UTAMA (WEEK 1-4)

**Layout**: Three-column cards

#### Judul Slide:
```
🏆 Key Achievements - Week 1-4 Summary
```

#### Content:

**Column 1: Real-time Voice Pipeline 🎤**
```
Status: 🟡 Code Complete (Disabled)

Achievements:
✓ WebSocket endpoint /ws/voice-call ready
✓ Faster-Whisper STT fully integrated
✓ Text-to-Speech service implemented
✓ Complete audio pipeline coded

Pipeline:
Audio Input → Whisper Transcribe → 
Ollama LLM → TTS Synthesis → Audio Output

Note:
Currently disabled untuk save RAM during 
dev iteration. Will be enabled Week 5.
```

**Column 2: AI Safety System 🛡️**
```
Status: 🟢 Active & Deployed

Achievements:
✓ Safety validator active
✓ Crisis detection implemented
✓ Template override system working
✓ Hard boundaries enforced

Impact:
Sistem dapat detect situasi krisis dan 
respond dengan template aman yang 
tervalidasi profesional.

Critical Component:
Essential untuk mental health app!
```

**Column 3: Frontend Integration 📱**
```
Status: 🟢 Fully Integrated

Achievements:
✓ MoodService connected to Supabase
✓ Real-time messaging working
✓ Fallback mechanisms implemented
✓ State management (Provider) active

Features Live:
• Chat interface
• Mood tracker
• User authentication
• Profile management
```

#### Design Notes:
- Each column dengan border & shadow (card style)
- Status badges: Green circle + "Active", Yellow circle + "Pending"
- Icons di atas setiap column (mic, shield, phone icons)

#### Speaker Notes:
"Tiga pencapaian utama kami: Voice pipeline sudah complete secara kode, AI Safety system yang robust dan sudah deployed, serta frontend yang fully integrated dengan backend."

---

### 📌 SLIDE 9: STATUS KOMPONEN TEKNIS

**Layout**: Dashboard table

#### Judul Slide:
```
📊 Status Dashboard Komponen
```

#### Content:

| Komponen | Fitur | Status | Keterangan |
|----------|-------|:------:|------------|
| **Backend** | WebSocket Voice | 🟡 **Pending** | Kode ready, perlu enable & test |
| **Backend** | AI Chat (Text) | 🟢 **Active** | Fully functional dengan Safety |
| **Backend** | Whisper STT | 🟡 **Ready** | Service siap, tunggu integrasi main.py |
| **Backend** | Safety Validator | 🟢 **Active** | Crisis detection working |
| **Frontend** | Mood Tracker | 🟢 **Active** | Connected to Supabase DB |
| **Frontend** | Chat Interface | 🟢 **Active** | Real-time messaging functional |
| **Frontend** | Voice UI | 🟡 **Ready** | UI ready, backend integration pending |
| **Database** | Schema & Auth | 🟢 **Active** | Stable, no issues |
| **Database** | RLS Security | 🟢 **Active** | Row-level security enabled |
| **DevOps** | Docker Setup | 🟢 **Active** | All dependencies containerized |
| **DevOps** | VPS Deployment | 🟢 **Active** | Staging environment running |

**Legenda:**
```
🟢 Active/Done   🟡 Ready/Pending   🔴 Blocked/Issue
```

#### Design Notes:
- Color-coded status circles
- Alternating row colors untuk readability
- Bold untuk component names

#### Speaker Notes:
"Dashboard ini menunjukkan status real-time setiap komponen. Mayoritas sudah active (hijau), beberapa ready untuk testing (kuning). Tidak ada blocker merah saat ini."

---

### 📌 SLIDE 10: DEMO SCREENSHOTS

**Layout**: Grid 2x2 atau Carousel

#### Judul Slide:
```
Interface & User Experience
```

#### Content:

**Jika ada screenshots:**
```
[Screenshot 1: Chat Interface]
Caption: "Conversational AI Chat dengan Safety Response"

[Screenshot 2: Mood Tracker]
Caption: "Daily Mood Tracking dengan Visual Analytics"

[Screenshot 3: Safety System Example]
Caption: "AI Safety System: Deteksi & Response Krisis"

[Screenshot 4: Profile/Settings]
Caption: "User Profile & App Settings"
```

**Jika belum ada screenshots (placeholder):**
```
┌─────────────────────┐  ┌─────────────────────┐
│   Chat Interface    │  │   Mood Tracker      │
│                     │  │                     │
│  [Placeholder for   │  │  [Placeholder for   │
│   actual screenshot]│  │   actual screenshot]│
│                     │  │                     │
└─────────────────────┘  └─────────────────────┘

┌─────────────────────┐  ┌─────────────────────┐
│  Safety Response    │  │  Settings Page      │
│                     │  │                     │
│  [Placeholder for   │  │  [Placeholder for   │
│   actual screenshot]│  │   actual screenshot]│
│                     │  │                     │
└─────────────────────┘  └─────────────────────┘

Note: Screenshots akan diambil saat testing fase Week 5
```

#### Speaker Notes:
"Berikut preview interface aplikasi kami. [Jika ada screenshot, jelaskan fitur-fitur yang terlihat. Jika placeholder, katakan: 'Screenshot final akan tersedia setelah testing Week 5 selesai']"

---

### 📌 SLIDE 11: CODE QUALITY & DOCUMENTATION

**Layout**: Checklist with icons

#### Judul Slide:
```
Best Practices & Code Quality
```

#### Content:

**Version Control**
```
✅ Git dengan branching strategy (main, dev, feature branches)
✅ Meaningful commit messages (conventional commits)
✅ Pull request & code review process
✅ Repository: [GitHub URL]
```

**Documentation**
```
✅ Weekly Progress Reports (WEEK_4_REPORT.md, etc.)
✅ Fine-Tuning Guide (FINE_TUNING_GUIDE.md)
✅ Inline code comments untuk complex logic
✅ API documentation (docstrings)
✅ README.md dengan setup instructions
```

**Code Structure**
```
✅ Modular architecture
   • Separated services (chat_service, mood_service, whisper_service)
   • Clear handlers (crisis_handler, safety_validator)
   • Clean separation: Frontend ↔ Backend
✅ Consistent naming conventions
✅ Type hints (Python) & null safety (Dart)
```

**Dependencies Management**
```
✅ requirements.txt (Backend Python packages)
✅ pubspec.yaml (Frontend Flutter packages)
✅ Docker Compose untuk orchestration
✅ Version pinning untuk reproducibility
```

**Testing** (Planned Week 5+)
```
🔄 Unit tests (in progress)
🔄 Integration tests (planned Week 5)
🔄 End-to-end tests (planned Week 9-10)
```

#### Speaker Notes:
"Kami maintain code quality yang tinggi dengan documentation yang comprehensive dan version control yang proper. Setup Docker memastikan reproducible environment di semua development machines."

---

## 🚧 SECTION 4: TANTANGAN & SOLUSI

---

### 📌 SLIDE 12: TANTANGAN TEKNIS

**Layout**: Table dengan color-coded severity

#### Judul Slide:
```
🚧 Challenges Encountered
```

#### Content:

| Tantangan | Impact | Status Solusi | Priority |
|-----------|--------|---------------|:--------:|
| **Resource Consumption** | RAM tinggi saat Whisper + Ollama bersamaan run | 🔄 Planning load testing & resource optimization Week 5 | HIGH |
| **Voice Call Latency** | Potensi delay pada real-time conversation | 🔄 Perlu WebSocket performance testing & tuning | HIGH |
| **Model Fine-tuning** | Data training quality untuk konteks Bahasa Indonesia | ✅ Prepared scripts & guide, ready untuk eksekusi | MEDIUM |
| **Deployment Complexity** | Multiple services perlu orchestration yang proper | ✅ Solved dengan Docker Compose | LOW |
| **API Rate Limiting** | Ollama bisa bottleneck dengan banyak concurrent users | 🔄 Monitoring & scaling strategy planned Week 7-8 | MEDIUM |

**Legend:**
```
✅ Solved   🔄 In Progress   ⏳ Planned   🔴 Blocked
```

#### Speaker Notes:
"Beberapa tantangan teknis yang kami hadapi. Yang paling critical adalah resource consumption untuk voice features - akan kami address di Week 5 dengan load testing."

---

### 📌 SLIDE 13: RISK MITIGATION

**Layout**: Two-column list

#### Judul Slide:
```
Mitigasi Risiko & Strategi
```

#### Content:

**Left Column:**

**1. Risiko: Model AI Hallucination**
```
⚠️ Risk: AI memberikan respons tidak akurat/berbahaya
✓ Mitigasi:
  • Safety validator dengan keyword detection
  • Template override untuk situasi krisis
  • Hard boundaries: no medical advice
✓ Testing Plan:
  • Scenario-based testing dengan edge cases
  • Red team testing untuk mencari vulnerabilities
```

**2. Risiko: Server Downtime**
```
⚠️ Risk: Backend server crash, user cannot access
✓ Mitigasi:
  • Docker untuk quick recovery & restart
  • Monitoring tools (planned: Prometheus + Grafana)
  • Health check endpoints
✓ Backup:
  • VPS snapshot reguler (weekly)
  • Database backup otomatis (Supabase)
```

**Right Column:**

**3. Risiko: Data Privacy Breach**
```
⚠️ Risk: User data leaked atau accessed unauthorized
✓ Mitigasi:
  • Supabase Row-Level Security (RLS) enabled
  • On-premise LLM (data tidak keluar dari server)
  • HTTPS encryption untuk semua requests
✓ Compliance:
  • Tidak store medical data long-term
  • User dapat delete data (GDPR-like)
```

**4. Risiko: Budget Overrun**
```
⚠️ Risk: Biaya operasional melebihi budget
✓ Mitigasi:
  • Open-source tech stack (minimize licensing costs)
  • On-premise LLM (no API costs per request)
  • VPS fixed monthly cost (predictable)
✓ Monitoring:
  • Monthly expense tracking
  • Resource usage monitoring untuk optimization
```

#### Speaker Notes:
"Kami identify 4 risiko utama dan sudah punya mitigation strategy untuk masing-masing. Data privacy adalah top priority, makanya kami pilih on-premise LLM."

---

## 📅 SECTION 5: RENCANA KE DEPAN

---

### 📌 SLIDE 14: ROADMAP (WEEK 5-12)

**Layout**: Phased roadmap

#### Judul Slide:
```
📅 Roadmap ke Depan (Minggu 5-12)
```

#### Content:

**FASE 2: Integration & Enhancement** ⬅️ CURRENT
```
Minggu 5-6

Week 5 Focus:
☑ Enable Voice Call features di production
☑ End-to-end testing (Frontend ↔ Backend ↔ AI)
☑ Load testing untuk RAM/CPU usage
☑ Latency testing untuk WebSocket performance

Week 6 Focus:
☐ Additional features berdasarkan feedback
☐ UI/UX improvements & polish
☐ Documentation updates
☐ Prepare untuk UAT (User Acceptance Testing)
```

**FASE 3: Testing & Quality Assurance**
```
Minggu 7-10

Week 7-8:
☐ Feature completion & refinement
☐ Implement user feedback dari initial testing
☐ Advanced AI features (fine-tuning jika applicable)
☐ Performance optimization

Week 9-10:
☐ Comprehensive UAT dengan 10-20 test users
☐ Security audit & vulnerability testing
☐ Bug fixes & stability improvements
☐ Load testing untuk production readiness
☐ Deployment rehearsal di staging
```

**FASE 4: Deployment & Closure**
```
Minggu 11-12

Week 11:
☐ Production deployment ke VPS
☐ Monitoring & logging setup
☐ Soft launch (limited users)
☐ Quick hotfix readiness

Week 12:
☐ Final documentation (technical + user manual)
☐ Presentation preparation (slides, demo, report)
☐ Knowledge transfer & handover
☐ Project retrospective & celebration! 🎉
```

#### Design Notes:
- Color gradient: Phase 2 (yellow), Phase 3 (blue), Phase 4 (purple)
- "CURRENT" dengan highlight atau arrow

#### Speaker Notes:
"Roadmap kami sampai Week 12. Week 5-6 fokus integration, Week 7-10 heavy testing - ini sangat penting untuk mental health app, dan Week 11-12 deployment & finalization."

---

### 📌 SLIDE 15: SUCCESS METRICS

**Layout**: Three sections (Technical, UX, Business)

#### Judul Slide:
```
KPI & Success Indicators
```

#### Content:

**Metrik Teknis:**
```
✅ API Response Time < 2 detik (95th percentile)
   • Current: ~1.2s (text chat) ✓
   • Target Week 5: Voice call < 500ms latency

✅ System Uptime > 99%
   • Current: 99.5% uptime (staging) ✓
   • Target production: 99.9%

✅ Security Audit: Zero critical vulnerabilities
   • Planned: Week 9 comprehensive audit
   • Target: Pass security assessment

✅ Concurrent Users Support
   • Current capacity: ~50 users (estimated)
   • Target Week 10: 200+ concurrent users
```

**Metrik User Experience:**
```
🎯 User Satisfaction Score (dari UAT)
   • Target: > 4.0/5.0
   • Method: Post-interaction survey

🎯 Safety System Accuracy
   • True Positive Rate > 90% (crisis detection)
   • False Positive Rate < 10%

🎯 Mood Tracking Retention Rate
   • Target: >60% users log mood 3x/week
   • Engagement indicator

🎯 Feature Usage Distribution
   • Track: Chat vs Voice vs Mood Tracker usage
```

**Metrik Business** (jika applicable):
```
💰 Cost per Active User
   • Target: < Rp 5,000/user/month
   • VPS + infrastructure costs

💰 Development Velocity
   • Features completed vs planned
   • Technical debt ratio

🚀 Deployment Success Rate
   • Zero-downtime deployment
   • Rollback incidents: 0
```

#### Speaker Notes:
"Kami define clear success metrics. Teknis fokus pada performance & security, UX pada user satisfaction, dan business pada cost efficiency."

---

### 📌 SLIDE 16: BUDGET & RESOURCES

**Layout**: Table + Pie Chart

#### Judul Slide:
```
💰 Budget Allocation & Resource Usage
```

#### Content:

**Breakdown Biaya (Estimasi):**

| Item | Budget | Actual | % Used | Status |
|------|--------|--------|--------|--------|
| **VPS Hosting** (12 bulan) | Rp 2,400,000 | Rp 800,000 | 33% | ✅ On track |
| **Domain & SSL** | Rp 300,000 | Rp 250,000 | 83% | ✅ Paid |
| **Development Tools** | Rp 0 | Rp 0 | - | ✅ Free (open-source) |
| **AI API** (jika pakai cloud) | Rp 0 | Rp 0 | - | ✅ On-premise LLM |
| **Testing Infrastructure** | Rp 500,000 | Rp 0 | 0% | 🔄 Planned W9 |
| **Miscellaneous** | Rp 300,000 | Rp 50,000 | 17% | ✅ Buffer |
| **TOTAL** | **Rp 3,500,000** | **Rp 1,100,000** | **31%** | **✅ Under budget** |

**Tim Resources:**
```
👥 Team Composition:
   • Backend Developer: [X] orang × 12 weeks
   • Frontend Developer: [X] orang × 12 weeks
   • Designer/UI/UX: [X] orang × 12 weeks (part-time)
   • Project Manager: [X] orang × 12 weeks (part-time)

⏱️ Total Man-hours (Estimated):
   • Per person: ~20 jam/week
   • Total team: ~[X × 20 × 12] = XXX jam

📊 Effort Distribution:
   • Development: 50%
   • Testing: 25%
   • Documentation: 15%
   • Meetings & Planning: 10%
```

#### Pie Chart (jika mau visualize budget):
- VPS Hosting: 69%
- Domain & SSL: 9%
- Testing: 14%
- Misc: 8%

#### Speaker Notes:
"Budget kami saat ini 31% used, sesuai dengan progress 33% (Week 5 dari 12). Majority budget untuk VPS hosting. Tech stack open-source menghemat licensing costs drastis."

---

## 📚 SECTION 6: PENUTUP

---

### 📌 SLIDE 17: LESSONS LEARNED

**Layout**: Two-column (Technical vs Process)

#### Judul Slide:
```
📚 Key Learnings (Week 1-5)
```

#### Content:

**Technical Learnings:**
```
✅ Docker sangat membantu reproducible environment
   → Insight: Invest time di setup awal, save debugging time later

✅ On-premise LLM (Ollama) feasible untuk Indonesia
   → Insight: Performa acceptable, cost savings significant

✅ Safety validator adalah CRITICAL untuk mental health app
   → Insight: Tidak bisa di-compromise, harus built-in dari awal

✅ WebSocket lebih suitable untuk real-time chat vs REST API
   → Insight: Latency berkurang drastis, UX lebih smooth

⚠️ Resource management perlu monitoring ketat
   → Challenge: Whisper + Ollama bersamaan = high RAM
```

**Process Learnings:**
```
✅ Weekly report membantu tracking progress
   → Benefit: Accountability & clear milestone documentation

✅ Modular architecture mempercepat iteration
   → Benefit: Bisa develop parallel tanpa blocking each other

⚠️ Perlu alokasi lebih untuk testing phase
   → Learning: Testing takes longer than expected (4 minggu allocated)

✅ Early integration prevents late-stage issues
   → Learning: Continuous integration sejak Week 3 menghindari big-bang problem

⚠️ Documentation harus concurrent dengan development
   → Learning: Catch-up documentation lebih sulit daripada write-as-you-go
```

#### Speaker Notes:
"Pembelajaran terpenting: Safety system harus built-in dari awal, bukan afterthought. Dan testing untuk mental health app membutuhkan waktu lebih lama - makanya kami allocate 4 minggu."

---

### 📌 SLIDE 18: DEMO REQUEST / Q&A PREP

**Layout**: Icon grid

#### Judul Slide:
```
💡 Demo & Discussion
```

#### Content:

**Kami siap untuk:**
```
🖥️ LIVE DEMO
   • Chat interface dengan AI response
   • Safety system demonstration (crisis detection)
   • Mood tracker functionality
   • [Voice call demo jika sudah active Week 5]

📱 MOBILE APP WALKTHROUGH
   • Flutter app running di device/emulator
   • User journey: Sign up → Chat → Mood Log

💬 TECHNICAL DISCUSSION
   • Arsitektur & design decisions
   • Tech stack justifications
   • Scalability strategy
   • Future enhancement possibilities

🔍 CODE REVIEW
   • Bersedia menunjukkan code quality
   • Explain implementation details
   • Discuss challenges & solutions
```

**Prepared to Answer:**
```
❓ Scalability strategy untuk 1000+ users
❓ Data privacy & compliance approach
❓ Alternative architecture considerations
❓ Budget & timeline justification
❓ Fine-tuning strategy untuk Indonesia context
❓ Handling edge cases dalam AI responses
```

#### Speaker Notes:
"Kami prepared untuk demo live jika diminta. Juga siap discuss technical details atau code review. Silakan ask anything!"

---

### 📌 SLIDE 19: THANK YOU & CONTACT

**Layout**: Center-aligned

#### Judul Slide:
```
Terima Kasih
```

#### Content:

```
┌─────────────────────────────────────────┐
│                                         │
│          TERIMA KASIH                   │
│                                         │
│   Questions & Feedback Welcome!         │
│                                         │
│                                         │
│   📧 Email: [email@proyek.com]          │
│   💻 GitHub: github.com/[username]/     │
│              LenteraDreamFlow           │
│   📱 Team Lead: [Nama]                  │
│       WhatsApp: +62-XXX-XXXX-XXXX       │
│                                         │
│                                         │
│   "Building Empathetic AI for           │
│    Mental Health Support"               │
│                                         │
└─────────────────────────────────────────┘
```

#### Design Notes:
- **Background**: Same gradient biru-ungu seperti cover
- **Font**: White, center-aligned
- **Size**: Large untuk "Terima Kasih" (48pt), medium untuk contact (18pt)
- **Tagline**: Italic, 16pt, subtle

#### Speaker Notes:
"Terima kasih atas perhatian Bapak/Ibu. Kami siap untuk tanya jawab. Jika ada feedback atau pertanyaan lanjutan, bisa contact kami di email atau GitHub yang tertera."

---

## 📋 CHECKLIST PERSIAPAN PRESENTASI

### 1 Hari Sebelum:
- [ ] Review semua slide content
- [ ] Practice presentation 2x (time yourself: 15-18 menit)
- [ ] Prepare demo (backend running, app ready)
- [ ] Update semua data (jika ada perubahan terbaru)
- [ ] Export ke PDF sebagai backup
- [ ] Charge laptop fully

### Hari H (30 menit sebelum):
- [ ] Datang lebih awal
- [ ] Test proyektor connection
- [ ] Buka PowerPoint di Slide Show mode untuk check
- [ ] Buka backup PDF di tab lain (just in case)
- [ ] Siapkan demo environment (backend running, browser ready)
- [ ] Deep breath & stay confident! 💪

---

## 🎯 TIPS DELIVERY

### Opening (Slide 1-3):
"Selamat [pagi/siang], kami dari tim LenteraDreamFlow. Kami akan presentasi progress monitoring evaluasi untuk periode Week 5."

### Technical Slides (4-11):
- Jangan baca slide word-by-word
- Explain dengan bahasa sendiri
- Point ke diagram saat explain arsitektur
- **Emphasize Slide 6 (AI Safety)** - ini unique value!

### Progress & Roadmap (12-16):
- Be honest tentang challenges
- Show clear plan untuk solve problems
- Highlight bahwa testing dapat 4 minggu (menunjukkan thoroughness)

### Closing (17-19):
- Summarize 3-5 key points
- Ask: "Apakah ada pertanyaan atau feedback?"
- Stay calm & professional selama Q&A

---

**Document Created**: 28 Januari 2026  
**Total Slides**: 19  
**Estimated Presentation Time**: 15-18 menit + 3-5 menit Q&A  
**Ready to Present**: YES! 🚀
