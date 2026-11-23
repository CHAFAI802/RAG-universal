import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.modules.identity.models import Identity, IdentityType
from app.modules.credentials.models import Credential
from app.modules.credentials.services import CredentialService
from app.modules.credentials.security import verify_password


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    TestingSession = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    db = TestingSession()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def identity(session):
    identity = Identity(
        identity_type=IdentityType.HUMAN,
        display_name="Utilisateur Test",
    )

    session.add(identity)
    session.flush()

    return identity


def test_create_credential_success(session, identity):
    service = CredentialService(session)

    credential = service.create_username_password_credential(
        identity_id=identity.identity_id,
        username="mabrouk",
        password="MotDePasseTest-2026!",
    )

    assert credential.username == "mabrouk"
    assert credential.identity_id == identity.identity_id
    assert credential.password_hash != "MotDePasseTest-2026!"
    assert verify_password(
        "MotDePasseTest-2026!",
        credential.password_hash,
    )


def test_username_is_normalized_to_lowercase(session, identity):
    service = CredentialService(session)

    credential = service.create_username_password_credential(
        identity_id=identity.identity_id,
        username="Mabrouk",
        password="MotDePasseTest-2026!",
    )

    assert credential.username == "mabrouk"


@pytest.mark.parametrize(
    "username",
    [
        "ab",
        "a" * 51,
        "user name",
        "utilisateur-é",
        "user@name",
        "",
        "   ",
    ],
)
def test_invalid_username_is_rejected(session, identity, username):
    service = CredentialService(session)

    with pytest.raises(ValueError):
        service.create_username_password_credential(
            identity_id=identity.identity_id,
            username=username,
            password="MotDePasseTest-2026!",
        )


def test_duplicate_username_is_rejected(session, identity):
    service = CredentialService(session)

    service.create_username_password_credential(
        identity_id=identity.identity_id,
        username="mabrouk",
        password="MotDePasseTest-2026!",
    )

    with pytest.raises(ValueError, match="déjà utilisé"):
        service.create_username_password_credential(
            identity_id=identity.identity_id,
            username="MABROUK",
            password="AutreMotDePasse-2026!",
        )


@pytest.mark.parametrize(
    "password",
    [
        "Court123!",
        "a" * 11,
        "a" * 129,
        "",
    ],
)
def test_invalid_password_length_is_rejected(session, identity, password):
    service = CredentialService(session)

    with pytest.raises(ValueError):
        service.create_username_password_credential(
            identity_id=identity.identity_id,
            username="mabrouk",
            password=password,
        )


def test_password_with_12_characters_is_accepted(session, identity):
    service = CredentialService(session)

    credential = service.create_username_password_credential(
        identity_id=identity.identity_id,
        username="mabrouk",
        password="Abcdef123456",
    )

    assert credential.password_hash
    assert verify_password("Abcdef123456", credential.password_hash)


def test_password_with_128_characters_is_accepted(session, identity):
    service = CredentialService(session)

    password = "A" * 128

    credential = service.create_username_password_credential(
        identity_id=identity.identity_id,
        username="mabrouk",
        password=password,
    )

    assert verify_password(password, credential.password_hash)


def test_non_string_username_is_rejected(session, identity):
    service = CredentialService(session)

    with pytest.raises(ValueError):
        service.create_username_password_credential(
            identity_id=identity.identity_id,
            username=None,
            password="MotDePasseTest-2026!",
        )


def test_non_string_password_is_rejected(session, identity):
    service = CredentialService(session)

    with pytest.raises(ValueError):
        service.create_username_password_credential(
            identity_id=identity.identity_id,
            username="mabrouk",
            password=None,
        )
