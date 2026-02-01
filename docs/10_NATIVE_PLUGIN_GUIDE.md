# 🦀 NATIVE PLUGIN GUIDE — CLIPSHOT

> Rust, C ve C++ ile yüksek performanslı backend mod geliştirme rehberi. Tauri Rust backend ile doğrudan entegrasyon.

---

## 📋 İÇİNDEKİLER

1. [Giriş](#-giriş)
2. [Desteklenen Diller](#-desteklenen-diller)
3. [Native Plugin Mimarisi](#-native-plugin-mimarisi)
4. [Tauri Entegrasyonu](#-tauri-entegrasyonu)
5. [Rust Plugin Geliştirme](#-rust-plugin-geliştirme)
6. [C Plugin Geliştirme](#-c-plugin-geliştirme)
7. [C++ Plugin Geliştirme](#-c-plugin-geliştirme-1)
8. [Manifest Uzantıları](#-manifest-uzantıları)
9. [ABI Spesifikasyonu](#-abi-spesifikasyonu)
10. [Memory Safety](#-memory-safety)
11. [Build Sistemi](#-build-sistemi)
12. [Test ve Debug](#-test-ve-debug)
13. [Performans Rehberi](#-performans-rehberi)

---

## 🎯 GİRİŞ

ClipShot, yüksek performans gerektiren işlemler için **native plugin** desteği sunar. Python plugin'lerin yanı sıra **Rust**, **C** ve **C++** ile yazılmış plugin'ler de aynı standartlara uyarak çalışabilir.

**Tauri Avantajı:** ClipShot'ın Tauri (Rust) tabanlı olması sayesinde, Rust plugin'leri doğrudan Tauri backend'e entegre edilebilir, ekstra FFI overhead'i olmadan çalışır.

### Ne Zaman Native Plugin Kullanmalı?

| Kullanım Durumu | Önerilen Dil | Neden |
|-----------------|--------------|-------|
| Video işleme (encode/decode) | Rust/C++ | Zero-copy, SIMD optimizasyonları |
| Real-time AI inference | Rust/C++ | Düşük latency, memory kontrolü |
| Image processing | Rust/C | FFI overhead'siz, GPU compute |
| Audio processing | C/C++ | Low-level codec erişimi |
| Screen capture | **Rust** | DirectX/DXGI, Tauri'ye direkt entegre |
| Compression | **Rust** | Memory safety + performance, Tauri uyumlu |
| Tauri Command Extensions | **Rust** | Zero overhead, aynı runtime |

### Native vs Python Plugin Karşılaştırma

```
┌─────────────────────────────────────────────────────────────┐
│                    PLUGIN KARŞILAŞTIRMA                     │
├───────────────────────┬─────────────┬───────────────────────┤
│        Özellik        │   Python    │   Native (Rust/C/C++) │
├───────────────────────┼─────────────┼───────────────────────┤
│ Geliştirme Hızı       │     ⭐⭐⭐⭐⭐    │        ⭐⭐⭐         │
│ Runtime Performance   │     ⭐⭐⭐      │        ⭐⭐⭐⭐⭐       │
│ Memory Efficiency     │     ⭐⭐⭐      │        ⭐⭐⭐⭐⭐       │
│ CPU-Intensive Tasks   │     ⭐⭐       │        ⭐⭐⭐⭐⭐       │
│ Ecosystem/Libraries   │     ⭐⭐⭐⭐⭐    │        ⭐⭐⭐⭐        │
│ Cross-Platform        │     ⭐⭐⭐⭐⭐    │        ⭐⭐⭐⭐        │
│ Debug Kolaylığı       │     ⭐⭐⭐⭐⭐    │        ⭐⭐⭐         │
└───────────────────────┴─────────────┴───────────────────────┘
```

---

## 🔧 DESTEKLENEN DİLLER

### Dil ve Toolchain Gereksinimleri

| Dil | Minimum Versiyon | Toolchain | FFI Bridge |
|-----|------------------|-----------|------------|
| **Rust** | 1.75+ | cargo, maturin | PyO3 |
| **C** | C11 | MSVC 2022 / Clang 16+ | cffi |
| **C++** | C++17 | MSVC 2022 / Clang 16+ | pybind11 |

### FFI Bridge Kütüphaneleri

```
┌─────────────────────────────────────────────────────────────┐
│                    FFI BRIDGE MİMARİSİ                      │
│                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │   Python    │      │   Python    │      │   Python    │ │
│  │   Backend   │      │   Backend   │      │   Backend   │ │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘ │
│         │                    │                    │         │
│         ▼                    ▼                    ▼         │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │    PyO3     │      │    cffi     │      │  pybind11   │ │
│  │  (Rust→Py)  │      │   (C→Py)    │      │  (C++→Py)   │ │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘ │
│         │                    │                    │         │
│         ▼                    ▼                    ▼         │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │    Rust     │      │      C      │      │     C++     │ │
│  │   Plugin    │      │   Plugin    │      │   Plugin    │ │
│  └─────────────┘      └─────────────┘      └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ NATIVE PLUGIN MİMARİSİ

### Plugin Loading Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  NATIVE PLUGIN LOADING                       │
│                                                              │
│  1. Manifest Validation                                      │
│     ├─ manifest.json okunur                                  │
│     ├─ native.language, native.abi_version kontrol           │
│     └─ Platform uyumluluğu doğrulanır                        │
│                                                              │
│  2. Binary Verification                                      │
│     ├─ SHA256 hash kontrolü                                  │
│     ├─ Code signing doğrulaması (Windows Authenticode)       │
│     └─ ABI uyumluluk kontrolü                                │
│                                                              │
│  3. Dynamic Loading                                          │
│     ├─ Rust: PyO3 modül olarak import                        │
│     ├─ C: cffi ile .dll/.so yükleme                          │
│     └─ C++: pybind11 modül olarak import                     │
│                                                              │
│  4. Symbol Resolution                                        │
│     ├─ Zorunlu fonksiyonlar kontrol (init, shutdown)         │
│     ├─ Event handler'lar kaydedilir                          │
│     └─ API endpoints expose edilir                           │
│                                                              │
│  5. Sandbox Integration                                      │
│     ├─ Permission enforcement                                │
│     ├─ Resource limitleri uygulanır                          │
│     └─ IPC channel kurulur                                   │
└─────────────────────────────────────────────────────────────┘
```

### Core Interface (Tüm Diller İçin Zorunlu)

```c
// clipshot_plugin.h — Ortak C ABI Interface

#ifndef CLIPSHOT_PLUGIN_H
#define CLIPSHOT_PLUGIN_H

#include <stdint.h>
#include <stdbool.h>

#ifdef _WIN32
    #define CLIPSHOT_EXPORT __declspec(dllexport)
#else
    #define CLIPSHOT_EXPORT __attribute__((visibility("default")))
#endif

// Plugin ABI Version
#define CLIPSHOT_ABI_VERSION 1

// Error codes
typedef enum {
    CLIPSHOT_OK = 0,
    CLIPSHOT_ERROR_INVALID_ARGUMENT = 1,
    CLIPSHOT_ERROR_OUT_OF_MEMORY = 2,
    CLIPSHOT_ERROR_IO = 3,
    CLIPSHOT_ERROR_PERMISSION_DENIED = 4,
    CLIPSHOT_ERROR_NOT_IMPLEMENTED = 5,
    CLIPSHOT_ERROR_INTERNAL = 100,
} ClipshotError;

// Plugin info returned by get_plugin_info
typedef struct {
    const char* id;
    const char* name;
    const char* version;
    uint32_t abi_version;
} ClipshotPluginInfo;

// Context passed to plugin functions
typedef struct ClipshotContext ClipshotContext;

// ═══════════════════════════════════════════════════════════════
// ZORUNLU FONKSİYONLAR — Her native plugin bunları implement etmeli
// ═══════════════════════════════════════════════════════════════

// Plugin bilgilerini döndürür
CLIPSHOT_EXPORT ClipshotPluginInfo* clipshot_get_plugin_info(void);

// Plugin başlatma
CLIPSHOT_EXPORT ClipshotError clipshot_init(ClipshotContext* ctx);

// Plugin durdurma
CLIPSHOT_EXPORT ClipshotError clipshot_shutdown(void);

// ABI versiyon kontrolü
CLIPSHOT_EXPORT uint32_t clipshot_get_abi_version(void);

// ═══════════════════════════════════════════════════════════════
// OPSİYONEL EVENT HANDLERS
// ═══════════════════════════════════════════════════════════════

// Clip yakalandığında
CLIPSHOT_EXPORT ClipshotError clipshot_on_clip_captured(
    const char* clip_id,
    const uint8_t* frame_data,
    uint32_t width,
    uint32_t height,
    uint32_t stride
);

// Frame işleme
CLIPSHOT_EXPORT ClipshotError clipshot_process_frame(
    const uint8_t* input,
    uint8_t* output,
    uint32_t width,
    uint32_t height
);

#endif // CLIPSHOT_PLUGIN_H
```

---

## 🦀 TAURI ENTEGRASYONU

ClipShot'ın Tauri (Rust) backend'i sayesinde, Rust plugin'leri ekstra FFI overhead'i olmadan doğrudan entegre edilebilir.

### Tauri Plugin Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                    TAURI BACKEND (Rust)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Plugin Manager (Rust)                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │   │
│  │  │  Rust    │  │   C/C++  │  │  Python  │          │   │
│  │  │ Plugins  │  │ Plugins  │  │ Plugins  │          │   │
│  │  │ (Direct) │  │  (FFI)   │  │  (PyO3)  │          │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘          │   │
│  │       │             │             │                 │   │
│  │       └─────────────┼─────────────┘                 │   │
│  │                     │                               │   │
│  │              ┌──────▼──────┐                        │   │
│  │              │   Unified   │                        │   │
│  │              │   Plugin    │                        │   │
│  │              │  Interface  │                        │   │
│  │              └──────┬──────┘                        │   │
│  └─────────────────────┼────────────────────────────────   │
│                        │                                   │
│                 ┌──────▼──────┐                            │
│                 │    Tauri    │                            │
│                 │   Commands  │                            │
│                 └──────┬──────┘                            │
└────────────────────────┼──────────────────────────────────┘
                         │
                  ┌──────▼──────┐
                  │  Frontend   │
                  │  (Vite +    │
                  │   React)    │
                  └─────────────┘
```

### Rust Plugin → Tauri Direct Integration

Rust plugin'leri Tauri backend'e doğrudan eklenebilir:

```rust
// src-tauri/src/plugins/mod.rs

use libloading::{Library, Symbol};
use std::path::Path;

pub trait ClipshotPlugin: Send + Sync {
    fn init(&mut self) -> Result<(), String>;
    fn shutdown(&mut self) -> Result<(), String>;
    fn get_info(&self) -> PluginInfo;
}

// Rust plugin örneği
pub struct MyRustPlugin {
    config: PluginConfig,
}

impl ClipshotPlugin for MyRustPlugin {
    fn init(&mut self) -> Result<(), String> {
        // Direct Rust implementation
        Ok(())
    }
    
    fn shutdown(&mut self) -> Result<(), String> {
        Ok(())
    }
    
    fn get_info(&self) -> PluginInfo {
        PluginInfo {
            id: "com.example.rust-plugin".to_string(),
            name: "My Rust Plugin".to_string(),
            version: "1.0.0".to_string(),
        }
    }
}

// Tauri Command olarak expose et
#[tauri::command]
pub async fn call_rust_plugin(
    plugin_id: String,
    method: String,
    params: serde_json::Value,
) -> Result<serde_json::Value, String> {
    // Rust plugin'e doğrudan çağrı - zero overhead
    let plugin = get_plugin(&plugin_id)?;
    plugin.call_method(&method, params)
}
```

### Tauri Plugin Registration

```rust
// src-tauri/src/main.rs

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Register native Rust plugins
            let plugin_manager = PluginManager::new();
            
            // Direct Rust plugin (zero overhead)
            plugin_manager.register_rust_plugin(Box::new(MyRustPlugin::new()));
            
            // C/C++ plugin via FFI
            plugin_manager.load_native_plugin("path/to/cpp_plugin.dll")?;
            
            // Python plugin via PyO3
            plugin_manager.load_python_plugin("path/to/py_plugin")?;
            
            app.manage(plugin_manager);
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            call_rust_plugin,
            load_plugin,
            unload_plugin,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Frontend → Rust Plugin Call

```typescript
// Frontend (React/TypeScript)
import { invoke } from '@tauri-apps/api/tauri'

// Call Rust plugin method directly
const result = await invoke('call_rust_plugin', {
  pluginId: 'com.example.rust-plugin',
  method: 'process_frame',
  params: {
    width: 1920,
    height: 1080,
    data: frameBuffer
  }
})
```

### Tauri Plugin Avantajları

| Özellik | Rust Plugin (Tauri) | C/C++ Plugin | Python Plugin |
|---------|---------------------|--------------|---------------|
| **FFI Overhead** | ❌ Yok | ⚠️ Var | ⚠️ Var (PyO3) |
| **Memory Safety** | ✅ Compile-time | ❌ Runtime | ⚠️ Runtime |
| **Integration** | ✅ Native | 🔶 FFI bridge | 🔶 PyO3 bridge |
| **Build Time** | ✅ Tek build | 🔶 Ayrı build | 🔶 Ayrı build |
| **Hot Reload** | ✅ Cargo watch | ❌ Restart | ⚠️ Limited |

### Tauri State Sharing

Plugin'ler arası state paylaşımı için Tauri'nin state management sistemi kullanılır:

```rust
// src-tauri/src/state.rs

use std::sync::{Arc, RwLock};
use std::collections::HashMap;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PluginState {
    pub enabled: bool,
    pub data: serde_json::Value,
}

#[derive(Debug, Default)]
pub struct SharedPluginState {
    states: Arc<RwLock<HashMap<String, PluginState>>>,
}

impl SharedPluginState {
    pub fn new() -> Self {
        Self {
            states: Arc::new(RwLock::new(HashMap::new())),
        }
    }
    
    pub fn set(&self, plugin_id: String, state: PluginState) {
        let mut states = self.states.write().unwrap();
        states.insert(plugin_id, state);
    }
    
    pub fn get(&self, plugin_id: &str) -> Option<PluginState> {
        let states = self.states.read().unwrap();
        states.get(plugin_id).cloned()
    }
    
    pub fn remove(&self, plugin_id: &str) {
        let mut states = self.states.write().unwrap();
        states.remove(plugin_id);
    }
}

// Tauri command
#[tauri::command]
pub async fn get_plugin_state(
    plugin_id: String,
    state: tauri::State<'_, SharedPluginState>,
) -> Result<Option<PluginState>, String> {
    Ok(state.get(&plugin_id))
}

#[tauri::command]
pub async fn set_plugin_state(
    plugin_id: String,
    plugin_state: PluginState,
    state: tauri::State<'_, SharedPluginState>,
) -> Result<(), String> {
    state.set(plugin_id, plugin_state);
    Ok(())
}
```

### Zero-Copy Data Passing

Tauri ve Rust plugin'leri arasında zero-copy data paylaşımı:

```rust
// src-tauri/src/plugins/zero_copy.rs

use std::sync::Arc;
use bytes::Bytes;

pub struct SharedFrameBuffer {
    data: Arc<Bytes>,
    width: u32,
    height: u32,
    format: FrameFormat,
}

impl SharedFrameBuffer {
    pub fn new(data: Vec<u8>, width: u32, height: u32) -> Self {
        Self {
            data: Arc::new(Bytes::from(data)),
            width,
            height,
            format: FrameFormat::RGBA8,
        }
    }
    
    // Zero-copy clone
    pub fn clone_buffer(&self) -> Self {
        Self {
            data: Arc::clone(&self.data),
            width: self.width,
            height: self.height,
            format: self.format,
        }
    }
    
    // Ref döndür - zero allocation
    pub fn as_bytes(&self) -> &[u8] {
        &self.data
    }
}

// Plugin'e zero-copy ile aktar
pub fn pass_to_plugin(buffer: SharedFrameBuffer, plugin: &dyn ClipshotPlugin) {
    // Arc sayesinde sadece pointer kopyalanır, data değil
    plugin.process_buffer(buffer.clone_buffer());
}
```

### Plugin Events (Tauri)

```rust
// src-tauri/src/plugins/events.rs

use tauri::{Manager, Window};
use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
pub struct PluginEvent {
    pub plugin_id: String,
    pub event_type: String,
    pub data: serde_json::Value,
}

pub fn emit_plugin_event(window: &Window, event: PluginEvent) {
    window.emit("plugin-event", event).ok();
}

// Plugin'den event gönder
impl MyRustPlugin {
    pub fn notify_frontend(&self, window: &Window, message: &str) {
        emit_plugin_event(window, PluginEvent {
            plugin_id: "com.example.my-plugin".to_string(),
            event_type: "notification".to_string(),
            data: serde_json::json!({ "message": message }),
        });
    }
}

// Frontend'de dinle
// TypeScript:
// import { listen } from '@tauri-apps/api/event'
// 
// listen('plugin-event', (event) => {
//   console.log('Plugin event:', event.payload)
// })
```

---

## 🦀 RUST PLUGIN GELİŞTİRME

### Proje Yapısı

```
my-rust-plugin/
├── manifest.json              # Plugin manifest
├── Cargo.toml                 # Rust dependencies
├── pyproject.toml             # maturin config
├── src/
│   ├── lib.rs                 # Main entry (PyO3)
│   ├── plugin.rs              # Plugin logic
│   ├── handlers.rs            # Event handlers
│   └── ffi.rs                 # FFI exports
├── locales/
│   └── en.json
└── README.md
```

### Cargo.toml

```toml
[package]
name = "my-rust-plugin"
version = "1.0.0"
edition = "2021"
license = "MIT"

[lib]
name = "my_rust_plugin"
crate-type = ["cdylib"]

[dependencies]
# PyO3 for Python bindings
pyo3 = { version = "0.22", features = ["extension-module", "abi3-py311"] }

# Async runtime
tokio = { version = "1.40", features = ["rt-multi-thread", "sync"] }

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Error handling
thiserror = "2.0"
anyhow = "1.0"

# Logging
tracing = "0.1"
tracing-subscriber = "0.3"

# Image processing (örnek)
image = "0.25"

# Video processing (örnek)
ffmpeg-next = "7.0"

[build-dependencies]
pyo3-build-config = "0.22"

[profile.release]
lto = true
codegen-units = 1
opt-level = 3
strip = true
```

### pyproject.toml (maturin)

```toml
[build-system]
requires = ["maturin>=1.7,<2.0"]
build-backend = "maturin"

[project]
name = "my-rust-plugin"
version = "1.0.0"
description = "High-performance Rust plugin for ClipShot"
requires-python = ">=3.11"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
    "Operating System :: Microsoft :: Windows",
]

[tool.maturin]
features = ["pyo3/extension-module"]
python-source = "python"
module-name = "my_rust_plugin"
```

### lib.rs — PyO3 Entry Point

```rust
// src/lib.rs

use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use std::sync::Arc;
use tokio::runtime::Runtime;

mod plugin;
mod handlers;

use plugin::RustPlugin;
use handlers::ClipHandler;

/// Rust plugin for ClipShot
#[pyclass]
struct MyRustPlugin {
    inner: Arc<RustPlugin>,
    runtime: Runtime,
}

#[pymethods]
impl MyRustPlugin {
    #[new]
    fn new() -> PyResult<Self> {
        let runtime = Runtime::new()
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to create runtime: {e}")))?;
        
        let inner = Arc::new(RustPlugin::new());
        
        Ok(Self { inner, runtime })
    }
    
    /// Plugin'i başlat
    fn init(&self, config: &str) -> PyResult<()> {
        let inner = self.inner.clone();
        let config = config.to_string();
        
        self.runtime.block_on(async move {
            inner.init(&config).await
        }).map_err(|e| PyRuntimeError::new_err(format!("{e}")))
    }
    
    /// Plugin'i durdur
    fn shutdown(&self) -> PyResult<()> {
        self.runtime.block_on(async {
            self.inner.shutdown().await
        }).map_err(|e| PyRuntimeError::new_err(format!("{e}")))
    }
    
    /// Frame işle (zero-copy ile)
    fn process_frame<'py>(
        &self,
        py: Python<'py>,
        input: &[u8],
        width: u32,
        height: u32,
    ) -> PyResult<Bound<'py, pyo3::types::PyBytes>> {
        let result = self.inner.process_frame(input, width, height)
            .map_err(|e| PyRuntimeError::new_err(format!("{e}")))?;
        
        Ok(pyo3::types::PyBytes::new(py, &result))
    }
    
    /// Clip yakalandığında çağrılır
    fn on_clip_captured(&self, clip_id: &str, metadata: &str) -> PyResult<String> {
        let inner = self.inner.clone();
        let clip_id = clip_id.to_string();
        let metadata = metadata.to_string();
        
        self.runtime.block_on(async move {
            inner.on_clip_captured(&clip_id, &metadata).await
        }).map_err(|e| PyRuntimeError::new_err(format!("{e}")))
    }
    
    /// AI inference çalıştır
    fn run_inference(&self, input: &[u8]) -> PyResult<Vec<f32>> {
        self.inner.run_inference(input)
            .map_err(|e| PyRuntimeError::new_err(format!("{e}")))
    }
}

/// Plugin modülü
#[pymodule]
fn my_rust_plugin(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MyRustPlugin>()?;
    
    // Utility functions
    m.add_function(wrap_pyfunction!(get_version, m)?)?;
    m.add_function(wrap_pyfunction!(get_abi_version, m)?)?;
    
    Ok(())
}

#[pyfunction]
fn get_version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pyfunction]
fn get_abi_version() -> u32 {
    1 // CLIPSHOT_ABI_VERSION
}
```

### plugin.rs — Core Logic

```rust
// src/plugin.rs

use anyhow::{Result, Context};
use serde::{Deserialize, Serialize};
use std::sync::atomic::{AtomicBool, Ordering};
use tracing::{info, warn, error};

#[derive(Debug, Deserialize)]
pub struct PluginConfig {
    pub enabled: bool,
    pub quality: String,
    pub max_threads: u32,
}

pub struct RustPlugin {
    initialized: AtomicBool,
    config: std::sync::RwLock<Option<PluginConfig>>,
}

impl RustPlugin {
    pub fn new() -> Self {
        Self {
            initialized: AtomicBool::new(false),
            config: std::sync::RwLock::new(None),
        }
    }
    
    pub async fn init(&self, config_json: &str) -> Result<()> {
        if self.initialized.load(Ordering::Acquire) {
            warn!("Plugin already initialized");
            return Ok(());
        }
        
        let config: PluginConfig = serde_json::from_str(config_json)
            .context("Failed to parse config")?;
        
        info!("Initializing Rust plugin with config: {:?}", config);
        
        // Config'i kaydet
        *self.config.write().unwrap() = Some(config);
        
        // Initialization logic
        self.setup_internal().await?;
        
        self.initialized.store(true, Ordering::Release);
        info!("Rust plugin initialized successfully");
        
        Ok(())
    }
    
    pub async fn shutdown(&self) -> Result<()> {
        if !self.initialized.load(Ordering::Acquire) {
            return Ok(());
        }
        
        info!("Shutting down Rust plugin");
        
        // Cleanup logic
        self.cleanup_internal().await?;
        
        self.initialized.store(false, Ordering::Release);
        Ok(())
    }
    
    pub fn process_frame(&self, input: &[u8], width: u32, height: u32) -> Result<Vec<u8>> {
        // SIMD-optimized frame processing
        let mut output = Vec::with_capacity(input.len());
        
        // Örnek: grayscale dönüşüm
        for chunk in input.chunks_exact(4) {
            let r = chunk[0] as f32;
            let g = chunk[1] as f32;
            let b = chunk[2] as f32;
            let a = chunk[3];
            
            let gray = (0.299 * r + 0.587 * g + 0.114 * b) as u8;
            output.extend_from_slice(&[gray, gray, gray, a]);
        }
        
        Ok(output)
    }
    
    pub async fn on_clip_captured(&self, clip_id: &str, metadata: &str) -> Result<String> {
        info!("Processing clip: {}", clip_id);
        
        // Clip işleme logic
        let result = serde_json::json!({
            "clip_id": clip_id,
            "processed": true,
            "timestamp": chrono::Utc::now().to_rfc3339(),
        });
        
        Ok(result.to_string())
    }
    
    pub fn run_inference(&self, input: &[u8]) -> Result<Vec<f32>> {
        // AI inference logic
        // Bu örnek için dummy output
        Ok(vec![0.95, 0.03, 0.02])
    }
    
    async fn setup_internal(&self) -> Result<()> {
        // Internal setup
        Ok(())
    }
    
    async fn cleanup_internal(&self) -> Result<()> {
        // Internal cleanup
        Ok(())
    }
}
```

### Build Komutu

```bash
# Development build
maturin develop

# Release build (wheel oluşturur)
maturin build --release

# Doğrudan install
maturin build --release --strip
pip install target/wheels/my_rust_plugin-*.whl
```

---

## 💻 C PLUGIN GELİŞTİRME

### Proje Yapısı

```
my-c-plugin/
├── manifest.json
├── CMakeLists.txt
├── include/
│   └── plugin.h
├── src/
│   ├── plugin.c
│   └── handlers.c
├── python/
│   └── wrapper.py           # cffi wrapper
├── locales/
│   └── en.json
└── README.md
```

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)
project(my_c_plugin VERSION 1.0.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Windows specific
if(WIN32)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# ClipShot plugin header
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../clipshot_sdk/include
)

# Plugin library
add_library(my_c_plugin SHARED
    src/plugin.c
    src/handlers.c
)

# Compiler flags
if(MSVC)
    target_compile_options(my_c_plugin PRIVATE /W4 /O2)
else()
    target_compile_options(my_c_plugin PRIVATE -Wall -Wextra -O3)
endif()

# Link libraries
target_link_libraries(my_c_plugin PRIVATE
    # External libs
)

# Install
install(TARGETS my_c_plugin
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)
```

### plugin.c — Main Implementation

```c
// src/plugin.c

#include "plugin.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// ═══════════════════════════════════════════════════════════════
// GLOBAL STATE
// ═══════════════════════════════════════════════════════════════

static bool g_initialized = false;
static ClipshotPluginInfo g_plugin_info = {
    .id = "com.example.my-c-plugin",
    .name = "My C Plugin",
    .version = "1.0.0",
    .abi_version = CLIPSHOT_ABI_VERSION,
};

// ═══════════════════════════════════════════════════════════════
// ZORUNLU FONKSİYONLAR
// ═══════════════════════════════════════════════════════════════

CLIPSHOT_EXPORT ClipshotPluginInfo* clipshot_get_plugin_info(void) {
    return &g_plugin_info;
}

CLIPSHOT_EXPORT uint32_t clipshot_get_abi_version(void) {
    return CLIPSHOT_ABI_VERSION;
}

CLIPSHOT_EXPORT ClipshotError clipshot_init(ClipshotContext* ctx) {
    if (g_initialized) {
        return CLIPSHOT_OK;
    }
    
    // Initialization logic
    printf("[C Plugin] Initializing...\n");
    
    // Setup resources
    
    g_initialized = true;
    printf("[C Plugin] Initialized successfully\n");
    
    return CLIPSHOT_OK;
}

CLIPSHOT_EXPORT ClipshotError clipshot_shutdown(void) {
    if (!g_initialized) {
        return CLIPSHOT_OK;
    }
    
    printf("[C Plugin] Shutting down...\n");
    
    // Cleanup resources
    
    g_initialized = false;
    return CLIPSHOT_OK;
}

// ═══════════════════════════════════════════════════════════════
// EVENT HANDLERS
// ═══════════════════════════════════════════════════════════════

CLIPSHOT_EXPORT ClipshotError clipshot_on_clip_captured(
    const char* clip_id,
    const uint8_t* frame_data,
    uint32_t width,
    uint32_t height,
    uint32_t stride
) {
    if (!g_initialized) {
        return CLIPSHOT_ERROR_INTERNAL;
    }
    
    printf("[C Plugin] Processing clip: %s (%ux%u)\n", clip_id, width, height);
    
    // Frame processing logic
    
    return CLIPSHOT_OK;
}

CLIPSHOT_EXPORT ClipshotError clipshot_process_frame(
    const uint8_t* input,
    uint8_t* output,
    uint32_t width,
    uint32_t height
) {
    if (!g_initialized || !input || !output) {
        return CLIPSHOT_ERROR_INVALID_ARGUMENT;
    }
    
    const uint32_t total_pixels = width * height;
    
    // SIMD-friendly loop (compiler will auto-vectorize)
    for (uint32_t i = 0; i < total_pixels * 4; i += 4) {
        // Grayscale conversion
        uint8_t r = input[i];
        uint8_t g = input[i + 1];
        uint8_t b = input[i + 2];
        uint8_t a = input[i + 3];
        
        uint8_t gray = (uint8_t)(0.299f * r + 0.587f * g + 0.114f * b);
        
        output[i] = gray;
        output[i + 1] = gray;
        output[i + 2] = gray;
        output[i + 3] = a;
    }
    
    return CLIPSHOT_OK;
}
```

### Python cffi Wrapper

```python
# python/wrapper.py

"""
C Plugin Python wrapper using cffi.
"""

import os
from pathlib import Path
from cffi import FFI

ffi = FFI()

# C header tanımları
ffi.cdef("""
    typedef enum {
        CLIPSHOT_OK = 0,
        CLIPSHOT_ERROR_INVALID_ARGUMENT = 1,
        CLIPSHOT_ERROR_OUT_OF_MEMORY = 2,
        CLIPSHOT_ERROR_IO = 3,
        CLIPSHOT_ERROR_PERMISSION_DENIED = 4,
        CLIPSHOT_ERROR_NOT_IMPLEMENTED = 5,
        CLIPSHOT_ERROR_INTERNAL = 100,
    } ClipshotError;
    
    typedef struct {
        const char* id;
        const char* name;
        const char* version;
        uint32_t abi_version;
    } ClipshotPluginInfo;
    
    typedef struct ClipshotContext ClipshotContext;
    
    ClipshotPluginInfo* clipshot_get_plugin_info(void);
    uint32_t clipshot_get_abi_version(void);
    ClipshotError clipshot_init(ClipshotContext* ctx);
    ClipshotError clipshot_shutdown(void);
    ClipshotError clipshot_on_clip_captured(
        const char* clip_id,
        const uint8_t* frame_data,
        uint32_t width,
        uint32_t height,
        uint32_t stride
    );
    ClipshotError clipshot_process_frame(
        const uint8_t* input,
        uint8_t* output,
        uint32_t width,
        uint32_t height
    );
""")


class CPlugin:
    """Python wrapper for C plugin."""
    
    def __init__(self, lib_path: str = None):
        if lib_path is None:
            # Default path
            lib_dir = Path(__file__).parent.parent / "lib"
            if os.name == "nt":
                lib_path = lib_dir / "my_c_plugin.dll"
            else:
                lib_path = lib_dir / "libmy_c_plugin.so"
        
        self._lib = ffi.dlopen(str(lib_path))
        self._initialized = False
    
    @property
    def info(self) -> dict:
        """Get plugin info."""
        info = self._lib.clipshot_get_plugin_info()
        return {
            "id": ffi.string(info.id).decode("utf-8"),
            "name": ffi.string(info.name).decode("utf-8"),
            "version": ffi.string(info.version).decode("utf-8"),
            "abi_version": info.abi_version,
        }
    
    @property
    def abi_version(self) -> int:
        """Get ABI version."""
        return self._lib.clipshot_get_abi_version()
    
    def init(self) -> None:
        """Initialize plugin."""
        result = self._lib.clipshot_init(ffi.NULL)
        if result != 0:
            raise RuntimeError(f"Plugin init failed with error code: {result}")
        self._initialized = True
    
    def shutdown(self) -> None:
        """Shutdown plugin."""
        result = self._lib.clipshot_shutdown()
        if result != 0:
            raise RuntimeError(f"Plugin shutdown failed with error code: {result}")
        self._initialized = False
    
    def process_frame(
        self, 
        input_data: bytes, 
        width: int, 
        height: int
    ) -> bytes:
        """Process a frame."""
        if not self._initialized:
            raise RuntimeError("Plugin not initialized")
        
        input_buf = ffi.from_buffer(input_data)
        output_buf = ffi.new(f"uint8_t[{len(input_data)}]")
        
        result = self._lib.clipshot_process_frame(
            input_buf, output_buf, width, height
        )
        
        if result != 0:
            raise RuntimeError(f"Frame processing failed: {result}")
        
        return ffi.buffer(output_buf)[:]
    
    def on_clip_captured(
        self,
        clip_id: str,
        frame_data: bytes,
        width: int,
        height: int,
        stride: int
    ) -> None:
        """Handle clip captured event."""
        if not self._initialized:
            raise RuntimeError("Plugin not initialized")
        
        result = self._lib.clipshot_on_clip_captured(
            clip_id.encode("utf-8"),
            ffi.from_buffer(frame_data),
            width,
            height,
            stride
        )
        
        if result != 0:
            raise RuntimeError(f"Clip processing failed: {result}")
    
    def __enter__(self):
        self.init()
        return self
    
    def __exit__(self, *args):
        self.shutdown()
```

---

## 🔷 C++ PLUGIN GELİŞTİRME

### Proje Yapısı

```
my-cpp-plugin/
├── manifest.json
├── CMakeLists.txt
├── include/
│   └── plugin.hpp
├── src/
│   ├── plugin.cpp
│   ├── bindings.cpp          # pybind11 bindings
│   └── handlers.cpp
├── locales/
│   └── en.json
└── README.md
```

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)
project(my_cpp_plugin VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Plugin sources
set(PLUGIN_SOURCES
    src/plugin.cpp
    src/handlers.cpp
)

# pybind11 module
pybind11_add_module(my_cpp_plugin
    ${PLUGIN_SOURCES}
    src/bindings.cpp
)

# Compiler flags
if(MSVC)
    target_compile_options(my_cpp_plugin PRIVATE /W4 /O2 /EHsc)
else()
    target_compile_options(my_cpp_plugin PRIVATE -Wall -Wextra -O3)
endif()

# Include directories
target_include_directories(my_cpp_plugin PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Install
install(TARGETS my_cpp_plugin DESTINATION .)
```

### plugin.hpp — Header

```cpp
// include/plugin.hpp

#pragma once

#include <string>
#include <vector>
#include <cstdint>
#include <memory>
#include <functional>

namespace clipshot {

// Error codes
enum class Error {
    Ok = 0,
    InvalidArgument = 1,
    OutOfMemory = 2,
    IoError = 3,
    PermissionDenied = 4,
    NotImplemented = 5,
    Internal = 100,
};

// Plugin info
struct PluginInfo {
    std::string id;
    std::string name;
    std::string version;
    uint32_t abi_version;
};

// Configuration
struct Config {
    bool enabled = true;
    std::string quality = "high";
    uint32_t max_threads = 4;
};

// Main plugin class
class CppPlugin {
public:
    CppPlugin();
    ~CppPlugin();
    
    // Prevent copying
    CppPlugin(const CppPlugin&) = delete;
    CppPlugin& operator=(const CppPlugin&) = delete;
    
    // Lifecycle
    Error init(const std::string& config_json);
    Error shutdown();
    
    // Processing
    std::vector<uint8_t> processFrame(
        const uint8_t* input,
        size_t size,
        uint32_t width,
        uint32_t height
    );
    
    // Events
    std::string onClipCaptured(
        const std::string& clip_id,
        const std::string& metadata
    );
    
    // AI
    std::vector<float> runInference(const std::vector<uint8_t>& input);
    
    // Info
    static PluginInfo getInfo();
    static uint32_t getAbiVersion();
    
private:
    struct Impl;
    std::unique_ptr<Impl> pImpl;
};

} // namespace clipshot
```

### plugin.cpp — Implementation

```cpp
// src/plugin.cpp

#include "plugin.hpp"
#include <iostream>
#include <nlohmann/json.hpp>

namespace clipshot {

using json = nlohmann::json;

// ═══════════════════════════════════════════════════════════════
// PIMPL IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════

struct CppPlugin::Impl {
    bool initialized = false;
    Config config;
};

CppPlugin::CppPlugin() : pImpl(std::make_unique<Impl>()) {}

CppPlugin::~CppPlugin() {
    if (pImpl->initialized) {
        shutdown();
    }
}

// ═══════════════════════════════════════════════════════════════
// LIFECYCLE
// ═══════════════════════════════════════════════════════════════

Error CppPlugin::init(const std::string& config_json) {
    if (pImpl->initialized) {
        return Error::Ok;
    }
    
    try {
        auto j = json::parse(config_json);
        
        pImpl->config.enabled = j.value("enabled", true);
        pImpl->config.quality = j.value("quality", "high");
        pImpl->config.max_threads = j.value("max_threads", 4u);
        
        std::cout << "[C++ Plugin] Initializing with quality: " 
                  << pImpl->config.quality << std::endl;
        
        pImpl->initialized = true;
        return Error::Ok;
        
    } catch (const std::exception& e) {
        std::cerr << "[C++ Plugin] Init error: " << e.what() << std::endl;
        return Error::InvalidArgument;
    }
}

Error CppPlugin::shutdown() {
    if (!pImpl->initialized) {
        return Error::Ok;
    }
    
    std::cout << "[C++ Plugin] Shutting down..." << std::endl;
    
    pImpl->initialized = false;
    return Error::Ok;
}

// ═══════════════════════════════════════════════════════════════
// PROCESSING
// ═══════════════════════════════════════════════════════════════

std::vector<uint8_t> CppPlugin::processFrame(
    const uint8_t* input,
    size_t size,
    uint32_t width,
    uint32_t height
) {
    std::vector<uint8_t> output;
    output.reserve(size);
    
    // SIMD-optimized grayscale conversion
    for (size_t i = 0; i < size; i += 4) {
        float r = static_cast<float>(input[i]);
        float g = static_cast<float>(input[i + 1]);
        float b = static_cast<float>(input[i + 2]);
        uint8_t a = input[i + 3];
        
        auto gray = static_cast<uint8_t>(0.299f * r + 0.587f * g + 0.114f * b);
        
        output.push_back(gray);
        output.push_back(gray);
        output.push_back(gray);
        output.push_back(a);
    }
    
    return output;
}

std::string CppPlugin::onClipCaptured(
    const std::string& clip_id,
    const std::string& metadata
) {
    std::cout << "[C++ Plugin] Processing clip: " << clip_id << std::endl;
    
    json result = {
        {"clip_id", clip_id},
        {"processed", true},
        {"plugin", "my_cpp_plugin"}
    };
    
    return result.dump();
}

std::vector<float> CppPlugin::runInference(const std::vector<uint8_t>& input) {
    // Dummy inference result
    return {0.95f, 0.03f, 0.02f};
}

// ═══════════════════════════════════════════════════════════════
// STATIC INFO
// ═══════════════════════════════════════════════════════════════

PluginInfo CppPlugin::getInfo() {
    return PluginInfo{
        .id = "com.example.my-cpp-plugin",
        .name = "My C++ Plugin",
        .version = "1.0.0",
        .abi_version = 1,
    };
}

uint32_t CppPlugin::getAbiVersion() {
    return 1;
}

} // namespace clipshot
```

### bindings.cpp — pybind11 Bindings

```cpp
// src/bindings.cpp

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "plugin.hpp"

namespace py = pybind11;
using namespace clipshot;

PYBIND11_MODULE(my_cpp_plugin, m) {
    m.doc() = "High-performance C++ plugin for ClipShot";
    
    // Error enum
    py::enum_<Error>(m, "Error")
        .value("Ok", Error::Ok)
        .value("InvalidArgument", Error::InvalidArgument)
        .value("OutOfMemory", Error::OutOfMemory)
        .value("IoError", Error::IoError)
        .value("PermissionDenied", Error::PermissionDenied)
        .value("NotImplemented", Error::NotImplemented)
        .value("Internal", Error::Internal);
    
    // PluginInfo struct
    py::class_<PluginInfo>(m, "PluginInfo")
        .def_readonly("id", &PluginInfo::id)
        .def_readonly("name", &PluginInfo::name)
        .def_readonly("version", &PluginInfo::version)
        .def_readonly("abi_version", &PluginInfo::abi_version);
    
    // Main plugin class
    py::class_<CppPlugin>(m, "CppPlugin")
        .def(py::init<>())
        
        .def("init", &CppPlugin::init,
             py::arg("config_json"),
             "Initialize the plugin with JSON config")
        
        .def("shutdown", &CppPlugin::shutdown,
             "Shutdown the plugin")
        
        .def("process_frame", 
             [](CppPlugin& self, py::bytes input, uint32_t width, uint32_t height) {
                 std::string data = input;
                 auto result = self.processFrame(
                     reinterpret_cast<const uint8_t*>(data.data()),
                     data.size(),
                     width,
                     height
                 );
                 return py::bytes(
                     reinterpret_cast<char*>(result.data()),
                     result.size()
                 );
             },
             py::arg("input"),
             py::arg("width"),
             py::arg("height"),
             "Process a frame")
        
        .def("on_clip_captured", &CppPlugin::onClipCaptured,
             py::arg("clip_id"),
             py::arg("metadata"),
             "Handle clip captured event")
        
        .def("run_inference",
             [](CppPlugin& self, py::bytes input) {
                 std::string data = input;
                 std::vector<uint8_t> vec(data.begin(), data.end());
                 return self.runInference(vec);
             },
             py::arg("input"),
             "Run AI inference")
        
        .def_static("get_info", &CppPlugin::getInfo,
                    "Get plugin info")
        
        .def_static("get_abi_version", &CppPlugin::getAbiVersion,
                    "Get ABI version");
    
    // Module-level functions
    m.def("get_version", []() { return "1.0.0"; });
    m.def("get_abi_version", []() { return CppPlugin::getAbiVersion(); });
}
```

---

## 📜 MANIFEST UZANTILARI

Native plugin'ler için manifest.json'a ek alanlar eklenir:

```json
{
  "$schema": "https://clipshot.io/schemas/manifest.v2.schema.json",
  
  "id": "com.yourname.my-native-plugin",
  "name": "My Native Plugin",
  "version": "1.0.0",
  "api_version": "v1",
  
  "type": "optional",
  "category": "enhancement",
  
  "native": {
    "language": "rust",
    "abi_version": 1,
    
    "binaries": {
      "windows-x64": {
        "path": "bin/windows-x64/my_plugin.pyd",
        "sha256": "abc123...",
        "signed": true
      },
      "linux-x64": {
        "path": "bin/linux-x64/my_plugin.so",
        "sha256": "def456...",
        "signed": false
      }
    },
    
    "build": {
      "tool": "maturin",
      "command": "maturin build --release",
      "requirements": ["rust >= 1.75", "maturin >= 1.7"]
    },
    
    "ffi": {
      "bridge": "pyo3",
      "module_name": "my_plugin",
      "entry_class": "MyPlugin"
    },
    
    "capabilities": {
      "simd": true,
      "gpu_compute": false,
      "async": true
    }
  },
  
  "entry": {
    "backend": "python/loader.py",
    "native_module": "my_plugin"
  },
  
  "permissions": {
    "memory": {
      "level": "required",
      "max_mb": 512,
      "reason": {
        "en": "Video frame buffers"
      }
    }
  },
  
  "resources": {
    "cpu": {
      "max_percent": 30
    },
    "memory": {
      "max_mb": 512
    },
    "gpu": {
      "max_percent": 20
    }
  }
}
```

### Native Manifest Alanları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `native.language` | `rust` \| `c` \| `cpp` | Plugin dili |
| `native.abi_version` | number | ABI versiyon numarası |
| `native.binaries` | object | Platform-specific binary'ler |
| `native.build.tool` | string | Build tool (maturin, cmake, etc.) |
| `native.ffi.bridge` | string | FFI bridge (pyo3, cffi, pybind11) |
| `native.capabilities` | object | Plugin özellikleri |

---

## 🔐 ABI SPESİFİKASYONU

### ABI Versiyon Kuralları

```
ABI Version: MAJOR
- Incompatible changes → MAJOR++
- New optional features → MAJOR aynı kalır

Mevcut: ABI v1

v1 Gereksinimleri:
├── clipshot_get_plugin_info() → Zorunlu
├── clipshot_get_abi_version() → Zorunlu  
├── clipshot_init() → Zorunlu
├── clipshot_shutdown() → Zorunlu
└── clipshot_* event handlers → Opsiyonel
```

### ABI Uyumluluk Kontrolü

```python
# src/plugins/native_loader.py

from typing import Protocol, Any
from dataclasses import dataclass
import importlib

SUPPORTED_ABI_VERSIONS = [1]

@dataclass
class NativePluginInfo:
    id: str
    name: str
    version: str
    abi_version: int
    module: Any


class NativePluginLoader:
    """Native plugin loader with ABI verification."""
    
    def load(self, manifest: dict) -> NativePluginInfo:
        """Load a native plugin."""
        native_config = manifest.get("native", {})
        
        # ABI version check
        abi_version = native_config.get("abi_version", 0)
        if abi_version not in SUPPORTED_ABI_VERSIONS:
            raise ValueError(
                f"Unsupported ABI version: {abi_version}. "
                f"Supported: {SUPPORTED_ABI_VERSIONS}"
            )
        
        # Load module
        module_name = native_config["ffi"]["module_name"]
        module = importlib.import_module(module_name)
        
        # Verify ABI version from module
        if hasattr(module, "get_abi_version"):
            actual_abi = module.get_abi_version()
            if actual_abi != abi_version:
                raise ValueError(
                    f"ABI mismatch: manifest says {abi_version}, "
                    f"module reports {actual_abi}"
                )
        
        # Get plugin info
        if hasattr(module, "get_version"):
            version = module.get_version()
        else:
            version = manifest["version"]
        
        return NativePluginInfo(
            id=manifest["id"],
            name=manifest["name"],
            version=version,
            abi_version=abi_version,
            module=module,
        )
```

---

## 🛡️ MEMORY SAFETY

### Rust — Built-in Safety

```rust
// Rust'ta memory safety otomatik

// ❌ Bu derlenmez
fn bad_example() {
    let data: Vec<u8> = vec![1, 2, 3];
    let ptr = data.as_ptr();
    drop(data);  // data freed
    // ptr artık dangling - Rust bunu yakalar
}

// ✅ Doğru kullanım
fn good_example() -> Vec<u8> {
    let data: Vec<u8> = vec![1, 2, 3];
    process(&data);  // borrow
    data  // ownership transfer
}
```

### C/C++ — Manuel Kontrol

```c
// C için güvenlik kuralları:

// 1. NULL check her zaman
CLIPSHOT_EXPORT ClipshotError clipshot_process(const uint8_t* input) {
    if (input == NULL) {
        return CLIPSHOT_ERROR_INVALID_ARGUMENT;
    }
    // ...
}

// 2. Buffer size kontrolü
CLIPSHOT_EXPORT ClipshotError clipshot_copy(
    const uint8_t* src,
    uint8_t* dst,
    size_t src_size,
    size_t dst_size
) {
    if (src_size > dst_size) {
        return CLIPSHOT_ERROR_INVALID_ARGUMENT;
    }
    memcpy(dst, src, src_size);
    return CLIPSHOT_OK;
}

// 3. Resource cleanup with RAII (C++)
class ResourceGuard {
public:
    explicit ResourceGuard(void* ptr) : ptr_(ptr) {}
    ~ResourceGuard() { if (ptr_) free(ptr_); }
private:
    void* ptr_;
};
```

### Memory Leak Detection

```python
# tests/test_memory.py

import tracemalloc
import gc

def test_no_memory_leak():
    """Native plugin memory leak testi."""
    from my_rust_plugin import MyRustPlugin
    
    tracemalloc.start()
    
    # Baseline
    gc.collect()
    snapshot1 = tracemalloc.take_snapshot()
    
    # Plugin kullan
    for _ in range(1000):
        plugin = MyRustPlugin()
        plugin.init('{"enabled": true}')
        plugin.process_frame(b'\x00' * 1000, 10, 25)
        plugin.shutdown()
        del plugin
    
    # Cleanup
    gc.collect()
    snapshot2 = tracemalloc.take_snapshot()
    
    # Karşılaştır
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    # 1MB'dan fazla artış olmamalı
    total_diff = sum(stat.size_diff for stat in stats)
    assert total_diff < 1024 * 1024, f"Memory leak detected: {total_diff} bytes"
```

---

## 🔨 BUILD SİSTEMİ

### Rust (maturin)

```bash
# Development
cd my-rust-plugin
maturin develop

# Release build
maturin build --release

# Cross-compile (optional, requires cross)
maturin build --release --target x86_64-pc-windows-msvc
```

### C/C++ (CMake)

```bash
# Configure
cd my-cpp-plugin
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --config Release

# Install
cmake --install build --prefix dist
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/build.yml

name: Build Native Plugin

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build-rust:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Rust
        uses: dtolnay/rust-action@stable
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install maturin
        run: pip install maturin
      
      - name: Build
        run: maturin build --release
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: rust-plugin-windows
          path: target/wheels/*.whl
  
  build-cpp:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install pybind11
        run: pip install pybind11[global]
      
      - name: Configure
        run: cmake -B build -DCMAKE_BUILD_TYPE=Release
      
      - name: Build
        run: cmake --build build --config Release
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: cpp-plugin-windows
          path: build/Release/*.pyd
```

---

## 🧪 TEST VE DEBUG

### Unit Tests (Rust)

```rust
// src/lib.rs

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_frame_processing() {
        let plugin = RustPlugin::new();
        
        // RGBA input
        let input = vec![255, 128, 64, 255, 0, 0, 0, 255];
        let output = plugin.process_frame(&input, 2, 1).unwrap();
        
        // Check grayscale output
        assert_eq!(output.len(), input.len());
        assert_eq!(output[3], 255); // Alpha preserved
    }
    
    #[tokio::test]
    async fn test_init_shutdown() {
        let plugin = RustPlugin::new();
        
        plugin.init(r#"{"enabled": true}"#).await.unwrap();
        plugin.shutdown().await.unwrap();
    }
}
```

### Integration Tests (Python)

```python
# tests/test_integration.py

import pytest
from my_rust_plugin import MyRustPlugin

@pytest.fixture
def plugin():
    p = MyRustPlugin()
    p.init('{"enabled": true}')
    yield p
    p.shutdown()

def test_process_frame(plugin):
    # 2x2 RGBA image
    input_data = bytes([
        255, 0, 0, 255,    # Red
        0, 255, 0, 255,    # Green
        0, 0, 255, 255,    # Blue
        255, 255, 255, 255 # White
    ])
    
    output = plugin.process_frame(input_data, 2, 2)
    
    assert len(output) == len(input_data)
    # Red → Gray
    assert output[0] == output[1] == output[2]

def test_clip_captured(plugin):
    result = plugin.on_clip_captured("clip_001", '{"duration": 30}')
    
    import json
    data = json.loads(result)
    assert data["clip_id"] == "clip_001"
    assert data["processed"] is True
```

### Debug (VS Code)

```json
// .vscode/launch.json

{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Rust Plugin",
      "type": "lldb",
      "request": "launch",
      "program": "${workspaceFolder}/.venv/Scripts/python.exe",
      "args": ["-m", "pytest", "tests/", "-v"],
      "cwd": "${workspaceFolder}",
      "env": {
        "RUST_BACKTRACE": "1"
      }
    },
    {
      "name": "Debug C++ Plugin",
      "type": "cppvsdbg",
      "request": "launch",
      "program": "${workspaceFolder}/.venv/Scripts/python.exe",
      "args": ["-m", "pytest", "tests/", "-v"],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

---

## ⚡ PERFORMANS REHBERİ

### Optimizasyon Teknikleri

| Teknik | Dil | Açıklama |
|--------|-----|----------|
| SIMD intrinsics | Rust/C/C++ | Vectorized operations |
| Zero-copy | Rust | Avoid unnecessary allocations |
| Memory pools | C/C++ | Pre-allocated buffers |
| Multithreading | All | Parallel processing |
| GPU compute | All | CUDA/Vulkan shaders |

### Rust SIMD Örneği

```rust
use std::simd::*;

pub fn process_rgba_simd(input: &[u8], output: &mut [u8]) {
    const LANE_COUNT: usize = 16;
    
    let chunks = input.len() / LANE_COUNT;
    
    for i in 0..chunks {
        let offset = i * LANE_COUNT;
        
        // Load 16 bytes at once
        let pixels = u8x16::from_slice(&input[offset..]);
        
        // Process...
        
        // Store
        pixels.copy_to_slice(&mut output[offset..]);
    }
}
```

### Benchmark

```rust
// benches/benchmark.rs

use criterion::{black_box, criterion_group, criterion_main, Criterion};
use my_rust_plugin::RustPlugin;

fn bench_frame_processing(c: &mut Criterion) {
    let plugin = RustPlugin::new();
    let input = vec![128u8; 1920 * 1080 * 4]; // 1080p RGBA
    
    c.bench_function("process_1080p_frame", |b| {
        b.iter(|| {
            plugin.process_frame(black_box(&input), 1920, 1080)
        })
    });
}

criterion_group!(benches, bench_frame_processing);
criterion_main!(benches);
```

---

## 📚 KAYNAKLAR

### Kütüphaneler

| Kütüphane | Kullanım | Link |
|-----------|----------|------|
| PyO3 | Rust→Python binding | https://pyo3.rs |
| maturin | Rust wheel builder | https://maturin.rs |
| pybind11 | C++→Python binding | https://pybind11.readthedocs.io |
| cffi | C→Python binding | https://cffi.readthedocs.io |
| abi_stable | Rust ABI stability | https://docs.rs/abi_stable |

### Örnek Projeler

- **Polars** — Rust DataFrame (PyO3 kullanır)
- **tiktoken** — OpenAI tokenizer (PyO3 kullanır)
- **pydantic-core** — Fast validation (PyO3 kullanır)
- **SWC** — JavaScript compiler (NAPI-RS kullanır)

---

## 🎯 CHECKLIST

Native plugin geliştirmeden önce:

- [ ] Performans gereksinimi analiz edildi
- [ ] Dil seçimi yapıldı (Rust/C/C++)
- [ ] Toolchain kuruldu
- [ ] ABI spesifikasyonu anlaşıldı
- [ ] Memory safety kuralları biliniyor
- [ ] Test stratejisi belirlendi
- [ ] CI/CD pipeline hazır

---

**Sonraki:** [11_RECOMMENDED_LIBRARIES.md](./11_RECOMMENDED_LIBRARIES.md) — Önerilen Kütüphaneler
