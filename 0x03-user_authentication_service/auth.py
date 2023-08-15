#!/usr/bin/env python3
"""
Authentication module.
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Class responsible for managing user  ."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.
        Args:
            email (str): User's email.
            password (str): User's password
            Returns:
            User: Instance of the created user.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the provided password is valid for the user.
         Args:
            email (str): User's email.
            password (str): User's password.        Returns:
            bool: True if the credentials are valid, otherwise False.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return False
        return True

    def create_session(self, email: str) -> str:
        """Creates a session for the user.
         Args:
            email (str): User's email.
             Returns:
            str: The created session ID.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        db.update_user(user.id, session_id=session_id)
        return session_id

    # ... (similar comments for other methods)

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Gets user based on their session id
            Args:
                - session_id: user's session_id
            Return:
                - User if found else None
        """
        if not session_id:
            return None
        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ Destroys user session
        """
        db = self._db
        db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Generates reset password token for valid user
            Args:
                - email: user's email
            Return:
                - reset password token
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update password for user with matching reset token
            Args:
                - reset_toke: user's reset token
                - password: new password
            Return:
                - None
        """
        db = self._db
        try:
            user = db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        db.update_user(user.id, hashed_password=_hash_password(password),
                       reset_token=None)


def _hash_password(password: str) -> bytes:
    """Hashes the provided password.
    Args:
        password (str): User's password.
    Returns:
        bytes: Hashed password.
    """
    e_pwd = password.encode()
    return bcrypt.hashpw(e_pwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a unique UUID.
    Returns:
        str: Generated UUID.
    """
    return str(uuid4())
