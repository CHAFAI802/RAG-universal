import pytest
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.core.dependencies import get_db
from app.main import app
from app.modules.identity.models import Identity, IdentityStatus, IdentityType
from app.modules.credentials.models import Credential


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def client(test_engine):
    def override_get_db():
        with Session(test_engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_create_human_identity_returns_201(client):
    response = client.post(
        "/api/v1/identities/human",
        json={"display_name": "Mabrouk"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["identity_type"] == "HUMAN"
    assert data["display_name"] == "Mabrouk"
    assert data["status"] == "ACTIVE"
    assert "identity_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_human_identity_persists_in_database(client, test_engine):
    response = client.post(
        "/api/v1/identities/human",
        json={"display_name": "Test Persistence"},
    )

    assert response.status_code == 201

    identity_id = UUID(response.json()["identity_id"])

    with Session(test_engine) as db:
        identity = db.get(Identity, identity_id)

        assert identity is not None
        assert identity.display_name == "Test Persistence"
        assert identity.identity_type == IdentityType.HUMAN
        assert identity.status == IdentityStatus.ACTIVE


def test_create_human_identity_normalizes_display_name(client):
    response = client.post(
        "/api/v1/identities/human",
        json={"display_name": "  Mabrouk  "},
    )

    assert response.status_code == 201
    assert response.json()["display_name"] == "Mabrouk"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"display_name": ""},
        {"display_name": "   "},
        {"display_name": "A" * 151},
        {"display_name": "Mabrouk", "status": "DISABLED"},
        {"display_name": "Mabrouk", "identity_type": "SERVICE"},
    ],
)
def test_create_human_identity_rejects_invalid_payload(client, payload):
    response = client.post(
        "/api/v1/identities/human",
        json=payload,
    )

    assert response.status_code == 422


def test_registered_tables_match_schema():
    assert set(Base.metadata.tables.keys()) == {
        "identities",
        "credentials",
        "users",
        "ingestions",
    }


def test_creation_returns_only_identity_fields(client):
    response = client.post(
        "/api/v1/identities/human",
        json={"display_name": "API Test"},
    )

    assert response.status_code == 201

    assert set(response.json().keys()) == {
        "identity_id",
        "identity_type",
        "display_name",
        "status",
        "created_at",
        "updated_at",
    }
