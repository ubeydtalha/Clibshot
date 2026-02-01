# 🤖 AI CONTEXT MANAGER — CLIPSHOT

> **Amaç:** 11 adet dokümantasyon dosyasını hiç unutmadan, sistematik şekilde implementation sırasında kullanmak.

---

## 📋 DOKÜMANTASYON INVENTORY

### Core Documentation Files (11 total)

| # | Dosya | Öncelik | İçerik | Kullanım Zamanı |
|---|-------|---------|--------|-----------------|
| 1 | `00_MASTER_AI_INSTRUCTION.md` | 🔴 CRITICAL | Ana mimari, prensipler, overview | Her zaman (tüm fázlarda) |
| 2 | `01_PROJECT_STRUCTURE.md` | 🔴 CRITICAL | Folder yapısı, dosya organizasyonu | Phase 1-2 (setup) |
| 3 | `02_PLUGIN_DEVELOPER_GUIDE.md` | 🟡 HIGH | Plugin development guide | Phase 4 (plugin system) |
| 4 | `03_BACKEND_ARCHITECTURE.md` | 🔴 CRITICAL | FastAPI, plugin manager, DB | Phase 2 (backend) |
| 5 | `04_FRONTEND_ARCHITECTURE.md` | 🔴 CRITICAL | Tauri, Vite, React, UI | Phase 3 (frontend) |
| 6 | `05_AI_RUNTIME_ABSTRACTION.md` | 🟡 HIGH | AI runtimes, model loading | Phase 5 (AI) |
| 7 | `06_SECURITY_SANDBOX.md` | 🟡 HIGH | Security, sandboxing, permissions | Phase 6 (security) |
| 8 | `07_MARKETPLACE_GITHUB.md` | 🟢 MEDIUM | Plugin marketplace, GitHub integration | Phase 4-7 (marketplace) |
| 9 | `08_LOCALIZATION.md` | 🟢 MEDIUM | i18n, multi-language support | Phase 7 (polish) |
| 10 | `10_NATIVE_PLUGIN_GUIDE.md` | 🟡 HIGH | Rust/C/C++ native plugins | Phase 4 (native plugins) |
| 11 | `11_RECOMMENDED_LIBRARIES.md` | 🔴 CRITICAL | Tech stack, dependencies | Phase 1-7 (tüm fázlar) |

---

## 🎯 PHASE-SPECIFIC DOCUMENTATION MAP

### Phase 1: Project Initialization
**Primary Docs:**
- ✅ `01_PROJECT_STRUCTURE.md` — Folder structure
- ✅ `11_RECOMMENDED_LIBRARIES.md` — Dependencies (Tauri, Vite, etc.)
- ✅ `00_MASTER_AI_INSTRUCTION.md` — Core principles

**Key Sections:**
- Project folder structure (01)
- Tauri setup (11)
- Vite configuration (11)
- Core principles (00)

**Action Items:**
```bash
# Read before starting:
1. 01_PROJECT_STRUCTURE.md (lines 1-300) — Full structure
2. 11_RECOMMENDED_LIBRARIES.md (lines 171-250) — Tauri + Vite
3. 00_MASTER_AI_INSTRUCTION.md (lines 82-110) — Principles
```

---

### Phase 2: Backend Infrastructure
**Primary Docs:**
- ✅ `03_BACKEND_ARCHITECTURE.md` — FastAPI architecture
- ✅ `02_PLUGIN_DEVELOPER_GUIDE.md` — Plugin interface
- ✅ `10_NATIVE_PLUGIN_GUIDE.md` — Native loader (Rust/PyO3)
- ✅ `11_RECOMMENDED_LIBRARIES.md` — Backend libs

**Key Sections:**
- FastAPI app structure (03)
- Plugin manager (03)
- Native plugin loader (10)
- Database models (03)
- API routes (03)

