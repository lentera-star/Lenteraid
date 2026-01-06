# 🎯 LENTERA - Team Collaboration Plan

## 📋 Tim Overview

**Project**: LENTERA - AI-Powered Mental Health Counseling App
**Team Size**: 3 anggota
**Tech Stack**: Flutter, FastAPI, Supabase, Ollama, Docker

---

## 👥 Pembagian Tim & Tanggung Jawab

### 👤 **Member 1: Frontend Lead (Flutter Developer)**

**Focus Area**: Flutter App Development & UI/UX

#### 🎯 Tanggung Jawab Utama:
- ✅ Flutter screens & UI components
- ✅ State management implementation (Provider)
- ✅ Navigation & routing
- ✅ Integration dengan backend API (REST & WebSocket)
- ✅ Audio recording & playback (flutter_sound)
- ✅ Responsive design & dark mode
- ✅ Authentication flow UI

#### 📦 Tasks:
**Sprint 1: Core UI & Authentication**
- [ ] Setup authentication screens (Login, Register)
- [ ] Implement Provider state management
- [ ] Connect authentication dengan Supabase
- [ ] Test auth flow di Android emulator

**Sprint 2: Main Features**
- [ ] Implement Chat AI screen dengan real-time updates
- [ ] Voice call screen dengan WebSocket integration
- [ ] Mood tracker history & visualization
- [ ] Profile screen dengan settings

**Sprint 3: Polish & Testing**
- [ ] UI/UX refinements
- [ ] Dark mode testing
- [ ] Performance optimization
- [ ] Handle offline scenarios

---

### 👤 **Member 2: Backend Lead (Python/FastAPI Developer)**

**Focus Area**: Backend API, AI Integration & Services

#### 🎯 Tanggung Jawab Utama:
- ✅ FastAPI development & API endpoints
- ✅ Ollama LLM integration & prompt engineering
- ✅ Whisper STT (Speech-to-Text) integration
- ✅ TTS (Text-to-Speech) integration
- ✅ WebSocket untuk voice call
- ✅ Docker & deployment setup
- ✅ API documentation

#### 📦 Tasks:
**Sprint 1: Core Backend & AI Setup**
- [ ] Complete REST API endpoints (chat, mood analysis)
- [ ] Setup Ollama dengan model yang sesuai (phi/llama2)
- [ ] Implement conversation memory & context
- [ ] Test API endpoints dengan Postman/Thunder Client

**Sprint 2: Voice Features**
- [ ] Integrate Whisper untuk STT
- [ ] Integrate TTS (Piper/XTTS)
- [ ] Implement WebSocket untuk real-time voice call
- [ ] Test voice pipeline end-to-end

**Sprint 3: Advanced AI & Optimization**
- [ ] Implement RAG (Retrieval Augmented Generation)
- [ ] Fine-tune prompts untuk counseling context
- [ ] Optimize response time
- [ ] Add error handling & logging

---

### 👤 **Member 3: Full-Stack Support & Database Lead**

**Focus Area**: Supabase, Database, Integration & Testing

#### 🎯 Tanggung Jawab Utama:
- ✅ Supabase database schema & setup
- ✅ Database migrations & seeding
- ✅ Backend-Frontend integration testing
- ✅ Authentication implementation (Supabase Auth)
- ✅ Data synchronization
- ✅ Testing & QA
- ✅ Documentation

#### 📦 Tasks:
**Sprint 1: Database & Auth**
- [ ] Design & implement Supabase database schema
- [ ] Setup Row Level Security (RLS) policies
- [ ] Implement Supabase Auth di backend & frontend
- [ ] Create seed data untuk testing

**Sprint 2: Integration & Real-time**
- [ ] Setup Supabase Realtime untuk chat
- [ ] Integrate psychologist booking dengan database
- [ ] Implement mood entry storage & retrieval
- [ ] Test data synchronization

**Sprint 3: Testing & Documentation**
- [ ] End-to-end testing (Frontend + Backend + DB)
- [ ] Write API documentation
- [ ] Create deployment guide
- [ ] Performance testing

---

## 🌿 GitHub Branching Strategy

### Branch Structure

```
main (production-ready)
  ├── dev (development integration)
  │   ├── feature/frontend-auth
  │   ├── feature/frontend-chat-ui
  │   ├── feature/backend-ollama
  │   ├── feature/backend-voice
  │   ├── feature/supabase-schema
  │   ├── feature/supabase-auth
  │   ├── bugfix/xxx
  │   └── hotfix/xxx
  └── staging (pre-production testing)
```

### Branch Naming Convention

**Feature Branches** (untuk fitur baru):
- `feature/frontend-<nama-fitur>` - untuk Frontend Lead
  - Contoh: `feature/frontend-auth-ui`, `feature/frontend-chat-screen`
- `feature/backend-<nama-fitur>` - untuk Backend Lead
  - Contoh: `feature/backend-ollama-integration`, `feature/backend-websocket`
- `feature/database-<nama-fitur>` - untuk Database Lead
  - Contoh: `feature/database-schema`, `feature/database-rls`

**Bugfix Branches** (untuk bug fixes):
- `bugfix/<issue-number>-<deskripsi-singkat>`
  - Contoh: `bugfix/42-login-error`, `bugfix/mood-save-fail`

