import asyncio
import json
import os
from unittest.mock import AsyncMock, MagicMock, call, patch

# Importamos prometheus_client directamente en lugar de Collector
import pytest

# Importamos directamente desde rollback_utils
from rollback_utils import (
    _apply_default_config,
    clear_redis_cache,
    close_all_elevenlabs_connections,
    reset_prometheus_metrics,
    restore_previous_config,
    take_config_snapshot,
)

@pytest.fixture(autouse=True)
def manage_snapshot_file(tmp_path):
    """Asegura que el directorio y archivo snapshot se manejen en tmp_path"""
    test_snapshot_dir = tmp_path / "snapshots"
    test_snapshot_file = test_snapshot_dir / "elevenlabs_config_snapshot.json"
    with (
        patch("rollback_utils.SNAPSHOT_DIR", test_snapshot_dir),
        patch("rollback_utils.SNAPSHOT_FILE", test_snapshot_file),
    ):
        yield test_snapshot_file


@pytest.fixture
def mock_redis_sync():
    """Mock para cliente Redis síncrono"""
    mock = MagicMock(spec=["scan_iter", "delete"])
    mock.scan_iter.return_value = iter([])
    mock.delete.return_value = 0
    mock.delete.__qualname__ = "MagicMock.delete"
    with patch("rollback_utils.redis_client", mock) as patched_mock:
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            asyncio,
            "iscoroutinefunction",
            lambda func: False if func == mock.delete else asyncio.iscoroutinefunction(func),
        )
        yield patched_mock
        monkeypatch.undo()


@pytest.fixture
def mock_redis_async():
    """Mock para cliente Redis asíncrono"""
    mock = AsyncMock(spec_set=["scan_iter", "delete"])

    async def mock_scan_iter_impl(*args, **kwargs):
        if False:
            yield

    mock.scan_iter.side_effect = mock_scan_iter_impl
    mock.delete.return_value = 0
    with patch("rollback_utils.redis_client", mock) as patched_mock:
        yield patched_mock


@pytest.fixture
def mock_connection_pool():
    """Mock para ConnectionPool"""
    mock_pool_instance = AsyncMock(
        spec_set=["close_all", "get_active_connections", "terminate_connection"]
    )
    del mock_pool_instance.close_all
    mock_pool_instance.get_active_connections.return_value = []
    mock_pool_instance.terminate_connection.return_value = None

    mock_pool_class = MagicMock()
    mock_pool_class.get_instance.return_value = mock_pool_instance
    with patch("rollback_utils.ConnectionPool", mock_pool_class):
        yield mock_pool_instance


@pytest.fixture
def mock_prometheus_registry():
    """Mock para prometheus_client.REGISTRY"""
    mock_registry = MagicMock(spec_set=["unregister", "_names_to_collectors"])
    mock_registry._names_to_collectors = {}
    with patch("rollback_utils.REGISTRY", mock_registry):
        yield mock_registry


@pytest.fixture
def mock_settings_object():
    """Mock para el objeto settings"""
    settings_obj = type("MockSettings", (), {})()
    settings_obj.ELEVENLABS_MAX_RETRIES = 99
    settings_obj.ELEVENLABS_CONNECTION_TIMEOUT = 99
    settings_obj.ELEVENLABS_POL_SIZE = 99
    settings_obj.reload = MagicMock()
    with patch("rollback_utils.settings", settings_obj):
        yield settings_obj


