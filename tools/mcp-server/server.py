"""
MCP (Model Context Protocol) Server for ClipShot Performance Monitoring.

This server exposes ClipShot's performance metrics and control APIs
to AI assistants and monitoring tools via the MCP protocol.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

# MCP Server implementation
class MCPServer:
    """
    Model Context Protocol server for ClipShot monitoring.
    
    Provides AI-controllable access to:
    - Performance metrics
    - Resource usage
    - System health
    - Plugin status
    """
    
    def __init__(self, metrics_collector=None):
        self.metrics = metrics_collector
        self.tools = self._register_tools()
        self.resources = self._register_resources()
    
    def _register_tools(self) -> Dict[str, Dict]:
        """Register available MCP tools."""
        return {
            "get_metrics": {
                "name": "get_metrics",
                "description": "Get current performance metrics",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metric_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific metrics to retrieve (optional)"
                        },
                        "window_seconds": {
                            "type": "number",
                            "description": "Time window for statistics (default: 60)",
                            "default": 60
                        }
                    }
                }
            },
            "get_system_health": {
                "name": "get_system_health",
                "description": "Get overall system health status",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            "get_plugin_status": {
                "name": "get_plugin_status",
                "description": "Get status of running plugins",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "plugin_id": {
                            "type": "string",
                            "description": "Specific plugin ID (optional)"
                        }
                    }
                }
            },
            "set_metric_threshold": {
                "name": "set_metric_threshold",
                "description": "Set alert threshold for a metric",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metric_name": {
                            "type": "string",
                            "description": "Metric name"
                        },
                        "threshold": {
                            "type": "number",
                            "description": "Threshold value"
                        }
                    },
                    "required": ["metric_name", "threshold"]
                }
            }
        }
    
    def _register_resources(self) -> Dict[str, Dict]:
        """Register available MCP resources."""
        return {
            "metrics://current": {
                "uri": "metrics://current",
                "name": "Current Metrics",
                "description": "Real-time performance metrics",
                "mimeType": "application/json"
            },
            "metrics://history": {
                "uri": "metrics://history",
                "name": "Metrics History",
                "description": "Historical performance data",
                "mimeType": "application/json"
            },
            "health://status": {
                "uri": "health://status",
                "name": "System Health",
                "description": "Overall system health status",
                "mimeType": "application/json"
            }
        }
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool call."""
        if name == "get_metrics":
            return await self._get_metrics(arguments)
        elif name == "get_system_health":
            return await self._get_system_health()
        elif name == "get_plugin_status":
            return await self._get_plugin_status(arguments)
        elif name == "set_metric_threshold":
            return await self._set_metric_threshold(arguments)
        else:
            return {"error": f"Unknown tool: {name}"}
    
    async def get_resource(self, uri: str) -> Dict[str, Any]:
        """Get an MCP resource."""
        if uri == "metrics://current":
            return await self._get_current_metrics()
        elif uri == "metrics://history":
            return await self._get_metrics_history()
        elif uri == "health://status":
            return await self._get_system_health()
        else:
            return {"error": f"Unknown resource: {uri}"}
    
    async def _get_metrics(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get specific metrics."""
        if not self.metrics:
            return {"error": "Metrics collector not available"}
        
        window_seconds = args.get("window_seconds", 60)
        metric_names = args.get("metric_names", [])
        
        result = {}
        
        if metric_names:
            # Get specific metrics
            for name in metric_names:
                stats = self.metrics.get_stats(name, window_seconds)
                if stats:
                    result[name] = {
                        "min": stats.min,
                        "max": stats.max,
                        "avg": stats.avg,
                        "p50": stats.p50,
                        "p95": stats.p95,
                        "p99": stats.p99,
                        "count": stats.count,
                    }
        else:
            # Get all metrics
            result = self.metrics.get_all_metrics()
        
        return {
            "success": True,
            "metrics": result,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_current_metrics(self) -> Dict[str, Any]:
        """Get current real-time metrics."""
        if not self.metrics:
            return {"error": "Metrics collector not available"}
        
        return {
            "success": True,
            "data": self.metrics.get_all_metrics(),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_metrics_history(self) -> Dict[str, Any]:
        """Get historical metrics data."""
        # This would pull from a time-series database in production
        return {
            "success": True,
            "data": {},
            "note": "Historical data not yet implemented"
        }
    
    async def _get_system_health(self, args: Optional[Dict] = None) -> Dict[str, Any]:
        """Get overall system health."""
        if not self.metrics:
            return {"error": "Metrics collector not available"}
        
        # Get key metrics
        cpu_stats = self.metrics.get_stats("system.cpu.percent", 10)
        memory_stats = self.metrics.get_stats("system.memory.percent", 10)
        
        # Determine health status
        health = "healthy"
        issues = []
        
        if cpu_stats and cpu_stats.p95 > 80:
            health = "degraded"
            issues.append(f"High CPU usage: {cpu_stats.p95:.1f}%")
        
        if memory_stats and memory_stats.p95 > 80:
            health = "degraded"
            issues.append(f"High memory usage: {memory_stats.p95:.1f}%")
        
        if len(issues) > 2:
            health = "critical"
        
        return {
            "success": True,
            "status": health,
            "issues": issues,
            "metrics": {
                "cpu": cpu_stats.p95 if cpu_stats else 0,
                "memory": memory_stats.p95 if memory_stats else 0,
            },
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_plugin_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get plugin execution status."""
        # This would query the plugin manager in production
        return {
            "success": True,
            "plugins": [],
            "note": "Plugin status tracking not yet implemented"
        }
    
    async def _set_metric_threshold(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Set a metric threshold for alerting."""
        if not self.metrics:
            return {"error": "Metrics collector not available"}
        
        metric_name = args.get("metric_name")
        threshold = args.get("threshold")
        
        if not metric_name or threshold is None:
            return {"error": "Missing required arguments"}
        
        self.metrics.set_threshold(metric_name, threshold)
        
        return {
            "success": True,
            "message": f"Threshold set for {metric_name}: {threshold}"
        }


# Server configuration
def create_mcp_config() -> Dict[str, Any]:
    """Create MCP server configuration."""
    return {
        "mcpServers": {
            "clipshot-performance": {
                "command": "python",
                "args": ["-m", "tools.mcp_server"],
                "env": {
                    "CLIPSHOT_API_URL": "http://localhost:8000"
                }
            }
        }
    }


if __name__ == "__main__":
    # Simple CLI for testing
    import sys
    
    async def main():
        server = MCPServer()
        
        # Test tool call
        result = await server.call_tool("get_system_health", {})
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
