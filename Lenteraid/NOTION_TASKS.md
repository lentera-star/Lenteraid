# 🎯 LENTERA - Sprint Task Database

> Copy this to Notion as a Database view

---

## Sprint 1 Tasks ✅ COMPLETED

| Task | Assignee | Category | Priority | Status | Due Date |
|------|----------|----------|----------|--------|----------|
| Setup Flutter project | Frontend | Setup | High | ✅ Done | Week 1 |
| Create login screen | Frontend | Frontend | High | ✅ Done | Week 1 |
| Create register screen | Frontend | Frontend | High | ✅ Done | Week 1 |
| Setup FastAPI | Backend | Backend | High | ✅ Done | Week 1 |
| Setup Docker Compose | Backend | DevOps | High | ✅ Done | Week 1 |
| Integrate Ollama | Backend | AI | High | ✅ Done | Week 1 |
| Design database schema | Database | Database | High | ✅ Done | Week 1 |
| Create Supabase tables | Database | Database | High | ✅ Done | Week 1 |
| Implement RLS policies | Database | Security | High | ✅ Done | Week 1 |
| Setup Supabase Auth | Database | Auth | High | ✅ Done | Week 2 |
| Build home screen | Frontend | Frontend | Medium | ✅ Done | Week 2 |
| Create all data models | Frontend | Frontend | Medium | ✅ Done | Week 2 |

---

## Sprint 2 Tasks 🔨 IN PROGRESS

| Task | Assignee | Category | Priority | Status | Progress | Due Date |
|------|----------|----------|----------|--------|----------|----------|
| Implement Provider state mgmt | Frontend | State | High | 🔨 In Progress | 50% | Week 3 |
| Build AI chat screen | Frontend | Frontend | High | ✅ Done | 100% | Week 3 |
| Build voice call screen | Frontend | Frontend | High | ✅ Done | 100% | Week 3 |
| Build mood tracker screens | Frontend | Frontend | Medium | ✅ Done | 100% | Week 3 |
| Build psychologist screens | Frontend | Frontend | Medium | ✅ Done | 100% | Week 3 |
| **Install Whisper STT** | **Backend** | **AI** | **🚨 Critical** | **⏸️ Not Started** | **0%** | **Week 3** |
| **Install TTS (Piper)** | **Backend** | **AI** | **🚨 Critical** | **⏸️ Not Started** | **0%** | **Week 3** |
| **Complete voice pipeline** | **Backend** | **AI** | **🚨 Critical** | **⏸️ Not Started** | **0%** | **Week 3** |
| Complete chat API endpoint | Backend | API | High | 🔨 In Progress | 30% | Week 3 |
| Implement WebSocket | Backend | API | High | 🔨 In Progress | 30% | Week 4 |
| Enable Supabase Realtime | Database | Database | High | 🔨 In Progress | 60% | Week 3 |
| Create integration tests | Database | Testing | Medium | 🔨 In Progress | 40% | Week 4 |
| **Review Ollama prompts** | **Backend** | **AI/ML** | **High** | **⏸️ Not Started** | **0%** | **Week 3** |
| **Test different LLM models** | **Backend** | **AI/ML** | **High** | **⏸️ Not Started** | **0%** | **Week 3** |
| **Optimize prompts for mental health** | **Backend** | **AI/ML** | **Medium** | **⏸️ Not Started** | **0%** | **Week 4** |
| **Research RAG architectures** | **Backend** | **AI/ML** | **Medium** | **⏸️ Not Started** | **0%** | **Week 4** |
| **Plan fine-tuning strategy** | **Backend** | **AI/ML** | **Medium** | **⏸️ Not Started** | **0%** | **Week 4** |
| Connect frontend to APIs | Frontend | Integration | High | ⏸️ Blocked | 0% | Week 4 |
| Test voice call end-to-end | All | Testing | High | ⏸️ Blocked | 0% | Week 4 |

---

## Sprint 3 Tasks ⏸️ PLANNED

| Task | Assignee | Category | Priority | Status | Due Date |
|------|----------|----------|----------|--------|----------|
| Frontend-Backend integration | Frontend | Integration | High | ⏸️ Planned | Week 5 |
| WebSocket voice integration | Frontend | Integration | High | ⏸️ Planned | Week 5 |
| Add error handling | Backend | Backend | High | ⏸️ Planned | Week 5 |
| Add logging & monitoring | Backend | DevOps | Medium | ⏸️ Planned | Week 5 |
| API endpoint optimization | Backend | Backend | Medium | ⏸️ Planned | Week 5 |
| **Setup vector database** | **Backend** | **AI/ML** | **🚨 Critical** | **⏸️ Planned** | **Week 5** |
| **Create knowledge base** | **Backend** | **AI/ML** | **🚨 Critical** | **⏸️ Planned** | **Week 5** |
| **Implement document embedding** | **Backend** | **AI/ML** | **High** | **⏸️ Planned** | **Week 5** |
| **Build RAG retrieval pipeline** | **Backend** | **AI/ML** | **High** | **⏸️ Planned** | **Week 5** |
| **Integrate RAG with chat** | **Backend** | **AI/ML** | **High** | **⏸️ Planned** | **Week 5** |
| **Collect fine-tuning dataset** | **Backend** | **AI/ML** | **Medium** | **⏸️ Planned** | **Week 5** |
| **Fine-tune Ollama model** | **Backend** | **AI/ML** | **Medium** | **⏸️ Planned** | **Week 6** |
| **Evaluate model performance** | **Backend** | **AI/ML** | **Medium** | **⏸️ Planned** | **Week 6** |
| Performance optimization | All | Optimization | High | ⏸️ Planned | Week 5 |
| End-to-end testing | Database | Testing | High | ⏸️ Planned | Week 5 |
| Write API documentation | Database | Documentation | Medium | ⏸️ Planned | Week 5 |
| UI polish & animations | Frontend | Frontend | Medium | ⏸️ Planned | Week 6 |
| Bug fixes | All | Testing | High | ⏸️ Planned | Week 6 |
| Deployment preparation | All | DevOps | High | ⏸️ Planned | Week 6 |

