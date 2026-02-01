# ClipShot Plugin Template - Rust

Template for creating high-performance Rust plugins with PyO3.

## Quick Start

```bash
# Copy template
cp -r plugins/templates/rust-template plugins/my-rust-plugin
cd plugins/my-rust-plugin

# Update manifest.json with your plugin info
# Edit src/lib.rs to implement your plugin

# Build
maturin develop

# Test
cargo test
```

## Building

```bash
# Install maturin
pip install maturin

# Development build
maturin develop

# Release build
maturin build --release
```

## Documentation

- [Native Plugin Guide](../../../docs/10_NATIVE_PLUGIN_GUIDE.md)
- [PyO3 Documentation](https://pyo3.rs/)

Customize manifest.json and src/lib.rs for your needs.
