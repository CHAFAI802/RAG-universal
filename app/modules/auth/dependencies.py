from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.tokens import (
    TOKEN_USE_IDENTITY_ADMIN,
    InvalidAccessTokenError,
    decode_access_token,
)
from app.modules.credentials.models import (
    Credential,
    CredentialOwnerType,
    CredentialStatus,
)
from app.modules.identity.models import Identity, IdentityStatus


_bearer_scheme = HTTPBearer(auto_error=False)


def get_authenticated_identity(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> Identity:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise ou jeton invalide.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        claims = decode_access_token(credentials.credentials)
        identity_id = UUID(str(claims["sub"]))
        credential_id = UUID(str(claims["credential_id"]))
    except (InvalidAccessTokenError, KeyError, TypeError, ValueError):
        raise unauthorized

    statement = (
        select(Identity)
        .join(Credential, Credential.identity_id == Identity.identity_id)
        .where(
            Identity.identity_id == identity_id,
            Identity.status == IdentityStatus.ACTIVE,
            Credential.credential_id == credential_id,
            Credential.status == CredentialStatus.ACTIVE,
        )
    )
    identity = db.scalar(statement)
    if identity is None:
        raise unauthorized

    return identity


def get_identity_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> Identity:
    """Résout l'Identity administrateur depuis un JWT et son Credential actif.

    Un JWT valide ne suffit pas : le Credential référencé doit exister,
    être actif, être de type IDENTITY_ADMIN et son Identity doit être active.
    """

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise ou jeton invalide.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    forbidden = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Privilèges administrateur d'Identity requis.",
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        claims = decode_access_token(credentials.credentials)
        identity_id = UUID(str(claims["sub"]))
        credential_id = UUID(str(claims["credential_id"]))
    except (InvalidAccessTokenError, KeyError, TypeError, ValueError):
        raise unauthorized

    if claims.get("token_use") != TOKEN_USE_IDENTITY_ADMIN:
        raise forbidden

    statement = (
        select(Identity, Credential)
        .join(Credential, Credential.identity_id == Identity.identity_id)
        .where(
            Identity.identity_id == identity_id,
            Identity.status == IdentityStatus.ACTIVE,
            Credential.credential_id == credential_id,
            Credential.status == CredentialStatus.ACTIVE,
        )
    )
    row = db.execute(statement).one_or_none()
    if row is None:
        raise unauthorized

    identity, credential = row

    if credential.owner_type != CredentialOwnerType.IDENTITY_ADMIN:
        raise forbidden

    return identity