**Action Items:**
```bash
# Read before starting:
1. 03_BACKEND_ARCHITECTURE.md — Full file
2. 10_NATIVE_PLUGIN_GUIDE.md (lines 230-450) — Rust plugin + PyO3
3. 11_RECOMMENDED_LIBRARIES.md (Backend section) — FastAPI, SQLAlchemy
```

---

### Phase 3: Frontend Core
**Primary Docs:**
- ✅ `04_FRONTEND_ARCHITECTURE.md` — Tauri + Vite + React
- ✅ `01_PROJECT_STRUCTURE.md` — Frontend folder structure
- ✅ `11_RECOMMENDED_LIBRARIES.md` — Frontend libs

**Key Sections:**
- Tauri backend (Rust) (04, lines 58-200)
- Tauri commands (04)
- Vite configuration (04, lines 204-265)
- Tauri API wrappers (04, lines 267-358)
- React components (04, lines 486-560)
- State management (04, lines 637-720)

**Action Items:**
```bash
# Read before starting:
1. 04_FRONTEND_ARCHITECTURE.md — Full file (critical!)
2. 01_PROJECT_STRUCTURE.md (lines 72-200) — Frontend structure
3. 11_RECOMMENDED_LIBRARIES.md (Frontend section) — React, Tailwind
```

---

### Phase 4: Plugin System
**Primary Docs:**
- ✅ `02_PLUGIN_DEVELOPER_GUIDE.md` — Plugin development
- ✅ `10_NATIVE_PLUGIN_GUIDE.md` — Native plugins (Rust/C/C++)
- ✅ `03_BACKEND_ARCHITECTURE.md` — Plugin manager
- ✅ `07_MARKETPLACE_GITHUB.md` — Plugin marketplace

**Key Sections:**
- Plugin structure (02, lines 88-200)
- Plugin lifecycle (02)
- Rust plugin development (10, lines 380-650)
- C/C++ plugins (10, lines 700-1200)
- Native plugin ABI (10)
- Marketplace integration (07)

**Action Items:**
```bash
# Read before starting:
1. 02_PLUGIN_DEVELOPER_GUIDE.md — Full file
2. 10_NATIVE_PLUGIN_GUIDE.md — Full file (Rust/C/C++ sections)
3. 07_MARKETPLACE_GITHUB.md — Marketplace system
```

---

### Phase 5: AI Runtime
**Primary Docs:**
- ✅ `05_AI_RUNTIME_ABSTRACTION.md` — AI runtimes
- ✅ `03_BACKEND_ARCHITECTURE.md` — AI service integration
- ✅ `11_RECOMMENDED_LIBRARIES.md` — AI libs (ONNX, TFLite)

**Key Sections:**
- AI runtime abstraction (05)
- Model loading (05)
- Inference pipeline (05)
- GPU acceleration (05)
- Plugin AI integration (05)

**Action Items:**
```bash
# Read before starting:
1. 05_AI_RUNTIME_ABSTRACTION.md — Full file
2. 11_RECOMMENDED_LIBRARIES.md (AI section) — ONNX Runtime, TensorFlow Lite
```

---

### Phase 6: Security & Sandbox
**Primary Docs:**
- ✅ `06_SECURITY_SANDBOX.md` — Security architecture
- ✅ `04_FRONTEND_ARCHITECTURE.md` — Tauri security config
- ✅ `03_BACKEND_ARCHITECTURE.md` — Backend security

**Key Sections:**
- Plugin sandboxing (06)
- Resource limits (06)
- Permission system (06)
- Tauri security (04, lines 360-450)
- Process isolation (06)

**Action Items:**
```bash
# Read before starting:
1. 06_SECURITY_SANDBOX.md — Full file
2. 04_FRONTEND_ARCHITECTURE.md (Security section) — Tauri allowlist
```

---

### Phase 7: Polish & Production
**Primary Docs:**
- ✅ `08_LOCALIZATION.md` — i18n system
- ✅ `09_PERFORMANCE_MCP.md` — Performance optimization
- ✅ `04_FRONTEND_ARCHITECTURE.md` — Production build
- ✅ `07_MARKETPLACE_GITHUB.md` — Release process

