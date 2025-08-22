from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class UUIDGenerator(Protocol):
    """UUID generator interface."""

    def __call__(self) -> UUID:
        """Generate a new UUID."""


class DBSession(Protocol):
    """Database session interface."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""

    @abstractmethod
    async def flush(self) -> None:
        """Flush the current transaction."""
