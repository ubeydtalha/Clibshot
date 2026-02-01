# Plugin Development Guide

## Overview

ClipShot's plugin system allows developers to extend functionality with custom capture sources, AI models, export destinations, and more.

## Plugin Types

### 1. Capture Plugins
Provide custom capture sources (OBS, specific games, etc.)

### 2. AI Plugins
Add AI models for highlight detection, editing, analysis

### 3. Export Plugins
Add export destinations (YouTube, Discord, custom services)

### 4. Editor Plugins
Extend the video editor with custom effects

### 5. UI Plugins
Add custom UI components and views

## Quick Start

### 1. Create Plugin Structure

```
my-plugin/
├── manifest.json       # Plugin metadata
├── main.py            # Entry point
├── requirements.txt   # Dependencies
├── locales/           # Translations
│   ├── en.json
│   └── tr.json
└── README.md          # Documentation
```

### 2. Define Manifest

```json
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "A sample plugin for ClipShot",
  "author": "Your Name",
  "license": "MIT",
  "homepage": "https://github.com/yourusername/my-plugin",
  
  "clipshot_version": ">=1.0.0",
  
  "type": "export",
  
  "permissions": {
    "filesystem": {
      "level": "limited",
      "paths": ["$PLUGIN_DATA", "$CLIPS"]
    },
    "network": {
      "level": "required",
      "hosts": ["api.example.com"]
    }
  },
  
  "entry": "main.py",
  
  "settings": {
    "api_key": {
      "type": "string",
      "label": "API Key",
      "description": "Your service API key",
      "required": true,
      "secret": true
    },
    "quality": {
      "type": "select",
      "label": "Export Quality",
      "options": ["low", "medium", "high"],
      "default": "high"
    }
  }
}
```

### 3. Implement Plugin

```python
# main.py
from clipshot.plugin import Plugin, ClipContext

class MyPlugin(Plugin):
    def __init__(self, context: ClipContext):
        super().__init__(context)
        self.api_key = self.get_setting('api_key')
    
    async def export(self, clip_path: str) -> dict:
        """Export clip to external service."""
        # Your implementation here
        return {
            "success": True,
            "url": "https://example.com/clip/123"
        }
    
    def on_activate(self):
        """Called when plugin is activated."""
        self.log("Plugin activated")
    
    def on_deactivate(self):
        """Called when plugin is deactivated."""
        self.log("Plugin deactivated")

# Register plugin
plugin = MyPlugin
```

## Plugin API

### Context Object

```python
class ClipContext:
    # Settings
    def get_setting(key: str) -> Any
    def set_setting(key: str, value: Any) -> None
    
    # Filesystem
    def read_file(path: str) -> bytes
    def write_file(path: str, data: bytes) -> None
    def list_directory(path: str) -> List[str]
    
    # Network
    def http_request(url: str, method: str, **kwargs) -> Response
    
    # Logging
    def log(message: str, level: str = "info") -> None
    
    # UI
    def show_notification(title: str, message: str) -> None
    def show_dialog(message: str, buttons: List[str]) -> str
    
    # i18n
    def t(key: str, **kwargs) -> str
    def get_language() -> str
```

### Permissions

Request permissions in manifest.json:

```json
{
  "permissions": {
    "filesystem": {
      "level": "limited",
      "paths": ["$PLUGIN_DATA", "$CLIPS"],
      "operations": ["read", "write"]
    },
    "network": {
      "level": "optional",
      "hosts": ["*.example.com", "api.service.io"]
    },
    "gpu": {
      "level": "optional"
    },
    "screen": {
      "level": "required"
    }
  }
}
```

## Examples

### Example 1: Simple Export Plugin

```python
from clipshot.plugin import Plugin, ClipContext
import requests

class DiscordExportPlugin(Plugin):
    async def export(self, clip_path: str) -> dict:
        webhook_url = self.get_setting('webhook_url')
        
        with open(clip_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(webhook_url, files=files)
        
        if response.status_code == 200:
            return {"success": True}
        else:
            return {
                "success": False,
                "error": f"Upload failed: {response.status_code}"
            }
```

### Example 2: AI Highlight Detector

```python
from clipshot.plugin import Plugin
import cv2
import numpy as np

class HighlightDetectorPlugin(Plugin):
    async def analyze(self, clip_path: str) -> dict:
        # Load video
        cap = cv2.VideoCapture(clip_path)
        
        highlights = []
        frame_idx = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Analyze frame for highlights
            # (simplified example)
            if self._is_highlight_frame(frame):
                timestamp = frame_idx / cap.get(cv2.CAP_PROP_FPS)
                highlights.append({
                    "timestamp": timestamp,
                    "confidence": 0.85,
                    "type": "kill"
                })
            
            frame_idx += 1
        
        cap.release()
        
        return {
            "success": True,
            "highlights": highlights
        }
    
    def _is_highlight_frame(self, frame: np.ndarray) -> bool:
        # Your highlight detection logic
        return False
```

## Testing Plugins

### Local Testing

```bash
# Install plugin locally
clipshot plugin install ./my-plugin

# Enable plugin
clipshot plugin enable com.example.my-plugin

# Test plugin
clipshot plugin test com.example.my-plugin
```

### Unit Tests

```python
# test_plugin.py
import pytest
from my_plugin.main import MyPlugin

@pytest.fixture
def plugin():
    # Mock context
    context = MockClipContext()
    return MyPlugin(context)

def test_export(plugin):
    result = plugin.export("/path/to/clip.mp4")
    assert result["success"] == True
```

## Publishing

### 1. Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/my-plugin.git
git push -u origin main
```

### 2. Submit to Marketplace

1. Fork `clipshot-plugins/registry`
2. Add your plugin to `plugins.json`
3. Create pull request

```json
{
  "id": "com.example.my-plugin",
  "repo": "yourusername/my-plugin",
  "name": "My Plugin",
  "description": "A sample plugin",
  "category": "export",
  "trust_level": "community",
  "latest_version": "1.0.0"
}
```

### 3. Release Versioning

Follow semantic versioning:
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Best Practices

### Security
- Validate all inputs
- Never store secrets in code
- Use secure API communication
- Request minimal permissions

### Performance
- Use async/await for I/O operations
- Cache expensive computations
- Respect resource limits
- Clean up resources

### User Experience
- Provide clear error messages
- Support multiple languages
- Include helpful documentation
- Test on multiple platforms

### Code Quality
- Write unit tests
- Follow Python PEP 8
- Document public APIs
- Use type hints

## Resources

- [Plugin API Reference](../api/plugin-api.md)
- [Example Plugins](../../plugins/examples/)
- [Community Plugins](https://github.com/clipshot-plugins)
- [Support Forum](https://github.com/ubeydtalha/Clibshot/discussions)
