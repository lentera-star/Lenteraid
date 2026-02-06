# 🎯 LENTERA - Sprint Task Database

> Copy this to Notion as a Database view
> **Current Status**: Week 6 of 8 | 75% Complete | Maintenance Mode

```
Project Progress: [███████████████████████████████░░░░░░░░░] 75%
```

---

## Sprint 1 Tasks ✅ COMPLETED (Week 1-2)

| Task | Assignee | Category | Priority | Status | Completion | 
|------|----------|----------|----------|--------|------------|
| Setup Flutter project | Frontend | Setup | High | ✅ Done | 100% |
| Create login screen | Frontend | Frontend | High | ✅ Done | 100% |
| Create register screen | Frontend | Frontend | High | ✅ Done | 100% |
| Setup FastAPI | Backend | Backend | High | ✅ Done | 100% |
| Setup Docker Compose | Backend | DevOps | High | ✅ Done | 100% |
| Integrate Ollama | Backend | AI | High | ✅ Done | 100% |
| Design database schema | Database | Database | High | ✅ Done | 100% |
| Create Supabase tables (5 tables) | Database | Database | High | ✅ Done | 100% |
| Implement RLS policies (12 policies) | Database | Security | High | ✅ Done | 100% |
| Setup Supabase Auth | Database | Auth | High | ✅ Done | 100% |
| Build home screen | Frontend | Frontend | Medium | ✅ Done | 100% |
| Create all data models (6 models) | Frontend | Frontend | Medium | ✅ Done | 100% |
| Theme system (Dark/Light) | Frontend | UI/UX | Medium | ✅ Done | 100% |

**Sprint 1 Summary**: 13 tasks | 100% completion | 3,500 LOC | 47 commits

---

## Sprint 2 Tasks ✅ COMPLETED (Week 3-4)

| Task | Assignee | Category | Priority | Status | Completion | Notes |
|------|----------|----------|----------|--------|------------|-------|
| Build all 16 screens | Frontend | Frontend | High | ✅ Done | 100% | 1,526 lines (home_page.dart) |
| AI chat screen + markdown | Frontend | Frontend | High | ✅ Done | 100% | 449 lines |
| Voice call screen + controls | Frontend | Frontend | High | ✅ Done | 100% | 279 lines |
| Mood tracker + calendar | Frontend | Frontend | High | ✅ Done | 100% | Calendar view working |
| Psychologist screens | Frontend | Frontend | High | ✅ Done | 100% | List + booking |
| Gamification system | Frontend | Frontend | Medium | ✅ Done | 100% | Poin, level, avatar shop, trivia |
| All 9 services (CRUD) | Frontend | Services | High | ✅ Done | 100% | MoodService, PsychologistService, etc |
| Provider state management | Frontend | State | High | ✅ Done | 80% | Partial implementation |
| FastAPI endpoints (3) | Backend | API | High | ✅ Done | 60% | Skeleton implemented |
| Ollama service class | Backend | AI | High | ✅ Done | 100% | 147 lines, mental health prompts |
| Docker Compose config | Backend | DevOps | High | ✅ Done | 100% | Backend + Ollama services |
| Sample data seeding | Database | Database | Medium | ✅ Done | 100% | Psychologist, avatars |
| Database testing | Database | Testing | Medium | ✅ Done | 80% | Manual testing done |

**Sprint 2 Summary**: 13 tasks | 95% completion | 12,000 LOC | 83 commits

---

## Maintenance Period (Week 5-6) 🔨 IN PROGRESS

**Mode**: Study Break - 2 hours/week maintenance

| Task | Assignee | Category | Priority | Status | Completion | Notes |
|------|----------|----------|----------|--------|------------|-------|
| Update README progress badges | Frontend | Docs | Medium | ✅ Done | 100% | Status badges added |
| Create Sprint 3 plan document | All | Planning | High | ✅ Done | 100% | SPRINT3_PLAN.md |
| GitHub issues for Sprint 3 | All | Planning | High | ✅ Done | 100% | 12 issues created |
| Code comments (5-10 functions) | Frontend | Docs | Low | ✅ Done | 100% | Complex functions documented |
| Update NOTION_PLANNING.md | All | Docs | Medium | ✅ Done | 100% | Timeline updated to 8 weeks |
| Create testing strategy doc | Database | Docs | Medium | 🔨 In Progress | 50% | Test scenarios defined |
| Create deployment checklist | Backend | DevOps | Medium | ⏸️ Planned | 0% | Week 6 target |
| Architecture diagram update | All | Docs | Low | ⏸️ Planned | 0% | Optional |
| GitHub project board | All | Planning | Medium | ✅ Done | 100% | Sprint 3 tasks added |

