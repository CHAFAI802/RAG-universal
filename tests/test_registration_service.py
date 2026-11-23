import pytest

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.modules.identity.models import Identity, IdentityType
from app.modules.credentials.models import Credential
from app.modules.credentials.services import CredentialService
from app.modules.credentials.security import verify_password
from app.modules.auth.registration import RegistrationService


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


def test_register_creates_identity_and_credential(session):
    service = RegistrationService(session)

    identity, credential = service.register(
        display_name="Mabrouk",
        username="Mabrouk",
        password="MotDePasseTest-2026!",
    )

    assert identity.identity_id is not None
    assert identity.identity_type == IdentityType.HUMAN
    assert identity.display_name == "Mabrouk"

    assert credential.identity_id == identity.identity_id
    assert credential.username == "mabrouk"
    assert verify_password(
        "MotDePasseTest-2026!",
        credential.password_hash,
    )

    assert session.scalar(select(func.count()).select_from(Identity)) == 1
    assert session.scalar(select(func.count()).select_from(Credential)) == 1


def test_register_commits_exactly_once(session, monkeypatch):
    service = RegistrationService(session)

    original_commit = session.commit
    commit_calls = []

    def tracked_commit():
        commit_calls.append(True)
        return original_commit()

    monkeypatch.setattr(session, "commit", tracked_commit)

    service.register(
        display_name="Utilisateur Test",
        username="testuser",
        password="MotDePasseTest-2026!",
    )

    assert len(commit_calls) == 1


def test_credential_failure_rolls_back_identity(session, monkeypatch):
    service = RegistrationService(session)

    def failing_credential_creation(**kwargs):
        raise RuntimeError("Simulated credential failure")

    monkeypatch.setattr(
        service.credential_service,
        "create_username_password_credential",
        failing_credential_creation,
    )

    with pytest.raises(RuntimeError, match="Simulated credential failure"):
        service.register(
            display_name="Utilisateur Test",
            username="testuser",
            password="MotDePasseTest-2026!",
        )

    assert session.scalar(select(func.count()).select_from(Identity)) == 0
    assert session.scalar(select(func.count()).select_from(Credential)) == 0


def test_duplicate_username_rolls_back_new_identity(session):
    existing_identity = Identity(
        identity_type=IdentityType.HUMAN,
        display_name="Utilisateur Existant",
    )

    session.add(existing_identity)
    session.flush()

    CredentialService(session).create_username_password_credential(
        identity_id=existing_identity.identity_id,
        username="mabrouk",
        password="MotDePasseTest-2026!",
    )

    session.commit()

    service = RegistrationService(session)

    with pytest.raises(ValueError, match="déjà utilisé"):
        service.register(
            display_name="Nouvel Utilisateur",
            username="MABROUK",
            password="AutreMotDePasse-2026!",
        )

    assert session.scalar(select(func.count()).select_from(Identity)) == 1
    assert session.scalar(select(func.count()).select_from(Credential)) == 1


@pytest.mark.parametrize(
    "display_name, username, password",
    [
        ("", "testuser", "MotDePasseTest-2026!"),
        ("Utilisateur", "ab", "MotDePasseTest-2026!"),
        ("Utilisateur", "testuser", "court"),
    ],
)
def test_invalid_registration_creates_nothing(
    session,
    display_name,
    username,
    password,
):
    service = RegistrationService(session)

    with pytest.raises(ValueError):
        service.register(
            display_name=display_name,
            username=username,
            password=password,
        )

    assert session.scalar(select(func.count()).select_from(Identity)) == 0
    assert session.scalar(select(func.count()).select_from(Credential)) == 0
