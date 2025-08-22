from __future__ import annotations

from kairo.application.dto.user import CreateUserDTO, GetUserByIdQuery
from kairo.application.interactors.base import Interactor, Query
from kairo.domain.entities.user import User
from kairo.domain.exceptions import DomainError
from kairo.domain.gateways.user_gateway import UserGateway, UserReader


class GetUserByIdUseCase(Query[GetUserByIdQuery, User | None]):
    """Use case for getting a user by ID."""

    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    def __call__(self, query: GetUserByIdQuery) -> User | None:
        """Execute the query."""
        return self._user_reader.get_by_id(query.user_id)


class CreateUserUseCase(Interactor[CreateUserDTO, User]):
    """Use case for creating a new user."""

    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    def __call__(self, user_dto: CreateUserDTO) -> User:
        """Execute the use case."""
        if self.user_gateway.get_by_email(user_dto.email):
            msg = f"User with email '{user_dto.email}' already exists."
            raise DomainError(msg)

        if self.user_gateway.get_by_username(user_dto.username):
            msg = f"User with username '{user_dto.username}' already exists."
            raise DomainError(msg)

        user = User(
            email=user_dto.email,
            username=user_dto.username,
            password=user_dto.password,
        )

        return self.user_gateway.create(user)
