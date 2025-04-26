import logging
from fastapi.testclient import TestClient
from app.main import app
from app.models.campaign import Campaign

logger = logging.getLogger(__name__)

def test_pagination(test_client: TestClient):
    logger.info("Iniciando test de paginación")
    # Crear múltiples campañas
    for i in range(15):
        test_client.post("/api/campaigns/", json={
            "name": f"Campaign {i}",
            "description": f"Description {i}",
            "contact_list_ids": [1],
            "max_retries": 3,
            "schedule_start": "2025-01-01T00:00:00",
            "schedule_end": "2025-12-31T23:59:59",
            "status": "active"
        })

    response = test_client.get("/api/campaigns/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 10

def test_filter_by_status(test_client: TestClient):
    logger.info("Iniciando test de filtrado por estado")
    # Crear campañas con diferentes estados
    states = ["active", "paused", "completed"]
    for state in states:
        test_client.post("/api/campaigns/", json={
            "name": f"Campaign {state}",
            "description": f"Description for {state}",
            "contact_list_ids": [1],
            "max_retries": 3,
            "schedule_start": "2025-01-01T00:00:00",
            "schedule_end": "2025-12-31T23:59:59",
            "status": state
        })

    response = test_client.get("/api/campaigns/?status=active")
    assert response.status_code == 200
    data = response.json()
    assert all(campaign["status"] == "active" for campaign in data)

def test_filter_by_date_range(test_client: TestClient):
    logger.info("Iniciando test de filtrado por rango de fechas")
    dates = [
        ("2025-01-01T00:00:00", "2025-06-30T23:59:59"),
        ("2025-07-01T00:00:00", "2025-12-31T23:59:59")
    ]

    for start, end in dates:
        test_client.post("/api/campaigns/", json={
            "name": f"Campaign {start}",
            "description": f"Description for {start}",
            "contact_list_ids": [1],
            "max_retries": 3,
            "schedule_start": start,
            "schedule_end": end,
            "status": "active"
        })

    response = test_client.get("/api/campaigns/?start_date=2025-01-01T00:00:00&end_date=2025-06-30T23:59:59")
    assert response.status_code == 200
    data = response.json()
    assert all(campaign["schedule_start"] <= "2025-06-30T23:59:59" for campaign in data)