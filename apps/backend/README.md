# ClipShot Backend

FastAPI backend for the ClipShot gaming clip platform.

## Features

- 🚀 **FastAPI** - Modern, fast web framework
- 🧩 **Plugin System** - Modular plugin architecture with discovery and lifecycle management
- 🤖 **AI Runtime** - Abstract AI runtime with ONNX support
- 📊 **OpenAPI** - Auto-generated API documentation
- 🔒 **CORS** - Configured for Tauri frontend
- 📝 **Logging** - Structured logging with loguru
- ⚙️ **Configuration** - Environment-based configuration with pydantic-settings

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

Key configuration options:
- `DEBUG` - Enable debug mode
- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `DATABASE_URL` - Database connection string
- `PLUGINS_DIR` - Directory for plugins
- `AI_MODELS_DIR` - Directory for AI models

### Running

Development mode:
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Production mode:
```bash
python src/main.py
```

## API Documentation

Once running, access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Project Structure

```
apps/backend/
├── src/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management
│   │
│   ├── api/                       # API layer
│   │   ├── deps.py                # Dependency injection
│   │   └── v1/
│   │       ├── router.py          # Main API router
│   │       └── routes/            # API route modules
│   │           ├── plugins.py     # Plugin management endpoints
│   │           └── ai.py          # AI runtime endpoints
│   │
│   ├── core/                      # Core utilities
│   │   ├── events.py              # Event bus
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── logging.py             # Logging configuration
│   │
│   ├── plugins/                   # Plugin system
│   │   └── manager.py             # Plugin manager
│   │
│   ├── ai/                        # AI runtime
│   │   ├── interface.py           # Abstract AI runtime interface
│   │   └── onnx_runtime.py        # ONNX Runtime implementation
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   └── plugin.py              # Plugin schemas
│   │
│   ├── models/                    # Database models (future)
│   ├── services/                  # Business logic (future)
│   └── db/                        # Database utilities (future)
│
├── tests/                         # Tests
├── alembic/                       # Database migrations
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project configuration
└── .env.example                   # Example environment variables
```

## API Endpoints

### System

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Plugins

- `GET /api/v1/plugins/` - List all plugins
- `GET /api/v1/plugins/{plugin_id}` - Get plugin details
- `POST /api/v1/plugins/{plugin_id}/load` - Load a plugin
- `POST /api/v1/plugins/{plugin_id}/unload` - Unload a plugin
- `POST /api/v1/plugins/{plugin_id}/reload` - Reload a plugin

### AI Runtime

- `GET /api/v1/ai/health` - Get AI runtime health status
- `GET /api/v1/ai/models` - List available AI models
- `POST /api/v1/ai/models/{model_id}/load` - Load an AI model
- `POST /api/v1/ai/models/{model_id}/unload` - Unload an AI model
- `POST /api/v1/ai/infer` - Run AI inference

## Plugin Development

### Plugin Structure

```
my-plugin/
├── manifest.json              # Plugin manifest (required)
├── src/
│   └── main.py                # Backend entry point (required)
├── locales/
│   └── en.json                # Localization (required)
└── README.md                  # Documentation (recommended)
```

### Example Plugin Manifest

```json
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "api_version": "v1",
  "type": "optional",
  "category": "enhancement",
  "description": {
    "en": "Description of my plugin"
  },
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "MIT",
  "entry": {
    "backend": "src/main.py"
  },
  "permissions": {},
  "platforms": ["windows"],
  "engines": {
    "clipshot": ">=0.1.0",
    "python": ">=3.11"
  }
}
```

### Example Plugin Code

```python
"""Example plugin for ClipShot."""

async def init() -> None:
    """Initialize the plugin."""
    print("Plugin initialized!")

async def shutdown() -> None:
    """Shutdown the plugin."""
    print("Plugin shutting down!")
```

## Development

### Code Style

- Use `black` for formatting
- Use `mypy` for type checking
- Use `pylint` for linting

```bash
# Format code
black src/

# Type check
mypy src/

# Lint
pylint src/
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## Architecture

### Plugin System

The plugin system uses a discovery-based approach:

1. **Discovery**: Scans the plugins directory for `manifest.json` files
2. **Dependency Resolution**: Resolves plugin dependencies using topological sort
3. **Loading**: Loads plugins in order, importing Python modules
4. **Lifecycle**: Manages plugin lifecycle (init, shutdown)
5. **Hot Reload**: Supports reloading plugins without restart

### AI Runtime

The AI runtime provides an abstract interface for different AI backends:

- **Abstract Interface**: Defines common operations (load, infer, health)
- **ONNX Runtime**: Implements local inference using ONNX models
- **Extensible**: Easy to add new backends (TensorFlow Lite, etc.)

### Event Bus

The event bus enables pub/sub communication between components:

```python
# Subscribe to events
event_bus.subscribe("plugin.loaded", on_plugin_loaded)

# Publish events
await event_bus.publish("plugin.loaded", {"plugin_id": "my-plugin"})
```

## Configuration

See `.env.example` for all configuration options.

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `APP_NAME` | string | "ClipShot API" | Application name |
| `VERSION` | string | "0.1.0" | Application version |
| `DEBUG` | boolean | false | Debug mode |
| `CORS_ORIGINS` | string (CSV) | See .env | Allowed CORS origins |
| `DATABASE_URL` | string | sqlite+aiosqlite:///./clipshot.db | Database URL |
| `PLUGINS_DIR` | string | ./plugins | Plugins directory |
| `AI_MODELS_DIR` | string | ./models | AI models directory |
| `LOG_LEVEL` | string | INFO | Logging level |

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read the contributing guidelines in the main repository.
