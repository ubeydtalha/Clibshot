# API Reference

## Overview

ClipShot provides a REST API for managing clips, plugins, and AI features.

**Base URL**: `http://localhost:8000`

**Authentication**: Bearer token (in production)

**Rate Limiting**: 100 requests/minute per IP

## Endpoints

### Health Check

#### GET /health

Check API server status.

**Response**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Performance Metrics

#### GET /api/metrics

Get current performance metrics.

**Query Parameters**
- `window` (optional): Time window in seconds (default: 60)
- `metrics` (optional): Comma-separated metric names

**Response**
```json
{
  "success": true,
  "metrics": {
    "system.cpu.percent": {
      "current": 45.2,
      "min": 20.1,
      "max": 78.5,
      "p95": 65.3
    },
    "system.memory.percent": {
      "current": 62.8,
      "min": 55.2,
      "max": 75.1,
      "p95": 72.4
    }
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### POST /api/metrics/threshold

Set metric alert threshold.

**Request Body**
```json
{
  "metric_name": "system.cpu.percent",
  "threshold": 80.0
}
```

**Response**
```json
{
  "success": true,
  "message": "Threshold set for system.cpu.percent: 80.0"
}
```

### Plugin Management

#### GET /api/plugins

List all installed plugins.

**Response**
```json
{
  "plugins": [
    {
      "id": "com.example.plugin",
      "name": "Example Plugin",
      "version": "1.0.0",
      "enabled": true,
      "type": "export"
    }
  ]
}
```

#### POST /api/plugins/{plugin_id}/permissions

Grant permissions to a plugin.

**Request Body**
```json
{
  "category": "filesystem",
  "level": "limited",
  "paths": ["$PLUGIN_DATA", "$CLIPS"]
}
```

**Response**
```json
{
  "success": true,
  "message": "Permission granted"
}
```

## Error Responses

### Error Format

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "Plugin does not have filesystem permission",
    "details": {
      "plugin_id": "com.example.plugin",
      "resource": "/path/to/file"
    }
  }
}
```

### Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## MCP Protocol

### Tools

#### get_metrics

Get performance metrics.

**Input Schema**
```json
{
  "type": "object",
  "properties": {
    "metric_names": {
      "type": "array",
      "items": {"type": "string"}
    },
    "window_seconds": {
      "type": "number",
      "default": 60
    }
  }
}
```

#### get_system_health

Get overall system health.

**Response**
```json
{
  "success": true,
  "status": "healthy",
  "issues": [],
  "metrics": {
    "cpu": 45.2,
    "memory": 62.8
  }
}
```

### Resources

- `metrics://current` - Real-time metrics
- `metrics://history` - Historical data
- `health://status` - System health

## TypeScript Types

```typescript
// Performance Metrics
interface MetricSample {
  name: string;
  value: number;
  timestamp: string;
  tags?: Record<string, string>;
}

interface MetricStats {
  name: string;
  min: number;
  max: number;
  avg: number;
  p50: number;
  p95: number;
  p99: number;
  count: number;
  window_seconds: number;
}

// Plugin Types
interface Plugin {
  id: string;
  name: string;
  version: string;
  enabled: boolean;
  type: 'capture' | 'ai' | 'export' | 'editor' | 'ui';
}

interface PermissionGrant {
  category: 'screen' | 'microphone' | 'filesystem' | 'network' | 'gpu' | 'system';
  level: 'none' | 'limited' | 'optional' | 'required';
  granted: boolean;
  paths?: string[];
  hosts?: string[];
  apis?: string[];
}
```

## WebSocket Events

Connect to: `ws://localhost:8000/ws`

### Events

#### metrics:update
Real-time metric updates

```json
{
  "event": "metrics:update",
  "data": {
    "system.cpu.percent": 45.2,
    "system.memory.percent": 62.8
  }
}
```

#### sandbox:limit_exceeded
Plugin resource limit exceeded

```json
{
  "event": "sandbox:limit_exceeded",
  "data": {
    "plugin_id": "com.example.plugin",
    "resource": "memory",
    "usage": 600.5,
    "limit": 512.0
  }
}
```

## Python SDK

```python
from clipshot import ClipShotClient

# Initialize client
client = ClipShotClient(base_url="http://localhost:8000")

# Get metrics
metrics = await client.metrics.get()

# Set threshold
await client.metrics.set_threshold("system.cpu.percent", 80.0)

# Get system health
health = await client.health.get()
```

## Rate Limiting

- **Default**: 100 requests/minute per IP
- **Burst**: 10 requests/second
- **Headers**:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## Versioning

API version is included in the base URL:
- `v1`: Current stable version
- Future: `v2`, `v3`, etc.

## Support

- API Issues: https://github.com/ubeydtalha/Clibshot/issues
- API Discussions: https://github.com/ubeydtalha/Clibshot/discussions
