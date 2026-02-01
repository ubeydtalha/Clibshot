# ClipShot Architecture

## Overview

ClipShot is a modular, plugin-driven platform for gaming clip capture and AI-powered editing. This document provides a high-level overview of the architecture.

## Technology Stack

### Frontend (Desktop App)
- **Tauri** - Desktop application framework
- **React 18** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS
- **Zustand** - State management
- **TanStack Query** - Data fetching

### Backend (API Server)
- **FastAPI** - Python web framework
- **Python 3.11+** - Programming language
- **PostgreSQL** - Primary database
- **Redis** - Caching and sessions
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation

### Native Components
- **Rust** - System-level operations
- **FFmpeg** - Video processing
- **OBS** - Screen capture (optional plugin)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TAURI DESKTOP APP                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              React Frontend (UI)                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │  Capture │ │   Clips  │ │  Market  │ │ Settings │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           Tauri Core (Rust Backend)                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐               │  │
│  │  │   IPC    │ │   FS     │ │  Window  │               │  │
│  │  └──────────┘ └──────────┘ └──────────┘               │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/WebSocket
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                  API Layer                             │  │
│  │  /clips  /plugins  /ai  /settings  /marketplace       │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                Business Logic                          │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐               │  │
│  │  │  Capture │ │  Plugin  │ │    AI    │               │  │
│  │  │  Manager │ │  Runtime │ │  Engine  │               │  │
│  │  └──────────┘ └──────────┘ └──────────┘               │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Data Access Layer                         │  │
│  │     SQLAlchemy ORM + Redis Cache                       │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │  PostgreSQL  │         │    Redis     │                  │
│  │   (Clips,    │         │  (Sessions,  │                  │
│  │   Plugins,   │         │   Cache)     │                  │
│  │   Users)     │         │              │                  │
│  └──────────────┘         └──────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Capture Engine
- Screen/window capture
- Hardware acceleration
- Real-time buffering
- Hotkey detection

### 2. Plugin System
- Sandboxed execution
- Permission management
- Resource limits
- IPC communication

### 3. AI Runtime
- Local models (ONNX)
- Cloud providers (OpenAI, etc.)
- Highlight detection
- Auto-editing

### 4. Storage Manager
- Local file storage
- Cloud upload (optional)
- Metadata database
- Thumbnail generation

### 5. Marketplace
- GitHub-based registry
- Plugin discovery
- Version management
- Security validation

## Data Flow

### Clip Capture Flow
```
1. User triggers capture (hotkey/UI)
2. Capture engine starts recording
3. Buffer stores last N seconds
4. User marks highlight moment
5. Video segment extracted
6. Metadata saved to database
7. Thumbnail generated
8. UI updated with new clip
```

### Plugin Execution Flow
```
1. User installs plugin from marketplace
2. Plugin validated and sandboxed
3. Permissions requested from user
4. Plugin code loaded in isolated environment
5. Plugin receives clip data via IPC
6. Plugin processes and returns result
7. Result validated and stored
8. UI displays processed output
```

### AI Processing Flow
```
1. Clip sent to AI engine
2. Model selection (local/cloud)
3. Inference performed
4. Results parsed and validated
5. Confidence scores calculated
6. UI displays AI suggestions
7. User accepts/rejects suggestions
```

## Security Architecture

### Sandboxing Layers

1. **Process Isolation**
   - Plugins run in separate processes
   - No direct memory access
   - Limited system calls

2. **Permission System**
   - Explicit permission grants
   - Granular access control
   - Audit logging

3. **Resource Limits**
   - CPU usage caps
   - Memory limits
   - Disk I/O throttling
   - Network restrictions

4. **Filesystem Jail**
   - Plugin-specific directories
   - No access to system files
   - Path validation

## Performance Optimizations

### Frontend
- Virtual scrolling for large clip lists
- Lazy loading of thumbnails
- Debounced search queries
- Memoized components
- Code splitting

### Backend
- Database query optimization
- Redis caching layer
- Async I/O operations
- Connection pooling
- Background task queue

### Video Processing
- Hardware acceleration (GPU)
- FFmpeg optimization
- Parallel processing
- Efficient codec selection
- Thumbnail caching

## Monitoring & Observability

### Metrics
- Request latency
- Resource usage (CPU, RAM, GPU)
- Plugin performance
- Error rates
- User actions

### Logging
- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARN, ERROR)
- Centralized log aggregation
- Error tracking (Sentry)

### Health Checks
- API endpoint health
- Database connectivity
- Redis availability
- Disk space monitoring

## Deployment

### Development
```bash
docker-compose up -d
```

### Production
- Docker containers
- Reverse proxy (nginx)
- SSL/TLS termination
- Auto-scaling (optional)
- CDN for static assets

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers
- Shared session storage (Redis)
- Load balancing
- Distributed caching

### Vertical Scaling
- GPU instances for AI
- High-memory nodes for processing
- SSD storage for clips

### Database Optimization
- Read replicas
- Sharding (if needed)
- Regular vacuum/analyze
- Index optimization

## Future Architecture

### Planned Enhancements
- WebAssembly plugins
- Real-time collaboration
- Cloud clip storage
- Mobile companion app
- Browser extension

## References

- [Frontend Architecture](04_FRONTEND_ARCHITECTURE.md)
- [Backend Architecture](03_BACKEND_ARCHITECTURE.md)
- [Plugin System](02_PLUGIN_DEVELOPER_GUIDE.md)
- [Security Model](06_SECURITY_SANDBOX.md)
