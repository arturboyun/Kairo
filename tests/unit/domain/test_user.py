from faker import Faker
import pytest

from kairo.domain.entities.user import User
from kairo.domain.exceptions import UserValidationError


def test_user_creation(faker: Faker):
    email = faker.email()
    username = faker.user_name()
    password = faker.password()
    user = User(username=username, email=email, password=password)

    assert user.id is not None
    assert user.username == username
    assert user.email == email
    assert user.password == password


def test_user_creation_with_invalid_email(faker: Faker):
    email = "invalid_email"
    username = faker.user_name()
    password = faker.password()

    with pytest.raises(UserValidationError):
        user = User(username=username, email=email, password=password)


def test_user_creation_with_too_short_password(faker: Faker):
    email = faker.email()
    username = faker.user_name()
    password = "1234"

    with pytest.raises(UserValidationError):
        user = User(username=username, email=email, password=password)


@pytest.mark.parametrize(
    ("email", "username", "password"),
    [
        (None, "testuser", "testpass"),
        ("test@example.com", None, "testpass"),
        ("test@example.com", "testuser", None),
    ],
)
def test_user_creation_with_empty_fields(email, username, password):
    with pytest.raises(UserValidationError):
        user = User(email=email, username=username, password=password)


def test_user_creation_with_empty_id(faker: Faker):
    with pytest.raises(UserValidationError):
        user = User(
            id=None,
            email=faker.email(),
            username=faker.user_name(),
            password=faker.password(),
        )
