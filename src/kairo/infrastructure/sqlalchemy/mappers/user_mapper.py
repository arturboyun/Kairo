"""User mapper for converting between User entity and UserModel."""

from __future__ import annotations

from adaptix.conversion import get_converter

from kairo.domain.entities.user import User
from kairo.infrastructure.sqlalchemy.models.user import UserModel

convert_user_model_to_domain = get_converter(UserModel, User)
convert_domain_to_user_model = get_converter(User, UserModel)
