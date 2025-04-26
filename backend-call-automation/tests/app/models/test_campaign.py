import pytest
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.models.campaign import (
    CampaignBase,
    CampaignCreate,
    CampaignUpdate, 
    Campaign,
    CampaignStatus
)

@pytest.fixture
def sample_campaign_data() -> dict:
    campaign_id = uuid4()
    contact_id = uuid4()
    return {
        "name": "Campaña de Ventas Q1",
        "description": "Campaña de ventas para el primer trimestre",
        "status": CampaignStatus.ACTIVE,
        "schedule_start": datetime(2025, 1, 25),
        "schedule_end": datetime(2025, 2, 25),
        "contact_list_ids": [contact_id],
        "script_template": "Hola {nombre}, le llamamos de...",
        "max_retries": 3,
        "retry_delay_minutes": 60,
        "calling_hours_start": "09:00",
        "calling_hours_end": "18:00",
        "id": campaign_id,
        "total_calls": 100,
        "successful_calls": 75,
        "failed_calls": 15,
        "pending_calls": 10,
        "created_at": datetime(2025, 1, 24, 20, 52, 51),
        "updated_at": datetime(2025, 1, 24, 20, 52, 51)
    }

def test_campaign_base(sample_campaign_data):
    data = {k:v for k,v in sample_campaign_data.items() 
            if k not in ["id", "total_calls", "successful_calls", 
                        "failed_calls", "pending_calls", "created_at", 
                        "updated_at"]}
    
    campaign = CampaignBase(**data)
    assert campaign.name == "Campaña de Ventas Q1"
    assert campaign.status == CampaignStatus.ACTIVE
    assert campaign.schedule_start == datetime(2025, 1, 25)
    assert isinstance(campaign.contact_list_ids[0], UUID)
    assert campaign.calling_hours_start == "09:00"
    assert campaign.calling_hours_end == "18:00"

def test_campaign_create(sample_campaign_data):
    data = {k:v for k,v in sample_campaign_data.items() 
            if k not in ["id", "total_calls", "successful_calls", 
                        "failed_calls", "pending_calls", "created_at", 
                        "updated_at"]}
    
    campaign = CampaignCreate(**data)
    assert campaign.name == "Campaña de Ventas Q1"
    assert campaign.status == CampaignStatus.ACTIVE
    assert isinstance(campaign.contact_list_ids[0], UUID)

def test_campaign_update(sample_campaign_data):
    data = {
        "name": "Campaña Actualizada",
        "status": CampaignStatus.PAUSED,
        "max_retries": 2
    }
    campaign = CampaignUpdate(**data)
    assert campaign.name == "Campaña Actualizada"
    assert campaign.status == CampaignStatus.PAUSED
    assert campaign.max_retries == 2

def test_campaign(sample_campaign_data):
    campaign = Campaign(**sample_campaign_data)
    assert campaign.name == "Campaña de Ventas Q1"
    assert campaign.status == CampaignStatus.ACTIVE
    assert isinstance(campaign.id, UUID)
    assert campaign.total_calls == 100
    assert campaign.successful_calls == 75
    assert campaign.failed_calls == 15
    assert campaign.pending_calls == 10

def test_invalid_campaign_status():
    with pytest.raises(ValidationError):
        CampaignBase(
            name="Test",
            status="invalid_status",
            schedule_start=datetime(2025, 1, 25),
            schedule_end=datetime(2025, 2, 25),
            contact_list_ids=[uuid4()],
            script_template="Test script",
            max_retries=3,
            retry_delay_minutes=60,
            calling_hours_start="09:00",
            calling_hours_end="18:00",
        )

def test_invalid_dates():
    with pytest.raises(ValidationError):
        CampaignBase(
            name="Test",
            status=CampaignStatus.DRAFT,
            schedule_start=datetime(2025, 2, 25),
            schedule_end=datetime(2025, 1, 25),  # End before start
            contact_list_ids=[uuid4()],
            script_template="Test script",
            max_retries=3,
            retry_delay_minutes=60,
            calling_hours_start="09:00",
            calling_hours_end="18:00",
        )

def test_invalid_calling_hours():
    with pytest.raises(ValidationError):
        CampaignBase(
            name="Test",
            status=CampaignStatus.DRAFT,
            schedule_start=datetime(2025, 1, 25),
            schedule_end=datetime(2025, 2, 25),
            contact_list_ids=[uuid4()],
            script_template="Test script",
            max_retries=3,
            retry_delay_minutes=60,
            calling_hours_start="18:00",  # Start after end
            calling_hours_end="09:00",
        )
