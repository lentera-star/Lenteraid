# 🎯 LENTERA Project Planning

> 💡 **Project**: AI-Powered Mental Health Counseling App  
> 📅 **Timeline**: 8 weeks (4 active sprints)  
> 👥 **Team**: 4 members  
> 📊 **Current Progress**: 75% overall | Week 6 of 8

**Status**: 🎓 Maintenance Mode (Exam Period) → Resumes Week 7

```
Progress: [███████████████████████████████░░░░░░░░░] 75%
```

---

## 👥 Team Structure

### 📱 Member 1: Frontend Lead
**Role**: Flutter Developer  
**Focus**: UI/UX, State Management, Mobile App  
**Sprint 1-2 Contribution**: 16 screens, 6 models, 9 services (~75% codebase)

### ⚙️ Member 2: Backend Lead
**Role**: Python/FastAPI Developer  
**Focus**: REST APIs, WebSocket, Voice Pipeline (STT/TTS)  
**Sprint 1-2 Contribution**: FastAPI setup, Ollama integration, Docker config

### 🗄️ Member 3: Database Lead
**Role**: Full-Stack Support  
**Focus**: Supabase, Testing, Integration, Deployment  
**Sprint 1-2 Contribution**: 5 tables, 12 RLS policies, sample data

### 🤖 Member 4: AI Engineer
**Role**: ML/AI Specialist  
**Focus**: RAG, Fine-tuning, LLM Optimization, Prompt Engineering  
**Sprint 1-2 Contribution**: Mental health prompts, model research

---

## 📋 Sprint Overview (8 Weeks Total)

### ✅ Sprint 1: Foundation (Week 1-2) - COMPLETED 100%
- [x] Flutter screens & UI components (10 screens)
- [x] FastAPI setup with Docker
- [x] Supabase database schema (5 tables, 12 RLS policies)
- [x] Authentication implementation (login/register/verify)
- [x] Basic AI integration (Ollama service)
- [x] Theme system (Dark/Light mode)

**Metrics**: 3,500 lines | 47 commits | 18 files

---

### ✅ Sprint 2: Core Features (Week 3-4) - COMPLETED 100%
- [x] Frontend: ALL 16 screens implemented
  - [x] Home page (1,526 lines!)
  - [x] AI Chat dengan markdown support
  - [x] Voice call UI dengan controls
  - [x] Mood tracker + calendar
  - [x] Psychologist booking
  - [x] Gamification (avatar shop, trivia, poin system)
- [x] Backend: FastAPI skeleton + Ollama integration
- [x] Database: All models & services (6 models, 9 services)
- [x] Data layer: Full CRUD operations

**Metrics**: 12,000 lines | 83 commits | 44 files

---

### 📚 Maintenance Period (Week 5-6) - IN PROGRESS 65%

**Mode**: Study Break - Minimal effort maintenance (~2 hours/week)

**Activities**:
- [x] Documentation updates
- [x] Sprint 3 detailed planning
- [x] GitHub project board setup (12 issues created)
- [x] Code comments added
- [x] README progress badges
- [ ] Testing strategy document
- [ ] Deployment checklist

**Strategy**: Keep project visible dengan automated commits & planning docs

**Metrics Target**: 4-6 commits | 3-5 documentation files

---

### 🚀 Sprint 3: Integration & Launch (Week 7-8) - PLANNED

**Mode**: Post-Exam Full Sprint

#### Week 7: Backend Integration (CRITICAL)
- [ ] **Voice AI Pipeline** 🚨 PRIORITY
  - [ ] Whisper STT integration (Speech-to-Text)
  - [ ] Piper TTS integration (Text-to-Speech)
  - [ ] WebSocket bidirectional audio streaming
  - [ ] End-to-end voice call testing
  
- [ ] **Chat API Integration**
  - [ ] Connect frontend to Ollama backend
  - [ ] Conversation context/memory implementation
  - [ ] Real AI responses (replace mock data)
  - [ ] Streaming response support
  
- [ ] **Real-time Chat Updates**
  - [ ] Supabase Realtime configuration
  - [ ] Frontend subscriptions
  - [ ] Live message sync
  
