from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from uuid import UUID

    from kairo.domain.entities.user import User


class UserReader(Protocol):
    """UserReader defines the interface for reading user-related data."""

    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by their unique identifier."""

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address."""

    def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by their username."""


class UserWriter(Protocol):
    """UserWriter defines the interface for writing user-related data."""

    def create(self, user: User) -> User:
        """Create a new user."""

    def update(self, user: User) -> User:
        """Update an existing user."""

    def delete(self, user: User) -> None:
        """Delete a user by their unique identifier."""


class UserGateway(UserReader, UserWriter, Protocol):
    """UserGateway defines the interface for user-related operations."""
