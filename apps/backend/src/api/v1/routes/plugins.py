"""
Plugin Management Routes.

Endpoints for managing plugins:
- List all plugins
- Get plugin details
- Load/unload plugins
- Reload plugins
- Get plugin configuration
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.deps import get_plugin_manager
from src.schemas.plugin import (
    PluginInfo,
    PluginLoadResponse,
    PluginStatus,
    PluginType,
    PluginCategory,
)
from src.plugins.manager import PluginManager, Plugin
from src.core.exceptions import PluginNotFoundError, PluginLoadError, PluginAlreadyLoadedError

router = APIRouter()


def plugin_to_info(plugin: Plugin) -> PluginInfo:
    """Convert Plugin to PluginInfo schema."""
    description = plugin.manifest.description.get("en", "")
    if not description and plugin.manifest.description:
        # Get first available description
        description = next(iter(plugin.manifest.description.values()), "")
    
    return PluginInfo(
        id=plugin.id,
        name=plugin.manifest.name,
        version=plugin.manifest.version,
        type=plugin.manifest.type,
        category=plugin.manifest.category,
        description=description,
        author=plugin.manifest.author,
        status=plugin.status,
        enabled=plugin.enabled,
        installed_at=plugin.installed_at,
        loaded_at=plugin.loaded_at,
        error=plugin.error,
    )


@router.get(
    "/",
    response_model=List[PluginInfo],
    summary="List all plugins",
    description="Get a list of all installed plugins with their current status.",
)
async def list_plugins(
    type: Optional[PluginType] = Query(None, description="Filter by plugin type"),
    category: Optional[PluginCategory] = Query(None, description="Filter by category"),
    enabled: Optional[bool] = Query(None, description="Filter by enabled status"),
    manager: PluginManager = Depends(get_plugin_manager),
) -> List[PluginInfo]:
    """List all installed plugins."""
    plugins = manager.list_plugins(type=type, category=category, enabled=enabled)
    return [plugin_to_info(p) for p in plugins]


@router.get(
    "/{plugin_id}",
    response_model=PluginInfo,
    summary="Get plugin details",
    description="Get detailed information about a specific plugin.",
)
async def get_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager),
) -> PluginInfo:
    """Get plugin details by ID."""
    plugin = manager.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin '{plugin_id}' not found",
        )
    return plugin_to_info(plugin)


@router.post(
    "/{plugin_id}/load",
    response_model=PluginLoadResponse,
    summary="Load plugin",
    description="Load a plugin into memory and initialize it.",
)
async def load_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager),
) -> PluginLoadResponse:
    """Load a plugin."""
    try:
        plugin = await manager.load_plugin(plugin_id)
        return PluginLoadResponse(
            plugin_id=plugin.id,
            status=plugin.status,
            message=f"Plugin {plugin.id} loaded successfully",
        )
    except PluginNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )
    except PluginAlreadyLoadedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.message),
        )
    except PluginLoadError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.message),
        )


@router.post(
    "/{plugin_id}/unload",
    response_model=PluginLoadResponse,
    summary="Unload plugin",
    description="Unload a plugin from memory.",
)
async def unload_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager),
) -> PluginLoadResponse:
    """Unload a plugin."""
    try:
        await manager.unload_plugin(plugin_id)
        plugin = manager.get_plugin(plugin_id)
        return PluginLoadResponse(
            plugin_id=plugin_id,
            status=plugin.status if plugin else PluginStatus.INSTALLED,
            message=f"Plugin {plugin_id} unloaded successfully",
        )
    except PluginNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )


@router.post(
    "/{plugin_id}/reload",
    response_model=PluginLoadResponse,
    summary="Reload plugin",
    description="Reload a plugin (unload and load again).",
)
async def reload_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager),
) -> PluginLoadResponse:
    """Reload a plugin."""
    try:
        plugin = await manager.reload_plugin(plugin_id)
        return PluginLoadResponse(
            plugin_id=plugin.id,
            status=plugin.status,
            message=f"Plugin {plugin.id} reloaded successfully",
        )
    except PluginNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )
    except PluginLoadError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.message),
        )
