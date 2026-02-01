# 🧩 PLUGIN DEVELOPER GUIDE — CLIPSHOT

> Bu dokuman, ClipShot için mod geliştiricilere yönelik kapsamlı bir rehberdir.

---

## 📋 İÇİNDEKİLER

1. [Giriş](#-giriş)
2. [Plugin Felsefesi](#-plugin-felsefesi)
3. [Plugin Yapısı](#-plugin-yapısı)
4. [Manifest Spesifikasyonu](#-manifest-spesifikasyonu)
5. [Permission Sistemi](#-permission-sistemi)
6. [Plugin Yaşam Döngüsü](#-plugin-yaşam-döngüsü)
7. [API Entegrasyonu](#-api-entegrasyonu)
8. [UI Geliştirme](#-ui-geliştirme)
9. [Lokalizasyon](#-lokalizasyon)
10. [Test Etme](#-test-etme)
11. [Yayınlama](#-yayınlama)

---

## 🎯 GİRİŞ

ClipShot'ta **her şey bir plugin**dir — kayıt sistemi, AI, UI panelleri, codec yönetimi dahil. Bu rehber, kendi mod'unuzu nasıl geliştireceğinizi açıklar.

### Temel Kurallar

1. **Global state YASAK** — Plugin'ler izole çalışır
2. **Hardcoded path YASAK** — Dinamik path kullanın
3. **Network varsayılan KAPALI** — Açıkça talep edilmeli
4. **OpenAPI sözleşmesi ZORUNLU** — Tüm endpoint'ler dokümante
5. **Lokalizasyon ZORUNLU** — Tüm string'ler i18n key

---

## 💡 PLUGIN FELSEFESİ

### Core ≠ Ayrıcalıklı

```
┌─────────────────────────────────────────────┐
│  Core Plugin'ler = Bundled + Trusted        │
│  Community Plugin'ler = Installed + Verified │
│                                             │
│  İKİSİ DE AYNI KURALLARA TABİ               │
└─────────────────────────────────────────────┘
```

### Puzzle Piece Architecture

Her plugin bir yapboz parçası gibi:
- Bağımsız çalışabilir
- Başka parçalarla birleşebilir
- Çıkarılabilir/değiştirilebilir

```
┌────────┐ ┌────────┐ ┌────────┐
│Capture │ │  AI    │ │ Editor │
│ Plugin │ │ Plugin │ │ Plugin │
└───┬────┘ └───┬────┘ └───┬────┘
    │          │          │
    └──────────┼──────────┘
               ↓
        ┌──────────────┐
        │ Core Runtime │
        └──────────────┘
```

---

## 📁 PLUGIN YAPISI

### Minimum Yapı

```
my-plugin/
├── manifest.json          # ✅ Zorunlu - Plugin tanımı
├── src/
│   └── main.py            # ✅ Zorunlu - Entry point
├── locales/
│   └── en.json            # ✅ Zorunlu - En az İngilizce
└── README.md              # 🔶 Önerilen - Dokümantasyon
```

### Tam Yapı

```
my-plugin/
├── manifest.json          # Plugin manifest
├── config.schema.json     # Config validation schema
├── src/
│   ├── main.py            # Backend entry
│   ├── handlers.py        # Event handlers
│   ├── services/
│   │   └── my_service.py
│   └── utils/
│       └── helpers.py
├── ui/                    # Frontend components
│   ├── index.tsx          # UI entry
│   ├── SettingsPanel.tsx
│   └── components/
│       └── CustomWidget.tsx
├── locales/
│   ├── en.json
│   ├── tr.json
│   ├── de.json
│   └── ...
├── tests/
│   ├── test_main.py
│   └── test_services.py
├── assets/
│   └── icon.png
├── LICENSE
└── README.md
```

---

## 📜 MANIFEST SPESİFİKASYONU

### Tam Manifest Örneği

```json
{
  "$schema": "https://clipshot.io/schemas/manifest.v2.schema.json",
  
  "id": "com.yourname.my-awesome-plugin",
  "name": "My Awesome Plugin",
  "version": "1.0.0",
  "api_version": "v1",
  
  "type": "optional",
  "category": "enhancement",
  
  "description": {
    "en": "This plugin does amazing things",
    "tr": "Bu plugin harika şeyler yapar"
  },
  
  "author": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/yourname"
  },
  
  "repository": "https://github.com/yourname/my-awesome-plugin",
  "license": "MIT",
  "homepage": "https://yourplugin.com",
  "bugs": "https://github.com/yourname/my-awesome-plugin/issues",
  
  "keywords": ["enhancement", "utility", "gaming"],
  
  "entry": {
    "backend": "src/main.py",
    "frontend": "ui/index.tsx"
  },
  
  "permissions": {
    "screen": {
      "level": "none"
    },
    "microphone": {
      "level": "none"
    },
    "filesystem": {
      "level": "limited",
      "paths": ["$PLUGIN_DATA"],
      "reason": {
        "en": "Store plugin settings",
        "tr": "Plugin ayarlarını sakla"
      }
    },
    "network": {
      "level": "optional",
      "hosts": ["api.example.com"],
      "reason": {
        "en": "Sync data with cloud",
        "tr": "Bulut ile veri senkronizasyonu"
      }
    },
    "gpu": {
      "level": "none"
    },
    "system": {
      "level": "none"
    }
  },
  
  "capabilities": [
    "custom_feature_a",
    "custom_feature_b"
  ],
  
  "provides": [
    "myapi.v1"
  ],
  
  "requires": [
    "core.events.api.v1"
  ],
  
  "conflicts": [],
  
  "settings": {
    "schema": "config.schema.json",
    "defaults": {
      "enabled": true,
      "refreshInterval": 30
    }
  },
  
  "ui": {
    "settingsPanel": true,
    "toolbar": false,
    "sidebar": true,
    "overlay": false
  },
  
  "localization": {
    "supported": ["en", "tr"],
    "fallback": "en",
    "path": "locales/"
  },
  
  "resources": {
    "cpu": {
      "max_percent": 5
    },
    "memory": {
      "max_mb": 128
    },
    "gpu": {
      "max_percent": 0
    }
  },
  
  "security": {
    "sandbox": "standard",
    "audit": true
  },
  
  "platforms": ["windows"],
  
  "engines": {
    "clipshot": ">=1.0.0",
    "python": ">=3.11",
    "node": ">=20.0.0"
  }
}
```

### Manifest Alanları Açıklaması

#### Temel Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | string | ✅ | Unique identifier (reverse domain) |
| `name` | string | ✅ | Display name |
| `version` | string | ✅ | Semantic versioning (X.Y.Z) |
| `api_version` | string | ✅ | ClipShot API version |
| `type` | string | ✅ | `core`, `optional`, `ai`, `ui`, `system` |
| `category` | string | ✅ | `capture`, `ai`, `editor`, `social`, `enhancement` |

#### Plugin Types

```typescript
type PluginType = 
  | 'core'      // Bundled, değiştirilebilir
  | 'optional'  // İsteğe bağlı eklenti
  | 'ai'        // AI model/runtime
  | 'ui'        // UI component
  | 'system';   // System-level eklenti
```

#### Plugin Categories

```typescript
type PluginCategory = 
  | 'capture'      // Kayıt sistemleri
  | 'ai'           // AI/ML özellikleri
  | 'editor'       // Düzenleme araçları
  | 'social'       // Sosyal medya
  | 'enhancement'  // Genel iyileştirmeler
  | 'codec'        // Codec/format
  | 'template'     // Video şablonları
  | 'analytics';   // Analitik araçları
```

---

## 🛡️ PERMISSION SİSTEMİ

### Permission Kategorileri

```typescript
interface Permissions {
  screen: PermissionEntry;       // Ekran yakalama
  microphone: PermissionEntry;   // Mikrofon erişimi
  filesystem: FilesystemPermission;  // Dosya sistemi
  network: NetworkPermission;    // Ağ erişimi
  gpu: PermissionEntry;          // GPU kullanımı
  system: SystemPermission;      // Sistem API'leri
  clipboard: PermissionEntry;    // Pano erişimi
  notifications: PermissionEntry; // Bildirimler
}
```

### Permission Seviyeleri

```typescript
type PermissionLevel = 
  | 'none'      // İzin yok (default)
  | 'limited'   // Sınırlı erişim
  | 'optional'  // Kullanıcı onayı ile
  | 'required'; // Zorunlu (mod çalışmaz yoksa)
```

### Filesystem Permission

```json
{
  "filesystem": {
    "level": "limited",
    "paths": [
      "$PLUGIN_DATA",    // Plugin özel dizin
      "$CLIPS",          // Clip dizini (read-only)
      "$TEMP",           // Geçici dosyalar
      "$CONFIG"          // Config dizini
    ],
    "operations": ["read", "write"],
    "reason": {
      "en": "Required to save processed clips"
    }
  }
}
```

### Network Permission

```json
{
  "network": {
    "level": "optional",
    "hosts": [
      "api.example.com",
      "*.cloudflare.com"
    ],
    "protocols": ["https"],
    "reason": {
      "en": "Upload clips to cloud storage"
    }
  }
}
```

### System Permission

```json
{
  "system": {
    "level": "limited",
    "apis": [
      "dxgi",           // DirectX Graphics
      "d3d11",          // Direct3D 11
      "gamebar",        // Windows Game Bar
      "media_foundation" // Windows Media Foundation
    ],
    "reason": {
      "en": "Required for hardware-accelerated capture"
    }
  }
}
```

### İzin İsteme Akışı

```
Plugin Kurulum
      │
      ▼
┌─────────────────────────────┐
│  Manifest İzinleri Okunur   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  İzin Diyaloğu Gösterilir   │
│                             │
│  ┌───────────────────────┐  │
│  │ 📁 Dosya Sistemi      │  │
│  │ ☑ Clips dizinine yazma│  │
│  │                       │  │
│  │ 🌐 İnternet           │  │
│  │ ☐ api.example.com     │  │
│  │ (isteğe bağlı)        │  │
│  └───────────────────────┘  │
│                             │
│    [Reddet]  [Kabul Et]     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  İzinler Veritabanına       │
│  Kaydedilir                 │
└──────────────┬──────────────┘
               │
               ▼
      Plugin Aktifleştirilir
```

---

## 🔄 PLUGIN YAŞAM DÖNGÜSÜ

### State Machine

```
┌─────────────┐
│  INSTALLED  │ ← GitHub'dan/Manuel kurulum
└──────┬──────┘
       │ validate()
       ▼
┌─────────────┐
│  VALIDATED  │ ← Manifest doğrulandı
└──────┬──────┘
       │ user_approve_permissions()
       ▼
┌─────────────┐
│  APPROVED   │ ← İzinler onaylandı
└──────┬──────┘
       │ initialize()
       ▼
┌─────────────┐
│ INITIALIZED │ ← Dependencies hazır
└──────┬──────┘
       │ start()
       ▼
┌─────────────┐
│   RUNNING   │ ← Aktif çalışıyor
└──────┬──────┘
       │ stop() / error
       ▼
┌─────────────┐
│   STOPPED   │ ← Durduruldu
└──────┬──────┘
       │ uninstall()
       ▼
┌─────────────┐
│  UNINSTALLED│
└─────────────┘
```

### Lifecycle Hooks

```python
# src/main.py

from clipshot.plugin import Plugin, PluginContext

class MyPlugin(Plugin):
    """My awesome plugin implementation."""
    
    async def on_load(self, context: PluginContext) -> None:
        """
        Plugin yüklendiğinde çağrılır.
        - Config oku
        - Kaynakları hazırla
        - Dependencies kontrol et
        """
        self.config = await context.get_config()
        self.logger = context.get_logger()
        self.logger.info("Plugin loading...")
    
    async def on_start(self) -> None:
        """
        Plugin başlatıldığında çağrılır.
        - Event listener'ları kaydet
        - Background task'ları başlat
        """
        await self.register_event_handlers()
        self.logger.info("Plugin started!")
    
    async def on_stop(self) -> None:
        """
        Plugin durdurulduğunda çağrılır.
        - Kaynakları serbest bırak
        - Event listener'ları kaldır
        - Cleanup yap
        """
        await self.cleanup()
        self.logger.info("Plugin stopped!")
    
    async def on_unload(self) -> None:
        """
        Plugin kaldırıldığında çağrılır.
        - Tüm verileri temizle
        - Kalıcı state'i kaydet
        """
        await self.save_state()
        self.logger.info("Plugin unloaded!")
    
    async def on_config_changed(self, new_config: dict) -> None:
        """
        Config değiştiğinde çağrılır.
        - Hot-reload destekle
        """
        self.config = new_config
        await self.apply_config()
```

---

## 🔌 API ENTEGRASYONU

### API Kayıt Etme

Plugin'ler kendi API'lerini kaydedebilir:

```python
from clipshot.plugin import Plugin, api_route
from pydantic import BaseModel

class MyRequest(BaseModel):
    data: str

class MyResponse(BaseModel):
    result: str

class MyPlugin(Plugin):
    
    @api_route("/my-endpoint", methods=["POST"])
    async def my_endpoint(self, request: MyRequest) -> MyResponse:
        """
        Custom endpoint.
        
        Bu endpoint otomatik olarak şu adreste erişilebilir:
        POST /api/v1/plugins/com.yourname.my-plugin/my-endpoint
        """
        result = await self.process(request.data)
        return MyResponse(result=result)
    
    @api_route("/status", methods=["GET"])
    async def get_status(self) -> dict:
        """Plugin status endpoint."""
        return {
            "status": "healthy",
            "uptime": self.get_uptime()
        }
```

### Core API'leri Kullanma

```python
from clipshot.plugin import Plugin
from clipshot.api import (
    CaptureAPI,
    ClipAPI,
    MetadataAPI,
    EventBus
)

class MyPlugin(Plugin):
    
    async def on_start(self):
        # Capture API kullan
        self.capture = await self.get_api(CaptureAPI)
        
        # Event bus'a abone ol
        self.events = await self.get_api(EventBus)
        await self.events.subscribe("clip.created", self.on_clip_created)
    
    async def on_clip_created(self, event: ClipCreatedEvent):
        """Yeni clip oluştuğunda çağrılır."""
        clip = event.clip
        
        # Metadata API ile metadata üret
        metadata_api = await self.get_api(MetadataAPI)
        metadata = await metadata_api.generate(clip.id)
        
        self.logger.info(f"Metadata generated: {metadata}")
```

### Provides & Requires

```json
{
  "provides": [
    "myfeature.api.v1"
  ],
  "requires": [
    "core.events.api.v1",
    "core.clips.api.v1"
  ]
}
```

Plugin yüklenirken, tüm `requires` API'lerinin mevcut olduğu kontrol edilir.

---

## 🖥️ UI GELİŞTİRME

### UI Slot'ları

```typescript
type UISlot = 
  | 'toolbar'           // Ana araç çubuğu
  | 'sidebar'           // Yan panel
  | 'settings-tab'      // Ayarlar sekmesi
  | 'clip-editor'       // Clip editör alanı
  | 'overlay'           // Oyun üstü overlay
  | 'context-menu'      // Sağ tık menüsü
  | 'status-bar'        // Durum çubuğu
  | 'modal'             // Modal pencereler
  | 'dashboard-widget'; // Dashboard widget
```

### React Component Örneği

```tsx
// ui/SettingsPanel.tsx

import React from 'react';
import { usePluginConfig, useTranslation } from '@clipshot/ui';

interface Props {
  pluginId: string;
}

export const SettingsPanel: React.FC<Props> = ({ pluginId }) => {
  const { config, updateConfig } = usePluginConfig(pluginId);
  const { t } = useTranslation(pluginId);
  
  return (
    <div className="plugin-settings">
      <h2>{t('settings.title')}</h2>
      
      <div className="setting-item">
        <label>{t('settings.enabled')}</label>
        <input
          type="checkbox"
          checked={config.enabled}
          onChange={(e) => updateConfig({ enabled: e.target.checked })}
        />
      </div>
      
      <div className="setting-item">
        <label>{t('settings.refreshInterval')}</label>
        <input
          type="number"
          value={config.refreshInterval}
          onChange={(e) => updateConfig({ refreshInterval: Number(e.target.value) })}
        />
      </div>
    </div>
  );
};

// Export metadata
export const metadata = {
  slot: 'settings-tab',
  priority: 100,
  icon: 'settings'
};
```

### UI Entry Point

```tsx
// ui/index.tsx

import { SettingsPanel } from './SettingsPanel';
import { ToolbarButton } from './ToolbarButton';
import { SidebarPanel } from './SidebarPanel';

export const components = {
  'settings-tab': SettingsPanel,
  'toolbar': ToolbarButton,
  'sidebar': SidebarPanel,
};
```

---

## 🌍 LOKALİZASYON

### Locale Dosyası Formatı (ICU)

```json
// locales/tr.json
{
  "plugin": {
    "name": "Harika Plugin",
    "description": "Bu plugin harika şeyler yapar"
  },
  "settings": {
    "title": "Ayarlar",
    "enabled": "Aktif",
    "refreshInterval": "Yenileme Aralığı (saniye)"
  },
  "messages": {
    "clipCount": "{count, plural, =0 {Clip yok} =1 {1 clip} other {# clip}}",
    "lastSync": "Son senkronizasyon: {date, date, medium}"
  },
  "errors": {
    "networkFailed": "Ağ bağlantısı başarısız",
    "invalidConfig": "Geçersiz yapılandırma"
  }
}
```

### Backend'de Kullanım

```python
from clipshot.i18n import get_translator

class MyPlugin(Plugin):
    
    async def on_start(self):
        self.t = await get_translator(self.id)
    
    async def notify_user(self, clip_count: int):
        message = self.t("messages.clipCount", count=clip_count)
        await self.send_notification(message)
```

### Frontend'de Kullanım

```tsx
import { useTranslation } from '@clipshot/ui';

const MyComponent: React.FC = () => {
  const { t, locale, setLocale } = useTranslation('com.yourname.my-plugin');
  
  return (
    <div>
      <h1>{t('plugin.name')}</h1>
      <p>{t('messages.clipCount', { count: 5 })}</p>
    </div>
  );
};
```

---

## 🧪 TEST ETME

### Unit Tests

```python
# tests/test_main.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.main import MyPlugin

@pytest.fixture
def plugin():
    return MyPlugin()

@pytest.fixture
def mock_context():
    context = MagicMock()
    context.get_config = AsyncMock(return_value={"enabled": True})
    context.get_logger = MagicMock()
    return context

@pytest.mark.asyncio
async def test_plugin_load(plugin, mock_context):
    await plugin.on_load(mock_context)
    assert plugin.config["enabled"] is True

@pytest.mark.asyncio
async def test_plugin_start(plugin, mock_context):
    await plugin.on_load(mock_context)
    await plugin.on_start()
    # Assert plugin is running
```

### Integration Tests

```python
# tests/test_integration.py

import pytest
from clipshot.testing import PluginTestHarness

@pytest.fixture
async def harness():
    harness = PluginTestHarness("com.yourname.my-plugin")
    await harness.setup()
    yield harness
    await harness.teardown()

@pytest.mark.asyncio
async def test_api_endpoint(harness):
    response = await harness.call_api("/my-endpoint", method="POST", json={"data": "test"})
    assert response.status_code == 200
    assert response.json()["result"] == "processed"
```

### Running Tests

```bash
# Plugin dizininde
cd plugins/community/my-plugin

# Testleri çalıştır
pytest tests/ -v

# Coverage ile
pytest tests/ --cov=src --cov-report=html
```

---

## 📦 YAYINLAMA

### Pre-release Checklist

- [ ] Manifest geçerli (`clipshot validate-manifest`)
- [ ] Tüm testler geçiyor
- [ ] En az İngilizce lokalizasyon var
- [ ] README.md güncel
- [ ] LICENSE dosyası var
- [ ] Security audit geçti

### GitHub Release

```yaml
# .github/workflows/release.yml

name: Release Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate Manifest
        run: |
          npx @clipshot/cli validate-manifest ./manifest.json
      
      - name: Run Tests
        run: |
          pip install -r requirements.txt
          pytest tests/ -v
      
      - name: Build Package
        run: |
          npx @clipshot/cli build-plugin .
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*.zip
          generate_release_notes: true
```

### Marketplace Submission

1. GitHub'da release oluştur
2. ClipShot Marketplace'e submit et
3. Review bekle
4. Onaylandığında yayınlanır

---

## ⚠️ YAPILAMAYACAKLAR

### Security Kısıtlamaları

```python
# ❌ YASAK - Arbitrary process spawn
import subprocess
subprocess.run(["cmd.exe", "/c", "dir"])

# ❌ YASAK - Raw file access
open("/etc/passwd", "r")

# ❌ YASAK - Network without permission
import requests
requests.get("https://evil.com")

# ❌ YASAK - Global state
GLOBAL_STATE = {}

# ✅ DOĞRU - Sandbox içinde izinli erişim
async def save_data(self, data):
    path = await self.context.get_plugin_data_path()
    async with aiofiles.open(path / "data.json", "w") as f:
        await f.write(json.dumps(data))
```

### Performans Kısıtlamaları

```python
# ❌ YASAK - Blocking main thread
time.sleep(10)

# ❌ YASAK - Infinite loop without yield
while True:
    process_data()

# ✅ DOĞRU - Async operations
async def long_task(self):
    for item in items:
        await self.process(item)
        await asyncio.sleep(0)  # Yield control
```

---

## 🦀 NATIVE PLUGIN DESTEĞİ

ClipShot, yüksek performans gerektiren işlemler için **Rust**, **C** ve **C++** ile yazılmış native plugin'leri destekler.

### Ne Zaman Native Plugin?

| Kullanım | Python | Native |
|----------|--------|--------|
| UI extension | ✅ | ❌ |
| Simple automation | ✅ | ❌ |
| Video encoding | ❌ | ✅ |
| AI inference | ❌ | ✅ |
| Image processing | ❌ | ✅ |
| Real-time filters | ❌ | ✅ |

### Desteklenen Diller ve FFI Bridge'ler

| Dil | FFI Bridge | Build Tool |
|-----|------------|------------|
| **Rust** | PyO3 | maturin |
| **C** | cffi | CMake |
| **C++** | pybind11 | CMake |

### Native Plugin Yapısı

```
my-native-plugin/
├── manifest.json           # native section eklenmiş
├── Cargo.toml              # Rust dependencies
├── pyproject.toml          # maturin config
├── src/
│   ├── lib.rs              # PyO3 entry
│   └── plugin.rs           # Core logic
├── locales/
│   └── en.json
└── README.md
```

### Manifest Native Uzantısı

```json
{
  "native": {
    "language": "rust",
    "abi_version": 1,
    "binaries": {
      "windows-x64": {
        "path": "bin/my_plugin.pyd",
        "sha256": "..."
      }
    },
    "ffi": {
      "bridge": "pyo3",
      "module_name": "my_plugin",
      "entry_class": "MyPlugin"
    }
  }
}
```

> 📖 **Detaylı rehber:** [10_NATIVE_PLUGIN_GUIDE.md](./10_NATIVE_PLUGIN_GUIDE.md)

---

## 📚 EK KAYNAKLAR

- [API Reference](/docs/API.md)
- [Example Plugins](https://github.com/clipshot/example-plugins)
- [Plugin Template](https://github.com/clipshot/plugin-template)
- [Native Plugin Guide](./10_NATIVE_PLUGIN_GUIDE.md)
- [Discord Community](https://discord.gg/clipshot)
- [Developer Forum](https://forum.clipshot.io/dev)
