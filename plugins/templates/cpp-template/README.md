# ClipShot Plugin Template - C++

Template for creating high-performance C++ plugins with pybind11.

## Quick Start

```bash
# Copy template
cp -r plugins/templates/cpp-template plugins/my-cpp-plugin
cd plugins/my-cpp-plugin

# Update manifest.json with your plugin info
# Edit src/plugin.cpp to implement your plugin

# Build
mkdir build && cd build
cmake ..
cmake --build .
```

## Building

```bash
# Install pybind11
pip install pybind11

# Configure and build
mkdir build && cd build
cmake ..
cmake --build . --config Release
cmake --install .
```

## Documentation

- [Native Plugin Guide](../../../docs/10_NATIVE_PLUGIN_GUIDE.md)
- [pybind11 Documentation](https://pybind11.readthedocs.io/)

Customize manifest.json and src/plugin.cpp for your needs.
