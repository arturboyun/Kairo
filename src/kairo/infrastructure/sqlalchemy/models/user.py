import uuid

from sqlalchemy import UUID, text
from sqlalchemy.orm import Mapped, mapped_column

from kairo.infrastructure.sqlalchemy.base import Base, DateTimeMixin


class UserModel(Base, DateTimeMixin):
    """User model."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuidv7()"),
    )
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
