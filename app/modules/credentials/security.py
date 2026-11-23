from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)


_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    if not isinstance(password, str):
        raise TypeError("Le mot de passe doit être une chaîne de caractères.")

    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    if not isinstance(password, str):
        return False

    if not isinstance(password_hash, str):
        return False

    try:
        return _password_hasher.verify(password_hash, password)

    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False