---

## 🚨 Critical Path Items

> These tasks MUST be completed for project success

| Task | Owner | Blocks | Deadline | Notes |
|------|-------|--------|----------|-------|
| Whisper STT Integration | Backend | Voice call, Frontend integration | End Week 3 | **URGENT - Start immediately** |
| TTS Integration | Backend | Voice call, Frontend integration | End Week 3 | **URGENT - Start immediately** |
| Voice Pipeline Complete | Backend | Sprint 2 completion | End Week 3 | Depends on STT + TTS |
| Chat API with Ollama | Backend | Frontend chat feature | End Week 3 | Partially done |
| LLM Prompt Optimization | Backend | Chat quality | End Week 4 | Improve AI responses |
| RAG Implementation | Backend | Advanced AI features | End Week 5 | Critical for contextual responses |
| Fine-tuning Setup | Backend | Specialized responses | Week 6 | Mental health domain expertise |
| API Integration | Frontend | All features working | End Week 4 | Blocked by backend |
| End-to-End Testing | All | Sprint 3, Deployment | Week 5 | Integration milestone |

---

## 📊 Progress by Category

| Category | Total Tasks | Completed | In Progress | Not Started | % Complete |
|----------|-------------|-----------|-------------|-------------|------------|
| Frontend | 18 | 16 | 2 | 0 | 89% |
| Backend + AI/ML | 22 | 4 | 2 | 16 | 18% |
| Database | 10 | 7 | 2 | 1 | 70% |
| Integration | 5 | 0 | 1 | 4 | 0% |
| Testing | 5 | 0 | 2 | 3 | 0% |
| **TOTAL** | **60** | **27** | **9** | **24** | **45%** |

---

## 🎯 Weekly Goals

### Week 3 (Current)
#### Frontend
- [ ] Complete Provider implementation
- [ ] Create API mock services
- [ ] Prepare WebSocket client code

#### Backend ⚠️ PRIORITY
- [ ] Install & test Whisper
- [ ] Install & test TTS
- [ ] Build voice pipeline prototype
- [ ] Complete Ollama chat integration
- [ ] Review existing Ollama prompts
- [ ] Test different models (llama2 vs phi vs mistral)
- [ ] Benchmark response quality
- [ ] Research RAG architectures

---

### Week 4
#### Frontend
- [ ] Connect all screens to backend APIs
- [ ] Implement error handling
- [ ] Add loading states

#### Backend
- [ ] Complete WebSocket implementation
- [ ] Test voice pipeline with frontend
- [ ] Add logging & monitoring
- [ ] Optimize mental health prompts
- [ ] Design conversation flow templates
- [ ] Evaluate vector database options
- [ ] Plan fine-tuning dataset collection

---

### Week 5-6 (Sprint 3)
#### Frontend
- [ ] Integration testing
- [ ] UI polish & animations
- [ ] Performance optimization

#### Backend ⚠️ PRIORITY
- [ ] Production configuration
- [ ] Error handling
- [ ] API documentation
- [ ] Setup vector database (Chroma)
- [ ] Build mental health knowledge base
- [ ] Implement RAG pipeline
- [ ] Collect & prepare fine-tuning dataset
- [ ] Fine-tune model for mental health

---

## 🏷️ Tag/Label Guide for Notion

Use these tags in your Notion database:

**Priority Tags**:
- 🚨 Critical
- 🔴 High
- 🟡 Medium
- 🟢 Low

**Status Tags**:
- ✅ Done
- 🔨 In Progress
- ⏸️ Not Started
- 🚫 Blocked
- ⏭️ Deferred

**Category Tags**:
- Frontend
- Backend
- Database
- Integration
- Testing
- DevOps
- Documentation
- AI
- Security

**Sprint Tags**:
- Sprint 1
- Sprint 2
- Sprint 3

---

## 📋 Kanban Board View (For Notion)

Suggested columns for Kanban view:

1. **Backlog** - All planned tasks
2. **Sprint Backlog** - Tasks for current sprint
3. **In Progress** - Currently being worked on
4. **In Review** - Code review / testing
5. **Blocked** - Cannot proceed
6. **Done** - Completed ✅

---

## 👥 Team View (For Notion)

Group tasks by assignee:

### Frontend Lead
- Total Tasks: 18
- Completed: 16 (89%)
- Current: Provider implementation, API prep

### Backend Lead
- Total Tasks: 24
- Completed: 4 (17%)
- Current: **Voice pipeline + AI/ML work (URGENT)**

### Database Lead
- Total Tasks: 10
- Completed: 7 (70%)
- Current: Realtime setup, testing

---

*Import this to Notion and create Database/Kanban/Timeline views*
