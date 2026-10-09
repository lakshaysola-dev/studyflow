import uuid

from cryptography.fernet import Fernet

from app.core.security import (
    CredentialCipher,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_roundtrip():
    hashed = hash_password("correct horse battery staple")
    assert hashed != "correct horse battery staple"
    assert verify_password("correct horse battery staple", hashed)
    assert not verify_password("wrong", hashed)


def test_access_token_roundtrip():
    user_id = uuid.uuid4()
    token = create_access_token(user_id)
    assert decode_access_token(token) == str(user_id)
    assert decode_access_token(token + "x") is None


def test_credential_cipher_roundtrip():
    cipher = CredentialCipher(Fernet.generate_key().decode())
    secret = '{"username": "2024ABC", "password": "hunter2"}'
    encrypted = cipher.encrypt(secret)
    assert encrypted != secret
    assert cipher.decrypt(encrypted) == secret


def test_credential_cipher_disabled_without_key():
    assert not CredentialCipher("").enabled
