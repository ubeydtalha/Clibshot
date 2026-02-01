# Hello World Plugin - Python Example

A simple example plugin that demonstrates how to use the ClipShot Python SDK.

## Features

- ✅ Basic plugin lifecycle management
- ✅ Event handling (clip captured, game detected)
- ✅ Custom API endpoints
- ✅ Configuration management
- ✅ Localization (English, Turkish)
- ✅ State persistence

## Installation

This plugin is included as an example and doesn't need separate installation.

## Configuration

Edit the plugin settings in ClipShot:

```json
{
  "enabled": true,
  "logLevel": "info",
  "message": "Hello from ClipShot!"
}
```

### Configuration Options

- **enabled** (boolean): Enable or disable the plugin
- **logLevel** (string): Logging level (`debug`, `info`, `warning`, `error`)
- **message** (string): Custom greeting message displayed on startup

## API Endpoints

The plugin exposes the following custom endpoints:

### GET `/api/v1/plugins/com.clipshot.hello-world-py/status`

Get plugin status and statistics.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "clip_count": 42,
  "game_count": 5,
  "config": {
    "enabled": true,
    "message": "Hello from ClipShot!",
    "logLevel": "info"
  }
}
```

### GET `/api/v1/plugins/com.clipshot.hello-world-py/stats`

Get plugin statistics.

**Response:**
```json
{
  "clips_captured": 42,
  "games_detected": 5
}
```

### POST `/api/v1/plugins/com.clipshot.hello-world-py/reset`

Reset all counters.

**Response:**
```json
{
  "success": true,
  "message": "Counters reset successfully",
  "previous": {
    "clip_count": 42,
    "game_count": 5
  }
}
```

## Event Handlers

The plugin listens to the following events:

- **on_clip_captured**: Logs information about captured clips
- **on_game_detected**: Logs information about detected games
- **on_config_changed**: Reacts to configuration changes

## Development

### File Structure

```
hello-world-py/
├── manifest.json           # Plugin metadata
├── config.schema.json      # Configuration schema
├── src/
│   └── main.py            # Plugin implementation
├── locales/
│   ├── en.json            # English translations
│   └── tr.json            # Turkish translations
├── tests/
│   └── test_main.py       # Unit tests
└── README.md              # This file
```

### Running Tests

```bash
cd plugins/examples/hello-world-py
pytest tests/ -v
```

## License

MIT License - see LICENSE file for details
