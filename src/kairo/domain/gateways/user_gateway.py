from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from uuid import UUID

    from kairo.domain.entities.user import User


class UserReader(Protocol):
    """UserReader defines the interface for reading user-related data."""

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by their unique identifier."""

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address."""

    async def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by their username."""


class UserWriter(Protocol):
    """UserWriter defines the interface for writing user-related data."""

    async def save(self, user: User) -> User:
        """Create a new user."""

    async def update(self, user: User) -> User:
        """Update an existing user."""

    async def delete(self, user: User) -> None:
        """Delete a user by their unique identifier."""
