from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt import InvalidTokenError

from app.core.config import settings


TOKEN_ALGORITHM = "HS256"
TOKEN_ISSUER = "rag-universal"
TOKEN_AUDIENCE = "rag-universal-api"

TOKEN_USE_IDENTITY_ADMIN = "identity_admin"
TOKEN_USE_USER = "user"

ALLOWED_TOKEN_USES = frozenset(
    {
        TOKEN_USE_IDENTITY_ADMIN,
        TOKEN_USE_USER,
    }
)


class InvalidAccessTokenError(Exception):
    """The access token is invalid or expired."""


def _signing_key() -> str:
    secret = settings.AUTH_TOKEN_SECRET
    if len(secret.encode("utf-8")) < 32:
        raise RuntimeError(
            "AUTH_TOKEN_SECRET must contain at least 32 bytes of random data."
        )
    return secret


def create_access_token(
    *,
    identity_id: UUID,
    credential_id: UUID,
    token_use: str = TOKEN_USE_IDENTITY_ADMIN,
) -> str:
    lifetime_seconds = settings.AUTH_TOKEN_TTL_SECONDS
    if lifetime_seconds <= 0:
        raise RuntimeError("AUTH_TOKEN_TTL_SECONDS must be positive.")

    if token_use not in ALLOWED_TOKEN_USES:
        raise RuntimeError("Unsupported token use.")

    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(identity_id),
        "credential_id": str(credential_id),
        "token_use": token_use,
        "iss": TOKEN_ISSUER,
        "aud": TOKEN_AUDIENCE,
        "iat": now,
        "exp": now + timedelta(seconds=lifetime_seconds),
    }
    return jwt.encode(payload, _signing_key(), algorithm=TOKEN_ALGORITHM)


def decode_access_token(token: str) -> dict[str, object]:
    try:
        claims = jwt.decode(
            token,
            _signing_key(),
            algorithms=[TOKEN_ALGORITHM],
            issuer=TOKEN_ISSUER,
            audience=TOKEN_AUDIENCE,
            options={
                "require": [
                    "sub",
                    "credential_id",
                    "token_use",
                    "iss",
                    "aud",
                    "iat",
                    "exp",
                ],
            },
        )
    except InvalidTokenError as exc:
        raise InvalidAccessTokenError from exc

    if claims.get("token_use") not in ALLOWED_TOKEN_USES:
        raise InvalidAccessTokenError

    return claims
