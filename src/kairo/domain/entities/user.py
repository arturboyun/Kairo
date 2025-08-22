import re
from dataclasses import dataclass, field
from uuid import UUID

from uuid_extensions import uuid7

from kairo.domain.exceptions import UserValidationError

PASSWORD_LENGTH = 8


@dataclass(slots=True, kw_only=True)
class User:
    """Represents a user entity.

    Attributes
    ----------
        id (UUID): Unique identifier for the user, generated using uuid7.
        username (str): Username of the user.
        email (str): Email address of the user.
        password (str): Password of the user.

    """

    id: UUID = field(default_factory=lambda: uuid7())

    username: str
    email: str
    password: str

    def __post_init__(self) -> None:
        if not self.id:
            msg = "User ID cannot be empty."
            raise UserValidationError(msg)
        if not self.username:
            msg = "Username cannot be empty."
            raise UserValidationError(msg)
        if not self.email:
            msg = "Email cannot be empty."
            raise UserValidationError(msg)
        if not self.password:
            msg = "Password cannot be empty."
            raise UserValidationError(msg)
        if not is_valid_email_regex(self.email):
            msg = "Invalid email format."
            raise UserValidationError(msg)
        if len(self.password) < PASSWORD_LENGTH:
            msg = f"Password must be at least {PASSWORD_LENGTH} characters long."
            raise UserValidationError(msg)


def is_valid_email_regex(email: str) -> bool:
    """Validate email address format using a regular expression."""
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, email))
