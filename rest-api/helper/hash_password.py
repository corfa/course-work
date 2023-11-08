import binascii
import hashlib
import os

from helper.exception.password_exception import IncorrectPasswordException


def hash_password(password: str) -> str:
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    password_hash = binascii.hexlify(password_hash)
    return (salt + password_hash).decode('ascii')


def verify_password(password: str, password_hash: str):
    salt = password_hash[:64]
    stored_password_hash = password_hash[64:]
    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('ascii')
    hashed_password = hashlib.pbkdf2_hmac('sha512', password_bytes, salt_bytes, 100000)
    hashed_password = binascii.hexlify(hashed_password).decode('ascii')
    if hashed_password != stored_password_hash:
        raise IncorrectPasswordException()
