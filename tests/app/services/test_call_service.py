from unittest.mock import ANY, AsyncMock, MagicMock

import pytest

from app.services.call_service import CallService


@pytest.fixture
def mock_supabase():
    return AsyncMock()


@pytest.fixture
def mock_elevenlabs_service():
    return MagicMock()


@pytest.fixture
def mock_ai_service():
    return MagicMock()


@pytest.mark.asyncio
async def test_handle_call_end(mock_supabase, mock_elevenlabs_service, mock_ai_service):
    # Arrange
    call_service = CallService(
        supabase_client=mock_supabase,
        elevenlabs_service=mock_elevenlabs_service,
        ai_service=mock_ai_service,
    )
    call_id = "test_call_id"

    # Act
    await call_service.handle_call_end(call_id)

    # Assert
    mock_elevenlabs_service.close_conversation.assert_called_once()
    # mock_ai_service.end_conversation.assert_called_once_with(conversation_id=call_id)
    mock_supabase.table.assert_called_once_with("calls")
    mock_supabase.table().update.assert_called_once_with({"status": "completed", "end_time": ANY})
    mock_supabase.table().update().eq.assert_called_once_with("id", call_id)
    mock_supabase.table().update().eq().execute.assert_called_once()