- [ ] **Error Handling**
  - [ ] Loading states untuk all API calls
  - [ ] Error widgets & messages
  - [ ] Retry mechanisms
  - [ ] Offline mode detection

#### Week 8: Polish & Deploy
- [ ] Bug fixes dari integration testing
- [ ] Performance optimization (< 2s response time)
- [ ] E2E testing all features
- [ ] Beta APK build
- [ ] Deployment preparation
- [ ] User documentation
- [ ] Demo video (3-5 min)

**Target Metrics**: 100% P0 tasks | < 5 critical bugs | Beta ready

---

## 📱 Frontend Lead - Detailed Tasks

### Sprint 1 ✅ COMPLETED (100%)

**Authentication UI**
- [x] Login screen with email/password
- [x] Register screen with validation
- [x] Splash screen & onboarding
- [x] Email verification flow

**Core Screens**
- [x] Home page with bottom navigation
- [x] Profile screen with settings
- [x] Edit profile functionality

**Models & Services**
- [x] User model
- [x] Mood entry model
- [x] Psychologist model
- [x] Conversation model
- [x] Booking model
- [x] Avatar model

### Sprint 2 🔨 IN PROGRESS (60%)

**Main Features**
- [x] AI Chat screen with message UI
- [x] Voice call screen interface
- [x] Video call screen interface
- [x] Mood tracker entry screen
- [x] Mood insights detail screen
- [x] Psychologist listing screen
- [x] Booking management screen
- [x] Payment methods screen
- [x] Avatar shop screen
- [x] Daily trivia screen

**State Management**
- [x] Provider setup (partial)
- [ ] Connect all services to Provider
- [ ] Real-time state updates

**API Integration**
- [ ] Connect to backend REST API
- [ ] Handle API errors
- [ ] Loading states
- [ ] Offline support

### Sprint 3 ⏸️ PLANNED

**Integration**
- [ ] WebSocket for voice call
- [ ] Real-time chat updates
- [ ] Supabase Realtime subscriptions

**Polish**
- [ ] Performance optimization
- [ ] Animation smoothness
- [ ] UI/UX refinements
- [ ] Accessibility improvements

**Testing**
- [ ] Widget tests
- [ ] Integration tests
- [ ] User acceptance testing

---

## ⚙️ Backend Lead - Detailed Tasks

### Sprint 1 ✅ COMPLETED (100%)

**Infrastructure**
- [x] FastAPI project setup
- [x] Docker configuration
- [x] Docker Compose for multi-service
- [x] CORS middleware
- [x] Health check endpoints

**AI Foundation**
- [x] Ollama service integration
- [x] Model management (list, load)
- [x] Chat completion API
- [x] Mental health system prompts

**API Endpoints**
- [x] `/health` - Health check
- [x] `/api/chat` - Basic chat endpoint

### Sprint 2 🔨 IN PROGRESS (10%) ⚠️ BEHIND SCHEDULE

**Voice AI Pipeline** 🚨 URGENT
- [ ] Install & configure Whisper (STT)
- [ ] Implement `/api/stt` endpoint
- [ ] Install & configure TTS (Piper/XTTS)
- [ ] Implement `/api/tts` endpoint
- [ ] Create voice pipeline: Audio → STT → LLM → TTS → Audio

**WebSocket**
- [ ] Complete `/ws/voice-call` implementation
- [ ] Handle audio streaming
- [ ] Bidirectional communication
- [ ] Connection management

**AI Enhancement**
- [ ] Integrate Ollama with chat endpoint
- [ ] Add conversation context/memory
- [ ] Implement streaming responses
- [ ] Mood analysis with LLM

### Sprint 3 ⏸️ PLANNED

**Production Readiness**
- [ ] Environment configuration
- [ ] Error handling & logging
- [ ] Rate limiting
- [ ] API documentation (Swagger)
- [ ] Performance monitoring
- [ ] API endpoint optimization

---

## 🤖 AI Engineer - Detailed Tasks

### Sprint 1 ⏸️ NOT STARTED (0%)
*(New role - joining in Sprint 2)*

