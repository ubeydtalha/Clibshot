# ClipShot Plugins

This directory contains the plugin system for ClipShot, including SDKs, example plugins, and templates.

## Directory Structure

```
plugins/
├── examples/           # Example plugins demonstrating different features
│   ├── hello-world-py/ # Python plugin example
│   ├── rust-demo/      # Rust plugin example (high-performance)
│   └── cpp-demo/       # C++ plugin example (high-performance)
│
└── templates/          # Templates for creating new plugins
    ├── python-template/ # Python plugin template
    ├── rust-template/   # Rust plugin template
    └── cpp-template/    # C++ plugin template
```

## Getting Started

### 1. Choose Your Language

ClipShot supports three languages for plugin development:

| Language | Best For | Performance | Development Speed |
|----------|----------|-------------|-------------------|
| **Python** | Quick prototyping, UI extensions, simple automations | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Rust** | CPU-intensive tasks, video encoding, AI inference | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **C++** | Legacy integrations, OpenCL/CUDA, codec development | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### 2. Create Your Plugin

#### From Template (Recommended)

```bash
# Python plugin
cp -r plugins/templates/python-template plugins/my-plugin

# Rust plugin
cp -r plugins/templates/rust-template plugins/my-rust-plugin

# C++ plugin
cp -r plugins/templates/cpp-template plugins/my-cpp-plugin
```

#### From Example

Study the example plugins in `plugins/examples/` to learn best practices:

```bash
# View Python example
cd plugins/examples/hello-world-py

# View Rust example
cd plugins/examples/rust-demo

# View C++ example
cd plugins/examples/cpp-demo
```

### 3. Install SDK

#### Python SDK

```bash
cd packages/sdk/python
pip install -e .
```

#### TypeScript SDK (for UI components)

```bash
cd packages/sdk/typescript
npm install
npm run build
```

### 4. Develop Your Plugin

1. **Update manifest.json**
   - Set unique plugin ID
   - Define permissions
   - Configure settings

2. **Implement functionality**
   - Override lifecycle hooks
   - Add event handlers
   - Create custom API endpoints

3. **Add localization**
   - Create translation files in `locales/`
   - Support at least English

4. **Test thoroughly**
   - Write unit tests
   - Test all features
   - Verify permissions

### 5. Package and Publish

```bash
# Build your plugin
# Python: No build needed
# Rust: maturin build --release
# C++: cmake --build . --config Release

# Create GitHub repository
# Create a release
# Submit to ClipShot marketplace
```

## Example Plugins

### Hello World (Python)

A simple plugin demonstrating basic SDK usage:
- Lifecycle hooks
- Event handling
- Custom API endpoints
- Configuration management

**Location:** `plugins/examples/hello-world-py/`

### Rust Demo

High-performance plugin with:
- PyO3 integration
- SIMD optimizations
- Zero-copy operations
- Atomic counters

**Location:** `plugins/examples/rust-demo/`

### C++ Demo

Native C++ plugin featuring:
- pybind11 bindings
- OpenCL support (optional)
- Video frame processing
- Modern C++17

**Location:** `plugins/examples/cpp-demo/`

## Plugin Templates

### Python Template

Complete starter template for Python plugins:
- SDK integration
- Best practices
- Configuration schema
- Localization setup

**Location:** `plugins/templates/python-template/`

### Rust Template

Template for high-performance Rust plugins:
- Cargo configuration
- PyO3 setup
- Build scripts
- Release optimization

**Location:** `plugins/templates/rust-template/`

### C++ Template

Template for native C++ plugins:
- CMake configuration
- pybind11 setup
- Cross-platform support
- Build instructions

**Location:** `plugins/templates/cpp-template/`

## Documentation

### For Plugin Developers

- [Plugin Developer Guide](../docs/02_PLUGIN_DEVELOPER_GUIDE.md) - Complete guide
- [Native Plugin Guide](../docs/10_NATIVE_PLUGIN_GUIDE.md) - Rust/C++ specifics
- [Marketplace Guide](../docs/07_MARKETPLACE_GITHUB.md) - Publishing

### SDK References

- [Python SDK](../packages/sdk/python/README.md)
- [TypeScript SDK](../packages/sdk/typescript/README.md)

### Architecture

- [Backend Architecture](../docs/03_BACKEND_ARCHITECTURE.md)
- [Frontend Architecture](../docs/04_FRONTEND_ARCHITECTURE.md)

## Quick Reference

### Python Plugin Structure

```python
from clipshot_sdk import Plugin, Clip, PluginContext

class MyPlugin(Plugin):
    id = "com.example.my-plugin"
    name = "My Plugin"
    version = "1.0.0"
    
    async def init(self, context: PluginContext):
        self.config = await context.get_config()
        self.logger = context.get_logger()
    
    async def on_clip_captured(self, clip: Clip):
        self.logger.info(f"Clip: {clip.title}")
```

### Rust Plugin Structure

```rust
use pyo3::prelude::*;

#[pyclass]
pub struct MyPlugin {
    // fields
}

#[pymethods]
impl MyPlugin {
    #[new]
    fn new() -> Self { /* ... */ }
    
    fn init(&mut self, config: &str) -> PyResult<()> {
        // Initialize
        Ok(())
    }
}
```

### Manifest.json Key Fields

```json
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "api_version": "v1",
  "type": "optional",
  "category": "enhancement",
  "entry": {
    "backend": "src/main.py"
  },
  "permissions": {
    "filesystem": {
      "level": "limited",
      "paths": ["$PLUGIN_DATA"]
    }
  }
}
```

## Contributing

When contributing plugins or templates:

1. Follow the existing code style
2. Add comprehensive documentation
3. Include tests
4. Support localization
5. Respect security guidelines

## Support

- [GitHub Issues](https://github.com/ubeydtalha/Clibshot/issues)
- [Documentation](https://clipshot.io/docs)
- [Discord Community](https://discord.gg/clipshot)

## License

See individual plugin licenses. Templates are MIT licensed.
