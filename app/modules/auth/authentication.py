from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.auth.tokens import (
    TOKEN_USE_IDENTITY_ADMIN,
    TOKEN_USE_USER,
    create_access_token,
)
from app.modules.credentials.models import (
    Credential,
    CredentialOwnerType,
    CredentialStatus,
)
from app.modules.credentials.security import verify_password
from app.modules.identity.models import Identity, IdentityStatus
from app.modules.users.models import User, UserStatus


class InvalidCredentialsError(Exception):
    """The username or password does not match an active administrator."""


class AccountDisabledError(Exception):
    """The credential or its associated identity is disabled."""


class AuthenticationService:
    def __init__(self, session: Session):
        self.session = session

    @property
    def token_lifetime_seconds(self) -> int:
        return settings.AUTH_TOKEN_TTL_SECONDS

    def authenticate(self, *, username: str, password: str) -> str:
        statement = (
            select(Credential, Identity)
            .join(Identity, Credential.identity_id == Identity.identity_id)
            .where(Credential.username == username.lower())
        )
        result = self.session.execute(statement).one_or_none()

        if result is None:
            raise InvalidCredentialsError

        credential, identity = result

        if not verify_password(password, credential.password_hash):
            raise InvalidCredentialsError

        if (
            credential.status != CredentialStatus.ACTIVE
            or identity.status != IdentityStatus.ACTIVE
        ):
            raise AccountDisabledError

        if credential.owner_type == CredentialOwnerType.USER:
            user = self.session.get(User, credential.user_id)

            if (
                user is None
                or user.identity_id != identity.identity_id
                or user.status != UserStatus.ACTIVE
            ):
                raise AccountDisabledError
        elif credential.owner_type != CredentialOwnerType.IDENTITY_ADMIN:
            raise InvalidCredentialsError

        token_use = (
            TOKEN_USE_IDENTITY_ADMIN
            if credential.owner_type == CredentialOwnerType.IDENTITY_ADMIN
            else TOKEN_USE_USER
        )

        return create_access_token(
            identity_id=identity.identity_id,
            credential_id=credential.credential_id,
            token_use=token_use,
        )
