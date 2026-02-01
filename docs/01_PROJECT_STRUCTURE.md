# 📁 PROJECT STRUCTURE — CLIPSHOT

> Modern, açık kaynak geliştirmeye uygun, temiz mimari prensipleriyle tasarlanmış klasör yapısı.

---

## 🎯 TASARIM PRENSİPLERİ

1. **Separation of Concerns** — Her katman ayrı sorumluluk
2. **Modular Architecture** — Bağımsız, değiştirilebilir modüller
3. **Clean Architecture** — Dependency inversion, interface-driven
4. **Monorepo Structure** — Tek repo, çoklu paket
5. **Convention over Configuration** — Tahmin edilebilir yapı

---

## 📂 TAM KLASÖR YAPISI

```
clipshot/
│
├── 📁 .github/                          # GitHub configurations
│   ├── 📁 workflows/                    # CI/CD pipelines
│   │   ├── ci.yml                       # Lint, test, build
│   │   ├── release.yml                  # Release automation
│   │   └── plugin-validator.yml         # Plugin validation
│   ├── 📁 ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── plugin_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── SECURITY.md
│
├── 📁 apps/                             # Uygulamalar
│   │
│   ├── 📁 desktop/                      # Tauri Desktop App
│   │   │
│   │   ├── 📁 src-tauri/                # Tauri Rust Backend
│   │   │   ├── 📁 src/
│   │   │   │   ├── main.rs              # Tauri entry point
│   │   │   │   ├── lib.rs               # Library root
│   │   │   │   │
│   │   │   │   ├── 📁 commands/         # Tauri Commands (IPC)
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── plugins.rs       # Plugin commands
│   │   │   │   │   ├── capture.rs       # Capture commands
│   │   │   │   │   ├── clips.rs         # Clip management
│   │   │   │   │   ├── ai.rs            # AI commands
│   │   │   │   │   └── system.rs        # System commands
│   │   │   │   │
│   │   │   │   ├── 📁 plugins/          # Plugin Manager (Rust)
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── loader.rs        # Plugin loader
│   │   │   │   │   ├── manifest.rs      # Manifest parser
│   │   │   │   │   ├── native.rs        # Native plugin loader
│   │   │   │   │   └── sandbox.rs       # Sandbox manager
│   │   │   │   │
│   │   │   │   ├── 📁 bridge/           # Python Bridge (PyO3)
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── python.rs        # Python runtime
│   │   │   │   │   └── fastapi.rs       # FastAPI bridge
│   │   │   │   │
│   │   │   │   ├── 📁 utils/
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── config.rs
│   │   │   │   │   └── logger.rs
│   │   │   │   │
│   │   │   │   └── 📁 state/            # App state
│   │   │   │       ├── mod.rs
│   │   │   │       └── app.rs
│   │   │   │
│   │   │   ├── Cargo.toml               # Rust dependencies
│   │   │   ├── tauri.conf.json          # Tauri configuration
│   │   │   ├── build.rs
│   │   │   └── 📁 icons/
│   │   │
│   │   ├── 📁 src/                      # Vite + React Frontend
│   │   │   ├── 📁 app/
│   │   │   │   ├── App.tsx
│   │   │   │   ├── Router.tsx
│   │   │   │   └── providers.tsx
│   │   │   │
│   │   │   ├── 📁 components/           # Shared Components
│   │   │   │   ├── 📁 ui/               # Base UI components
│   │   │   │   │   ├── Button.tsx
│   │   │   │   │   ├── Input.tsx
│   │   │   │   │   ├── Modal.tsx
│   │   │   │   │   ├── Toast.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── 📁 layout/
│   │   │   │   │   ├── Sidebar.tsx
│   │   │   │   │   ├── Header.tsx
│   │   │   │   │   ├── Footer.tsx
│   │   │   │   │   └── MainLayout.tsx
│   │   │   │   ├── 📁 capture/
│   │   │   │   │   ├── CaptureControls.tsx
│   │   │   │   │   ├── SourceSelector.tsx
│   │   │   │   │   └── RecordingIndicator.tsx
│   │   │   │   ├── 📁 clips/
│   │   │   │   │   ├── ClipCard.tsx
│   │   │   │   │   ├── ClipGrid.tsx
│   │   │   │   │   ├── ClipEditor.tsx
│   │   │   │   │   └── ClipTimeline.tsx
│   │   │   │   ├── 📁 ai/
│   │   │   │   │   ├── AIStatus.tsx
│   │   │   │   │   ├── ModelSelector.tsx
│   │   │   │   │   └── InferenceProgress.tsx
│   │   │   │   ├── 📁 plugins/
│   │   │   │   │   ├── PluginCard.tsx
│   │   │   │   │   ├── PluginHost.tsx
│   │   │   │   │   ├── PermissionDialog.tsx
│   │   │   │   │   └── ConflictWarning.tsx
│   │   │   │   └── 📁 dev/
│   │   │   │       ├── APIExplorer.tsx
│   │   │   │       ├── EventInspector.tsx
│   │   │   │       ├── PermissionManager.tsx
│   │   │   │       └── PerformanceMonitor.tsx
│   │   │   │
│   │   │   ├── 📁 pages/                # Page Components
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── Capture.tsx
│   │   │   │   ├── Editor.tsx
│   │   │   │   ├── AIModels.tsx
│   │   │   │   ├── Plugins.tsx
│   │   │   │   ├── Marketplace.tsx
│   │   │   │   ├── Settings.tsx
│   │   │   │   └── DevPanel.tsx
│   │   │   │
│   │   │   ├── 📁 hooks/                # Custom React Hooks
│   │   │   │   ├── useCapture.ts
│   │   │   │   ├── useClips.ts
│   │   │   │   ├── useAI.ts
│   │   │   │   ├── usePlugins.ts
│   │   │   │   ├── useConfig.ts
│   │   │   │   ├── useLocale.ts
│   │   │   │   ├── useTheme.ts
│   │   │   │   └── useTauri.ts          # Tauri helpers
│   │   │   │
│   │   │   ├── 📁 stores/               # State Management (Zustand/Jotai)
│   │   │   │   ├── captureStore.ts
│   │   │   │   ├── clipStore.ts
│   │   │   │   ├── aiStore.ts
│   │   │   │   ├── pluginStore.ts
│   │   │   │   ├── configStore.ts
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── 📁 lib/                  # Tauri API Wrappers
│   │   │   │   ├── tauri.ts             # Tauri invoke helpers
│   │   │   │   ├── commands/            # Command wrappers
│   │   │   │   │   ├── plugins.ts
│   │   │   │   │   ├── capture.ts
│   │   │   │   │   ├── clips.ts
│   │   │   │   │   ├── ai.ts
│   │   │   │   │   └── system.ts
│   │   │   │   └── events.ts            # Event listeners
│   │   │   │
│   │   │   ├── 📁 i18n/                 # Internationalization
│   │   │   │   ├── index.ts
│   │   │   │   ├── detector.ts
│   │   │   │   └── 📁 locales/
│   │   │   │       ├── en.json
│   │   │   │       ├── tr.json
│   │   │   │       └── ...
│   │   │   │
│   │   │   ├── 📁 styles/               # Global Styles
│   │   │   │   ├── globals.css
│   │   │   │   ├── variables.css
│   │   │   │   └── themes/
│   │   │   │
│   │   │   ├── 📁 utils/                # Utility Functions
│   │   │   │   ├── format.ts
│   │   │   │   ├── validation.ts
│   │   │   │   └── constants.ts
│   │   │   │
│   │   │   ├── main.tsx                 # React entry point
│   │   │   └── vite-env.d.ts
│   │   │
│   │   ├── index.html                   # HTML template
│   │   ├── vite.config.ts               # Vite configuration
│   │   ├── tsconfig.json
│   │   ├── tsconfig.node.json
│   │   ├── package.json
│   │   └── .env.example
│   │
│   └── 📁 backend/                      # FastAPI Backend
│       ├── 📁 src/
│       │   ├── __init__.py
│       │   ├── main.py                  # Application entry
│       │   ├── config.py                # Configuration
│       │   │
│       │   ├── 📁 api/                  # API Layer
│       │   │   ├── __init__.py
│       │   │   ├── deps.py              # Dependencies
│       │   │   └── 📁 v1/
│       │   │       ├── __init__.py
│       │   │       ├── router.py        # Main router
│       │   │       └── 📁 routes/       # Route modules
│       │   │           ├── __init__.py
│       │   │           ├── plugins.py
│       │   │           ├── capture.py
│       │   │           ├── clips.py
│       │   │           ├── ai.py
│       │   │           ├── metadata.py
│       │   │           ├── config.py
│       │   │           ├── marketplace.py
│       │   │           └── system.py
│       │   │
│       │   ├── 📁 core/                 # Core Utilities
│       │   │   ├── __init__.py
│       │   │   ├── config.py            # Config management
│       │   │   ├── security.py          # Security utilities
│       │   │   ├── events.py            # Event bus
│       │   │   ├── exceptions.py        # Custom exceptions
│       │   │   └── logging.py           # Logging setup
│       │   │
│       │   ├── 📁 models/               # Database Models
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   ├── clip.py
│       │   │   ├── plugin.py
│       │   │   ├── config.py
│       │   │   └── ai_model.py
│       │   │
│       │   ├── 📁 schemas/              # Pydantic Schemas
│       │   │   ├── __init__.py
│       │   │   ├── clip.py
│       │   │   ├── plugin.py
│       │   │   ├── capture.py
│       │   │   ├── ai.py
│       │   │   └── config.py
│       │   │
│       │   ├── 📁 services/             # Business Logic
│       │   │   ├── __init__.py
│       │   │   ├── capture.py
│       │   │   ├── clip.py
│       │   │   ├── ai_runtime.py
│       │   │   ├── metadata.py
│       │   │   ├── marketplace.py
│       │   │   └── github_fetcher.py
│       │   │
│       │   ├── 📁 plugins/              # Plugin System
│       │   │   ├── __init__.py
│       │   │   ├── loader.py            # Plugin loader
│       │   │   ├── sandbox.py           # Sandbox implementation
│       │   │   ├── permissions.py       # Permission system
│       │   │   ├── validator.py         # Manifest validator
│       │   │   ├── conflict.py          # Conflict detection
│       │   │   └── watchdog.py          # Resource monitoring
│       │   │
│       │   ├── 📁 ai/                   # AI Runtime
│       │   │   ├── __init__.py
│       │   │   ├── interface.py         # Abstract interface
│       │   │   ├── local.py             # Local runtime
│       │   │   ├── cloud.py             # Cloud adapters
│       │   │   ├── self_host.py         # Self-hosted
│       │   │   └── schema_validator.py  # Output validation
│       │   │
│       │   └── 📁 db/                   # Database
│       │       ├── __init__.py
│       │       ├── session.py
│       │       ├── base.py
│       │       └── migrations/
│       │
│       ├── 📁 tests/
│       │   ├── __init__.py
│       │   ├── conftest.py
│       │   ├── 📁 unit/
│       │   ├── 📁 integration/
│       │   └── 📁 e2e/
│       │
│       ├── 📁 alembic/                  # Database migrations
│       │   ├── env.py
│       │   ├── alembic.ini
│       │   └── versions/
│       │
│       ├── pyproject.toml
│       ├── requirements.txt
│       └── Dockerfile
│
├── 📁 core/                             # Shared Core Logic (TypeScript)
│   ├── 📁 plugin-system/
│   │   ├── manifest.schema.json         # JSON Schema for manifests
│   │   ├── manifest.ts                  # Manifest types
│   │   ├── lifecycle.ts                 # Plugin lifecycle
│   │   ├── permission-types.ts          # Permission definitions
│   │   └── api-registry.ts              # API registration
│   │
│   ├── 📁 security/
│   │   ├── 📁 sandbox/
│   │   │   ├── process-isolation.ts
│   │   │   ├── resource-limits.ts
│   │   │   └── filesystem-jail.ts
│   │   ├── 📁 permissions/
│   │   │   ├── checker.ts
│   │   │   ├── grant.ts
│   │   │   └── audit.ts
│   │   └── 📁 audit/
│   │       ├── logger.ts
│   │       └── types.ts
│   │
│   ├── 📁 ai-runtime/
│   │   ├── interface.ts                 # Unified AI interface
│   │   ├── local-adapter.ts
│   │   ├── cloud-adapter.ts
│   │   ├── self-host-adapter.ts
│   │   └── model-registry.ts
│   │
│   ├── 📁 ipc/
│   │   ├── channels.ts
│   │   ├── handlers.ts
│   │   └── types.ts
│   │
│   └── package.json
│
├── 📁 plugins/                          # Plugin Directory
│   ├── 📁 core/                         # Bundled Core Plugins
│   │   ├── 📁 capture-ffmpeg/
│   │   │   ├── manifest.json
│   │   │   ├── 📁 src/
│   │   │   │   ├── main.py
│   │   │   │   └── capture.py
│   │   │   ├── 📁 ui/
│   │   │   │   └── SettingsPanel.tsx
│   │   │   ├── 📁 locales/
│   │   │   │   ├── en.json
│   │   │   │   └── tr.json
│   │   │   ├── config.schema.json
│   │   │   └── README.md
│   │   │
│   │   ├── 📁 capture-winapi/
│   │   │   ├── manifest.json
│   │   │   ├── 📁 src/
│   │   │   │   ├── main.py
│   │   │   │   ├── dxgi.py
│   │   │   │   └── gamebar.py
│   │   │   ├── 📁 ui/
│   │   │   ├── 📁 locales/
│   │   │   └── README.md
│   │   │
│   │   ├── 📁 codec-manager/
│   │   ├── 📁 ai-local/
│   │   ├── 📁 ai-cloud/
│   │   ├── 📁 metadata-generator/
│   │   ├── 📁 clip-editor/
│   │   ├── 📁 template-engine/
│   │   ├── 📁 social-publisher/
│   │   ├── 📁 dev-panel/
│   │   └── 📁 storage/
│   │
│   └── 📁 community/                    # Community plugins (git submodules)
│       └── .gitkeep
│
├── 📁 shared/                           # Shared Resources
│   ├── 📁 schemas/                      # JSON Schemas
│   │   ├── manifest.schema.json
│   │   ├── config.schema.json
│   │   ├── clip.schema.json
│   │   └── ai-model.schema.json
│   │
│   ├── 📁 contracts/                    # API Contracts
│   │   ├── capture.contract.ts
│   │   ├── ai.contract.ts
│   │   └── plugin.contract.ts
│   │
│   ├── 📁 types/                        # TypeScript Types
│   │   ├── index.ts
│   │   ├── plugin.ts
│   │   ├── capture.ts
│   │   ├── ai.ts
│   │   └── config.ts
│   │
│   └── 📁 locales/                      # Global Localization
│       ├── 📁 en/
│       │   ├── common.json
│       │   ├── errors.json
│       │   ├── permissions.json
│       │   └── settings.json
│       ├── 📁 tr/
│       ├── 📁 de/
│       ├── 📁 fr/
│       ├── 📁 es/
│       ├── 📁 pt/
│       ├── 📁 ru/
│       ├── 📁 zh/
│       ├── 📁 ja/
│       └── 📁 ko/
│
├── 📁 docs/                             # Documentation
│   ├── 00_MASTER_AI_INSTRUCTION.md
│   ├── 01_PROJECT_STRUCTURE.md
│   ├── 02_PLUGIN_DEVELOPER_GUIDE.md
│   ├── 03_BACKEND_ARCHITECTURE.md
│   ├── 04_FRONTEND_ARCHITECTURE.md
│   ├── 05_AI_RUNTIME_ABSTRACTION.md
│   ├── 06_SECURITY_SANDBOX.md
│   ├── 07_MARKETPLACE_GITHUB.md
│   ├── 08_LOCALIZATION.md
│   ├── 09_PERFORMANCE_MCP.md
│   ├── API.md
│   └── 📁 guides/
│       ├── getting-started.md
│       ├── creating-first-plugin.md
│       └── contributing.md
│
├── 📁 scripts/                          # Build & Development Scripts
│   ├── dev.ps1                          # Development environment
│   ├── build.ps1                        # Production build
│   ├── validate-plugins.ps1             # Plugin validation
│   ├── generate-api-docs.ps1            # API documentation
│   └── release.ps1                      # Release automation
│
├── 📁 tools/                            # Development Tools
│   ├── 📁 plugin-template/              # Plugin boilerplate generator
│   ├── 📁 api-generator/                # OpenAPI client generator
│   └── 📁 locale-extractor/             # i18n string extractor
│
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .prettierrc
├── .prettierignore
├── .eslintrc.js
├── .eslintignore
├── tsconfig.base.json
├── package.json                         # Root package.json (workspace)
├── pnpm-workspace.yaml                  # pnpm workspace config
├── LICENSE
├── README.md
└── CHANGELOG.md
```

