import pytest
from unittest.mock import AsyncMock, patch
from app.services.campaign_scheduler import CampaignScheduler
from app.models.campaign import Campaign, CampaignStatus
from app.models.call import Call, CallStatus, CallCreate
from app.services.campaign_service import CampaignService
from app.services.call_service import CallService
from app.services.contact_service import ContactService
from app.models.contact import Contact, ContactCreate, ContactUpdate
from datetime import datetime, timedelta

@pytest.fixture
def mock_campaign_service():
    return AsyncMock(spec=CampaignService)

@pytest.fixture
def mock_call_service():
    return AsyncMock(spec=CallService)

@pytest.fixture
def mock_contact_service():
    return AsyncMock(spec=ContactService)

@pytest.fixture
def campaign_scheduler(mock_campaign_service, mock_call_service, mock_contact_service):
    return CampaignScheduler(
        campaign_service=mock_campaign_service,
        call_service=mock_call_service,
        contact_service=mock_contact_service,
        check_interval=1
    )

@pytest.mark.asyncio
async def test_start_stop(campaign_scheduler):
    await campaign_scheduler.start()
    assert campaign_scheduler.is_running
    await campaign_scheduler.stop()
    assert not campaign_scheduler.is_running

@pytest.mark.asyncio
async def test_process_active_campaigns(campaign_scheduler, mock_campaign_service, mock_contact_service):
    now = datetime.now()
    campaign = Campaign(
        id=1,
        name="Test Campaign",
        description="Test Description",
        status=CampaignStatus.ACTIVE,
        schedule_start=now - timedelta(hours=1),
        schedule_end=now + timedelta(hours=1),
        contact_list_ids=[1, 2, 3],
        script_template="Test script",
        max_retries=3,
        retry_delay_minutes=15,
        pending_calls=3
    )
    mock_campaign_service.list_campaigns.return_value = [campaign]
    mock_contact_service.get_campaign_contacts.return_value = []

    await campaign_scheduler._process_active_campaigns()

    mock_campaign_service.list_campaigns.assert_called_once_with(
        status=CampaignStatus.ACTIVE,
        start_date=now,
        end_date=now
    )
    mock_contact_service.get_campaign_contacts.assert_called_once_with(campaign.id)

@pytest.mark.asyncio
async def test_retry_failed_calls(campaign_scheduler, mock_call_service, mock_campaign_service):
    now = datetime.now()
    call = Call(
        id=1,
        campaign_id=1,
        phone_number="+1234567890",
        from_number="+0987654321",
        webhook_url="http://example.com/webhook",
        status_callback_url="http://example.com/callback",
        status=CallStatus.FAILED,
        retry_attempts=0,
        max_retries=3,
        created_at=now - timedelta(hours=1),
        updated_at=now - timedelta(hours=1)
    )
    campaign = Campaign(
        id=1,
        name="Test Campaign",
        description="Test Description",
        status=CampaignStatus.ACTIVE,
        schedule_start=now - timedelta(hours=1),
        schedule_end=now + timedelta(hours=1),
        contact_list_ids=[1, 2, 3],
        script_template="Test script",
        max_retries=3,
        retry_delay_minutes=15,
        pending_calls=3
    )
    mock_call_service.list_calls.return_value = [call]
    mock_call_service.is_retry_allowed.return_value = True
    mock_campaign_service.get_campaign.return_value = campaign

    await campaign_scheduler._retry_failed_calls()

    mock_call_service.list_calls.assert_called_once_with(status=CallStatus.FAILED)
    mock_call_service.is_retry_allowed.assert_called_once_with(call)
    mock_campaign_service.get_campaign.assert_called_once_with(call.campaign_id)
    mock_call_service.retry_call.assert_called_once_with(call.id)

@pytest.mark.asyncio
async def test_update_campaign_stats(campaign_scheduler, mock_call_service, mock_campaign_service):
    campaign_id = 1
    metrics = {
        "total_calls": 10,
        "completed_calls": 8,
        "failed_calls": 2,
        "pending_calls": 0
    }
    mock_call_service.get_call_metrics.return_value = metrics

    await campaign_scheduler.update_campaign_stats(campaign_id)

    mock_call_service.get_call_metrics.assert_called_once_with(campaign_id)
    mock_campaign_service.update_campaign_stats.assert_called_once_with(
        campaign_id,
        {
            "total_calls": 10,
            "successful_calls": 8,
            "failed_calls": 2,
            "pending_calls": 0
        }
    )
