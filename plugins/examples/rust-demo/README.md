# Rust Demo Plugin

A high-performance Rust plugin demonstrating native integration with ClipShot using PyO3.

## Features

- ✅ Native Rust implementation with PyO3
- ✅ High-performance image processing
- ✅ SIMD optimization support
- ✅ Zero-copy operations
- ✅ Thread-safe atomic counters
- ✅ Custom API endpoints

## Building

### Prerequisites

- Rust 1.75 or later
- Python 3.11 or later
- maturin (Rust to Python build tool)

### Build Commands

```bash
# Install maturin
pip install maturin

# Development build
maturin develop

# Release build
maturin build --release

# Install the built package
pip install target/wheels/rust_demo_plugin-*.whl
```

## Usage

The plugin is loaded automatically by ClipShot. It demonstrates:

1. **High-Performance Processing**: Process image data with optional SIMD optimizations
2. **Event Handling**: React to clip capture events
3. **Custom APIs**: Expose custom endpoints for status and statistics

## Configuration

```json
{
  "enabled": true,
  "useSIMD": true,
  "threadCount": 4
}
```

### Configuration Options

- **enabled** (boolean): Enable or disable the plugin
- **useSIMD** (boolean): Enable SIMD optimizations for image processing
- **threadCount** (number): Number of threads for parallel processing

## API Endpoints

### GET `/api/v1/plugins/com.clipshot.rust-demo/status`

Get plugin status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "clip_count": 42,
  "use_simd": true,
  "language": "rust"
}
```

### GET `/api/v1/plugins/com.clipshot.rust-demo/stats`

Get plugin statistics.

**Response:**
```json
{
  "clips_processed": 42,
  "simd_enabled": true
}
```

### POST `/api/v1/plugins/com.clipshot.rust-demo/reset`

Reset all counters.

## Performance

Rust plugins offer significant performance benefits:

- **10-100x faster** than Python for CPU-intensive tasks
- **Zero-copy** operations with NumPy arrays
- **SIMD** vectorization for parallel processing
- **Memory safety** without garbage collection overhead

## Development

### Project Structure

```
rust-demo/
├── Cargo.toml          # Rust dependencies
├── pyproject.toml      # Python package metadata
├── src/
│   └── lib.rs          # Main Rust implementation
├── locales/
│   └── en.json         # Translations
└── README.md           # This file
```

### Testing

```bash
# Run Rust tests
cargo test

# Run with Python
python -c "import rust_demo_plugin; p = rust_demo_plugin.RustDemoPlugin(); p.init('{}')"
```

## Documentation

- [Native Plugin Guide](../../../docs/10_NATIVE_PLUGIN_GUIDE.md)
- [PyO3 Documentation](https://pyo3.rs/)

## License

MIT License - see LICENSE file for details