---

## 📦 PACKAGE MANAGEMENT

### Monorepo with pnpm Workspaces

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'core'
  - 'shared'
  - 'plugins/core/*'
```

### Root package.json

```json
{
  "name": "clipshot",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "pnpm -r --parallel dev",
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "typecheck": "pnpm -r typecheck",
    "clean": "pnpm -r clean",
    "prepare": "husky install"
  },
  "devDependencies": {
    "husky": "^9.0.0",
    "lint-staged": "^15.0.0",
    "prettier": "^3.0.0",
    "typescript": "^5.4.0"
  },
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=9.0.0"
  }
}
```

---

## 🔧 CONFIGURATION FILES

### .editorconfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.{py,pyi}]
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

### .prettierrc

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

### .eslintrc.js

```javascript
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'react', 'react-hooks'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
```

---

## 📝 NAMING CONVENTIONS

### Files & Folders

| Type | Convention | Example |
|------|------------|---------|
| Folders | kebab-case | `ai-runtime`, `clip-editor` |
| React Components | PascalCase | `ClipEditor.tsx`, `DevPanel.tsx` |
| Hooks | camelCase with `use` | `useCapture.ts`, `usePlugins.ts` |
| Utils/Services | camelCase | `apiClient.ts`, `formatTime.ts` |
| Types/Interfaces | PascalCase | `Plugin.ts`, `CaptureConfig.ts` |
| Constants | SCREAMING_SNAKE | `MAX_CLIP_DURATION` |
| Python files | snake_case | `plugin_loader.py`, `ai_runtime.py` |

### Code Style

```typescript
// TypeScript/React
interface PluginManifest {
  id: string;
  name: string;
  version: string;
}

