import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import get_db
from backend.main import app
from backend.models import Base


@pytest.fixture
def client():
    # Create an isolated in-memory SQLite database for this test.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    # Override the production database dependency.
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


def create_test_ticket(
    client,
    title="VPN connection failing",
    description="Unable to connect to the company VPN.",
    category="Network",
    priority="High",
):
    return client.post(
        "/tickets",
        json={
            "title": title,
            "description": description,
            "category": category,
            "priority": priority,
        },
    )


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_ticket(client):
    response = create_test_ticket(client)

    assert response.status_code == 201

    ticket = response.json()
    assert ticket["title"] == "VPN connection failing"
    assert ticket["priority"] == "High"
    assert ticket["status"] == "Open"
    assert isinstance(ticket["id"], int)
    assert ticket["created_at"] is not None


def test_list_tickets(client):
    create_test_ticket(client)
    create_test_ticket(
        client,
        title="Email not syncing",
        description="New messages are missing from the inbox.",
        category="Email",
        priority="Medium",
    )

    response = client.get("/tickets")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_tickets_by_status_and_priority(client):
    create_test_ticket(client)

    create_test_ticket(
        client,
        title="Laptop running slowly",
        description="Applications take too long to open.",
        category="Hardware",
        priority="High",
    )

    create_test_ticket(
        client,
        title="Email not syncing",
        description="New messages are missing from the inbox.",
        category="Email",
        priority="Medium",
    )

    response = client.get(
        "/tickets",
        params={"status": "Open", "priority": "High"},
    )

    assert response.status_code == 200

    tickets = response.json()
    assert len(tickets) == 2
    assert all(ticket["status"] == "Open" for ticket in tickets)
    assert all(ticket["priority"] == "High" for ticket in tickets)


def test_get_single_ticket(client):
    created = create_test_ticket(client)
    ticket_id = created.json()["id"]

    response = client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200
    assert response.json()["id"] == ticket_id


def test_get_nonexistent_ticket_returns_404(client):
    response = client.get("/tickets/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_update_ticket(client):
    created = create_test_ticket(client)
    ticket_id = created.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={
            "status": "In Progress",
            "priority": "Low",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "In Progress"
    assert response.json()["priority"] == "Low"


def test_empty_update_returns_400(client):
    created = create_test_ticket(client)
    ticket_id = created.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Provide at least one field to update"
    )

def test_create_ticket_rejects_short_title(client):
    response = client.post(
        "/tickets",
        json={
            "title": "AB",
            "description": "Unable to connect to the company VPN.",
            "category": "Network",
            "priority": "High",
        },
    )

    assert response.status_code == 422


def test_create_ticket_rejects_invalid_priority(client):
    response = client.post(
        "/tickets",
        json={
            "title": "VPN connection failing",
            "description": "Unable to connect to the company VPN.",
            "category": "Network",
            "priority": "Urgent",
        },
    )

    assert response.status_code == 422


def test_create_ticket_rejects_missing_category(client):
    response = client.post(
        "/tickets",
        json={
            "title": "VPN connection failing",
            "description": "Unable to connect to the company VPN.",
            "priority": "High",
        },
    )

    assert response.status_code == 422


def test_invalid_status_filter_returns_422(client):
    response = client.get(
        "/tickets",
        params={"status": "Waiting"},
    )

    assert response.status_code == 422
def test_create_ticket_rejects_whitespace_title(client):
    response = client.post(
        "/tickets",
        json={
            "title": "   ",
            "description": "Unable to connect to the company VPN.",
            "category": "Network",
            "priority": "High",
        },
    )

    assert response.status_code == 422


def test_create_ticket_rejects_whitespace_description(client):
    response = client.post(
        "/tickets",
        json={
            "title": "VPN connection failing",
            "description": "     ",
            "category": "Network",
            "priority": "High",
        },
    )

    assert response.status_code == 422


def test_create_ticket_rejects_whitespace_category(client):
    response = client.post(
        "/tickets",
        json={
            "title": "VPN connection failing",
            "description": "Unable to connect to the company VPN.",
            "category": "   ",
            "priority": "High",
        },
    )

    assert response.status_code == 422