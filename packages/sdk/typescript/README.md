# ClipShot TypeScript SDK

TypeScript/JavaScript SDK for developing ClipShot plugins.

## Installation

```bash
npm install @clipshot/sdk
# or
yarn add @clipshot/sdk
```

## Quick Start

Create a simple plugin:

```typescript
import { ClipShotPlugin, PluginContext, Clip } from '@clipshot/sdk';

export class MyPlugin implements ClipShotPlugin {
  id = "com.example.my-plugin";
  name = "My Plugin";
  version = "1.0.0";
  
  async init(context: PluginContext): Promise<void> {
    const config = await context.getConfig();
    const logger = context.getLogger();
    logger.info("Plugin initialized!");
  }
  
  async shutdown(): Promise<void> {
    // Cleanup resources
  }
  
  async onClipCaptured(clip: Clip): Promise<void> {
    console.log("Clip captured:", clip.id);
  }
}
```

## API Reference

### ClipShotPlugin Interface

Base interface for all plugins. Implement these methods:

#### Required Methods

- `init(context: PluginContext): Promise<void>` - Initialize the plugin
- `shutdown(): Promise<void>` - Cleanup when plugin unloads

#### Optional Event Hooks

- `onClipCaptured(clip: Clip): Promise<void>` - Called when a clip is captured
- `onGameDetected(game: Game): Promise<void>` - Called when a game is detected
- `onConfigChanged(newConfig: PluginConfig): Promise<void>` - Called when config changes

### Custom API Endpoints

Use the `@apiRoute` decorator to expose custom endpoints:

```typescript
import { ClipShotPlugin, apiRoute } from '@clipshot/sdk';

export class MyPlugin implements ClipShotPlugin {
  // ... other methods
  
  @apiRoute("/status", ["GET"])
  async getStatus(): Promise<{ status: string }> {
    return { status: "healthy" };
  }
  
  @apiRoute("/process", ["POST"])
  async processData(request: any): Promise<{ result: string }> {
    // Process data
    return { result: "processed" };
  }
}
```

## Type Definitions

The SDK includes comprehensive TypeScript types for:

- `Clip` - Captured clip data
- `Game` - Detected game information
- `PluginManifest` - Plugin manifest schema
- `Permissions` - Permission system types
- Core APIs: `CaptureAPI`, `ClipAPI`, `MetadataAPI`, `EventBus`

## Building

```bash
npm run build
```

## Documentation

Full documentation available at: https://clipshot.io/docs/plugin-development

## Examples

See the [examples directory](../../../plugins/examples/) for complete plugin examples.

## License

MIT License - see LICENSE file for details