const usePlugin = (id: string): Plugin => {
  // ...
};

export const PluginCard: React.FC<Props> = ({ plugin }) => {
  // ...
};
```

```python
# Python
class PluginLoader:
    """Plugin loader with sandbox support."""
    
    async def load_plugin(self, plugin_id: str) -> Plugin:
        """Load a plugin by ID."""
        pass
    
    def _validate_manifest(self, manifest: dict) -> bool:
        """Validate plugin manifest."""
        pass
```

---

## 🚫 ANTI-PATTERNS

### Yapılmaması Gerekenler

❌ **God Files**
```
// YANLIŞ: Her şey tek dosyada
src/
├── app.ts  // 5000+ satır
```

❌ **Deep Nesting**
```
// YANLIŞ: Çok derin klasör yapısı
src/modules/core/services/internal/helpers/utils/...
```

❌ **Circular Dependencies**
```typescript
// YANLIŞ
// a.ts
import { b } from './b';
// b.ts
import { a } from './a';
```

❌ **Mixed Concerns**
```
// YANLIŞ: UI ve business logic karışık
components/
├── ClipCard.tsx  // API çağrıları + UI + state
```

### Yapılması Gerekenler

✅ **Feature-based Structure**
```
features/
├── capture/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── types/
```

✅ **Explicit Dependencies**
```typescript
// DOĞRU: Dependency injection
class CaptureService {
  constructor(
    private readonly encoder: Encoder,
    private readonly storage: Storage
  ) {}
}
```

✅ **Single Responsibility**
```
// DOĞRU: Her dosya tek sorumluluk
components/
├── ClipCard.tsx      // Sadece UI
├── ClipEditor.tsx    // Sadece UI
hooks/
├── useClips.ts       // Sadece state
services/
├── clipService.ts    // Sadece API
```

---

## 📊 IMPORT ORDER

```typescript
// 1. Node/built-in modules
import path from 'path';
import fs from 'fs';

// 2. External packages
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 3. Internal packages (workspace)
import { type Plugin } from '@clipshot/shared';

// 4. Relative imports - furthest first
import { usePlugins } from '../../hooks';
import { PluginCard } from '../PluginCard';
import { styles } from './styles';
```

---

## 🎯 Bu Yapının Avantajları

1. **Scalability** — Yeni özellikler kolayca eklenebilir
2. **Maintainability** — Her şey yerinde, bulması kolay
3. **Testability** — Bağımsız modüller test edilebilir
4. **Team Collaboration** — Birden fazla kişi çakışmadan çalışabilir
5. **Open Source Ready** — Katkıda bulunanlar için anlaşılır yapı
