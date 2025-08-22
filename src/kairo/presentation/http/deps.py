import sqlite3
from sqlite3 import Connection
from typing import Annotated

from fastapi import Depends

from kairo.application.interactors.user import CreateUserUseCase, GetUserByIdUseCase
from kairo.domain.gateways.user_gateway import UserGateway
from kairo.infrastructure.user_gateway_sqlite import UserGatewaySqlite


def init_db() -> None:
    """Initialize the database."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """,
    )
    conn.commit()
    conn.close()


def get_sqlite3_connection() -> Connection:
    """Get a SQLite3 database connection."""
    conn = sqlite3.connect("database.db")
    init_db()
    return conn


def get_user_gateway(
    connection: Annotated[Connection, Depends(get_sqlite3_connection)],
) -> UserGateway:
    """Get the user gateway."""
    return UserGatewaySqlite(connection)


def get_user_create_use_case(
    user_gateway: Annotated[UserGateway, Depends(get_user_gateway)],
) -> CreateUserUseCase:
    """Get the user create use case."""
    return CreateUserUseCase(user_gateway)


def get_user_by_id_use_case(
    user_gateway: Annotated[UserGateway, Depends(get_user_gateway)],
) -> GetUserByIdUseCase:
    """Get the user by ID use case."""
    return GetUserByIdUseCase(user_gateway)
