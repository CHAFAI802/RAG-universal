from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.core.config import settings
from app.core.dependencies import get_db
from app.main import app
from app.modules.auth.tokens import (
    TOKEN_ALGORITHM,
    TOKEN_USE_IDENTITY_ADMIN,
    TOKEN_USE_USER,
    create_access_token,
    decode_access_token,
)
from app.modules.credentials.models import (
    Credential,
    CredentialOwnerType,
    CredentialStatus,
)
from app.modules.credentials.security import verify_password
from app.modules.credentials.services import CredentialService
from app.modules.identity.models import Identity, IdentityStatus, IdentityType
from app.modules.users.models import User, UserStatus
from app.modules.users.services import UserService


ADMIN_PASSWORD = "AdminPassword-2026!"
USER_PASSWORD = "UserPassword-2026!"


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


def _create_admin(
    engine,
    *,
    username="admin",
    display_name="Administrateur",
    password=ADMIN_PASSWORD,
):
    with Session(engine) as db:
        identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name=display_name,
        )
        db.add(identity)
        db.flush()
        credential = CredentialService(db).create_username_password_credential(
            identity_id=identity.identity_id,
            username=username,
            password=password,
        )
        db.commit()
        return identity.identity_id, credential.credential_id


@pytest.fixture
def admin(test_engine):
    return _create_admin(test_engine)


def _login(client, username="admin", password=ADMIN_PASSWORD):
    return client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )


def _create_user(client, token, username="agent.smith", password=USER_PASSWORD):
    return client.post(
        "/api/v1/users",
        json={"username": username, "password": password},
        headers={"Authorization": f"Bearer {token}"},
    )


def _count(engine, model):
    with Session(engine) as db:
        return db.scalar(select(func.count()).select_from(model))


def test_identity_admin_creates_user_in_own_identity(client, admin, test_engine):
    login = _login(client)
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = _create_user(client, token)

    assert response.status_code == 201
    data = response.json()
    assert set(data) == {
        "user_id",
        "identity_id",
        "username",
        "status",
        "created_at",
        "updated_at",
    }
    assert data["identity_id"] == str(admin[0])
    assert data["username"] == "agent.smith"
    assert data["status"] == "ACTIVE"
    assert "password" not in response.text
    assert "password_hash" not in response.text
    assert USER_PASSWORD not in response.text

    with Session(test_engine) as db:
        user = db.get(User, UUID(data["user_id"]))
        credential = db.scalar(
            select(Credential).where(Credential.user_id == user.user_id)
        )

        assert user is not None
        assert user.identity_id == admin[0]
        assert credential is not None
        assert credential.identity_id == admin[0]
        assert credential.owner_type == CredentialOwnerType.USER
        assert credential.username == "agent.smith"
        assert credential.password_hash != USER_PASSWORD
        assert credential.password_hash.startswith("$argon2id$")
        assert verify_password(USER_PASSWORD, credential.password_hash)

    # Créer un User ne crée pas une nouvelle Identity.
    assert _count(test_engine, Identity) == 1


def test_admin_credential_remains_identity_admin_after_user_creation(
    client,
    admin,
    test_engine,
):
    token = _login(client).json()["access_token"]
    assert _create_user(client, token).status_code == 201

    with Session(test_engine) as db:
        credential = db.get(Credential, admin[1])
        assert credential.owner_type == CredentialOwnerType.IDENTITY_ADMIN
        assert credential.user_id is None


def test_ordinary_user_cannot_create_another_user(client, admin, test_engine):
    admin_token = _login(client).json()["access_token"]
    created = _create_user(client, admin_token)
    assert created.status_code == 201

    user_login = _login(client, "agent.smith", USER_PASSWORD)
    assert user_login.status_code == 200
    user_token = user_login.json()["access_token"]
    assert decode_access_token(user_token)["token_use"] == TOKEN_USE_USER

    response = _create_user(
        client,
        user_token,
        username="second.user",
        password="SecondPassword-2026!",
    )

    assert response.status_code == 403
    assert _count(test_engine, User) == 1
    assert _count(test_engine, Credential) == 2


def test_forged_admin_token_with_user_credential_is_rejected(
    client,
    admin,
    test_engine,
):
    admin_token = _login(client).json()["access_token"]
    created = _create_user(client, admin_token)
    assert created.status_code == 201

    with Session(test_engine) as db:
        user_credential = db.scalar(
            select(Credential).where(
                Credential.owner_type == CredentialOwnerType.USER
            )
        )
        assert user_credential is not None

        forged_token = create_access_token(
            identity_id=admin[0],
            credential_id=user_credential.credential_id,
            token_use=TOKEN_USE_IDENTITY_ADMIN,
        )

    response = _create_user(
        client,
        forged_token,
        username="second.user",
        password="SecondPassword-2026!",
    )

    assert response.status_code == 403
    assert _count(test_engine, User) == 1


def test_disabled_admin_credential_cannot_create_user(client, admin, test_engine):
    token = _login(client).json()["access_token"]

    with Session(test_engine) as db:
        credential = db.get(Credential, admin[1])
        credential.status = CredentialStatus.DISABLED
        db.commit()

    response = _create_user(client, token)

    assert response.status_code == 401
    assert _count(test_engine, User) == 0


def test_disabled_identity_cannot_create_user(client, admin, test_engine):
    token = _login(client).json()["access_token"]

    with Session(test_engine) as db:
        identity = db.get(Identity, admin[0])
        identity.status = IdentityStatus.DISABLED
        db.commit()

    response = _create_user(client, token)

    assert response.status_code == 401
    assert _count(test_engine, User) == 0


