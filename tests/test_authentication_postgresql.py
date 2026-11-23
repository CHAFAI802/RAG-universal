from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.core.base import Base
from app.core.database import engine
from app.modules.auth.authentication import AuthenticationService
from app.modules.auth.dependencies import get_authenticated_identity
from app.modules.credentials.models import Credential
from app.modules.credentials.services import CredentialService
from app.modules.identity.models import Identity, IdentityType


@pytest.fixture(scope="module")
def postgres_test_engine():
    if engine.url.database != "rag_universal_test":
        pytest.skip("PostgreSQL auth integration requires rag_universal_test.")

    Base.metadata.create_all(bind=engine)
    yield engine


def test_postgresql_admin_authentication_and_identity_resolution(
    postgres_test_engine,
    monkeypatch,
):
    from app.core.config import settings

    monkeypatch.setattr(settings, "AUTH_TOKEN_SECRET", "test-only-secret-" + "x" * 32)
    monkeypatch.setattr(settings, "AUTH_TOKEN_TTL_SECONDS", 900)

    username = f"pg-{uuid4().hex}"
    password = "PostgresAdminPassword-2026!"

    with Session(postgres_test_engine) as db:
        identity = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="PostgreSQL test administrator",
        )
        db.add(identity)
        db.flush()
        credential = CredentialService(db).create_username_password_credential(
            identity_id=identity.identity_id,
            username=username,
            password=password,
        )
        db.commit()

        try:
            token = AuthenticationService(db).authenticate(
                username=username,
                password=password,
            )
            from fastapi.security import HTTPAuthorizationCredentials

            authenticated_identity = get_authenticated_identity(
                HTTPAuthorizationCredentials(scheme="Bearer", credentials=token),
                db,
            )
            assert authenticated_identity.identity_id == identity.identity_id
        finally:
            db.delete(credential)
            db.delete(identity)
            db.commit()
