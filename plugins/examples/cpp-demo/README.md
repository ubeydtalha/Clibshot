# C++ Demo Plugin

A high-performance C++ plugin demonstrating native integration with ClipShot using pybind11.

## Features

- ✅ Native C++17 implementation with pybind11
- ✅ High-performance video frame processing
- ✅ Optional OpenCL support for GPU acceleration
- ✅ Thread-safe atomic counters
- ✅ Custom API endpoints
- ✅ Zero-copy operations with NumPy arrays

## Building

### Prerequisites

- CMake 3.15 or later
- C++17 compatible compiler (GCC 7+, Clang 5+, MSVC 2017+)
- Python 3.11 or later
- pybind11

### Build Commands

#### Linux/macOS

```bash
# Install pybind11
pip install pybind11

# Create build directory
mkdir build && cd build

# Configure
cmake ..

# Build
cmake --build .

# Install
cmake --install .
```

#### Windows (MSVC)

```cmd
REM Install pybind11
pip install pybind11

REM Create build directory
mkdir build
cd build

REM Configure
cmake .. -G "Visual Studio 17 2022" -A x64

REM Build
cmake --build . --config Release

REM Install
cmake --install . --config Release
```

## Usage

The plugin is loaded automatically by ClipShot. It demonstrates:

1. **High-Performance Processing**: Process video frames with C++ speed
2. **Event Handling**: React to clip capture events
3. **Custom APIs**: Expose custom endpoints for status and statistics
4. **Memory Safety**: Modern C++ with RAII and smart pointers

## Configuration

```json
{
  "enabled": true,
  "useOpenCL": false,
  "bufferSize": 1024
}
```

### Configuration Options

- **enabled** (boolean): Enable or disable the plugin
- **useOpenCL** (boolean): Enable OpenCL for GPU acceleration
- **bufferSize** (number): Buffer size for frame processing

## API Endpoints

### GET `/api/v1/plugins/com.clipshot.cpp-demo/status`

Get plugin status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "clip_count": 42,
  "use_opencl": false,
  "language": "cpp"
}
```

### GET `/api/v1/plugins/com.clipshot.cpp-demo/stats`

Get plugin statistics.

**Response:**
```json
{
  "clips_processed": 42,
  "opencl_enabled": false
}
```

### POST `/api/v1/plugins/com.clipshot.cpp-demo/reset`

Reset all counters.

## Performance

C++ plugins offer excellent performance:

- **10-100x faster** than Python for CPU-intensive tasks
- **OpenCL support** for GPU acceleration
- **Zero-copy** operations with NumPy/OpenCV
- **RAII** for automatic resource management
- **Modern C++17** features for clean, safe code

## Development

### Project Structure

```
cpp-demo/
├── CMakeLists.txt      # CMake build configuration
├── src/
│   └── plugin.cpp      # Main C++ implementation
├── locales/
│   └── en.json         # Translations
└── README.md           # This file
```

### Testing

```bash
# After building
python -c "import cpp_demo_plugin; p = cpp_demo_plugin.CppDemoPlugin(); p.init('{}')"
```

### Dependencies

The plugin uses:
- **pybind11**: C++ to Python bindings
- **STL**: Standard Template Library
- **Optional**: OpenCL for GPU acceleration

## Documentation

- [Native Plugin Guide](../../../docs/10_NATIVE_PLUGIN_GUIDE.md)
- [pybind11 Documentation](https://pybind11.readthedocs.io/)

## License

MIT License - see LICENSE file for details
