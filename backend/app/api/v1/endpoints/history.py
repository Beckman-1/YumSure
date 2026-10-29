from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_profile import UserProfile
from app.models.scan_history import ScanHistory
from app.schemas.scan_history import ScanHistoryItem, FavoriteToggleRequest

router = APIRouter()

@router.get("", response_model=List[ScanHistoryItem], summary="Get authenticated user's scan history")
async def get_my_history(
    only_favorites: bool = Query(False),
    limit: int = Query(30, ge=1, le=100),
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves scan history strictly scoped to the authenticated user."""
    query = select(ScanHistory).where(ScanHistory.user_id == current_user.id)
    if only_favorites:
        query = query.where(ScanHistory.is_favorite == True)
    query = query.order_by(desc(ScanHistory.scanned_at)).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

@router.patch("/{history_id}/favorite", response_model=ScanHistoryItem, summary="Toggle favorite on own scan item")
async def toggle_favorite(
    history_id: int,
    req: FavoriteToggleRequest,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Allows toggling favorite strictly on scan records owned by the authenticated user."""
    result = await db.execute(
        select(ScanHistory).where(
            ScanHistory.id == history_id,
            ScanHistory.user_id == current_user.id
        )
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Scan history item not found or unauthorized."
        )
    
    item.is_favorite = req.is_favorite
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete own history item")
async def delete_history_item(
    history_id: int,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Deletes a history item strictly owned by the authenticated user."""
    result = await db.execute(
        select(ScanHistory).where(
            ScanHistory.id == history_id,
            ScanHistory.user_id == current_user.id
        )
    )
    item = result.scalars().first()
    if item:
        await db.delete(item)
        await db.commit()
    return None