**Key Sections:**
- i18n setup (08)
- Performance monitoring (09)
- MCP server (09)
- Production build (04)
- Release workflow (07)

**Action Items:**
```bash
# Read before starting:
1. 08_LOCALIZATION.md — Full file
2. 09_PERFORMANCE_MCP.md — Full file
3. 07_MARKETPLACE_GITHUB.md (Release section)
```

---

## 🔍 CONTEXT RETENTION STRATEGY

### Before Starting Each Phase
1. **Read phase-specific docs** (listed above)
2. **Extract key code patterns** from docs
3. **Create implementation checklist** from docs
4. **Reference docs** during implementation
5. **Update docs** if changes needed

### During Implementation
1. **Keep docs open** in separate tabs
2. **Copy code templates** from docs
3. **Follow naming conventions** from docs
4. **Check architecture diagrams** from docs
5. **Validate against principles** (00_MASTER_AI_INSTRUCTION.md)

### Document Update Protocol
If implementation requires doc changes:
1. **Note the change** in CHANGELOG.md
2. **Update the relevant doc** immediately
3. **Mark as [UPDATED]** in commit message
4. **Keep docs in sync** with code

---

## 📊 DOCUMENTATION CHECKLIST (Per Phase)

### Phase 1 Checklist
- [ ] Read `01_PROJECT_STRUCTURE.md` (full)
- [ ] Read `11_RECOMMENDED_LIBRARIES.md` (Tauri + Vite sections)
- [ ] Read `00_MASTER_AI_INSTRUCTION.md` (Principles)
- [ ] Reference `04_FRONTEND_ARCHITECTURE.md` (Vite config)

### Phase 2 Checklist
- [ ] Read `03_BACKEND_ARCHITECTURE.md` (full)
- [ ] Read `10_NATIVE_PLUGIN_GUIDE.md` (Rust + PyO3 sections)
- [ ] Read `02_PLUGIN_DEVELOPER_GUIDE.md` (Plugin interface)
- [ ] Reference `11_RECOMMENDED_LIBRARIES.md` (Backend libs)

### Phase 3 Checklist
- [ ] Read `04_FRONTEND_ARCHITECTURE.md` (FULL - CRITICAL!)
- [ ] Read `01_PROJECT_STRUCTURE.md` (Frontend structure)
- [ ] Reference `11_RECOMMENDED_LIBRARIES.md` (Frontend libs)

### Phase 4 Checklist
- [ ] Read `02_PLUGIN_DEVELOPER_GUIDE.md` (full)
- [ ] Read `10_NATIVE_PLUGIN_GUIDE.md` (full)
- [ ] Read `07_MARKETPLACE_GITHUB.md` (Marketplace)
- [ ] Reference `03_BACKEND_ARCHITECTURE.md` (Plugin manager)

### Phase 5 Checklist
- [ ] Read `05_AI_RUNTIME_ABSTRACTION.md` (full)
- [ ] Reference `11_RECOMMENDED_LIBRARIES.md` (AI libs)
- [ ] Reference `03_BACKEND_ARCHITECTURE.md` (AI service)

### Phase 6 Checklist
- [ ] Read `06_SECURITY_SANDBOX.md` (full)
- [ ] Read `04_FRONTEND_ARCHITECTURE.md` (Security section)
- [ ] Reference `03_BACKEND_ARCHITECTURE.md` (Backend security)

### Phase 7 Checklist
- [ ] Read `08_LOCALIZATION.md` (full)
- [ ] Read `09_PERFORMANCE_MCP.md` (full)
- [ ] Reference `07_MARKETPLACE_GITHUB.md` (Release)

---

## 🤝 COLLABORATION STRATEGY (Multi-Agent)

### Agent Specialization
If splitting work across multiple AI agents/chats:

**Agent 1: Backend Specialist**
- Focus: `03_BACKEND_ARCHITECTURE.md`
- Secondary: `10_NATIVE_PLUGIN_GUIDE.md`, `05_AI_RUNTIME_ABSTRACTION.md`
- Tasks: FastAPI, Plugin Manager, Native Loader, AI Runtime

