from faker import Faker
import pytest

from kairo.domain.entities.project import Project
from kairo.domain.entities.user import User
from kairo.domain.exceptions import ProjectValidationError


def test_project_creation(faker: Faker) -> None:
    user = User(username=faker.user_name(), email=faker.email(), password="password123")
    project = Project(name="Test Project", description="A test project", owner=user)

    assert project.id is not None
    assert project.name == "Test Project"
    assert project.description == "A test project"
    assert project.owner == user
    assert project.tasks == []


def test_project_creation_with_empty_fields(faker: Faker) -> None:
    user = User(username=faker.user_name(), email=faker.email(), password="password123")

    with pytest.raises(ProjectValidationError) as e:
        Project(name="", description="A test project", owner=user)

    with pytest.raises(ProjectValidationError) as e:
        Project(name="Test Project", description="", owner=user)

    with pytest.raises(ProjectValidationError) as e:
        Project(name="Test Project", description="A test project", owner=None)
