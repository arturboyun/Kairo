from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class CreateUserDTO:
    """Data transfer object for creating a new user."""

    email: str
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class GetUserByIdQuery:
    """Query for getting a user by ID."""

    user_id: UUID
