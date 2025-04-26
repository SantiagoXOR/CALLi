from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate
from app.crud.campaign import (
    create_campaign,
    get_campaign,
    get_campaigns,
    update_campaign,
    delete_campaign,
    add_client_to_campaign
)

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])

@router.post("/", response_model=Campaign)
async def create_campaign_endpoint(
    campaign: CampaignCreate,
    db: AsyncSession = Depends(get_session)
) -> Campaign:
    return await create_campaign(db, campaign)

@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign_endpoint(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_session)
) -> Campaign:
    campaign = await get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.get("/", response_model=List[Campaign])
async def list_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_session)
) -> List[Campaign]:
    return await get_campaigns(db, skip=skip, limit=limit)

@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign_endpoint(
    campaign_id: UUID,
    campaign_update: CampaignUpdate,
    db: AsyncSession = Depends(get_session)
) -> Campaign:
    campaign = await update_campaign(db, campaign_id, campaign_update)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.delete("/{campaign_id}")
async def delete_campaign_endpoint(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_session)
):
    deleted = await delete_campaign(db, campaign_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}

@router.post("/{campaign_id}/clients/{client_id}")
async def add_client_to_campaign_endpoint(
    campaign_id: UUID,
    client_id: UUID,
    db: AsyncSession = Depends(get_session)
):
    try:
        await add_client_to_campaign(db, campaign_id, client_id)
        return {"message": "Client added to campaign successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
