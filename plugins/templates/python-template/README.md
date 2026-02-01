# ClipShot Plugin Template - Python

This template provides a starting point for creating ClipShot plugins in Python.

## Quick Start

1. **Copy this template:**
   ```bash
   cp -r plugins/templates/python-template plugins/my-plugin
   cd plugins/my-plugin
   ```

2. **Update `manifest.json`:**
   - Change `id` to your unique plugin ID (e.g., `com.yourname.my-plugin`)
   - Update `name`, `description`, and `author` fields
   - Adjust permissions as needed

3. **Implement your plugin in `src/main.py`:**
   - Modify the `MyPlugin` class
   - Implement event handlers
   - Add custom API endpoints

4. **Configure localization:**
   - Edit `locales/en.json` (required)
   - Add additional language files as needed

5. **Test your plugin:**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Load in ClipShot (development mode)
   clipshot dev --plugin-dir ./plugins/my-plugin
   ```

## Template Structure

```
python-template/
├── manifest.json          # Plugin metadata
├── config.schema.json     # Configuration schema
├── src/
│   └── main.py           # Plugin implementation
├── locales/
│   └── en.json           # English translations
├── tests/
│   └── test_plugin.py    # Unit tests
└── README.md             # This file
```

## Customization Guide

### manifest.json

Update these key fields:

```json
{
  "id": "com.yourname.my-plugin",           // REQUIRED: Unique ID
  "name": "My Plugin",                       // REQUIRED: Display name
  "version": "1.0.0",                        // REQUIRED: Version
  "author": {
    "name": "Your Name",                     // REQUIRED
    "email": "you@example.com",              // REQUIRED
    "url": "https://yourwebsite.com"         // Optional
  },
  "description": {
    "en": "What your plugin does"            // REQUIRED
  }
}
```

### src/main.py

Implement your plugin logic:

```python
from clipshot_sdk import Plugin, Clip, PluginContext

class MyPlugin(Plugin):
    id = "com.yourname.my-plugin"
    name = "My Plugin"
    version = "1.0.0"
    
    async def init(self, context: PluginContext):
        # Initialize your plugin
        self.config = await context.get_config()
        self.logger = context.get_logger()
    
    async def on_clip_captured(self, clip: Clip):
        # Handle clip events
        self.logger.info(f"Clip: {clip.title}")
```

## Documentation

- [Plugin Developer Guide](../../../docs/02_PLUGIN_DEVELOPER_GUIDE.md)
- [Python SDK Reference](../../../packages/sdk/python/README.md)
- [Example Plugins](../../examples/)

## Publishing

When ready to publish:

1. Ensure all tests pass
2. Update version in `manifest.json`
3. Create a GitHub repository
4. Create a release
5. Submit to ClipShot marketplace

## License

Choose a license for your plugin (e.g., MIT, Apache 2.0, GPL)
