#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt

# ... (Other code from the auth module)

def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        bytes: Salted hash of the input password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# ... (Other code from the auth module)

if __name__ == "__main__":
    hashed_password = _hash_password("Hello Holberton")
    print(hashed_password.decode("utf-8"))
