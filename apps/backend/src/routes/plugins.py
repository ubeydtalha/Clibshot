"""
Plugin API Routes - CRUD operations for plugin management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..models import Plugin, PluginConfiguration
from ..schemas import (
    PluginCreate, PluginUpdate, PluginResponse,
    PluginConfigCreate, PluginConfigUpdate, PluginConfigResponse,
    MessageResponse
)
from ..plugin_manager import get_plugin_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/plugins", tags=["plugins"])


# ============ Plugin CRUD Operations ============

@router.get("/", response_model=List[PluginResponse])
async def list_plugins(
    skip: int = 0,
    limit: int = 100,
    enabled_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    List all plugins
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **enabled_only**: Filter to only enabled plugins
    """
    logger.info(f"Listing plugins: skip={skip}, limit={limit}, enabled_only={enabled_only}")
    
    query = db.query(Plugin)
    
    if enabled_only:
        query = query.filter(Plugin.enabled == True)
    
    plugins = query.offset(skip).limit(limit).all()
    logger.debug(f"Found {len(plugins)} plugins")
    
    return plugins


@router.get("/{plugin_id}", response_model=PluginResponse)
async def get_plugin(plugin_id: int, db: Session = Depends(get_db)):
    """Get a specific plugin by ID"""
    logger.info(f"Getting plugin: {plugin_id}")
    
    plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    
    if not plugin:
        logger.warning(f"Plugin not found: {plugin_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin with id {plugin_id} not found"
        )
    
    return plugin


@router.post("/", response_model=PluginResponse, status_code=status.HTTP_201_CREATED)
async def create_plugin(plugin: PluginCreate, db: Session = Depends(get_db)):
    """
    Create a new plugin
    
    - **name**: Unique plugin name
    - **display_name**: Display name for the plugin
    - **version**: Plugin version
    - **entry_point**: Path to plugin entry point
    - **plugin_type**: Type of plugin (python, rust, cpp, etc.)
    """
    logger.info(f"Creating plugin: {plugin.name}")
    
    # Check if plugin with same name already exists
    existing = db.query(Plugin).filter(Plugin.name == plugin.name).first()
    if existing:
        logger.warning(f"Plugin already exists: {plugin.name}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Plugin with name '{plugin.name}' already exists"
        )
    
    # Create plugin record
    db_plugin = Plugin(**plugin.model_dump())
    db.add(db_plugin)
    db.commit()
    db.refresh(db_plugin)
    
    logger.info(f"Plugin created successfully: {plugin.name} (ID: {db_plugin.id})")
    
    # Try to load the plugin if enabled
    if db_plugin.enabled:
        try:
            pm = get_plugin_manager()
            config = db_plugin.plugin_metadata.get("config", {}) if db_plugin.plugin_metadata else {}
            pm.load_plugin(db_plugin.name, config)
            logger.info(f"Plugin loaded into manager: {plugin.name}")
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin.name}: {str(e)}", exc_info=True)
    
    return db_plugin


