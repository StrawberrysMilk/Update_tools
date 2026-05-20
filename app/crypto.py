"""Encryption helpers.

Master password -> PBKDF2-HMAC-SHA256 -> 32-byte key -> AES-256-GCM.

The master password itself is never persisted. Only the PBKDF2 salt and
a small verification ciphertext are stored on disk (see meta.json).
"""
from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PBKDF2_ITERATIONS = 200_000
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32  # AES-256


def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(master_password.encode("utf-8"))


def encrypt(plaintext: str, key: bytes) -> str:
    """Encrypt and return base64(nonce || ciphertext)."""
    if plaintext is None:
        return ""
    aes = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ct = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.b64encode(nonce + ct).decode("ascii")


def decrypt(token: str, key: bytes) -> str:
    """Inverse of encrypt(). Raises if the key is wrong or data is corrupt."""
    if not token:
        return ""
    raw = base64.b64decode(token)
    nonce, ct = raw[:NONCE_SIZE], raw[NONCE_SIZE:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, ct, None).decode("utf-8")
