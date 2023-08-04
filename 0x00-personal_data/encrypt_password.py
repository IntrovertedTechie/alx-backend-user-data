#!/usr/bin/env python3
import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hash the password using bcrypt and return the hashed password as bytes.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password using bcrypt.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
