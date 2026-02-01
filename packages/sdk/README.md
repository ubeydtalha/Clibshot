# ClipShot Plugin SDKs

This directory contains the Software Development Kits (SDKs) for creating ClipShot plugins.

## Available SDKs

### Python SDK

**Location:** `packages/sdk/python/`

The Python SDK provides a simple, Pythonic API for creating ClipShot plugins.

**Features:**
- Abstract base class for plugins
- Lifecycle hooks (init, shutdown)
- Event hooks (clip captured, game detected)
- Custom API endpoint decorators
- Type hints for better IDE support
- Async/await support

**Installation:**
```bash
pip install clipshot-sdk
```

**Quick Example:**
```python
from clipshot_sdk import Plugin, Clip, PluginContext

class MyPlugin(Plugin):
    id = "com.example.my-plugin"
    name = "My Plugin"
    version = "1.0.0"
    
    async def init(self, context: PluginContext):
        self.logger = context.get_logger()
        self.logger.info("Plugin initialized!")
    
    async def on_clip_captured(self, clip: Clip):
        self.logger.info(f"Clip: {clip.title}")
```

**Documentation:** [Python SDK README](python/README.md)

---

### TypeScript SDK

**Location:** `packages/sdk/typescript/`

The TypeScript SDK provides type-safe interfaces for creating ClipShot plugins in TypeScript/JavaScript.

**Features:**
- Full TypeScript type definitions
- Plugin interface and types
- Core API types
- Event system types
- Decorator support
- Comprehensive JSDoc comments

**Installation:**
```bash
npm install @clipshot/sdk
```

**Quick Example:**
```typescript
import { ClipShotPlugin, PluginContext, Clip } from '@clipshot/sdk';

export class MyPlugin implements ClipShotPlugin {
  id = "com.example.my-plugin";
  name = "My Plugin";
  version = "1.0.0";
  
  async init(context: PluginContext): Promise<void> {
    const logger = context.getLogger();
    logger.info("Plugin initialized!");
  }
  
  async onClipCaptured(clip: Clip): Promise<void> {
    console.log(`Clip: ${clip.title}`);
  }
  
  async shutdown(): Promise<void> {
    // Cleanup
  }
}
```

**Documentation:** [TypeScript SDK README](typescript/README.md)

---

## Choosing an SDK

| Use Case | Recommended SDK | Why |
|----------|----------------|-----|
| Backend processing | Python | Rich ecosystem, easy async |
| UI components | TypeScript | Type safety, React integration |
| High performance | Rust/C++ | Native speed (see native plugins) |

## SDK Comparison

| Feature | Python SDK | TypeScript SDK |
|---------|-----------|----------------|
| **Platform** | Backend | Frontend/Backend |
| **Type Safety** | Type hints | Full TypeScript |
| **Async Support** | ✅ Native | ✅ Native |
| **Event System** | ✅ | ✅ |
| **Custom APIs** | ✅ Decorator | ✅ Decorator |
| **UI Components** | ❌ | ✅ |
| **Performance** | ⭐⭐⭐ | ⭐⭐⭐ |
| **Learning Curve** | Easy | Moderate |

## Common Patterns

### Lifecycle Management

Both SDKs follow the same lifecycle pattern:

1. **Initialize** - Load configuration, setup resources
2. **Running** - Handle events, process data
3. **Shutdown** - Clean up resources

### Event Handling

Plugins can respond to various events:

- `on_clip_captured` / `onClipCaptured` - When a clip is captured
- `on_game_detected` / `onGameDetected` - When a game is detected
- `on_config_changed` / `onConfigChanged` - When settings change

### Custom API Endpoints

Both SDKs support custom HTTP endpoints:

**Python:**
```python
@api_route("/status", methods=["GET"])
async def get_status(self) -> dict:
    return {"status": "healthy"}
```

**TypeScript:**
```typescript
@apiRoute("/status", ["GET"])
async getStatus(): Promise<{ status: string }> {
  return { status: "healthy" };
}
```

## Development Workflow

1. **Install SDK**
   ```bash
   # Python
   pip install clipshot-sdk
   
   # TypeScript
   npm install @clipshot/sdk
   ```

2. **Create Plugin**
   - Use templates from `plugins/templates/`
   - Implement required methods
   - Add event handlers

3. **Test Locally**
   ```bash
   # Python
   pytest tests/
   
   # TypeScript
   npm test
   ```

4. **Build** (TypeScript only)
   ```bash
   npm run build
   ```

5. **Package**
   - Python: Use setuptools/pip
   - TypeScript: Use npm/yarn

## Documentation

### Guides
- [Plugin Developer Guide](../../docs/02_PLUGIN_DEVELOPER_GUIDE.md)
- [Native Plugin Guide](../../docs/10_NATIVE_PLUGIN_GUIDE.md)
- [Marketplace Guide](../../docs/07_MARKETPLACE_GITHUB.md)

### API References
- [Python SDK API](python/README.md)
- [TypeScript SDK API](typescript/README.md)

### Examples
- [Python Examples](../../plugins/examples/hello-world-py/)
- [Rust Examples](../../plugins/examples/rust-demo/)
- [C++ Examples](../../plugins/examples/cpp-demo/)

## Contributing

We welcome contributions to the SDKs! Please:

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Submit PRs with clear descriptions

## Support

- [GitHub Issues](https://github.com/ubeydtalha/Clibshot/issues)
- [Documentation](https://clipshot.io/docs)
- [Discord](https://discord.gg/clipshot)

## License

MIT License - see individual SDK directories for details.
