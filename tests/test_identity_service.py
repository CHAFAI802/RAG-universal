import pytest

from sqlalchemy import create_engine, select
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.modules.identity.models import Identity, IdentityStatus, IdentityType
from app.modules.identity.services import IdentityService


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    db_session = TestingSessionLocal()

    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_create_human_identity(session):
    service = IdentityService(session)

    identity = service.create_human_identity("Test User")

    assert identity.identity_id is not None
    assert identity.identity_type == IdentityType.HUMAN
    assert identity.display_name == "Test User"
    assert identity.status == IdentityStatus.ACTIVE
    assert identity.created_at is not None


def test_identity_is_persisted(session):
    service = IdentityService(session)

    created_identity = service.create_human_identity("Persisted User")

    statement = select(Identity).where(
        Identity.identity_id == created_identity.identity_id
    )
    stored_identity = session.execute(statement).scalar_one()

    assert stored_identity.display_name == "Persisted User"


@pytest.mark.parametrize("display_name", ["", " ", "   "])
def test_reject_empty_display_name(session, display_name):
    service = IdentityService(session)

    with pytest.raises(ValueError, match="obligatoire"):
        service.create_human_identity(display_name)


def test_reject_display_name_longer_than_150_characters(session):
    service = IdentityService(session)

    with pytest.raises(ValueError, match="150 caractères"):
        service.create_human_identity("A" * 151)


def test_accept_display_name_of_exactly_150_characters(session):
    service = IdentityService(session)

    identity = service.create_human_identity("A" * 150)

    assert len(identity.display_name) == 150

def test_display_name_is_trimmed(session):
    service = IdentityService(session)

    identity = service.create_human_identity("  Mabrouk Chafai  ")

    assert identity.display_name == "Mabrouk Chafai"


def test_accept_150_characters_after_trimming(session):
    service = IdentityService(session)

    identity = service.create_human_identity("  " + "A" * 150 + "  ")

    assert len(identity.display_name) == 150
    assert identity.display_name == "A" * 150

def test_database_error_rolls_back_transaction(session):
    session.execute(text("""
        CREATE TRIGGER reject_identity_insert
        BEFORE INSERT ON identities
        WHEN NEW.display_name = 'Trigger Failure'
        BEGIN
            SELECT RAISE(ABORT, 'simulated database failure');
        END;
    """))
    session.commit()

    service = IdentityService(session)

    with pytest.raises(IntegrityError):
        service.create_human_identity("Trigger Failure")

    stored_identities = session.execute(
        select(Identity)
    ).scalars().all()

    assert stored_identities == []

    identity = service.create_human_identity("After rollback")

    assert identity.display_name == "After rollback"

def test_refresh_error_rolls_back_after_flush(session, monkeypatch):
    service = IdentityService(session)

    original_refresh = session.refresh

    def failing_refresh(instance):
        raise RuntimeError("Simulated refresh failure")

    monkeypatch.setattr(session, "refresh", failing_refresh)

    with pytest.raises(RuntimeError, match="Simulated refresh failure"):
        service.create_human_identity("Refresh Failure")

    # Restaurer refresh pour pouvoir réutiliser la session.
    monkeypatch.setattr(session, "refresh", original_refresh)

    # Vérifier que le rollback a annulé l'insertion.
    stored_identities = session.execute(
        select(Identity)
    ).scalars().all()

    assert stored_identities == []

    # Vérifier que la session fonctionne toujours.
    identity = service.create_human_identity("After refresh failure")

    assert identity.display_name == "After refresh failure"
def test_build_human_identity_does_not_persist(session):
    service = IdentityService(session)

    identity = service.build_human_identity("Test User")

    assert identity.identity_id is not None
    assert identity.identity_type == IdentityType.HUMAN
    assert identity.display_name == "Test User"
    assert identity.status == IdentityStatus.ACTIVE

    # L'identité n'est ni ajoutée à la session ni enregistrée en base.
    assert identity not in session
    assert identity not in session.new

    stored_identities = session.execute(
        select(Identity)
    ).scalars().all()

    assert stored_identities == []


def test_build_human_identity_trims_display_name(session):
    service = IdentityService(session)

    identity = service.build_human_identity("  Mabrouk Chafai  ")

    assert identity.display_name == "Mabrouk Chafai"
    assert identity not in session.new


@pytest.mark.parametrize("display_name", ["", " ", "   "])
def test_build_human_identity_rejects_empty_display_name(
    session,
    display_name,
):
    service = IdentityService(session)

    with pytest.raises(ValueError, match="obligatoire"):
        service.build_human_identity(display_name)

    assert len(session.new) == 0


def test_build_human_identity_rejects_display_name_longer_than_150_characters(
    session,
):
    service = IdentityService(session)

    with pytest.raises(ValueError, match="150 caractères"):
        service.build_human_identity("A" * 151)

    assert len(session.new) == 0


def test_build_human_identity_accepts_150_characters(session):
    service = IdentityService(session)

    identity = service.build_human_identity("A" * 150)

    assert len(identity.display_name) == 150
    assert identity not in session.new
