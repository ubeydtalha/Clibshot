# ClipShot CLI

Command-line tool for ClipShot plugin development.

## Installation

```bash
# Make the script executable
chmod +x tools/clipshot-cli/clipshot

# Add to PATH (optional)
export PATH="$PATH:$(pwd)/tools/clipshot-cli"

# Or create a symlink
ln -s $(pwd)/tools/clipshot-cli/clipshot /usr/local/bin/clipshot
```

## Usage

### Create a New Plugin

```bash
# Create a Python plugin
clipshot create my-plugin --language python

# Create a Rust plugin
clipshot create my-rust-plugin --language rust

# Create a C++ plugin
clipshot create my-cpp-plugin --language cpp

# Specify output directory
clipshot create my-plugin --output ./custom/path
```

### Validate Plugin Manifest

```bash
# Validate a manifest file
clipshot validate ./plugins/my-plugin/manifest.json
```

## Commands

### `clipshot create`

Create a new plugin from template.

**Arguments:**
- `name` - Plugin name (required)
- `--language, -l` - Plugin language: python, rust, cpp (default: python)
- `--output, -o` - Output directory (default: ./plugins/{name})

**Example:**
```bash
clipshot create awesome-plugin --language python
```

### `clipshot validate`

Validate a plugin manifest file.

**Arguments:**
- `manifest` - Path to manifest.json (required)

**Example:**
```bash
clipshot validate ./plugins/my-plugin/manifest.json
```

## Development

The CLI tool is written in Python and uses only standard library modules for maximum compatibility.

### Adding New Commands

1. Add a new subparser in `main()`
2. Implement the command function
3. Update this README

## Requirements

- Python 3.11 or later
- No external dependencies

## License

MIT License - see LICENSE file for details
