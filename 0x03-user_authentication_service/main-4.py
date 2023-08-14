#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth, _hash_password

auth = Auth()  # Create an instance of the Auth class

email = "test@test.com"
password = "SuperHashedPwd"

hashed_password = _hash_password(password)  # Hash the password

user = auth.register_user(email, hashed_password)  # Register the user
print(user.id)
