# 🎮 ClipShot - Plugin System

> **Status:** Plugin System Implementation Complete ✅

This repository contains the complete plugin system for ClipShot, a modular gaming clip platform.

## 📦 What's Included

### SDKs (Software Development Kits)

#### Python SDK (`packages/sdk/python/`)
- Abstract base class for plugins
- Lifecycle hooks (init, shutdown)
- Event system (clip captured, game detected)
- Custom API endpoints
- Full async/await support

#### TypeScript SDK (`packages/sdk/typescript/`)
- Type-safe plugin interfaces
- UI component types
- Event system types
- Decorator support
- Comprehensive type definitions

### Example Plugins

#### Hello World - Python (`plugins/examples/hello-world-py/`)
A complete Python plugin example demonstrating:
- Basic plugin structure
- Event handling
- Custom API endpoints
- Configuration management
- Localization (English, Turkish)

#### Rust Demo (`plugins/examples/rust-demo/`)
High-performance Rust plugin featuring:
- PyO3 integration
- SIMD optimizations
- Zero-copy operations
- Thread-safe atomic counters
- Performance benchmarks

#### C++ Demo (`plugins/examples/cpp-demo/`)
Native C++ plugin showcasing:
- pybind11 bindings
- Modern C++17
- OpenCL support (optional)
- Video frame processing
- CMake build system

### Plugin Templates

Ready-to-use templates for quick plugin development:

- **Python Template** (`plugins/templates/python-template/`) - For rapid development
- **Rust Template** (`plugins/templates/rust-template/`) - For high performance
- **C++ Template** (`plugins/templates/cpp-template/`) - For native integrations

### Tools

#### ClipShot CLI (`tools/clipshot-cli/`)
Command-line tool for plugin development:
```bash
# Create a new plugin
clipshot create my-plugin --language python

# Validate plugin manifest
clipshot validate ./plugins/my-plugin/manifest.json
```

## 🚀 Quick Start

### For Plugin Developers

#### 1. Install SDK

**Python:**
```bash
cd packages/sdk/python
pip install -e .
```

**TypeScript:**
```bash
cd packages/sdk/typescript
npm install
npm run build
```

#### 2. Create Your Plugin

**Option A: Use CLI (Recommended)**
```bash
./tools/clipshot-cli/clipshot create my-plugin --language python
```

**Option B: Copy Template**
```bash
cp -r plugins/templates/python-template plugins/my-plugin
```

#### 3. Customize

Edit `manifest.json`:
```json
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  ...
}
```

Implement your plugin in `src/main.py`:
```python
from clipshot_sdk import Plugin, Clip

class MyPlugin(Plugin):
    id = "com.example.my-plugin"
    
    async def on_clip_captured(self, clip: Clip):
        self.logger.info(f"Clip: {clip.title}")
```

#### 4. Test
```bash
pytest tests/
```

### For Contributors

1. Clone the repository
2. Read the documentation in `docs/`
3. Check example plugins in `plugins/examples/`
4. Follow coding standards
5. Submit pull requests

## 📚 Documentation

### Core Guides
- [Plugin Developer Guide](docs/02_PLUGIN_DEVELOPER_GUIDE.md) - Complete development guide
- [Native Plugin Guide](docs/10_NATIVE_PLUGIN_GUIDE.md) - Rust/C++ specifics
- [Marketplace Guide](docs/07_MARKETPLACE_GITHUB.md) - Publishing plugins

### SDK Documentation
- [Python SDK](packages/sdk/python/README.md)
- [TypeScript SDK](packages/sdk/typescript/README.md)
- [SDK Overview](packages/sdk/README.md)

### Examples & Templates
- [Plugin Examples](plugins/examples/)
- [Plugin Templates](plugins/templates/)
- [Plugins Overview](plugins/README.md)

### Architecture
- [Backend Architecture](docs/03_BACKEND_ARCHITECTURE.md)
- [Frontend Architecture](docs/04_FRONTEND_ARCHITECTURE.md)
- [Project Structure](docs/01_PROJECT_STRUCTURE.md)

## 🎯 Features

### Multi-Language Support
- **Python** - Fast development, rich ecosystem
- **Rust** - Maximum performance, memory safety
- **C++** - Legacy integrations, GPU acceleration

### Comprehensive SDK
- Lifecycle management
- Event system
- Custom APIs
- Type safety
- Async support

### Developer Tools
- CLI for scaffolding
- Validation tools
- Example plugins
- Ready-to-use templates

### Security & Sandboxing
- Permission system
- Resource limits
- Manifest validation
- Code signing support

## 📊 Plugin System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ClipShot Core                         │
│  ┌────────────────────────────────────────────────┐     │
│  │              Plugin Manager                     │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │     │
│  │  │  Python  │  │   Rust   │  │   C++    │     │     │
│  │  │ Plugins  │  │ Plugins  │  │ Plugins  │     │     │
│  │  │  (PyO3)  │  │  (PyO3)  │  │(pybind11)│     │     │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘     │     │
│  │       │             │             │            │     │
│  │       └─────────────┼─────────────┘            │     │
│  │                     │                          │     │
│  │              ┌──────▼──────┐                   │     │
│  │              │   Plugin    │                   │     │
│  │              │     SDK     │                   │     │
│  │              └─────────────┘                   │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python) |
| Frontend | Tauri + Vite + React |
| Native FFI | PyO3 (Rust), pybind11 (C++) |
| Build | Cargo, CMake, maturin |
| Testing | pytest, cargo test |

## 📈 Performance

| Plugin Type | Development Speed | Runtime Performance | Memory Efficiency |
|-------------|------------------|---------------------|-------------------|
| Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Rust | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| C++ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🤝 Contributing

We welcome contributions! Please:

1. Read the documentation
2. Follow code style guidelines
3. Add tests for new features
4. Update documentation
5. Submit clear PRs

## 📝 License

MIT License - see LICENSE file for details

## 🔗 Links

- **GitHub:** https://github.com/ubeydtalha/Clibshot
- **Documentation:** https://clipshot.io/docs
- **Discord:** https://discord.gg/clipshot

## ✅ Implementation Status

### Completed ✅
- [x] Python SDK with full lifecycle support
- [x] TypeScript SDK with type definitions
- [x] Python example plugin (hello-world)
- [x] Rust example plugin with PyO3
- [x] C++ example plugin with pybind11
- [x] Python plugin template
- [x] Rust plugin template
- [x] C++ plugin template
- [x] CLI tool for scaffolding
- [x] Comprehensive documentation

### Future Enhancements 🚀
- [ ] Hot reload system
- [ ] Plugin marketplace integration
- [ ] Visual plugin editor
- [ ] Performance profiling tools
- [ ] Automated testing framework

---

**Built with ❤️ by the ClipShot Team**
