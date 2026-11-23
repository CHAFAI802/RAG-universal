from argon2 import extract_parameters
from argon2.exceptions import InvalidHashError

from app.modules.credentials.security import (
    hash_password,
    verify_password,
)


def test_hash_password_returns_argon2id_hash():
    password = "MotDePasseTest-2026!"

    password_hash = hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2id$")
    assert extract_parameters(password_hash).type.name == "ID"


def test_hash_password_generates_different_hashes():
    password = "MotDePasseTest-2026!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash


def test_verify_password_accepts_correct_password():
    password = "MotDePasseTest-2026!"
    password_hash = hash_password(password)

    assert verify_password(password, password_hash) is True


def test_verify_password_rejects_incorrect_password():
    password_hash = hash_password("MotDePasseTest-2026!")

    assert verify_password("MauvaisMotDePasse", password_hash) is False


def test_verify_password_rejects_invalid_hash():
    assert verify_password(
        "MotDePasseTest-2026!",
        "hash_invalide",
    ) is False


def test_verify_password_rejects_non_string_password():
    password_hash = hash_password("MotDePasseTest-2026!")

    assert verify_password(None, password_hash) is False


def test_verify_password_rejects_non_string_hash():
    assert verify_password("MotDePasseTest-2026!", None) is False


def test_hash_password_rejects_non_string_password():
    try:
        hash_password(None)
    except TypeError:
        pass
    else:
        raise AssertionError("Un TypeError était attendu.")
