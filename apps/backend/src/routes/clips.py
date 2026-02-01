"""
Clip API Routes - CRUD operations for clip management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..database import get_db
from ..models import Clip
from ..schemas import ClipCreate, ClipUpdate, ClipResponse, MessageResponse
from ..plugin_manager import get_plugin_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clips", tags=["clips"])


@router.get("/", response_model=List[ClipResponse])
async def list_clips(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    game_name: Optional[str] = Query(None, description="Filter by game name"),
    processed: Optional[bool] = Query(None, description="Filter by processed status"),
    db: Session = Depends(get_db)
):
    """
    List all clips with optional filtering
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (1-1000)
    - **game_name**: Filter by game name
    - **processed**: Filter by processed status
    """
    logger.info(f"Listing clips: skip={skip}, limit={limit}, game_name={game_name}, processed={processed}")
    
    query = db.query(Clip)
    
    if game_name:
        query = query.filter(Clip.game_name == game_name)
    
    if processed is not None:
        query = query.filter(Clip.processed == processed)
    
    # Order by created_at descending (newest first)
    clips = query.order_by(Clip.created_at.desc()).offset(skip).limit(limit).all()
    
    logger.debug(f"Found {len(clips)} clips")
    
    return clips


@router.get("/stats")
async def get_clip_stats(db: Session = Depends(get_db)):
    """Get clip statistics"""
    logger.info("Getting clip statistics")
    
    total_clips = db.query(Clip).count()
    processed_clips = db.query(Clip).filter(Clip.processed == True).count()
    unprocessed_clips = total_clips - processed_clips
    
    # Get clips by game
    games_query = db.query(Clip.game_name).distinct().all()
    games = [g[0] for g in games_query if g[0]]
    
    stats = {
        "total_clips": total_clips,
        "processed_clips": processed_clips,
        "unprocessed_clips": unprocessed_clips,
        "total_games": len(games),
        "games": games
    }
    
    logger.debug(f"Clip stats: {stats}")
    
    return stats


@router.get("/{clip_id}", response_model=ClipResponse)
async def get_clip(clip_id: int, db: Session = Depends(get_db)):
    """Get a specific clip by ID"""
    logger.info(f"Getting clip: {clip_id}")
    
    clip = db.query(Clip).filter(Clip.id == clip_id).first()
    
    if not clip:
        logger.warning(f"Clip not found: {clip_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with id {clip_id} not found"
        )
    
    return clip


@router.post("/", response_model=ClipResponse, status_code=status.HTTP_201_CREATED)
async def create_clip(clip: ClipCreate, db: Session = Depends(get_db)):
    """
    Create a new clip
    
    - **title**: Clip title
    - **file_path**: Path to the clip file
    - **description**: Optional description
    - **game_name**: Optional game name
    - **tags**: Optional list of tags
    """
    logger.info(f"Creating clip: {clip.title}")
    
    # Create clip record
    db_clip = Clip(**clip.model_dump())
    db.add(db_clip)
    db.commit()
    db.refresh(db_clip)
    
    logger.info(f"Clip created successfully: {clip.title} (ID: {db_clip.id})")
    
    # Trigger plugin event: on_clip_captured
    try:
        pm = get_plugin_manager()
        clip_data = {
            "id": db_clip.id,
            "title": db_clip.title,
            "file_path": db_clip.file_path,
            "game_name": db_clip.game_name,
            "metadata": db_clip.clip_metadata or {}
        }
        
        result_data = pm.trigger_event("on_clip_captured", clip_data)
        
        # Update clip with plugin modifications
        if result_data.get("metadata") != clip_data.get("metadata"):
            db_clip.clip_metadata = result_data.get("metadata")
            db.commit()
            db.refresh(db_clip)
            logger.info(f"Clip metadata updated by plugins: {db_clip.id}")
    
    except Exception as e:
        logger.error(f"Failed to trigger plugin event for clip {db_clip.id}: {str(e)}", exc_info=True)
        # Continue even if plugin event fails
    
    return db_clip


@router.put("/{clip_id}", response_model=ClipResponse)
@router.patch("/{clip_id}", response_model=ClipResponse)
async def update_clip(
    clip_id: int,
    clip_update: ClipUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing clip"""
    logger.info(f"Updating clip: {clip_id}")
    
    db_clip = db.query(Clip).filter(Clip.id == clip_id).first()
    
    if not db_clip:
        logger.warning(f"Clip not found: {clip_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with id {clip_id} not found"
        )
    
    # Track if processed status changed
    was_processed = db_clip.processed
    
    # Update only provided fields
    update_data = clip_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_clip, field, value)
    
    db.commit()
    db.refresh(db_clip)
    
    logger.info(f"Clip updated successfully: {db_clip.title}")
    
    # Trigger plugin event if clip was just processed
    if not was_processed and db_clip.processed:
        try:
            pm = get_plugin_manager()
            clip_data = {
                "id": db_clip.id,
                "title": db_clip.title,
                "file_path": db_clip.file_path,
                "game_name": db_clip.game_name,
                "metadata": db_clip.clip_metadata or {}
            }
            
            result_data = pm.trigger_event("on_clip_processed", clip_data)
            
            # Update clip with plugin modifications
            if result_data.get("metadata") != clip_data.get("metadata"):
                db_clip.clip_metadata = result_data.get("metadata")
                db.commit()
                db.refresh(db_clip)
                logger.info(f"Clip metadata updated by plugins after processing: {db_clip.id}")
        
        except Exception as e:
            logger.error(f"Failed to trigger plugin event for processed clip {db_clip.id}: {str(e)}", exc_info=True)
    
    return db_clip


@router.delete("/{clip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clip(clip_id: int, db: Session = Depends(get_db)):
    """Delete a clip"""
    logger.info(f"Deleting clip: {clip_id}")
    
    db_clip = db.query(Clip).filter(Clip.id == clip_id).first()
    
    if not db_clip:
        logger.warning(f"Clip not found: {clip_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with id {clip_id} not found"
        )
    
    clip_title = db_clip.title
    
    db.delete(db_clip)
    db.commit()
    
    logger.info(f"Clip deleted successfully: {clip_title}")
