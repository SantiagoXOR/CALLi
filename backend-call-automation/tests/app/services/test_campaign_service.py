import logging
from datetime import datetime

import pytest
from fastapi import HTTPException

from app.models.campaign import CampaignCreate, CampaignStats, CampaignUpdate
from app.services.campaign_service import CampaignService

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_create_campaign(campaign_service: CampaignService, mock_campaign_data):
    campaign = await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    assert campaign.name == mock_campaign_data["name"]
    assert campaign.status == mock_campaign_data["status"]
    assert campaign.schedule_start == datetime.fromisoformat(mock_campaign_data["schedule_start"])
    assert campaign.schedule_end == datetime.fromisoformat(mock_campaign_data["schedule_end"])
    assert campaign.contact_list_ids == mock_campaign_data["contact_list_ids"]
    assert campaign.script_template == mock_campaign_data["script_template"]
    assert campaign.max_retries == mock_campaign_data["max_retries"]
    assert campaign.retry_delay_minutes == mock_campaign_data["retry_delay_minutes"]
    assert campaign.pending_calls == mock_campaign_data["pending_calls"]
    assert campaign.total_calls == mock_campaign_data["total_calls"]
    assert campaign.successful_calls == mock_campaign_data["successful_calls"]
    assert campaign.failed_calls == mock_campaign_data["failed_calls"]


@pytest.mark.asyncio
async def test_get_campaign(campaign_service: CampaignService, mock_campaign_data):
    campaign = await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    retrieved_campaign = await campaign_service.get_campaign(campaign.id)
    assert retrieved_campaign.id == campaign.id
    assert retrieved_campaign.name == campaign.name


@pytest.mark.asyncio
async def test_get_nonexistent_campaign(campaign_service: CampaignService):
    with pytest.raises(HTTPException) as exc:
        await campaign_service.get_campaign(999)
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_list_campaigns_with_pagination(
    campaign_service: CampaignService, mock_campaign_data
):
    for i in range(15):
        await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    campaigns = await campaign_service.list_campaigns(page=1, page_size=10)
    assert len(campaigns) == 10


@pytest.mark.asyncio
async def test_list_campaigns_with_filters(campaign_service: CampaignService, mock_campaign_data):
    mock_campaign_data["status"] = "active"
    await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    mock_campaign_data["status"] = "paused"
    await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    campaigns = await campaign_service.list_campaigns(status="active")
    assert all(campaign.status == "active" for campaign in campaigns)


@pytest.mark.asyncio
async def test_update_campaign(campaign_service: CampaignService, mock_campaign_data):
    campaign = await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    update_data = CampaignUpdate(name="Updated Campaign", status="paused")
    updated_campaign = await campaign_service.update_campaign(campaign.id, update_data)
    assert updated_campaign.name == "Updated Campaign"
    assert updated_campaign.status == "paused"


@pytest.mark.asyncio
async def test_delete_campaign(campaign_service: CampaignService, mock_campaign_data):
    campaign = await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    result = await campaign_service.delete_campaign(campaign.id)
    assert result is True
    with pytest.raises(HTTPException) as exc:
        await campaign_service.get_campaign(campaign.id)
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_update_campaign_stats(campaign_service: CampaignService, mock_campaign_data):
    campaign = await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))
    stats = CampaignStats(total_calls=100, successful_calls=80, failed_calls=20, pending_calls=0)
    updated_campaign = await campaign_service.update_campaign_stats(campaign.id, stats)
    assert updated_campaign.total_calls == 100
    assert updated_campaign.successful_calls == 80
    assert updated_campaign.failed_calls == 20
    assert updated_campaign.pending_calls == 0


@pytest.mark.asyncio
async def test_invalid_campaign_stats(campaign_service: CampaignService, mock_campaign_data):
    logger.info("Iniciando test de validación de estadísticas inválidas")
    campaign = await campaign_service.create_campaign(CampaignCreate(**mock_campaign_data))

    # Caso 1: Suma de llamadas exitosas y fallidas mayor que el total
    with pytest.raises(HTTPException) as exc:
        stats = CampaignStats(
            total_calls=50,
            successful_calls=40,
            failed_calls=20,  # 40 + 20 > 50
            pending_calls=0,
        )
        await campaign_service.update_campaign_stats(campaign.id, stats)
    assert exc.value.status_code == 422
    assert "Estadísticas inválidas" in str(exc.value.detail)

    # Caso 2: Valores negativos - Este caso es manejado por Pydantic
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc:
        CampaignStats(
            total_calls=50,
            successful_calls=-1,  # Valor negativo - Pydantic lo detectará
            failed_calls=20,
            pending_calls=0,
        )
    error_detail = str(exc.value)
    assert "greater_than_equal" in error_detail
    assert "successful_calls" in error_detail

    logger.info("Test de validación de estadísticas inválidas completado exitosamente")
