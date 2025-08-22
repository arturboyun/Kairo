from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import select

from kairo.domain.entities.user import User
from kairo.domain.gateways.user_gateway import UserReader, UserWriter
from kairo.infrastructure.sqlalchemy.mappers.user_mapper import (
    convert_domain_to_user_model,
    convert_user_model_to_domain,
)
from kairo.infrastructure.sqlalchemy.models.user import UserModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserGateway(UserReader, UserWriter):
    """UserGateway implementation for SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Get a user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id),
        )
        user = result.scalar_one_or_none()
        if not user:
            return None
        return convert_user_model_to_domain(user)

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email),
        )
        user = result.scalar_one_or_none()
        if not user:
            return None
        return convert_user_model_to_domain(user)

    async def get_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username),
        )
        user = result.scalar_one_or_none()
        if not user:
            return None
        return convert_user_model_to_domain(user)

    async def save(self, user: User) -> User:
        """Create a new user."""
        user_model = convert_domain_to_user_model(user)
        self.session.add(user_model)
        await self.session.flush()
        return convert_user_model_to_domain(user_model)

    async def update(self, user: User) -> User:
        """Update an existing user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id),
        )
        user_model = result.scalar_one_or_none()
        if not user_model:
            msg = f"User with id {user.id} does not exist."
            raise ValueError(msg)
        # Update fields from domain entity
        user_model.email = user.email
        user_model.username = user.username
        user_model.password = user.password
        # Flush changes
        await self.session.flush()
        return convert_user_model_to_domain(user_model)

    async def delete(self, user: User) -> None:
        """Delete a user by their unique identifier."""
        user_model = await self.get_by_id(user.id)
        if user_model:
            await self.session.delete(user_model)
            await self.session.flush()