### Sprint 2 🔨 IN PROGRESS (0%)

**LLM Optimization**
- [ ] Review & optimize Ollama prompts
- [ ] Test different models (llama2, phi, mistral)
- [ ] Benchmark response quality
- [ ] Optimize model parameters

**Prompt Engineering**
- [ ] Refine mental health system prompts
- [ ] Create specialized prompts for mood analysis
- [ ] Design conversation flow templates
- [ ] Test prompt effectiveness

**Research & Planning**
- [ ] Research RAG architectures for mental health domain
- [ ] Evaluate vector databases (Chroma, Pinecone, Qdrant)
- [ ] Plan fine-tuning strategy
- [ ] Document AI architecture

### Sprint 3 ⏸️ PLANNED

**RAG Implementation** 🚨 PRIORITY
- [ ] Setup vector database (Chroma recommended)
- [ ] Create mental health knowledge base
- [ ] Implement document embedding (OpenAI/Cohere)
- [ ] Build retrieval mechanism
- [ ] Integrate RAG into chat pipeline
- [ ] Test context relevance

**Fine-tuning**
- [ ] Collect mental health conversation dataset
- [ ] Prepare training data (format, clean)
- [ ] Fine-tune Ollama model for mental health
- [ ] Evaluate fine-tuned model performance
- [ ] A/B test: base model vs fine-tuned

**Advanced AI Features**
- [ ] Implement conversation summarization
- [ ] Build emotion detection from text
- [ ] Create safety filters (crisis detection)
- [ ] Recommendation engine for resources

---

## 🗄️ Database Lead - Detailed Tasks

### Sprint 1 ✅ COMPLETED (100%)

**Database Schema**
- [x] `users` table with auth reference
- [x] `psychologists` table
- [x] `bookings` table with relationships
- [x] `mood_entries` table
- [x] `conversations` table
- [x] `messages` table
- [x] Indexes for performance
- [x] Foreign key constraints

**Security**
- [x] Row Level Security (RLS) policies
- [x] User data isolation
- [x] Service role configuration

**Data**
- [x] Sample psychologists data
- [x] Test bookings
- [x] TypeScript type definitions

### Sprint 2 🔨 IN PROGRESS (70%)

**Authentication**
- [x] Supabase Auth setup
- [x] Email/password authentication
- [x] Email verification
- [x] Password reset
- [x] Flutter integration (`supabase_auth_manager.dart`)

**Real-time** 🔨 IN PROGRESS
- [ ] Enable Realtime on `messages` table
- [ ] Enable Realtime on `mood_entries` table
- [ ] Configure replica identity
- [ ] Test real-time subscriptions

**Testing**
- [ ] Create integration test examples
- [ ] Document API usage patterns
- [ ] Test data sync scenarios

### Sprint 3 ⏸️ PLANNED

**Testing & Documentation**
- [ ] End-to-end test scripts
- [ ] API documentation
- [ ] Database migration guide
- [ ] Deployment checklist

**Performance**
- [ ] Query optimization
- [ ] Index tuning
- [ ] Load testing
- [ ] Backup strategy

---

## 🚨 Critical Blockers & Priorities

### 🔴 HIGH PRIORITY (This Week)

> ⚠️ **Backend Voice Pipeline**  
> **Owner**: Backend Lead  
> **Deadline**: End of Week 3  
> **Blocks**: Frontend voice call integration, Sprint 2 completion

**Tasks**:
1. Install Whisper: `pip install openai-whisper`
2. Implement STT endpoint
3. Install TTS: `pip install piper-tts` (recommended)
4. Implement TTS endpoint
5. Connect pipeline: WebSocket → STT → Ollama → TTS → WebSocket
6. Test end-to-end audio flow

---

### 🟡 MEDIUM PRIORITY (Next Week)

> 🔗 **API Integration**  
> **Owner**: Frontend Lead + Backend Lead  
> **Dependencies**: Backend chat API must be complete

**Tasks**:
1. Backend: Complete Ollama chat integration
2. Frontend: Implement API service layer
3. Test chat flow end-to-end
4. Handle errors & edge cases