@router.put("/{plugin_id}", response_model=PluginResponse)
@router.patch("/{plugin_id}", response_model=PluginResponse)
async def update_plugin(
    plugin_id: int,
    plugin_update: PluginUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing plugin"""
    logger.info(f"Updating plugin: {plugin_id}")
    
    db_plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    
    if not db_plugin:
        logger.warning(f"Plugin not found: {plugin_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin with id {plugin_id} not found"
        )
    
    # Update only provided fields
    update_data = plugin_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plugin, field, value)
    
    db.commit()
    db.refresh(db_plugin)
    
    logger.info(f"Plugin updated successfully: {db_plugin.name}")
    
    # Reload plugin if it's enabled
    if db_plugin.enabled:
        try:
            pm = get_plugin_manager()
            config = db_plugin.plugin_metadata.get("config", {}) if db_plugin.plugin_metadata else {}
            pm.reload_plugin(db_plugin.name, config)
            logger.info(f"Plugin reloaded: {db_plugin.name}")
        except Exception as e:
            logger.error(f"Failed to reload plugin {db_plugin.name}: {str(e)}", exc_info=True)
    
    return db_plugin


@router.delete("/{plugin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plugin(plugin_id: int, db: Session = Depends(get_db)):
    """Delete a plugin"""
    logger.info(f"Deleting plugin: {plugin_id}")
    
    db_plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    
    if not db_plugin:
        logger.warning(f"Plugin not found: {plugin_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin with id {plugin_id} not found"
        )
    
    plugin_name = db_plugin.name
    
    # Unload plugin from manager
    try:
        pm = get_plugin_manager()
        pm.unload_plugin(plugin_name)
        logger.info(f"Plugin unloaded: {plugin_name}")
    except Exception as e:
        logger.error(f"Failed to unload plugin {plugin_name}: {str(e)}", exc_info=True)
    
    db.delete(db_plugin)
    db.commit()
    
    logger.info(f"Plugin deleted successfully: {plugin_name}")


# ============ Plugin Control Operations ============

@router.post("/{plugin_id}/enable", response_model=PluginResponse)
async def enable_plugin(plugin_id: int, db: Session = Depends(get_db)):
    """Enable a plugin and load it into the plugin manager"""
    logger.info(f"Enabling plugin: {plugin_id}")
    
    db_plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    
    if not db_plugin:
        logger.warning(f"Plugin not found: {plugin_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin with id {plugin_id} not found"
        )
    
    if db_plugin.enabled:
        logger.info(f"Plugin already enabled: {db_plugin.name}")
        return db_plugin
    
    # Enable plugin
    db_plugin.enabled = True
    db.commit()
    db.refresh(db_plugin)
    
    # Load plugin into manager
    try:
        pm = get_plugin_manager()
        config = db_plugin.plugin_metadata.get("config", {}) if db_plugin.plugin_metadata else {}
        success = pm.load_plugin(db_plugin.name, config)
        
        if not success:
            error = pm.get_plugin_error(db_plugin.name)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to load plugin: {error}"
            )
        
        logger.info(f"Plugin enabled and loaded: {db_plugin.name}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to enable plugin {db_plugin.name}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enable plugin: {str(e)}"
        )
    
    return db_plugin


@router.post("/{plugin_id}/disable", response_model=PluginResponse)
async def disable_plugin(plugin_id: int, db: Session = Depends(get_db)):
    """Disable a plugin and unload it from the plugin manager"""
    logger.info(f"Disabling plugin: {plugin_id}")
    
    db_plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    
    if not db_plugin:
        logger.warning(f"Plugin not found: {plugin_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin with id {plugin_id} not found"
        )
    
    if not db_plugin.enabled:
        logger.info(f"Plugin already disabled: {db_plugin.name}")
        return db_plugin
    
    # Disable plugin
    db_plugin.enabled = False
    db.commit()
    db.refresh(db_plugin)
    
    # Unload plugin from manager
    try:
        pm = get_plugin_manager()
        pm.unload_plugin(db_plugin.name)
        logger.info(f"Plugin disabled and unloaded: {db_plugin.name}")
    
    except Exception as e:
        logger.error(f"Failed to disable plugin {db_plugin.name}: {str(e)}", exc_info=True)
        # Continue even if unload fails, plugin is already marked as disabled
    
    return db_plugin


# ============ Plugin Configuration Operations ============

@router.get("/{plugin_id}/config", response_model=List[PluginConfigResponse])
async def get_plugin_configurations(plugin_id: int, db: Session = Depends(get_db)):
    """Get all configurations for a plugin"""
    logger.info(f"Getting configurations for plugin: {plugin_id}")
    
    # Verify plugin exists
    plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    if not plugin:
        logger.warning(f"Plugin not found: {plugin_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin with id {plugin_id} not found"
        )
    
    configs = db.query(PluginConfiguration).filter(
        PluginConfiguration.plugin_id == plugin_id
    ).all()
    
    logger.debug(f"Found {len(configs)} configurations for plugin {plugin_id}")
    
    return configs


@router.post("/{plugin_id}/config", response_model=PluginConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_plugin_configuration(
    plugin_id: int,
    config: PluginConfigCreate,
    db: Session = Depends(get_db)
):
    """Create a new configuration for a plugin"""
    logger.info(f"Creating configuration for plugin: {plugin_id}")
    
    # Verify plugin exists
    plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    if not plugin:
        logger.warning(f"Plugin not found: {plugin_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin with id {plugin_id} not found"
        )
    
    # Check if config with same key already exists
    existing = db.query(PluginConfiguration).filter(
        PluginConfiguration.plugin_id == plugin_id,
        PluginConfiguration.key == config.key
    ).first()
    
    if existing:
        logger.warning(f"Configuration key already exists: {config.key}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Configuration with key '{config.key}' already exists for this plugin"
        )
    
    # Create config with plugin_id from URL
    db_config = PluginConfiguration(**config.model_dump(), plugin_id=plugin_id)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    logger.info(f"Configuration created: {config.key} for plugin {plugin_id}")
    
    return db_config


@router.put("/{plugin_id}/config/{config_id}", response_model=PluginConfigResponse)
@router.patch("/{plugin_id}/config/{config_id}", response_model=PluginConfigResponse)
async def update_plugin_configuration(
    plugin_id: int,
    config_id: int,
    config_update: PluginConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update a plugin configuration"""
    logger.info(f"Updating configuration {config_id} for plugin {plugin_id}")
    
    db_config = db.query(PluginConfiguration).filter(
        PluginConfiguration.id == config_id,
        PluginConfiguration.plugin_id == plugin_id
    ).first()
    
    if not db_config:
        logger.warning(f"Configuration not found: {config_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuration with id {config_id} not found for plugin {plugin_id}"
        )
    
    update_data = config_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_config, field, value)
    
    db.commit()
    db.refresh(db_config)
    
    logger.info(f"Configuration updated: {db_config.key}")
    
    return db_config


@router.delete("/{plugin_id}/config/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plugin_configuration(
    plugin_id: int,
    config_id: int,
    db: Session = Depends(get_db)
):
    """Delete a plugin configuration"""
    logger.info(f"Deleting configuration {config_id} for plugin {plugin_id}")
    
    db_config = db.query(PluginConfiguration).filter(
        PluginConfiguration.id == config_id,
        PluginConfiguration.plugin_id == plugin_id
    ).first()
    
    if not db_config:
        logger.warning(f"Configuration not found: {config_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuration with id {config_id} not found for plugin {plugin_id}"
        )
    
    config_key = db_config.key
    
    db.delete(db_config)
    db.commit()
    
    logger.info(f"Configuration deleted: {config_key}")
