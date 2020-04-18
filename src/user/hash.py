"""Hash utils."""

import binascii
import hashlib
import os

ASCII = 'ascii'
ITERATIONS_NUM = 100000
BYTE_BORDER = 64


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode(ASCII)
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        password.encode('utf-8'),
        salt,
        ITERATIONS_NUM,
    )
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode(ASCII)


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    salt = stored_password[:BYTE_BORDER]
    stored_password = stored_password[BYTE_BORDER:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode(ASCII),
        ITERATIONS_NUM,
    )
    pwdhash = binascii.hexlify(pwdhash)
    return pwdhash.decode(ASCII) == stored_password
