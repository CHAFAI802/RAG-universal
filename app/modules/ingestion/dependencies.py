from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.tokens import (
    TOKEN_USE_USER,
    InvalidAccessTokenError,
    decode_access_token,
)
from app.modules.credentials.models import (
    Credential,
    CredentialOwnerType,
    CredentialStatus,
)
from app.modules.identity.models import Identity, IdentityStatus
from app.modules.users.models import User, UserStatus


_bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class AuthenticatedUser:
    """Identity et User résolus exclusivement depuis le contexte vérifié."""

    identity: Identity
    user: User
    credential: Credential


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> AuthenticatedUser:
    """Résout l'Identity et le User propriétaires d'une ingestion.

    Réutilise le JWT existant et revalide côté serveur le Credential, son
    Identity, son User et leurs statuts. Aucun identifiant fourni par le
    client n'est accepté comme preuve d'appartenance.
    """

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise ou jeton invalide.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    forbidden = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Un compte User actif est requis pour ingérer des sources.",
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        claims = decode_access_token(credentials.credentials)
        identity_id = UUID(str(claims["sub"]))
        credential_id = UUID(str(claims["credential_id"]))
    except (InvalidAccessTokenError, KeyError, TypeError, ValueError):
        raise unauthorized

    if claims.get("token_use") != TOKEN_USE_USER:
        raise forbidden

    row = db.execute(
        select(Identity, Credential)
        .join(Credential, Credential.identity_id == Identity.identity_id)
        .where(
            Identity.identity_id == identity_id,
            Identity.status == IdentityStatus.ACTIVE,
            Credential.credential_id == credential_id,
            Credential.status == CredentialStatus.ACTIVE,
        )
    ).one_or_none()

    if row is None:
        raise unauthorized

    identity, credential = row

    if (
        credential.owner_type != CredentialOwnerType.USER
        or credential.user_id is None
    ):
        raise forbidden

    user = db.scalar(
        select(User).where(
            User.user_id == credential.user_id,
            User.identity_id == identity.identity_id,
        )
    )

    if user is None:
        raise unauthorized

    if user.status != UserStatus.ACTIVE:
        raise unauthorized

    return AuthenticatedUser(
        identity=identity,
        user=user,
        credential=credential,
    )
