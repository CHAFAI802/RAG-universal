import re
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.credentials.models import (
    Credential,
    CredentialOwnerType,
    CredentialType,
)
from app.modules.credentials.security import hash_password


class UsernameAlreadyExistsError(ValueError):
    """Username déjà utilisé lors d'une inscription."""


USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{3,50}$")

MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 128


class CredentialService:
    def __init__(self, session: Session):
        self.session = session

    def create_username_password_credential(
        self,
        *,
        identity_id: uuid.UUID,
        username: str,
        password: str,
        owner_type: CredentialOwnerType = CredentialOwnerType.IDENTITY_ADMIN,
        user_id: uuid.UUID | None = None,
    ) -> Credential:

        if owner_type == CredentialOwnerType.USER and user_id is None:
            raise ValueError(
                "Un credential User doit être associé à un User."
            )

        if owner_type == CredentialOwnerType.IDENTITY_ADMIN and user_id is not None:
            raise ValueError(
                "Un credential administrateur ne peut pas être associé à un User."
            )

        if not isinstance(username, str):
            raise ValueError("Le username doit être une chaîne de caractères.")

        if not USERNAME_PATTERN.fullmatch(username):
            raise ValueError(
                "Le username doit contenir entre 3 et 50 caractères : "
                "lettres non accentuées, chiffres, _, - ou ."
            )

        normalized_username = username.lower()

        if not isinstance(password, str):
            raise ValueError("Le mot de passe doit être une chaîne de caractères.")

        if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
            raise ValueError(
                "Le mot de passe doit contenir entre 12 et 128 caractères."
            )

        existing_credential = self.session.scalar(
            select(Credential).where(
                func.lower(Credential.username) == normalized_username
            )
        )

        if existing_credential is not None:
            raise UsernameAlreadyExistsError("Ce username est déjà utilisé.")

        credential = Credential(
            identity_id=identity_id,
            credential_type=CredentialType.USERNAME_PASSWORD,
            owner_type=owner_type,
            user_id=user_id,
            username=normalized_username,
            password_hash=hash_password(password),
        )

        self.session.add(credential)
        self.session.flush()

        return credential
