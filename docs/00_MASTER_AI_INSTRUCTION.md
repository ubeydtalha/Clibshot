# 🎮 CLIPSHOT — MASTER AI INSTRUCTION v2.0

> **Bu dosya, projeyi sıfırdan ve eksiksiz şekilde geliştirebilmesi için bir AI modeline verilecek TEK, KAPSAMLI ve YETERLİ instrüksiyon dosyasıdır.**

---

## 🎭 ROL TANIMI

Sen şu rollerde hareket ediyorsun:

- **Principal Software Architect** — Sistem tasarımı ve mimari kararlar
- **Security & Sandbox Engineer** — Plugin izolasyonu ve güvenlik modeli
- **AI Infrastructure Architect** — Lokal/Cloud/Self-host AI entegrasyonu
- **Open-Source Project Maintainer** — Topluluk dostu kod ve dokümantasyon
- **UX/UI Lead** — Modern, kullanışlı ve erişilebilir arayüz tasarımı

Tüm mimari, güvenlik ve modülerlik kısıtlamalarına **kesinlikle** uyman gerekiyor.

---

## 🎯 PROJE MİSYONU

**Açık kaynak, masaüstü öncelikli, tamamen modüler bir gaming AI platformu** oluştur:

### Temel Özellikler
- ✅ Oyun kayıtlarını otomatik olarak kaydet
- ✅ AI ile highlight/önemli anları tespit et
- ✅ Video metadata'sı AI ile üret (başlık, etiket, açıklama, timeline)
- ✅ Sosyal medyada yayınla (TikTok, YouTube Shorts, Instagram Reels)
- ✅ Clip düzenleme araçları (AI altyazı, efektler, şablonlar)
- ✅ Montaj oluşturma (birden fazla clip'i birleştirme)

### Rekabet Analizi — Şu Uygulamaların TÜM Özelliklerini İçermeli:

| Uygulama | Ana Özellikler |
|----------|---------------|
| **Powder AI** | Lokal AI highlight tespiti, 40+ oyun desteği, otomatik montaj, düşük kaynak kullanımı, AMD NPU optimizasyonu |
| **Sludge AI** | AI caption, viral hook, split screen, template sistem, multi-platform export, otomasyon |
| **Streamlabs** | Multistream, overlay sistemi, widget'lar, donation/alert, app store, collab cam |

---

## 🧩 TEMEL PRENSİPLER (DEĞİŞTİRİLEMEZ)

### 1. **HER ŞEY BİR MOD**
```
Kayıt sistemi = Mod
AI inference = Mod  
UI panelleri = Mod
Codec seçimi = Mod
Marketplace = Mod
Dev araçları = Mod
WinAPI Capture = Mod
```

### 2. **CORE'UN AYRICALIK YOK**
- Core modlar sadece **bundled + trusted**
- Aynı kurallara tabi
- Değiştirilebilir/devre dışı bırakılabilir

### 3. **LOCAL-FIRST MİMARİ**
- Uygulama tamamen offline çalışmalı
- Cloud isteğe bağlı ve değiştirilebilir
- Tüm AI modelleri lokal çalışabilmeli

### 4. **GÜVENLİK ÖNCELİKLİ**
- Modlar sandbox'ta çalışır
- Sadece açık izinler
- OS kaynaklarına sessiz erişim YOK

### 5. **OpenAPI-FIRST BACKEND**
- Tüm özellikler dokümante API ile
- Dil bağımsız tasarım
- Swagger/ReDoc auto-docs

### 6. **PERFORMANS-KRİTİK**
- Düşük gecikme
- Async AI inference
- GPU-aware scheduling
- UI latency < 16ms

### 7. **MODERN DESKTOP STACK (TAURI + VITE)**
- **Tauri** v2 ile hafif, güvenli desktop framework (~3-5MB)
- **Vite** ile lightning-fast HMR ve optimized builds
- Native webview kullanımı (Chromium bundle'a gerek yok)
- Rust backend Tauri Commands ile frontend'e expose
- Modüler ve pluginlenebilir frontend mimarisi

### 8. **MULTI-LANGUAGE NATIVE PLUGIN DESTEĞİ**
- Python plugin'lerin yanı sıra **Rust**, **C** ve **C++** plugin desteği
- Tüm diller aynı ABI ve manifest standartına uyar
- FFI Bridge'ler: PyO3 (Rust), pybind11 (C++), cffi (C)
- Performans-kritik işlemler native plugin'lerle yapılabilir
- Video encode/decode, AI inference, image processing native'de çalışabilir
- Tauri Rust backend ile doğrudan entegrasyon

---

## 🏗️ ÜST DÜZEY MİMARİ

```
┌─────────────────────────────────────────────────────────────────┐
│                     TAURI FRONTEND (Vite + React)                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ Plugin UI   │ │ Dev Panel   │ │ Settings UI │ │ Mod Market │ │
│  │ Host        │ │ (API View)  │ │ (Codec etc) │ │ Browser    │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘ │
│                  │                                               │
│                  ↓ Tauri IPC (invoke/emit)                       │
├─────────────────────────────────────────────────────────────────┤
│                      TAURI BACKEND (Rust)                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ Tauri       │ │ Plugin      │ │ Native      │ │ Python     │ │
│  │ Commands    │ │ Manager     │ │ Plugin Mgr  │ │ Bridge     │ │
│  │ (Rust API)  │ │ (Lifecycle) │ │ (Rust/C/C++)│ │ (PyO3)     │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘ │
│                              ↓                                   │
│                  FastAPI Service Layer (Python)                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ AI Runtime  │ │ Capture     │ │ Clip        │ │ Metadata   │ │
│  │ Abstraction │ │ Manager     │ │ Manager     │ │ Generator  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘ │
│                              ↓                                   │
├─────────────────────────────────────────────────────────────────┤
│                     PLUGIN ECOSYSTEM                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ Core Mods   │ │ Community   │ │ AI Models   │ │ Native     │ │
│  │ (Bundled)   │ │ Mods        │ │ (Local)     │ │ Plugins    │ │
│  │ Python/Rust │ │ Python/Rust │ │ ONNX/llama  │ │ Rust/C/C++ │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘ │
└─────────────────────────────────────────────────────────────────┘

**Tauri Avantajları:**
- ✅ ~3-5MB bundle size (vs Electron ~150MB)
- ✅ Native webview (Chromium bundle'a gerek yok)
- ✅ Rust security guarantees
- ✅ Vite ile instant HMR (<100ms)
- ✅ Doğrudan Rust plugin entegrasyonu
- ✅ Cross-platform (Windows, macOS, Linux)
```

---

## 📁 PROJE YAPISI (CLEAN ARCHITECTURE)

```
clipshot/
├── .github/
│   ├── workflows/           # CI/CD (lint, test, build)
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CONTRIBUTING.md
│
├── apps/
│   ├── desktop/             # Tauri Desktop App
│   │   ├── src-tauri/       # Tauri Rust backend
│   │   │   ├── src/
│   │   │   │   ├── main.rs  # Tauri entry point
│   │   │   │   ├── commands/ # Tauri commands
│   │   │   │   ├── plugins/ # Plugin manager
│   │   │   │   └── bridge/  # Python bridge (PyO3)
│   │   │   ├── Cargo.toml
│   │   │   └── tauri.conf.json
│   │   │
│   │   ├── src/             # Vite + React frontend
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── stores/      # State management
│   │   │   ├── lib/         # Tauri API wrappers
│   │   │   │   └── tauri.ts # invoke helpers
│   │   │   ├── i18n/
│   │   │   └── main.tsx
│   │   │
│   │   ├── vite.config.ts   # Vite configuration
│   │   ├── package.json
│   │   └── index.html
│   │
│   └── backend/             # FastAPI Backend
│       ├── src/
│       │   ├── api/
│       │   │   ├── v1/
│       │   │   │   ├── routes/
│       │   │   │   │   ├── plugins.py
│       │   │   │   │   ├── capture.py
│       │   │   │   │   ├── ai.py
│       │   │   │   │   ├── metadata.py
│       │   │   │   │   ├── config.py
│       │   │   │   │   └── marketplace.py
│       │   │   │   └── __init__.py
│       │   │   └── deps.py
│       │   ├── core/
│       │   │   ├── config.py
│       │   │   ├── security.py
│       │   │   ├── events.py
│       │   │   └── exceptions.py
│       │   ├── services/
│       │   ├── models/
│       │   ├── schemas/
│       │   └── plugins/
│       │       ├── loader.py
│       │       ├── sandbox.py
│       │       ├── permissions.py
│       │       └── validator.py
│       ├── tests/
│       ├── alembic/
│       └── pyproject.toml
│
├── core/                    # Shared Core Logic
│   ├── plugin-system/
│   │   ├── manifest.schema.json
│   │   ├── permission-types.ts
│   │   └── lifecycle.ts
│   ├── security/
│   │   ├── sandbox/
│   │   ├── permissions/
│   │   └── audit/
│   ├── ai-runtime/
│   │   ├── interface.ts
│   │   ├── local-adapter.ts
│   │   ├── cloud-adapter.ts
│   │   └── self-host-adapter.ts
│   └── ipc/
│       ├── channels.ts
│       └── handlers.ts
│
├── plugins/
│   ├── core/                # Bundled Core Mods
│   │   ├── capture-ffmpeg/
│   │   ├── capture-winapi/
│   │   ├── codec-manager/
│   │   ├── ai-local/
│   │   ├── ai-cloud/
│   │   ├── metadata-generator/
│   │   ├── clip-editor/
│   │   ├── social-publisher/
│   │   ├── template-engine/
│   │   └── dev-panel/
│   │
│   └── community/           # Community mods (git submodules)
│
├── shared/
│   ├── schemas/             # JSON Schemas
│   ├── contracts/           # API Contracts
│   ├── types/               # TypeScript Types
│   └── locales/             # i18n files
│       ├── en/
│       ├── tr/
│       └── ...
│
├── docs/
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
│   ├── 10_NATIVE_PLUGIN_GUIDE.md    # Rust/C/C++ Plugin Rehberi
│   ├── 11_RECOMMENDED_LIBRARIES.md  # Önerilen Kütüphaneler
│   └── API.md
│
├── scripts/
│   ├── dev.ps1
│   ├── build.ps1
│   └── validate-plugins.ps1
│
├── .gitignore
├── .editorconfig
├── .prettierrc
├── .eslintrc.js
├── LICENSE (MIT)
└── README.md
```

---

## 🧩 PLUGIN MANIFEST SPECİFİKASYONU v2.0

```json
{
  "$schema": "./manifest.schema.json",
  "id": "com.clipshot.capture-winapi",
  "name": "Windows Native Capture",
  "version": "1.0.0",
  "type": "core",
  "category": "capture",
  "description": {
    "en": "Native Windows screen capture using DXGI and Game Bar",
    "tr": "DXGI ve Game Bar kullanarak Windows ekran kaydı"
  },
  "author": {
    "name": "ClipShot Team",
    "email": "dev@clipshot.io",
    "url": "https://github.com/clipshot"
  },
  "repository": "https://github.com/clipshot/capture-winapi",
  "license": "MIT",
  "entry": {
    "backend": "src/main.py",
    "frontend": "src/ui/index.tsx"
  },
  "api_version": "v1",
  
  "permissions": {
    "screen": {
      "level": "required",
      "reason": {
        "en": "Required to capture gameplay",
        "tr": "Oyun kaydı için gerekli"
      }
    },
    "microphone": {
      "level": "optional",
      "reason": {
        "en": "For voice recording",
        "tr": "Ses kaydı için"
      }
    },
    "filesystem": {
      "level": "limited",
      "paths": ["$PLUGIN_DATA", "$CLIPS"],
      "reason": {
        "en": "To save recorded clips",
        "tr": "Kaydedilen clipleri saklamak için"
      }
    },
    "network": {
      "level": "none"
    },
    "gpu": {
      "level": "required",
      "reason": {
        "en": "Hardware acceleration for encoding",
        "tr": "Kodlama için donanım hızlandırma"
      }
    },
    "system": {
      "level": "limited",
      "apis": ["dxgi", "gamebar", "d3d11"],
      "reason": {
        "en": "Windows capture APIs",
        "tr": "Windows yakalama API'leri"
      }
    }
  },
  
  "capabilities": [
    "video_capture",
    "window_capture", 
    "game_capture",
    "replay_buffer"
  ],
  
  "provides": [
    "capture.api.v1",
    "replay.api.v1"
  ],
  
  "requires": [
    "core.codec.api.v1",
    "core.events.api.v1"
  ],
  
  "conflicts": [
    "com.clipshot.capture-ffmpeg"
  ],
  
  "settings": {
    "schema": "config.schema.json",
    "defaults": {
      "captureMode": "game",
      "fps": 60,
      "quality": "high"
    }
  },
  
  "ui": {
    "settingsPanel": true,
    "toolbar": true,
    "overlay": true
  },
  
  "localization": {
    "supported": ["en", "tr", "de", "fr", "es", "pt", "ru", "zh", "ja", "ko"],
    "path": "locales/"
  },
  
  "resources": {
    "cpu": {
      "max_percent": 20
    },
    "memory": {
      "max_mb": 512
    },
    "gpu": {
      "max_percent": 30
    }
  },
  
  "security": {
    "sandbox": "strict",
    "audit": true
  }
}
```

---

## 🛡️ GÜVENLİK MODELİ

### Permission Seviyeleri

| Seviye | Açıklama |
|--------|----------|
| `none` | İzin yok, erişim tamamen engelli |
| `limited` | Belirli path/API'lere sınırlı erişim |
| `optional` | Kullanıcı onayı ile aktif |
| `required` | Mod çalışması için zorunlu |

### Sandbox Katmanları

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: Process Isolation                          │
│ - Her mod ayrı process                              │
│ - Windows Job Objects + Restricted Tokens           │
│ - IPC-only communication                            │
├─────────────────────────────────────────────────────┤
│ Layer 2: Permission Gate                            │
│ - Manifest dışı erişim DENIED                       │
│ - Runtime permission toggle                         │
│ - Audit logging                                     │
├─────────────────────────────────────────────────────┤
│ Layer 3: Resource Control                           │
│ - CPU/GPU/RAM quota                                 │
│ - Timeout & watchdog                                │
│ - Auto-throttle                                     │
├─────────────────────────────────────────────────────┤
│ Layer 4: Filesystem Jail                            │
│ - Plugin özel dizin                                 │
│ - Read-only core erişimi                            │
│ - Whitelist path sistemi                            │
└─────────────────────────────────────────────────────┘
```

### Kullanıcı İzin Onay Akışı

```
[Mod Kurulumu]
      ↓
[Manifest Okunur]
      ↓
[İzin Listesi Gösterilir]
┌─────────────────────────────────────┐
│ 🎤 Mikrofon Erişimi        [✓] [?] │
│    "Ses kaydı için"                 │
│                                     │
│ 📺 Ekran Kaydı            [✓] [?]  │
│    "Oyun kaydı için"                │
│                                     │
│ 💾 Dosya Sistemi          [✓] [?]  │
│    "Clipleri kaydetmek için"        │
│    Sadece: clips/, temp/            │
│                                     │
│ 🌐 İnternet               [ ] [?]  │
│    "Bu mod internet gerektirmiyor"  │
└─────────────────────────────────────┘
      ↓
[Kullanıcı Onayı]
      ↓
[Mod Aktif]
```

---

## 🧠 AI RUNTIME ABSTRACTION

### Unified AI Interface

```typescript
interface AIRuntime {
  // Lifecycle
  initialize(config: AIConfig): Promise<void>;
  shutdown(): Promise<void>;
  
  // Model Management
  loadModel(modelId: string, options?: LoadOptions): Promise<Model>;
  unloadModel(modelId: string): Promise<void>;
  listModels(): Promise<ModelInfo[]>;
  
  // Inference
  infer<T>(input: InferenceInput): Promise<InferenceResult<T>>;
  inferStream<T>(input: InferenceInput): AsyncGenerator<T>;
  
  // Health
  health(): Promise<HealthStatus>;
  metrics(): Promise<RuntimeMetrics>;
}

interface InferenceInput {
  modelId: string;
  task: 'highlight_detection' | 'metadata_generation' | 'transcription' | 'caption';
  data: StructuredInput;
  schema: OutputSchema;  // Çıktı şeması - prompt injection koruması
}
```

### AI Provider Types

```typescript
type AIProviderType = 'local' | 'cloud' | 'self-host';

// Local: llama.cpp, AirLLM, ONNX Runtime
// Cloud: OpenAI, Anthropic, Google AI
// Self-host: vLLM, Ollama, LocalAI
```

### AI Marketplace

```yaml
# AI Model Marketplace Manifest
id: "llama-3.2-vision-11b"
name: "Llama 3.2 Vision 11B"
type: "local"
provider: "meta"
capabilities:
  - highlight_detection
  - scene_analysis
  - metadata_generation
requirements:
  vram_gb: 8
  disk_gb: 24
quantizations:
  - q4_k_m
  - q5_k_m
  - q8_0
download_url: "https://huggingface.co/..."
```

---

## ⚙️ BACKEND ARCHITECTURE (FastAPI)

### Router Yapısı

```
/api/v1/
├── /plugins
│   ├── GET    /                    # Tüm modları listele
│   ├── GET    /{id}                # Mod detayları
│   ├── POST   /{id}/install        # Mod kur
│   ├── DELETE /{id}                # Mod kaldır
│   ├── GET    /{id}/config         # Mod ayarları
│   ├── PUT    /{id}/config         # Mod ayarlarını güncelle
│   ├── GET    /{id}/permissions    # Mod izinleri
│   ├── PUT    /{id}/permissions    # İzinleri güncelle
│   └── GET    /{id}/health         # Mod sağlık durumu
│
├── /capture
│   ├── POST   /start               # Kayda başla
│   ├── POST   /stop                # Kaydı durdur
│   ├── GET    /status              # Kayıt durumu
│   ├── POST   /replay/save         # Replay buffer kaydet
│   └── GET    /sources             # Yakalama kaynakları
│
├── /ai
│   ├── GET    /models              # Mevcut modeller
│   ├── POST   /models/{id}/load    # Model yükle
│   ├── POST   /infer               # Inference yap
│   ├── GET    /tasks               # Aktif görevler
│   └── GET    /health              # AI runtime durumu
│
├── /metadata
│   ├── POST   /generate            # Metadata üret
│   ├── GET    /templates           # Metadata şablonları
│   └── POST   /analyze             # Clip analizi
│
├── /clips
│   ├── GET    /                    # Clip listesi
│   ├── GET    /{id}                # Clip detayları
│   ├── PUT    /{id}                # Clip güncelle
│   ├── DELETE /{id}                # Clip sil
│   └── POST   /{id}/export         # Clip export
│
├── /config
│   ├── GET    /                    # Tüm ayarlar
│   ├── PUT    /                    # Ayarları güncelle
│   ├── GET    /{key}               # Belirli ayar
│   └── PUT    /{key}               # Belirli ayarı güncelle
│
├── /marketplace
│   ├── GET    /plugins             # Mevcut modlar
│   ├── GET    /ai-models           # AI modelleri
│   ├── POST   /install             # GitHub'dan kur
│   └── GET    /updates             # Güncellemeler
│
└── /system
    ├── GET    /health              # Sistem sağlığı
    ├── GET    /metrics             # Performans metrikleri
    ├── GET    /events              # Event stream (SSE)
    └── GET    /openapi             # OpenAPI spec
```

### Config Yönetimi

```python
# SQLite + JSON Override sistemi

class ConfigManager:
    """
    Öncelik sırası:
    1. Environment variables
    2. JSON override dosyası
    3. SQLite database
    4. Default values
    """
    
    async def get(self, key: str) -> Any:
        # 1. Check env
        if value := os.getenv(f"CLIPSHOT_{key.upper()}"):
            return value
        
        # 2. Check JSON override
        if value := self.json_overrides.get(key):
            return value
        
        # 3. Check database
        if value := await self.db.get_config(key):
            return value
        
        # 4. Return default
        return self.defaults.get(key)
```

---

## 🖥️ FRONTEND ARCHITECTURE (Electron)

### Dev Panel Özellikleri

```typescript
interface DevPanel {
  // API Explorer
  apiEndpoints: Endpoint[];      // Tüm backend uç noktaları
  apiTester: RequestBuilder;     // API test aracı
  
  // Plugin Manager
  loadedPlugins: Plugin[];       // Yüklü modlar
  pluginLogs: LogStream;         // Mod logları
  
  // Permission Manager
  permissions: PermissionTree;   // İzin ağacı
  toggles: PermissionToggle[];   // İzin açma/kapama
  
  // Event Inspector
  eventBus: EventStream;         // Event akışı
  eventHistory: Event[];         // Event geçmişi
  
  // AI Debugger
  aiInputs: AIRequest[];         // AI istekleri
  aiOutputs: AIResponse[];       // AI yanıtları
  
  // Performance Monitor
  metrics: PerformanceMetrics;   // CPU, GPU, RAM
  pluginMetrics: Map<string, Metrics>;
}
```

### UI Modlama Sistemi

```typescript
// Plugin UI injection points
type UISlot = 
  | 'toolbar'           // Ana araç çubuğu
  | 'sidebar'           // Yan panel
  | 'settings-tab'      // Ayarlar sekmesi
  | 'clip-editor'       // Clip editör alanı
  | 'overlay'           // Oyun üstü overlay
  | 'context-menu'      // Sağ tık menüsü
  | 'status-bar'        // Durum çubuğu
  | 'modal'             // Modal pencereler
  | 'notification';     // Bildirimler

interface UIPluginManifest {
  slots: {
    [K in UISlot]?: {
      component: string;
      priority: number;
      props?: Record<string, unknown>;
    };
  };
}
```

---

## 🌍 LOCALIZATION (i18n)

### Standart Format (ICU Message Format)

```json
// locales/tr/common.json
{
  "app": {
    "name": "ClipShot",
    "tagline": "AI destekli oyun klip kaydedici"
  },
  "capture": {
    "start": "Kayda Başla",
    "stop": "Kaydı Durdur",
    "status": {
      "recording": "Kayıt yapılıyor...",
      "idle": "Hazır",
      "processing": "İşleniyor..."
    }
  },
  "permissions": {
    "screen": {
      "title": "Ekran Kaydı",
      "description": "Oyun ekranınızı kaydetmek için gerekli"
    },
    "microphone": {
      "title": "Mikrofon",
      "description": "Ses kaydı için kullanılır"
    }
  },
  "clips": {
    "count": "{count, plural, =0 {Clip yok} =1 {1 clip} other {# clip}}"
  }
}
```

### Mod Lokalizasyonu

Her mod kendi locale dosyalarını içermeli:

```
plugins/core/capture-winapi/
└── locales/
    ├── en.json
    ├── tr.json
    └── ...
```

---

## ⚡ PERFORMANS HEDEFLERİ

| Metrik | Hedef | Kritik |
|--------|-------|--------|
| UI Frame Latency | < 16ms | < 32ms |
| Clip Trigger | < 50ms | < 100ms |
| AI Inference Start | < 100ms | < 500ms |
| Plugin Load | < 200ms | < 500ms |
| Memory per Plugin | < 512MB | < 1GB |
| CPU per Plugin | < 20% | < 30% |
| GPU per Plugin | < 30% | < 50% |

### Otomatik Throttling

```python
class PluginWatchdog:
    async def monitor(self, plugin_id: str):
        while self.running:
            metrics = await self.get_metrics(plugin_id)
            
            if metrics.cpu > CRITICAL_CPU:
                await self.throttle(plugin_id, 'cpu')
                await self.notify_user(plugin_id, 'cpu_high')
            
            if metrics.memory > CRITICAL_MEMORY:
                await self.throttle(plugin_id, 'memory')
                await self.notify_user(plugin_id, 'memory_high')
            
            await asyncio.sleep(1)
```

---

## 🤖 MCP READINESS

Tüm özellikler AI tarafından kontrol edilebilir olmalı:

```typescript
// Her özellik için MCP-uyumlu endpoint
interface MCPEndpoint {
  name: string;
  description: string;
  parameters: JSONSchema;
  returns: JSONSchema;
  
  // Deterministik davranış
  idempotent: boolean;
  
  // Yan etkiler
  sideEffects: SideEffect[];
}

// Örnek: Clip kaydetme
const saveClipEndpoint: MCPEndpoint = {
  name: 'capture.save_replay',
  description: 'Son N saniyeyi clip olarak kaydet',
  parameters: {
    type: 'object',
    properties: {
      duration_seconds: { type: 'number', minimum: 5, maximum: 300 },
      format: { enum: ['mp4', 'webm', 'mov'] },
      quality: { enum: ['low', 'medium', 'high', 'lossless'] }
    },
    required: ['duration_seconds']
  },
  returns: {
    type: 'object',
    properties: {
      clip_id: { type: 'string' },
      path: { type: 'string' },
      duration: { type: 'number' }
    }
  },
  idempotent: false,
  sideEffects: ['file_created', 'storage_used']
};
```

---

## 🏪 MARKETPLACE & GITHUB INTEGRATION

### GitHub'dan Mod Kurulumu

```typescript
interface MarketplacePlugin {
  id: string;
  name: string;
  description: string;
  author: GitHubUser;
  repository: string;
  releases: Release[];
  
  // Trust Levels
  trustLevel: 'unverified' | 'community' | 'verified' | 'core';
  
  // Validation
  manifestValid: boolean;
  checksumValid: boolean;
  signatureValid: boolean;
  
  // Stats
  downloads: number;
  stars: number;
  lastUpdated: Date;
}

async function installFromGitHub(repoUrl: string): Promise<InstallResult> {
  // 1. Fetch manifest
  const manifest = await fetchManifest(repoUrl);
  
  // 2. Validate manifest schema
  if (!validateManifest(manifest)) {
    throw new InvalidManifestError();
  }
  
  // 3. Check conflicts
  const conflicts = await checkConflicts(manifest);
  if (conflicts.length > 0) {
    throw new ConflictError(conflicts);
  }
  
  // 4. Show permissions to user
  const approved = await showPermissionDialog(manifest.permissions);
  if (!approved) {
    throw new PermissionDeniedError();
  }
  
  // 5. Download and verify
  const archive = await downloadRelease(repoUrl);
  if (!verifyChecksum(archive, manifest.checksum)) {
    throw new ChecksumMismatchError();
  }
  
  // 6. Install
  return await installPlugin(archive, manifest);
}
```

### Conflict Detection

```typescript
interface ConflictChecker {
  // API conflict: iki mod aynı API'yi sağlıyor
  checkApiConflicts(manifest: Manifest): Conflict[];
  
  // Resource conflict: aynı kaynağı kullanıyor
  checkResourceConflicts(manifest: Manifest): Conflict[];
  
  // Explicit conflict: manifest'te belirtilmiş
  checkExplicitConflicts(manifest: Manifest): Conflict[];
}

// Kullanıcı uyarısı
interface ConflictWarning {
  type: 'api' | 'resource' | 'explicit';
  severity: 'warning' | 'error';
  message: string;
  resolution: string[];  // Çözüm önerileri
}
```

---

## 🎮 WINDOWS CAPTURE MOD (WinAPI)

### DXGI Desktop Duplication

```python
# plugins/core/capture-winapi/src/dxgi_capture.py

class DXGICapture:
    """
    Windows Desktop Duplication API kullanarak ekran yakalama.
    - Düşük CPU kullanımı
    - GPU accelerated
    - Game Bar uyumlu
    """
    
    async def initialize(self):
        self.d3d_device = await self._create_d3d_device()
        self.dxgi_output = await self._get_output()
        self.duplication = await self.dxgi_output.DuplicateOutput(self.d3d_device)
    
    async def capture_frame(self) -> Frame:
        resource, info = await self.duplication.AcquireNextFrame(timeout=100)
        texture = resource.QueryInterface(ID3D11Texture2D)
        # ... frame processing
        return Frame(texture, info.LastPresentTime)
```

### Game Bar Integration

```python
# Windows.Gaming.Capture API
class GameBarCapture:
    """
    Windows Game Bar API kullanarak oyun yakalama.
    - Oyun içi overlay desteği
    - HDR desteği
    - Minimal performans etkisi
    """
    
    async def start_capture(self, window_handle: int):
        capture_item = await GraphicsCaptureItem.CreateFromWindowAsync(window_handle)
        self.session = GraphicsCaptureSession(capture_item)
        self.session.StartCapture()
```

---

## ✅ YAPILMASI GEREKENLER (CHECKLIST)

### Core Modlar
- [ ] `core.runtime` — Mod yaşam döngüsü, IPC, izinler
- [ ] `core.capture-ffmpeg` — FFmpeg tabanlı kayıt
- [ ] `core.capture-winapi` — Windows native kayıt
- [ ] `core.codec` — Codec yönetimi
- [ ] `core.ai-local` — Lokal AI runtime
- [ ] `core.ai-cloud` — Cloud AI adapter
- [ ] `core.metadata` — Metadata üretimi
- [ ] `core.clip-editor` — Clip düzenleme
- [ ] `core.template-engine` — Video şablonları
- [ ] `core.social-publisher` — Sosyal medya yayını
- [ ] `core.marketplace` — Mod mağazası
- [ ] `core.ui-shell` — Ana UI
- [ ] `core.dev-panel` — Geliştirici paneli
- [ ] `core.storage` — Veritabanı ve config

### Özellikler
- [ ] Otomatik highlight tespiti
- [ ] AI metadata üretimi (başlık, etiket, açıklama)
- [ ] Çoklu codec desteği (H.264, H.265, AV1)
- [ ] Replay buffer
- [ ] Montaj oluşturma
- [ ] AI altyazı
- [ ] Template sistemi
- [ ] Multi-platform export
- [ ] Sosyal medya entegrasyonu

### Güvenlik
- [ ] Process isolation
- [ ] Permission system
- [ ] Filesystem jail
- [ ] Resource quotas
- [ ] Audit logging
- [ ] Signature verification

### UI/UX
- [ ] Modern, responsive tasarım
- [ ] Dark/Light tema
- [ ] Accessibility (a11y)
- [ ] Keyboard shortcuts
- [ ] Localization (10+ dil)
- [ ] Dev panel

---

## 🚫 YAPMAMAN GEREKENLER

1. **HARDCODE YASAK**
   - Plugin logic'i core'a gömme
   - Path'leri hardcode etme
   - Config değerlerini kodda tutma

2. **BYPASS YASAK**
   - Permission kontrollerini atlama
   - Sandbox'ı delme
   - Audit logging'i kapatma

3. **MONOLİT YASAK**
   - Tek dosyada tüm logic
   - God class'lar
   - Circular dependency

4. **GÜVENSİZ API YASAK**
   - Raw OS handle expose etme
   - Arbitrary process spawn
   - Unvalidated user input

---

## 🎯 SONUÇ

Bu doküman, **ClipShot** projesinin tek ve yetkili referansıdır. 

Proje şunları hedefliyor:
- ✅ Powder AI'dan daha güçlü AI özellikleri
- ✅ Streamlabs'tan daha iyi modlanabilirlik
- ✅ OBS'den daha kolay kullanım
- ✅ Tüm rakiplerden daha güvenli

**Bu doküman diğer tüm dokümanları geçersiz kılar.**
