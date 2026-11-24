import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.base import Base
from app.core.config import settings
from app.core.database import engine
from app.core.dependencies import get_db
from app.main import app
from app.modules.credentials.models import Credential, CredentialOwnerType
from app.modules.credentials.services import CredentialService
from app.modules.identity.models import Identity, IdentityType
from app.modules.ingestion.models import Ingestion
from app.modules.users.models import User


@pytest.fixture(scope="module")
def postgres_test_engine():
    if engine.url.database != "rag_universal_test":
        pytest.skip("PostgreSQL ingestion integration requires rag_universal_test.")

    Base.metadata.create_all(bind=engine)
    yield engine


def test_postgresql_ingestion_persists_owner_and_original(
    postgres_test_engine,
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(settings, "AUTH_TOKEN_SECRET", "test-only-secret-" + "x" * 32)
    monkeypatch.setattr(settings, "AUTH_TOKEN_TTL_SECONDS", 900)
    monkeypatch.setattr(
        settings,
        "INGESTION_TEMP_STORAGE_PATH",
        str(tmp_path / "postgres-temporary"),
    )
    monkeypatch.setattr(settings, "INGESTION_MAX_FILE_SIZE_BYTES", 1024)
    monkeypatch.setattr(settings, "INGESTION_ALLOWED_EXTENSIONS", "txt")

    owner = uuid.uuid4().hex[:12]
    username = f"ingest-pg-{owner}"
    password = "PostgreSQLIngestionPassword-2026!"

    with Session(postgres_test_engine) as db:
        identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="PostgreSQL ingestion test",
        )
        db.add(identity)
        db.flush()
        user = User(identity_id=identity.identity_id)
        db.add(user)
        db.flush()
        credential = CredentialService(db).create_username_password_credential(
            identity_id=identity.identity_id,
            username=username,
            password=password,
            owner_type=CredentialOwnerType.USER,
            user_id=user.user_id,
        )
        db.commit()
        identity_id = identity.identity_id
        user_id = user.user_id
        credential_id = credential.credential_id

    def override_get_db():
        with Session(postgres_test_engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": username, "password": password},
            )
            assert login.status_code == 200
            token = login.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            created = client.post(
                "/api/v1/ingestions",
                json={"document_name": "postgres.txt"},
                headers=headers,
            )
            assert created.status_code == 201
            ingestion_id = created.json()["ingestion_id"]

            received = client.put(
                f"/api/v1/ingestions/{ingestion_id}/source",
                content=b"postgres original",
                headers=headers,
            )
            assert received.status_code == 200
            assert received.json()["status"] == "RECEIVED"
            assert received.json()["identity_id"] == str(identity_id)
            assert received.json()["user_id"] == str(user_id)

            with Session(postgres_test_engine) as db:
                row = db.get(Ingestion, uuid.UUID(ingestion_id))
                assert row is not None
                assert row.identity_id == identity_id
                assert row.user_id == user_id
                assert row.status.value == "RECEIVED"

            source = client.get(
                f"/api/v1/ingestions/{ingestion_id}/source",
                headers=headers,
            )
            assert source.status_code == 200
            assert source.content == b"postgres original"
    finally:
        app.dependency_overrides.clear()
        with Session(postgres_test_engine) as db:
            db.execute(
                delete(Ingestion).where(
                    Ingestion.identity_id == identity_id,
                    Ingestion.user_id == user_id,
                )
            )
            db.execute(
                delete(Credential).where(
                    Credential.credential_id == credential_id
                )
            )
            db.execute(delete(User).where(User.user_id == user_id))
            db.execute(
                delete(Identity).where(Identity.identity_id == identity_id)
            )
            db.commit()
