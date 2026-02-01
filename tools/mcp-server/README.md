# ClipShot MCP Server

Model Context Protocol server for ClipShot performance monitoring.

## Features

- Real-time performance metrics
- System health monitoring
- Plugin status tracking
- AI-controllable via MCP protocol

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a standalone server

```bash
python -m tools.mcp_server.server
```

### As an MCP server

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "clipshot-performance": {
      "command": "python",
      "args": ["-m", "tools.mcp_server.server"],
      "env": {
        "CLIPSHOT_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

## Available Tools

### get_metrics
Get current performance metrics.

**Arguments:**
- `metric_names` (array, optional): Specific metrics to retrieve
- `window_seconds` (number, default: 60): Time window for statistics

### get_system_health
Get overall system health status.

### get_plugin_status
Get status of running plugins.

**Arguments:**
- `plugin_id` (string, optional): Specific plugin ID

### set_metric_threshold
Set alert threshold for a metric.

**Arguments:**
- `metric_name` (string, required): Metric name
- `threshold` (number, required): Threshold value

## Resources

- `metrics://current` - Real-time performance metrics
- `metrics://history` - Historical performance data
- `health://status` - Overall system health status
