from uuid import uuid4

import pytest
from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.base import Base
from app.core.database import engine
from app.modules.credentials.models import (
    Credential,
    CredentialOwnerType,
)
from app.modules.credentials.services import CredentialService
from app.modules.identity.models import Identity, IdentityType
from app.modules.users.models import User


@pytest.fixture(scope="module")
def postgres_users_engine():
    if engine.url.database != "rag_universal_test":
        pytest.skip("PostgreSQL integration requires rag_universal_test.")

    Base.metadata.create_all(bind=engine)
    yield engine


def test_postgresql_rejects_credential_from_another_identity(
    postgres_users_engine,
):
    identity_a_id = None
    identity_b_id = None
    user_id = None
    credential_id = None

    with Session(postgres_users_engine) as db:
        identity_a = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="Composite FK test A",
        )
        identity_b = Identity(
            identity_type=IdentityType.HUMAN,
            display_name="Composite FK test B",
        )
        db.add_all([identity_a, identity_b])
        db.flush()

        identity_a_id = identity_a.identity_id
        identity_b_id = identity_b.identity_id

        user = User(identity_id=identity_a_id)
        db.add(user)
        db.flush()
        user_id = user.user_id

        credential = CredentialService(db).create_username_password_credential(
            identity_id=identity_a_id,
            username=f"fk-test-{uuid4().hex[:12]}",
            password="CompositeForeignKeyTest-2026!",
            owner_type=CredentialOwnerType.USER,
            user_id=user_id,
        )
        credential_id = credential.credential_id
        db.commit()

        try:
            with pytest.raises(IntegrityError) as exc_info:
                with db.begin_nested():
                    db.execute(
                        update(Credential)
                        .where(Credential.credential_id == credential_id)
                        .values(identity_id=identity_b_id)
                    )

            diagnostic = getattr(exc_info.value.orig, "diag", None)
            constraint_name = getattr(
                diagnostic,
                "constraint_name",
                None,
            )

            assert constraint_name == "fk_credentials_identity_user_users"

            db.expire_all()
            persisted_credential = db.get(Credential, credential_id)

            assert persisted_credential is not None
            assert persisted_credential.identity_id == identity_a_id

        finally:
            db.rollback()

            db.execute(
                delete(Credential).where(
                    Credential.credential_id == credential_id
                )
            )
            db.execute(
                delete(User).where(User.user_id == user_id)
            )
            db.execute(
                delete(Identity).where(
                    Identity.identity_id.in_(
                        [identity_a_id, identity_b_id]
                    )
                )
            )
            db.commit()