**Maintenance Summary**: 9 tasks | 65% completion | Strategic visibility maintenance

---

## Sprint 3 Tasks 🚀 PLANNED (Week 7-8)

### Week 7: Backend Integration (CRITICAL PRIORITY)

#### P0 Tasks (Must Have)

| Task | Assignee | Category | Priority | Estimate | Status | Dependency |
|------|----------|----------|----------|----------|--------|------------|
| **Install Whisper STT** | **Backend** | **AI** | **🚨 P0** | **2h** | **⏸️ Planned** | None |
| **Configure Whisper API** | **Backend** | **AI** | **🚨 P0** | **1h** | **⏸️ Planned** | Whisper installed |
| **Create /api/stt endpoint** | **Backend** | **API** | **🚨 P0** | **3h** | **⏸️ Planned** | Whisper ready |
| **Install Piper TTS** | **Backend** | **AI** | **🚨 P0** | **2h** | **⏸️ Planned** | None |
| **Create /api/tts endpoint** | **Backend** | **API** | **🚨 P0** | **3h** | **⏸️ Planned** | Piper installed |
| **Complete WebSocket /ws/voice-call** | **Backend** | **API** | **🚨 P0** | **4h** | **⏸️ Planned** | STT + TTS ready |
| **Test voice pipeline end-to-end** | **Backend** | **Testing** | **🚨 P0** | **2h** | **⏸️ Planned** | WebSocket ready |
| **Connect /api/chat to Ollama** | **Backend** | **AI** | **🚨 P0** | **3h** | **⏸️ Planned** | Ollama working |
| **Implement conversation context** | **Backend** | **AI** | **🚨 P0** | **2h** | **⏸️ Planned** | Chat endpoint |
| **Add streaming response support** | **Backend** | **API** | **🚨 P0** | **3h** | **⏸️ Planned** | Chat working |
| **Create ChatService (frontend)** | **Frontend** | **Services** | **🚨 P0** | **2h** | **⏸️ Planned** | None |
| **Replace mock AI responses** | **Frontend** | **Integration** | **🚨 P0** | **3h** | **⏸️ Planned** | ChatService ready |
| **Enable Supabase Realtime** | **Database** | **Database** | **🚨 P0** | **2h** | **⏸️ Planned** | None |
| **Frontend: Subscribe to messages** | **Frontend** | **Integration** | **🚨 P0** | **3h** | **⏸️ Planned** | Realtime enabled |
| **Add loading states (all APIs)** | **Frontend** | **UI/UX** | **🚨 P0** | **3h** | **⏸️ Planned** | None |
| **Create ErrorWidget component** | **Frontend** | **UI/UX** | **🚨 P0** | **2h** | **⏸️ Planned** | None |
| **Implement retry mechanisms** | **Frontend** | **Integration** | **🚨 P0** | **2h** | **⏸️ Planned** | Error handling |

**Week 7 Total**: 17 P0 tasks | ~40 hours estimated

---

#### P1 Tasks (Should Have)

| Task | Assignee | Category | Priority | Estimate | Status |
|------|----------|----------|----------|----------|--------|
| Add caching (psychologist list) | Frontend | Performance | P1 | 1h | ⏸️ Planned |
| Implement pagination (chat history) | Frontend | Performance | P1 | 2h | ⏸️ Planned |
| Optimize image loading | Frontend | Performance | P1 | 1h | ⏸️ Planned |
| Profile slow screens | Frontend | Performance | P1 | 2h | ⏸️ Planned |
| Add comprehensive error logging | Backend | DevOps | P1 | 2h | ⏸️ Planned |
| Backend health monitoring | Backend | DevOps | P1 | 2h | ⏸️ Planned |

**Week 7 P1**: 6 tasks | ~10 hours estimated

---

### Week 8: Polish & Deploy

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
... (rest of the file remains same)