**Agent 2: Frontend Specialist**
- Focus: `04_FRONTEND_ARCHITECTURE.md`
- Secondary: `01_PROJECT_STRUCTURE.md`, `11_RECOMMENDED_LIBRARIES.md`
- Tasks: Tauri, Vite, React, UI Components

**Agent 3: Plugin System Specialist**
- Focus: `02_PLUGIN_DEVELOPER_GUIDE.md`, `10_NATIVE_PLUGIN_GUIDE.md`
- Secondary: `07_MARKETPLACE_GITHUB.md`
- Tasks: Plugin SDK, Example Plugins, Marketplace

**Agent 4: Infrastructure Specialist**
- Focus: `06_SECURITY_SANDBOX.md`, `09_PERFORMANCE_MCP.md`
- Secondary: `08_LOCALIZATION.md`
- Tasks: Security, Performance, Localization, Deployment

### Merge Protocol
When merging work from multiple agents:
1. **Code Review:** Each agent reviews others' code
2. **Integration Test:** Run full integration tests
3. **Doc Sync:** Ensure all docs are updated
4. **Conflict Resolution:** Prioritize architecture docs

---

## 🚨 CRITICAL REMINDERS

### Always Keep in Mind
1. **Tauri + Vite Stack** (NOT Electron!) — `00_MASTER_AI_INSTRUCTION.md` #7
2. **Plugin-Driven Architecture** — Everything is a plugin
3. **Modular & Extensible** — Follow clean architecture
4. **Security First** — Sandbox, permissions, limits
5. **Documentation Parallel** — Write docs alongside code

### Never Forget
- [ ] `00_MASTER_AI_INSTRUCTION.md` — Core principles
- [ ] `01_PROJECT_STRUCTURE.md` — Folder structure
- [ ] `04_FRONTEND_ARCHITECTURE.md` — Tauri + Vite (CRITICAL!)
- [ ] `10_NATIVE_PLUGIN_GUIDE.md` — Native plugins (Rust/C/C++)
- [ ] `11_RECOMMENDED_LIBRARIES.md` — Tech stack

### Before ANY Code Change
Ask yourself:
1. Does this align with `00_MASTER_AI_INSTRUCTION.md` principles?
2. Does this follow the structure in `01_PROJECT_STRUCTURE.md`?
3. Is this documented in the relevant guide?
4. Have I read the phase-specific docs?

---

## 📝 USAGE EXAMPLE

### Starting Phase 2 (Backend)
```bash
# 1. Read docs (in order)
1. docs/00_MASTER_AI_INSTRUCTION.md (refresh principles)
2. docs/03_BACKEND_ARCHITECTURE.md (FULL READ)
3. docs/10_NATIVE_PLUGIN_GUIDE.md (Rust + PyO3 sections)
4. docs/11_RECOMMENDED_LIBRARIES.md (Backend section)

# 2. Extract code patterns
- FastAPI app structure (03)
- Plugin manager class (03)
- Native loader (10)

# 3. Create implementation checklist
- [ ] Setup FastAPI app
- [ ] Create plugin manager
- [ ] Implement native loader
- [ ] Setup DB models
- [ ] Create API routes

# 4. Start implementation
- Reference docs during coding
- Copy code templates from docs
- Follow naming conventions

# 5. Update docs if needed
- Note changes in CHANGELOG
- Update relevant docs
```

---

## 🎯 SUCCESS METRICS

### Documentation Coverage
- [ ] All 11 docs read before implementation
- [ ] Phase-specific docs referenced during coding
- [ ] Code matches doc patterns 95%+
- [ ] Docs updated when architecture changes

### Context Retention
- [ ] No "forgotten" docs
- [ ] All architecture decisions documented
- [ ] Code follows doc conventions
- [ ] Agent handoffs include full context

---

**Ready to start implementation with full documentation context!** 🚀

Every phase will reference this file to ensure NO documentation is forgotten.
