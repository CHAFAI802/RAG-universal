import pytest
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine

from app.core.base import Base
from app.core.dependencies import get_db
from app.main import app
from app.modules.credentials.models import Credential
from app.modules.credentials.security import verify_password
from app.modules.identity.models import Identity, IdentityType


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


def test_register_returns_201_and_public_account_data(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Mabrouk",
            "username": "Mabrouk",
            "password": "MotDePasseTest-2026!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["identity_type"] == "HUMAN"
    assert data["display_name"] == "Mabrouk"
    assert data["username"] == "mabrouk"
    assert data["status"] == "ACTIVE"
    assert "identity_id" in data
    assert "created_at" in data
    assert "updated_at" in data

    assert "password" not in data
    assert "password_hash" not in data


def test_register_persists_identity_and_hashed_credential(client, test_engine):
    password = "MotDePasseTest-2026!"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Utilisateur Test",
            "username": "testuser",
            "password": password,
        },
    )

    assert response.status_code == 201

    identity_id = UUID(response.json()["identity_id"])

    with Session(test_engine) as db:
        identity = db.get(Identity, identity_id)

        credential = db.scalar(
            select(Credential).where(
                Credential.identity_id == identity_id
            )
        )

        assert identity is not None
        assert identity.identity_type == IdentityType.HUMAN

        assert credential is not None
        assert credential.username == "testuser"
        assert credential.password_hash != password
        assert credential.password_hash.startswith("$argon2id$")
        assert verify_password(password, credential.password_hash)


def test_register_rejects_duplicate_username_case_insensitively(client):
    payload = {
        "display_name": "Premier utilisateur",
        "username": "mabrouk",
        "password": "MotDePasseTest-2026!",
    }

    first_response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Deuxième utilisateur",
            "username": "MABROUK",
            "password": "AutreMotDePasse-2026!",
        },
    )

    assert second_response.status_code == 409


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {
            "display_name": "",
            "username": "testuser",
            "password": "MotDePasseTest-2026!",
        },
        {
            "display_name": "Utilisateur",
            "username": "ab",
            "password": "MotDePasseTest-2026!",
        },
        {
            "display_name": "Utilisateur",
            "username": "nom invalide",
            "password": "MotDePasseTest-2026!",
        },
        {
            "display_name": "Utilisateur",
            "username": "testuser",
            "password": "court",
        },
        {
            "display_name": "Utilisateur",
            "username": "testuser",
            "password": "MotDePasseTest-2026!",
            "unexpected": "value",
        },
    ],
)
def test_register_rejects_invalid_payload_without_creating_data(
    client,
    test_engine,
    payload,
):
    response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == 422

    with Session(test_engine) as db:
        assert db.scalar(
            select(func.count()).select_from(Identity)
        ) == 0

        assert db.scalar(
            select(func.count()).select_from(Credential)
        ) == 0
