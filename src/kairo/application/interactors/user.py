from __future__ import annotations

from kairo.application.dto.user import CreateUserDTO, GetUserByIdQuery
from kairo.application.interactors.base import Interactor, Query
from kairo.application.interfaces import DBSession
from kairo.domain.entities.user import User
from kairo.domain.exceptions import DomainError
from kairo.domain.gateways.user_gateway import UserReader, UserWriter


class GetUserByIdUseCase(Query[GetUserByIdQuery, User | None]):
    """Use case for getting a user by ID."""

    def __init__(self, user_reader: UserReader) -> None:
        self.user_reader = user_reader

    async def __call__(self, query: GetUserByIdQuery) -> User | None:
        """Execute the query."""
        return await self.user_reader.get_by_id(query.user_id)


class CreateUserUseCase(Interactor[CreateUserDTO, User]):
    """Use case for creating a new user."""

    def __init__(
        self,
        db_session: DBSession,
        user_writer: UserWriter,
        user_reader: UserReader,
    ):
        self.db_session = db_session
        self.user_writer = user_writer
        self.user_reader = user_reader

    async def __call__(self, user_dto: CreateUserDTO) -> User:
        """Execute the use case."""
        if self.user_reader.get_by_email(user_dto.email):
            msg = f"User with email '{user_dto.email}' already exists."
            raise DomainError(msg)

        if self.user_reader.get_by_username(user_dto.username):
            msg = f"User with username '{user_dto.username}' already exists."
            raise DomainError(msg)

        user = User(
            email=user_dto.email,
            username=user_dto.username,
            password=user_dto.password,
        )

        user = await self.user_writer.save(user)
        await self.db_session.commit()
        return user
