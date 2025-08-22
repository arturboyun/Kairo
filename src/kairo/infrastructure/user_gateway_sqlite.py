from __future__ import annotations

import sqlite3
from uuid import UUID

from kairo.domain.entities.user import User
from kairo.domain.gateways.user_gateway import UserGateway


class UserGatewaySqlite(UserGateway):
    """UserGateway implementation for SQLite."""

    def __init__(self, db_connection: sqlite3.Connection):
        self.db_connection = db_connection

    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by their unique identifier."""
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password FROM users WHERE id = ?",
            (str(user_id),),
        )
        row = cursor.fetchone()
        if not row:
            return None

        return User(
            id=row[0],
            username=row[1],
            email=row[2],
            password=row[3],
        )

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address."""
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password FROM users WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
        if not row:
            return None

        return User(
            id=row[0],
            username=row[1],
            email=row[2],
            password=row[3],
        )

    def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by their username."""
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if not row:
            return None

        return User(
            id=row[0],
            username=row[1],
            email=row[2],
            password=row[3],
        )

    def create(self, user: User) -> User:
        """Create a new user."""
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)",
            (str(user.id), user.username, user.email, user.password),
        )
        self.db_connection.commit()
        return user

    def update(self, user: User) -> User:
        """Update an existing user."""
        cursor = self.db_connection.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
            (user.username, user.email, user.password, str(user.id)),
        )
        self.db_connection.commit()
        return user

    def delete(self, user: User) -> None:
        """Delete a user by their unique identifier."""
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (str(user.id),))
        self.db_connection.commit()
