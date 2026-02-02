"""
Plugin Marketplace Routes

FastAPI routes for plugin marketplace functionality.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from src.marketplace import (
    PluginMarketplace,
    PluginListing,
    PluginSearchQuery,
    PluginInstallRequest,
    MarketplaceConfig
)

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

# Initialize marketplace with default config
marketplace = PluginMarketplace(MarketplaceConfig())


@router.get("/plugins", response_model=List[PluginListing])
async def search_plugins(
    q: Optional[str] = Query(None, description="Search query"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    author: Optional[str] = Query(None, description="Filter by author"),
    min_rating: Optional[float] = Query(None, description="Minimum rating"),
    sort_by: str = Query("downloads", description="Sort field"),
    limit: int = Query(20, le=100, description="Results limit"),
    offset: int = Query(0, description="Results offset")
):
    """
    Search for plugins in the marketplace.
    
    - **q**: Text search query
    - **tags**: Filter by tags (comma-separated)
    - **author**: Filter by author name
    - **min_rating**: Minimum rating threshold
    - **sort_by**: Sort field (downloads, rating, created_at, updated_at)
    - **limit**: Maximum results (max 100)
    - **offset**: Pagination offset
    """
    query = PluginSearchQuery(
        query=q,
        tags=tags.split(",") if tags else None,
        author=author,
        min_rating=min_rating,
        sort_by=sort_by,
        limit=limit,
        offset=offset
    )
    
    try:
        return await marketplace.search_plugins(query)
    except NotImplementedError:
        # Return mock data for now
        return [
            PluginListing(
                plugin_id="ai-clip-analyzer",
                name="AI Clip Analyzer",
                version="1.0.0",
                author="ClipShot Team",
                description="Analyze gaming clips using AI to detect highlights",
                repository_url="https://github.com/clipshot/plugin-ai-analyzer",
                download_url="https://github.com/clipshot/plugin-ai-analyzer/releases/latest/download/plugin.zip",
                tags=["ai", "analysis", "highlights"],
                downloads=1234,
                rating=4.5,
                created_at="2026-01-01T00:00:00Z",
                updated_at="2026-02-01T00:00:00Z"
            )
        ]


@router.get("/plugins/{plugin_id}", response_model=PluginListing)
async def get_plugin(plugin_id: str):
    """
    Get details for a specific plugin.
    
    - **plugin_id**: Unique plugin identifier
    """
    plugin = await marketplace.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return plugin


@router.post("/plugins/install")
async def install_plugin(request: PluginInstallRequest):
    """
    Install a plugin from the marketplace.
    
    - **plugin_id**: Plugin to install
    - **version**: Specific version (optional, defaults to latest)
    """
    try:
        success = await marketplace.install_plugin(request)
        if not success:
            raise HTTPException(status_code=500, detail="Installation failed")
        return {"status": "installed", "plugin_id": request.plugin_id}
    except NotImplementedError:
        return {
            "status": "pending",
            "message": "Installation feature coming soon",
            "plugin_id": request.plugin_id
        }


@router.post("/plugins/{plugin_id}/update")
async def update_plugin(plugin_id: str):
    """
    Update an installed plugin to the latest version.
    
    - **plugin_id**: Plugin to update
    """
    try:
        success = await marketplace.update_plugin(plugin_id)
        if not success:
            raise HTTPException(status_code=500, detail="Update failed")
        return {"status": "updated", "plugin_id": plugin_id}
    except NotImplementedError:
        return {
            "status": "pending",
            "message": "Update feature coming soon",
            "plugin_id": plugin_id
        }


@router.delete("/plugins/{plugin_id}/uninstall")
async def uninstall_plugin(plugin_id: str):
    """
    Uninstall a plugin.
    
    - **plugin_id**: Plugin to uninstall
    """
    try:
        success = await marketplace.uninstall_plugin(plugin_id)
        if not success:
            raise HTTPException(status_code=500, detail="Uninstallation failed")
        return {"status": "uninstalled", "plugin_id": plugin_id}
    except NotImplementedError:
        return {
            "status": "pending",
            "message": "Uninstall feature coming soon",
            "plugin_id": plugin_id
        }


@router.get("/updates")
async def check_updates():
    """
    Check for updates to installed plugins.
    
    Returns list of plugins with available updates.
    """
    try:
        updates = await marketplace.check_updates()
        return {"updates": updates}
    except NotImplementedError:
        return {
            "updates": [],
            "message": "Update check feature coming soon"
        }