**Hotfix Branches** (untuk critical fixes di production):
- `hotfix/<deskripsi-critical-issue>`
  - Contoh: `hotfix/auth-crash`, `hotfix/api-timeout`

---

## 🔄 Git Workflow

### 1️⃣ Mulai Fitur Baru

```bash
# Update dev branch
git checkout dev
git pull origin dev

# Buat branch baru dari dev
git checkout -b feature/frontend-auth-ui

# Coding...
# Commit regularly dengan message yang jelas
git add .
git commit -m "feat: implement login screen UI"
```

### 2️⃣ Commit Message Convention

Gunakan **Conventional Commits**:

```
<type>(<scope>): <description>

[optional body]
```

**Types:**
- `feat`: Fitur baru
- `fix`: Bug fix
- `docs`: Dokumentasi
- `style`: Formatting, typo
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

**Contoh:**
```bash
git commit -m "feat(auth): implement login screen"
git commit -m "fix(backend): resolve Ollama connection timeout"
git commit -m "docs(readme): update setup instructions"
git commit -m "refactor(mood): extract mood card into component"
```

### 3️⃣ Push & Pull Request

```bash
# Push ke GitHub
git push origin feature/frontend-auth-ui

# Buat Pull Request di GitHub:
# - Base: dev
# - Compare: feature/frontend-auth-ui
# - Assign reviewers (minimal 1 anggota tim lain)
# - Add description: apa yang dibuat, screenshot jika UI
```

### 4️⃣ Code Review Process

1. **Reviewer checklist**:
   - ✅ Code runs without errors
   - ✅ Follows coding conventions
   - ✅ No hardcoded values
   - ✅ UI looks good (untuk frontend)
   - ✅ API works properly (untuk backend)
   
2. **Approve & Merge**:
   - Minimal 1 approval sebelum merge
   - Gunakan "Squash and merge" untuk clean history
   - Delete branch setelah merge

### 5️⃣ Deploy ke Staging & Production

```bash
# Merge dev ke staging untuk testing
dev → staging (weekly/bi-weekly)

# Setelah testing OK, merge ke main
staging → main (release)
```

---

## 📅 Sprint Planning (2 weeks per sprint)

### Sprint Rituals

**Daily Standup** (15 menit, async via Discord/Slack):
- Kemarin: apa yang dikerjakan?
- Hari ini: apa yang akan dikerjakan?
- Blocker: ada masalah?

**Sprint Planning** (awal sprint):
- Review tasks dari backlog
- Assign tasks ke masing-masing member
- Set sprint goals

**Sprint Review** (akhir sprint):
- Demo fitur yang selesai
- Collect feedback

**Sprint Retrospective** (akhir sprint):
- Apa yang berjalan baik?
- Apa yang perlu diperbaiki?
- Action items untuk sprint berikutnya

---

## 🛠️ Development Environment Setup

### Prerequisites untuk semua member:
- Git
- VS Code / Android Studio
- Docker Desktop (untuk Backend & Database Lead)

### Frontend Lead:
```bash
# Install Flutter
flutter doctor

# Run app
cd LenteraDreamFlow
flutter pub get
flutter run
```

### Backend Lead:
```bash
# Setup Docker
cd LenteraDreamFlow
docker-compose up -d

# Install Ollama model
docker exec -it lentera-ollama ollama pull phi

# Development
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Database Lead:
- Create Supabase project: https://supabase.com
- Setup environment variables
- Run migrations

---

## 📞 Communication Channels

### Recommended Tools:
- **Discord/Slack**: Daily standup & quick discussions
- **GitHub Issues**: Task tracking & bug reports
- **GitHub Projects**: Sprint board (Kanban)
- **Google Meet/Zoom**: Weekly sprint planning & review

### Guidelines:
- Response time: < 24 jam untuk non-urgent
- Use GitHub Issues untuk semua bugs/features
- Tag relevant members di PR comments
- Keep communication professional & constructive

---

## 🎯 Success Metrics

### Sprint Goals:
- ✅ All assigned tasks completed
- ✅ Code review rate > 90%
- ✅ Zero critical bugs in production
- ✅ Features demo-ready setiap akhir sprint

### Code Quality:
- ✅ No merge tanpa code review
- ✅ Clean commit history
- ✅ Documentation up-to-date
- ✅ Tests passing (jika ada)

---

## 📚 Resources

### Documentation:
- [Flutter Docs](https://flutter.dev/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Supabase Docs](https://supabase.com/docs)
- [Ollama Docs](https://ollama.ai)

### Learning:
- [Git Best Practices](https://www.conventionalcommits.org/)
- [Flutter State Management](https://docs.flutter.dev/data-and-backend/state-mgmt/intro)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

---

## 🚀 Quick Start Checklist

### First Week (Setup):
- [ ] All members: Clone repo
- [ ] All members: Setup development environment
- [ ] Frontend Lead: Run Flutter app
- [ ] Backend Lead: Setup Docker & Ollama
- [ ] Database Lead: Create Supabase project
- [ ] All members: Create first feature branch
- [ ] All members: Make first commit & PR
- [ ] Team: First standup meeting

### Ready to Go! 🎉

Selamat bekerja sama! Jika ada pertanyaan, diskusikan di channel tim atau buat GitHub Issue.
