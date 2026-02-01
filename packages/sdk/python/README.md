# ClipShot Python SDK

Python SDK for developing ClipShot plugins.

## Installation

```bash
pip install clipshot-sdk
```

## Quick Start

Create a simple plugin:

```python
from clipshot_sdk import Plugin, Clip, PluginContext

class MyPlugin(Plugin):
    id = "com.example.my-plugin"
    name = "My Plugin"
    version = "1.0.0"
    
    async def init(self, context: PluginContext):
        self.config = await context.get_config()
        self.logger = context.get_logger()
        self.logger.info("Plugin initialized!")
    
    async def on_clip_captured(self, clip: Clip):
        self.logger.info(f"Clip captured: {clip.id}")
```

## API Reference

### Plugin Class

Base class for all plugins. Implement the following methods:

#### Lifecycle Hooks

- `init(context: PluginContext)` - Called when plugin loads
- `shutdown()` - Called when plugin unloads
- `on_config_changed(new_config: dict)` - Called when config changes

#### Event Hooks

- `on_clip_captured(clip: Clip)` - Called when a clip is captured
- `on_game_detected(game: Game)` - Called when a game is detected

### Custom API Endpoints

Use the `@api_route` decorator to expose custom endpoints:

```python
from clipshot_sdk import Plugin, api_route

class MyPlugin(Plugin):
    @api_route("/status", methods=["GET"])
    async def get_status(self) -> dict:
        return {"status": "healthy"}
    
    @api_route("/process", methods=["POST"])
    async def process_data(self, request: dict) -> dict:
        result = await self.process(request["data"])
        return {"result": result}
```

## Documentation

Full documentation available at: https://clipshot.io/docs/plugin-development

## Examples

See the [examples directory](../../../plugins/examples/) for complete plugin examples.

## License

MIT License - see LICENSE file for details
