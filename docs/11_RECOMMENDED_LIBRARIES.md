# 📚 RECOMMENDED LIBRARIES & TOOLS — CLIPSHOT

> Araştırma sonuçlarına dayanan, ClipShot geliştirmede kullanılabilecek hazır kütüphane, tool ve framework önerileri.

---

## 📋 İÇİNDEKİLER

1. [FFI Bridge Kütüphaneleri](#-ffi-bridge-kütüphaneleri)
2. [Masaüstü Uygulama Framework'leri](#-masaüstü-uygulama-frameworkleri)
3. [Video/Audio İşleme](#-videoaudio-i̇şleme)
4. [UI Kütüphaneleri](#-ui-kütüphaneleri)
5. [AI/ML Runtime](#-aiml-runtime)
6. [Ekran Yakalama](#-ekran-yakalama)
7. [Diğer Faydalı Kütüphaneler](#-diğer-faydalı-kütüphaneler)
8. [Teknoloji Stack Özeti](#-teknoloji-stack-özeti)

---

## 🔗 FFI BRIDGE KÜTÜPHANELERİ

### PyO3 — Rust → Python

> **Öneri: ✅ YÜKSEK**

Rust ile yazılmış native modüllerin Python'a expose edilmesi için en iyi seçenek.

| Özellik | Değer |
|---------|-------|
| **Web** | https://pyo3.rs |
| **Repo** | https://github.com/PyO3/pyo3 |
| **Kullanıcılar** | polars, tiktoken, pydantic-core, ruff, cryptography |
| **Build Tool** | maturin |
| **Python ABI** | abi3 (stable ABI) desteği |

```toml
# Cargo.toml
[dependencies]
pyo3 = { version = "0.22", features = ["extension-module", "abi3-py311"] }

[build-dependencies]
pyo3-build-config = "0.22"
```

**Neden PyO3?**
- Rust'ın memory safety garantileri
- Async/await desteği (tokio ile)
- Zero-copy buffer sharing mümkün
- Python exception'ları Rust'ta handle edilebilir
- Major projeler tarafından production'da kullanılıyor

---

### pybind11 — C++ → Python

> **Öneri: ✅ YÜKSEK**

C++ kodunu Python'a bağlamak için hafif (~4K LOC) header-only kütüphane.

| Özellik | Değer |
|---------|-------|
| **Web** | https://pybind11.readthedocs.io |
| **Repo** | https://github.com/pybind/pybind11 |
| **Boyut** | ~4,000 satır kod |
| **C++ Versiyon** | C++11-23 desteği |

```cpp
#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int a, int b) { return a + b; }

PYBIND11_MODULE(example, m) {
    m.def("add", &add, "Add two numbers");
}
```

**Neden pybind11?**
- Basit, temiz syntax
- STL container otomatik dönüşüm
- NumPy buffer protocol desteği
- CMake entegrasyonu kolay

---

### cffi — C → Python

> **Öneri: ✅ ORTA**

Pure C kütüphanelerini Python'a bağlamak için.

| Özellik | Değer |
|---------|-------|
| **Web** | https://cffi.readthedocs.io |
| **Repo** | https://github.com/python-cffi/cffi |
| **Kullanım** | C header parse edip binding oluşturur |

```python
from cffi import FFI
ffi = FFI()

ffi.cdef("""
    int add(int a, int b);
""")

lib = ffi.dlopen("./mylib.dll")
result = lib.add(1, 2)
```

**Neden cffi?**
- Pure C projeler için ideal
- Header tanımları ile binding
- ABI ve API mode destekler

---

### CXX.rs — Rust ↔ C++

> **Öneri: ✅ YÜKSEK**

Rust ve C++ arasında güvenli, zero-cost FFI.

| Özellik | Değer |
|---------|-------|
| **Web** | https://cxx.rs |
| **Repo** | https://github.com/dtolnay/cxx |
| **Performans** | Zero/minimal overhead |

```rust
// Rust side
#[cxx::bridge]
mod ffi {
    extern "C++" {
        include!("mylib.h");
        fn process_frame(data: &[u8]) -> Vec<u8>;
    }
}
```

**Neden CXX?**
- Compile-time type checking
- Otomatik memory management
- C++ exception safety

---

### abi_stable — Rust ↔ Rust FFI

> **Öneri: ✅ ORTA**

Farklı Rust compiler versiyonları arasında ABI uyumluluğu sağlar.

| Özellik | Değer |
|---------|-------|
| **Web** | https://docs.rs/abi_stable |
| **Repo** | https://github.com/rodrimati1992/abi_stable_crates |
| **Kullanım** | Plugin sistemleri |

**Neden abi_stable?**
- Rust plugin'leri farklı versiyonlarda derlenebilir
- Runtime type checking
- Stabil ABI garantisi

---

## 🖥️ MASAÜSTÜ UYGULAMA FRAMEWORK'LERİ

### Tauri — Ana Desktop Framework

> **Öneri: ✅ YÜKSEK (MEVCUT STACK)**

Rust-tabanlı, güvenli, hafif ve native performanslı desktop framework.

| Özellik | Değer |
|---------|-------|
| **Web** | https://tauri.app |
| **Dil** | Rust (backend) + TypeScript (frontend) |
| **UI** | Vite + React/Vue/Svelte |
| **Bundle Size** | ~3-5MB (native webview kullanır) |
| **Versiyon** | v2.0+ (2024+) |

**Avantajlar:**
- ✅ 40x daha küçük bundle (~3MB vs ~150MB)
- ✅ Daha düşük memory kullanımı
- ✅ Native webview (Chromium bundle'a gerek yok)
- ✅ Rust security guarantees
- ✅ Native Rust plugin sistemi entegrasyonu
- ✅ Tauri CLI ile kolay build/dev
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Mobile support (iOS/Android - beta)
- ✅ Hot module replacement (Vite ile)

**Dezavantajlar:**
- ⚠️ Daha yeni ekosistem (Electron'dan küçük)
- ⚠️ Native build gereksinimleri (Rust toolchain)

**Native Plugin Entegrasyonu:**
```rust
// Tauri Command (Rust backend)
#[tauri::command]
async fn load_native_plugin(plugin_path: String) -> Result<String, String> {
    // Native plugin loading logic
    Ok("Plugin loaded".to_string())
}
```

**Neden Tauri?**
- ClipShot zaten Rust native plugin sistemi kullanıyor
- PyO3 bridge Tauri Rust backend ile uyumlu
- Daha küçük ve hızlı uygulamalar
- Security-first design
- Modern web teknolojileri (Vite, HMR)

---

### Vite — Frontend Build Tool

> **Öneri: ✅ ZORUNLU**

Next-generation frontend build tool, lightning-fast HMR.

| Özellik | Değer |
|---------|-------|
| **Web** | https://vitejs.dev |
| **Kullanım** | Development server + production build |
| **HMR** | <100ms |
| **Plugin Sistemi** | Zengin plugin ekosistemi |

**Özellikler:**
- ⚡ Instant server start
- ⚡ Lightning-fast HMR
- 📦 Optimized production builds
- 🔌 Plugin-based architecture
- 🎨 CSS/SCSS/PostCSS support
- 📱 Multi-framework support (React/Vue/Svelte)

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  clearScreen: false,
  server: {
    port: 5173,
    strictPort: true,
  },
  envPrefix: ['VITE_', 'TAURI_'],
})
```

---

### Electron — Legacy

> **Öneri: ❌ KULLANILMIYOR (Tauri ile değiştirildi)**

| Özellik | Değer |
|---------|-------|
| **Web** | https://electronjs.org |
| **Bundle Size** | ~150MB |
| **Neden değiştirildi?** | Tauri daha küçük, hızlı ve güvenli |

**ClipShot Tauri'ye geçiş nedenleri:**
- 40x daha küçük bundle size
- Native Rust plugin sistemi ile doğrudan uyumlu
- Daha düşük memory footprint
- Modern security model

---

### Neutralino.js — Lightweight Alternatif

> **Öneri: 🔸 REFERANS**

System webview kullanan çok hafif alternatif.

| Özellik | Değer |
|---------|-------|
| **Web** | https://neutralino.js.org |
| **Bundle Size** | ~2MB |
| **Runtime** | No Node.js |

**Avantajlar:**
- Çok küçük boyut
- Hızlı başlangıç
- Basit mimari

**Dezavantajlar:**
- Sınırlı native API
- Küçük ekosistem

---

## 🎬 VIDEO/AUDIO İŞLEME

### FFmpeg

> **Öneri: ✅ YÜKSEK**

Video/audio işleme için endüstri standardı.

| Özellik | Değer |
|---------|-------|
| **Web** | https://ffmpeg.org |
| **Versiyon** | 8.0+ önerilir |
| **Özellikler** | Vulkan compute, AV1, HW encode |

**FFmpeg 8.0 Yenilikleri:**
- Vulkan AV1 decoder (vulkan_av1)
- Pure Vulkan compute shaders
- OpenHarmony H.264/H.265 decoders
- Mali GPU VVC decoding
- Improved hardware encoding

**Rust Binding:**
```toml
[dependencies]
ffmpeg-next = "7.0"
```

**Python Binding:**
```bash
pip install ffmpeg-python
```

---

### SDL3

> **Öneri: ✅ ORTA**

Cross-platform multimedia layer.

| Özellik | Değer |
|---------|-------|
| **Web** | https://libsdl.org |
| **Repo** | https://github.com/libsdl-org/SDL |
| **Kullanım** | Audio, input, window management |

**Avantajlar:**
- Düşük seviye erişim
- Cross-platform
- Oyun motorlarında yaygın

---

## 🎨 UI KÜTÜPHANELERİ

### Clay — High-Performance UI Layout

> **Öneri: 🔶 ORTA (Değerlendirme)**

Microsecond performanslı UI layout engine.

| Özellik | Değer |
|---------|-------|
| **Repo** | https://github.com/nicbarker/clay |
| **Boyut** | ~4,000 LOC single header |
| **Performans** | Microsecond layout |
| **Bağımlılık** | Sıfır |

```c
CLAY({
    .layout = { 
        .sizing = { CLAY_SIZING_GROW(), CLAY_SIZING_FIXED(50) },
        .padding = { 16, 16 },
        .childGap = 8
    }
}) {
    CLAY_TEXT("Hello World", CLAY_TEXT_CONFIG({
        .fontId = FONT_BODY,
        .fontSize = 24,
        .textColor = {255, 255, 255, 255}
    }));
}
```

**Özellikler:**
- React-like declarative syntax
- Flexbox benzeri layout
- WASM desteği
- Renderer agnostic (SDL, OpenGL, Metal, WebGL)

**Kullanım Alanı:**
- Overlay UI
- In-app widgets
- Performance-critical panels

---

### React + Electron (Mevcut)

> **Öneri: ✅ YÜKSEK (Mevcut Stack)**

| Özellik | Değer |
|---------|-------|
| **Kullanım** | Ana uygulama UI |
| **State** | Zustand/Jotai |
| **Styling** | Tailwind CSS |

---

## 🤖 AI/ML RUNTIME

### llama.cpp

> **Öneri: ✅ YÜKSEK**

Lokal LLM inference için hafif C++ kütüphanesi.

| Özellik | Değer |
|---------|-------|
| **Repo** | https://github.com/ggerganov/llama.cpp |
| **Format** | GGUF |
| **Quantization** | 2-8 bit |
| **Backend** | CPU, CUDA, Metal, Vulkan |

**Python Binding:**
```bash
pip install llama-cpp-python
```

---

### ONNX Runtime

> **Öneri: ✅ YÜKSEK**

Cross-platform ML inference.

| Özellik | Değer |
|---------|-------|
| **Web** | https://onnxruntime.ai |
| **Format** | ONNX |
| **Backend** | CPU, CUDA, DirectML, TensorRT |

```python
import onnxruntime as ort

session = ort.InferenceSession("model.onnx", providers=['CUDAExecutionProvider'])
```

---

### Ollama

> **Öneri: ✅ YÜKSEK (Self-host)**

Kolay LLM deployment.

| Özellik | Değer |
|---------|-------|
| **Web** | https://ollama.ai |
| **API** | OpenAI compatible |
| **Modeller** | Llama, Mistral, Phi, etc. |

```python
import openai

client = openai.OpenAI(base_url="http://localhost:11434/v1")
```

---

## 📸 EKRAN YAKALAMA

### Windows (DXGI/Desktop Duplication API)

> **Öneri: ✅ YÜKSEK**

Windows'ta en performanslı capture yöntemi.

**Rust Crate:**
```toml
[dependencies]
windows = { version = "0.58", features = ["Win32_Graphics_Dxgi", "Win32_Graphics_Direct3D11"] }
```

**C++ Header:**
```cpp
#include <dxgi1_2.h>
#include <d3d11.h>
```

---

### scap (Rust)

> **Öneri: ✅ ORTA**

Cross-platform screen capture.

| Özellik | Değer |
|---------|-------|
| **Repo** | https://github.com/MirrorX-Desktop/scap |
| **Platform** | Windows, macOS, Linux |

---

## 🔧 DİĞER FAYDALI KÜTÜPHANELER

### Async Runtime

| Kütüphane | Dil | Kullanım |
|-----------|-----|----------|
| **tokio** | Rust | Async runtime |
| **asyncio** | Python | Async I/O |
| **uvloop** | Python | Hızlı event loop |

### Serialization

| Kütüphane | Dil | Format |
|-----------|-----|--------|
| **serde** | Rust | JSON, TOML, YAML, etc. |
| **pydantic** | Python | JSON, validation |

### Logging

| Kütüphane | Dil | Özellik |
|-----------|-----|---------|
| **tracing** | Rust | Structured logging |
| **loguru** | Python | Modern logging |
| **structlog** | Python | Structured logging |

### Image Processing

| Kütüphane | Dil | Kullanım |
|-----------|-----|----------|
| **image** | Rust | Image manipulation |
| **Pillow** | Python | Image processing |
| **opencv** | Python/C++ | Computer vision |

### HTTP Client

| Kütüphane | Dil | Kullanım |
|-----------|-----|----------|
| **reqwest** | Rust | HTTP client |
| **httpx** | Python | Async HTTP |
| **aiohttp** | Python | Async HTTP |

---

## 📊 TEKNOLOJİ STACK ÖZETİ

### Önerilen Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                  │
│  Electron + React + TypeScript + Tailwind                        │
│  (Gelecekte Tauri değerlendirilebilir)                           │
├─────────────────────────────────────────────────────────────────┤
│                        BACKEND                                   │
│  FastAPI (Python) + Pydantic + SQLAlchemy                       │
├─────────────────────────────────────────────────────────────────┤
│                    NATIVE PLUGINS                                │
│  Rust (PyO3) — Primary choice for performance                   │
│  C++ (pybind11) — Legacy/existing code integration               │
│  C (cffi) — Low-level system APIs                                │
├─────────────────────────────────────────────────────────────────┤
│                    VIDEO PROCESSING                              │
│  FFmpeg (8.0+) — Primary video/audio                             │
│  SDL3 — Audio playback, input                                    │
├─────────────────────────────────────────────────────────────────┤
│                    AI RUNTIME                                    │
│  llama.cpp — Local LLM                                           │
│  ONNX Runtime — ML inference                                     │
│  Ollama — Self-hosted LLM                                        │
│  OpenAI/Anthropic — Cloud AI (optional)                          │
├─────────────────────────────────────────────────────────────────┤
│                    SCREEN CAPTURE                                │
│  DXGI Desktop Duplication — Windows                              │
│  FFmpeg avdevice — Cross-platform fallback                       │
└─────────────────────────────────────────────────────────────────┘
```

### Kütüphane Öncelik Sıralaması

| Öncelik | Kütüphane | Kullanım Alanı |
|---------|-----------|----------------|
| 1 | **PyO3 + maturin** | Rust native plugin'ler |
| 2 | **FFmpeg** | Video işleme |
| 3 | **llama.cpp** | Lokal AI |
| 4 | **ONNX Runtime** | ML inference |
| 5 | **pybind11** | C++ entegrasyonu |
| 6 | **tokio** | Rust async |
| 7 | **DXGI** | Windows capture |
| 8 | **Tauri** | Gelecek frontend (değerlendirme) |

---

## 🔗 YARARLI LİNKLER

### Dokümantasyon

- [PyO3 Guide](https://pyo3.rs/main/)
- [maturin Tutorial](https://maturin.rs/)
- [pybind11 Docs](https://pybind11.readthedocs.io/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Tauri Guides](https://tauri.app/v1/guides/)

### Örnek Projeler

- **polars** — PyO3 kullanımı için mükemmel örnek
- **tiktoken** — OpenAI'ın tokenizer'ı (PyO3)
- **SWC** — JavaScript compiler (NAPI-RS/Rust)
- **ruff** — Python linter (Rust + PyO3)

---

**Önceki:** [10_NATIVE_PLUGIN_GUIDE.md](./10_NATIVE_PLUGIN_GUIDE.md) — Native Plugin Rehberi
