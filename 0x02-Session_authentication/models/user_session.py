from models.base import Base

class UserSession(Base):
    """
    Model class for UserSession that inherits from Base
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize the UserSession instance
        Args:
            args: List of arguments
            kwargs: Dictionary of keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