def test_invalid_token_is_rejected(client, admin, test_engine):
    response = _create_user(client, "not-a-valid-token")

    assert response.status_code == 401
    assert _count(test_engine, User) == 0


def test_missing_token_is_rejected(client, admin, test_engine):
    response = client.post(
        "/api/v1/users",
        json={"username": "agent.smith", "password": USER_PASSWORD},
    )

    assert response.status_code == 401
    assert _count(test_engine, User) == 0


def test_expired_token_is_rejected(client, admin, test_engine):
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

    response = _create_user(client, expired_token)

    assert response.status_code == 401
    assert _count(test_engine, User) == 0


def test_signed_token_with_unknown_credential_is_rejected(client, admin, test_engine):
    token = create_access_token(
        identity_id=admin[0],
        credential_id=uuid4(),
        token_use=TOKEN_USE_IDENTITY_ADMIN,
    )

    response = _create_user(client, token)

    assert response.status_code == 401
    assert _count(test_engine, User) == 0


def test_payload_cannot_choose_another_identity(client, admin, test_engine):
    other_identity_id, _ = _create_admin(
        test_engine,
        username="other-admin",
        display_name="Autre administrateur",
    )
    token = _login(client).json()["access_token"]

    response = client.post(
        "/api/v1/users",
        json={
            "username": "agent.smith",
            "password": USER_PASSWORD,
            "identity_id": str(other_identity_id),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
    assert _count(test_engine, User) == 0


def test_username_uniqueness_is_global_across_identities(client, test_engine):
    _create_admin(test_engine, username="admin", display_name="Admin 1")
    _create_admin(test_engine, username="admin2", display_name="Admin 2")

    first_token = _login(client, "admin", ADMIN_PASSWORD).json()["access_token"]
    second_token = _login(client, "admin2", ADMIN_PASSWORD).json()["access_token"]

    first = _create_user(client, first_token, username="shared.user")
    assert first.status_code == 201

    duplicate = _create_user(
        client,
        second_token,
        username="SHARED.USER",
        password="AnotherPassword-2026!",
    )

    assert duplicate.status_code == 409
    assert _count(test_engine, User) == 1


def test_existing_admin_username_is_rejected_for_user_creation(client, admin):
    token = _login(client).json()["access_token"]

    response = _create_user(client, token, username="Admin")

    assert response.status_code == 409


def test_credential_failure_rolls_back_user_creation(test_engine, monkeypatch):
    _create_admin(test_engine)

    with Session(test_engine) as db:
        identity = db.scalar(select(Identity))
        service = UserService(db)

        def failing_credential_creation(**kwargs):
            raise RuntimeError("Simulated credential failure")

        monkeypatch.setattr(
            service.credential_service,
            "create_username_password_credential",
            failing_credential_creation,
        )

        with pytest.raises(RuntimeError, match="Simulated credential failure"):
            service.create_user(
                identity_id=identity.identity_id,
                username="agent.smith",
                password=USER_PASSWORD,
            )

    assert _count(test_engine, User) == 0
    # Seul le credential administrateur préexistant subsiste.
    assert _count(test_engine, Credential) == 1


def test_registration_credential_can_still_create_users(client, test_engine):
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Admin Inscription",
            "username": "registered.admin",
            "password": ADMIN_PASSWORD,
        },
    )
    assert registration.status_code == 201
    identity_id = UUID(registration.json()["identity_id"])

    with Session(test_engine) as db:
        admin_credential = db.scalar(
            select(Credential).where(Credential.identity_id == identity_id)
        )
        assert admin_credential.owner_type == CredentialOwnerType.IDENTITY_ADMIN
        assert admin_credential.user_id is None

    login = _login(client, "registered.admin", ADMIN_PASSWORD)
    assert login.status_code == 200

    response = _create_user(
        client,
        login.json()["access_token"],
        username="agent.smith",
    )

    assert response.status_code == 201
    assert response.json()["identity_id"] == str(identity_id)


def test_user_creation_validates_username_and_hides_password(client, admin):
    token = _login(client).json()["access_token"]

    for payload in (
        {"username": "ab", "password": USER_PASSWORD},
        {"username": "invalid name", "password": USER_PASSWORD},
        {"username": "agent.smith", "password": "TooShort!"},
    ):
        response = client.post(
            "/api/v1/users",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422
        assert payload["password"] not in response.text


def test_disabled_user_cannot_login(client, admin, test_engine):
    admin_token = _login(client).json()["access_token"]

    creation = _create_user(client, admin_token)
    assert creation.status_code == 201

    user_id = UUID(creation.json()["user_id"])

    # Vérifier que le User actif peut se connecter.
    active_login = _login(client, "agent.smith", USER_PASSWORD)
    assert active_login.status_code == 200

    # Désactiver uniquement le User, pas son Credential.
    with Session(test_engine) as db:
        user = db.get(User, user_id)
        credential = db.scalar(
            select(Credential).where(Credential.user_id == user_id)
        )

        assert user is not None
        assert credential is not None
        assert user.status == UserStatus.ACTIVE
        assert credential.status == CredentialStatus.ACTIVE

        user.status = UserStatus.DISABLED
        db.commit()

    # La connexion doit maintenant être refusée.
    disabled_login = _login(client, "agent.smith", USER_PASSWORD)

    assert disabled_login.status_code == 401
    assert disabled_login.json()["detail"] == (
        "Identifiants invalides ou compte désactivé."
    )