@pytest.mark.asyncio
class TestRollbackUtils:
    async def test_take_config_snapshot_success(self, mock_settings_object, manage_snapshot_file):
        os.environ["ELEVENLABS_API_KEY"] = "test_api_key"
        os.environ["OTHER_VAR"] = "ignore_me"

        await take_config_snapshot()

        assert manage_snapshot_file.exists()
        with open(manage_snapshot_file) as f:
            snapshot = json.load(f)

        assert "env_vars" in snapshot
        assert snapshot["env_vars"]["ELEVENLABS_API_KEY"] == "test_api_key"
        assert "OTHER_VAR" not in snapshot["env_vars"]

        assert "settings" in snapshot
        assert snapshot["settings"]["ELEVENLABS_MAX_RETRIES"] == 99
        assert snapshot["settings"]["ELEVENLABS_CONNECTION_TIMEOUT"] == 99

        del os.environ["ELEVENLABS_API_KEY"]
        del os.environ["OTHER_VAR"]

    async def test_clear_redis_cache_sync_found(self, mock_redis_sync):
        mock_redis_sync.scan_iter.return_value = iter(["elevenlabs:1", "elevenlabs:2"])
        mock_redis_sync.delete.return_value = 1

        deleted = await clear_redis_cache("elevenlabs:*")

        assert deleted == 2
        mock_redis_sync.scan_iter.assert_called_once_with(match="elevenlabs:*", count=100)
        assert mock_redis_sync.delete.call_count == 2
        mock_redis_sync.delete.assert_has_calls([call("elevenlabs:1"), call("elevenlabs:2")])

    async def test_clear_redis_cache_sync_not_found(self, mock_redis_sync):
        mock_redis_sync.scan_iter.return_value = iter([])

        deleted = await clear_redis_cache("elevenlabs:*")

        assert deleted == 0
        mock_redis_sync.scan_iter.assert_called_once_with(match="elevenlabs:*", count=100)
        mock_redis_sync.delete.assert_not_called()

    async def test_clear_redis_cache_async_found(self, mock_redis_async):
        async def mock_scan_iter_impl(*args, **kwargs):
            yield "elevenlabs:a1"
            yield "elevenlabs:a2"

        mock_redis_async.scan_iter.side_effect = mock_scan_iter_impl
        mock_redis_async.delete.return_value = 1

        deleted = await clear_redis_cache("elevenlabs:*")

        assert deleted == 2
        mock_redis_async.scan_iter.assert_called_once_with(match="elevenlabs:*", count=100)
        assert mock_redis_async.delete.call_count == 2
        mock_redis_async.delete.assert_has_calls(
            [call("elevenlabs:a1"), call("elevenlabs:a2")], any_order=True
        )

    async def test_clear_redis_cache_async_not_found(self, mock_redis_async):
        deleted = await clear_redis_cache("elevenlabs:*")

        assert deleted == 0
        mock_redis_async.scan_iter.assert_called_once_with(match="elevenlabs:*", count=100)
        mock_redis_async.delete.assert_not_called()

    async def test_reset_prometheus_metrics_unregisters(self, mock_prometheus_registry):
        # Usamos MagicMock directamente sin especificar spec=Collector
        collector1 = MagicMock(_name="elevenlabs_requests_total")
        collector2 = MagicMock(_name="elevenlabs_pool_usage_ratio")
        mock_prometheus_registry._names_to_collectors = {
            "elevenlabs_requests_total": collector1,
            "elevenlabs_pool_usage_ratio": collector2,
            "other_metric": MagicMock(_name="other_metric"),
        }

        await reset_prometheus_metrics()

        assert mock_prometheus_registry.unregister.call_count == 2
        mock_prometheus_registry.unregister.assert_has_calls(
            [call(collector1), call(collector2)], any_order=True
        )

    async def test_reset_prometheus_metrics_specific_and_missing(self, mock_prometheus_registry):
        # Usamos MagicMock directamente sin especificar spec=Collector
        collector1 = MagicMock(_name="metric_exists")
        mock_prometheus_registry._names_to_collectors = {"metric_exists": collector1}

        await reset_prometheus_metrics(["metric_exists", "metric_missing"])

        mock_prometheus_registry.unregister.assert_called_once_with(collector1)

    async def test_close_all_connections_uses_close_all(self, mock_connection_pool):
        mock_connection_pool.close_all = AsyncMock(return_value=5)

        await close_all_elevenlabs_connections()

        mock_connection_pool.close_all.assert_called_once()
        mock_connection_pool.get_active_connections.assert_not_called()
        mock_connection_pool.terminate_connection.assert_not_called()

    async def test_close_all_connections_uses_fallback(self, mock_connection_pool):
        mock_conn1 = MagicMock()
        mock_conn2 = MagicMock()
        mock_connection_pool.get_active_connections.return_value = [mock_conn1, mock_conn2]

        await close_all_elevenlabs_connections()

        assert not hasattr(mock_connection_pool, "close_all")
        mock_connection_pool.get_active_connections.assert_called_once()
        assert mock_connection_pool.terminate_connection.call_count == 2
        mock_connection_pool.terminate_connection.assert_has_calls(
            [call(mock_conn1), call(mock_conn2)], any_order=True
        )

    async def test_restore_config_from_snapshot(self, mock_settings_object, manage_snapshot_file):
        test_snapshot = {
            "env_vars": {"ELEVENLABS_API_KEY": "key_from_snapshot"},
            "settings": {
                "ELEVENLABS_MAX_RETRIES": 5,
                "ELEVENLABS_CONNECTION_TIMEOUT": 50,
                "ELEVENLABS_POOL_SIZE": 5,
            },
        }
        with open(manage_snapshot_file, "w") as f:
            json.dump(test_snapshot, f)

        os.environ["ELEVENLABS_API_KEY"] = "initial_key"

        await restore_previous_config()

        assert os.environ["ELEVENLABS_API_KEY"] == "key_from_snapshot"
        assert mock_settings_object.ELEVENLABS_MAX_RETRIES == 5
        assert mock_settings_object.ELEVENLABS_CONNECTION_TIMEOUT == 50
        assert mock_settings_object.ELEVENLABS_POOL_SIZE == 5
        mock_settings_object.reload.assert_called_once()

        del os.environ["ELEVENLABS_API_KEY"]

    async def test_restore_config_to_defaults_no_snapshot(
        self, mock_settings_object, manage_snapshot_file
    ):
        if manage_snapshot_file.exists():
            manage_snapshot_file.unlink()

        mock_settings_object.ELEVENLABS_MAX_RETRIES = 100
        mock_settings_object.ELEVENLABS_CONNECTION_TIMEOUT = 100
        mock_settings_object.ELEVENLABS_POOL_SIZE = 100
        os.environ["ELEVENLABS_API_KEY"] = "initial_key"

        await restore_previous_config()

        assert mock_settings_object.ELEVENLABS_MAX_RETRIES == 3
        assert mock_settings_object.ELEVENLABS_CONNECTION_TIMEOUT == 30
        assert mock_settings_object.ELEVENLABS_POOL_SIZE == 10
        mock_settings_object.reload.assert_called_once()

        if "ELEVENLABS_API_KEY" in os.environ:
            del os.environ["ELEVENLABS_API_KEY"]

    async def test_restore_config_to_defaults_snapshot_error(
        self, mock_settings_object, manage_snapshot_file
    ):
        with open(manage_snapshot_file, "w") as f:
            f.write("{invalid_json")

        await restore_previous_config()

        assert mock_settings_object.ELEVENLABS_MAX_RETRIES == 3
        assert mock_settings_object.ELEVENLABS_CONNECTION_TIMEOUT == 30
        assert mock_settings_object.ELEVENLABS_POOL_SIZE == 10
        mock_settings_object.reload.assert_called_once()

    async def test_apply_default_config(self, mock_settings_object):
        mock_settings_object.ELEVENLABS_MAX_RETRIES = 55
        os.environ["ELEVENLABS_API_KEY"] = "some_key"

        await _apply_default_config()

        assert mock_settings_object.ELEVENLABS_MAX_RETRIES == 3
        assert mock_settings_object.ELEVENLABS_CONNECTION_TIMEOUT == 30
        assert mock_settings_object.ELEVENLABS_POOL_SIZE == 10

        if "ELEVENLABS_API_KEY" in os.environ:
            del os.environ["ELEVENLABS_API_KEY"]