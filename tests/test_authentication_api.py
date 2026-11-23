from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient
from jwt import InvalidTokenError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.core.config import settings
from app.core.dependencies import get_db
from app.main import app
from app.modules.auth.dependencies import get_authenticated_identity
from app.modules.auth.tokens import (
    TOKEN_ALGORITHM,
    TOKEN_AUDIENCE,
    TOKEN_ISSUER,
    decode_access_token,
)
from app.modules.credentials.models import Credential, CredentialStatus
from app.modules.credentials.services import CredentialService
from app.modules.identity.models import Identity, IdentityStatus, IdentityType


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
def client(test_engine, monkeypatch):
    monkeypatch.setattr(settings, "AUTH_TOKEN_SECRET", "test-only-secret-" + "x" * 32)
    monkeypatch.setattr(settings, "AUTH_TOKEN_TTL_SECONDS", 900)

    def override_get_db():
        with Session(test_engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def account(test_engine):
    with Session(test_engine) as db:
        identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="Administrateur",
        )
        db.add(identity)
        db.flush()
        credential = CredentialService(db).create_username_password_credential(
            identity_id=identity.identity_id,
            username="admin",
            password="AdminPassword-2026!",
        )
        db.commit()
        return identity.identity_id, credential.credential_id


def _login(client, username="admin", password="AdminPassword-2026!"):
    return client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )


def test_login_returns_identity_scoped_bearer_token_without_secrets(
    client,
    account,
):
    response = _login(client)

    assert response.status_code == 200
    assert set(response.json()) == {"access_token", "token_type", "expires_in"}
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == 900
    claims = decode_access_token(response.json()["access_token"])
    assert claims["sub"] == str(account[0])
    assert claims["credential_id"] == str(account[1])
    assert "password" not in response.text
    assert "password_hash" not in response.text
    assert "AdminPassword-2026!" not in response.text


@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("admin", "IncorrectPassword-2026!"),
        ("unknown", "AdminPassword-2026!"),
    ],
)
def test_login_rejects_bad_credentials_with_same_public_error(
    client,
    account,
    username,
    password,
):
    response = _login(client, username, password)

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides ou compte désactivé."
    assert "password_hash" not in response.text
    assert "AdminPassword-2026!" not in response.text


def test_login_rejects_disabled_credential(client, account, test_engine):
    with Session(test_engine) as db:
        credential = db.get(Credential, account[1])
        credential.status = CredentialStatus.DISABLED
        db.commit()

    response = _login(client)

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides ou compte désactivé."


def test_login_rejects_disabled_identity(client, account, test_engine):
    with Session(test_engine) as db:
        identity = db.get(Identity, account[0])
        identity.status = IdentityStatus.DISABLED
        db.commit()

    response = _login(client)

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides ou compte désactivé."


def test_invalid_token_is_rejected(client, account, test_engine):
    with Session(test_engine) as db:
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="not-a-valid-token",
        )
        with pytest.raises(HTTPException) as error:
            get_authenticated_identity(credentials, db)

    assert error.value.status_code == 401


def test_expired_token_is_rejected(client, account, test_engine):
    valid_token = _login(client).json()["access_token"]
    claims = jwt.decode(
        valid_token,
        options={"verify_signature": False},
        algorithms=[TOKEN_ALGORITHM],
    )
    claims["iat"] = datetime.now(timezone.utc) - timedelta(minutes=2)
    claims["exp"] = datetime.now(timezone.utc) - timedelta(minutes=1)
    expired_token = jwt.encode(
        claims,
        settings.AUTH_TOKEN_SECRET,
        algorithm=TOKEN_ALGORITHM,
    )

    with Session(test_engine) as db:
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=expired_token,
        )
        with pytest.raises(HTTPException) as error:
            get_authenticated_identity(credentials, db)

    assert error.value.status_code == 401


def test_dependency_returns_the_token_identity_and_rejects_disabled_accounts(
    client,
    account,
    test_engine,
):
    token = _login(client).json()["access_token"]
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    with Session(test_engine) as db:
        identity = get_authenticated_identity(credentials, db)
        assert identity.identity_id == UUID(str(account[0]))

        identity.status = IdentityStatus.DISABLED
        db.commit()
        with pytest.raises(HTTPException) as error:
            get_authenticated_identity(credentials, db)

    assert error.value.status_code == 401


def test_token_requires_a_valid_signature_and_audience(client, account):
    response = _login(client)
    token = response.json()["access_token"]

    with pytest.raises(InvalidTokenError):
        jwt.decode(
            token,
            "wrong-signing-secret-" + "x" * 32,
            algorithms=[TOKEN_ALGORITHM],
            issuer=TOKEN_ISSUER,
            audience=TOKEN_AUDIENCE,
        )


def test_login_validation_errors_do_not_echo_password(client):
    password = "Sensitive-Invalid-Password-" + "x" * 110
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": password},
    )

    assert response.status_code == 422
    assert password not in response.text