---

> 📡 **Real-time Features**  
> **Owner**: Database Lead + Frontend Lead

**Tasks**:
1. Database: Enable Supabase Realtime
2. Frontend: Implement Realtime subscriptions
3. Test live updates for chat & mood

---

## 📊 Progress Dashboard

### Overall Project Progress
- **Total**: 65% complete
- **Sprint 1**: ✅ 100% (All tasks done)
- **Sprint 2**: 🔨 47% (Backend lagging)
- **Sprint 3**: ⏸️ 0% (Not started)

### Team Progress

| Role | Progress | Status | Notes |
|------|----------|--------|-------|
| Frontend | 75% | 🟢 Ahead | UI complete, waiting for backend |
| Backend | 45% | 🔴 Behind | Voice features critical |
| Database | 80% | 🟢 Ahead | Solid foundation ready |
| AI Engineer | 0% | 🟡 New | Starting Sprint 2, RAG in Sprint 3 |

### Sprint 2 Progress by Task

| Task | Owner | Status | Progress |
|------|-------|--------|----------|
| UI Screens | Frontend | ✅ Done | 100% |
| Provider Setup | Frontend | 🔨 In Progress | 50% |
| Voice Pipeline | Backend | ⏸️ Not Started | 0% |
| Chat API | Backend | 🔨 In Progress | 30% |
| WebSocket | Backend | 🔨 Skeleton Only | 30% |
| Realtime Setup | Database | 🔨 In Progress | 60% |
| Auth Integration | Database | ✅ Done | 100% |

---

## 📅 Weekly Schedule

### Week 1-2 ✅ COMPLETED
- Sprint 1 Planning & Execution
- Foundation setup
- Basic implementations

### Week 3 (Current) 🔨 IN PROGRESS
**Monday**: Sprint 2 planning
**Tuesday-Thursday**: Development
- Frontend: Provider + API integration prep
- Backend: **PRIORITY** - Whisper + TTS integration
- Database: Realtime setup
- AI Engineer: Prompt optimization, model testing

**Friday**: Sprint review & standup

### Week 4
**Monday-Wednesday**: Integration development
- Backend: Complete voice pipeline
- Frontend: Connect to APIs
- Database: Testing & documentation

**Thursday-Friday**: Integration testing

### Week 5-6
**Sprint 3**: Polish, optimization, deployment prep

---

## 🎯 Success Metrics

### Sprint 2 Goals (Must Complete)
- [ ] Voice call works end-to-end (user speaks → AI responds)
- [ ] Chat AI functional with Ollama
- [ ] Real-time chat updates working
- [ ] All screens connected to backend APIs

### Sprint 3 Goals
- [ ] App fully functional (all features working)
- [ ] Performance acceptable (< 2s response time)
- [ ] Zero critical bugs
- [ ] Deployment ready

---

## 💼 Daily Standup Template

Use this format for async updates:

```
**Yesterday**:
- [What you completed]

**Today**:
- [What you're working on]

**Blockers**:
- [Any issues or dependencies]
```

---

## 🔗 Quick Links

### Documentation
- [Team Plan](TEAM_PLAN.md)
- [Git Strategy](GIT_STRATEGY.md)
- [Progress Report](PROGRESS_REPORT.md)
- [Architecture](architecture.md)

### Development
- **Frontend**: `cd LenteraDreamFlow && flutter run`
- **Backend**: `docker-compose up -d`
- **Database**: [Supabase Dashboard](https://supabase.com)

### Resources
- [Flutter Docs](https://flutter.dev/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Supabase Docs](https://supabase.com/docs)
- [Ollama Models](https://ollama.ai/library)

---

## 📝 Notes

> 💡 **Tip**: Backend Lead should focus 100% on voice pipeline this week. This is the critical path blocker.

> ⚠️ **Risk**: If voice features are not complete by end of Week 4, Sprint 3 timeline is at risk.

> ✅ **Good News**: Frontend & Database are ahead of schedule and can support integration testing.

---

*Last Updated: 2025-12-17*  
*Overall Status: 🟢 On Track (with Backend catch-up required)*
