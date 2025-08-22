from uuid import UUID
from faker import Faker
import pytest

from kairo.domain.entities.task import Task
from kairo.domain.exceptions import DomainError, TaskValidationError


def test_task_creation() -> None:
    task = Task(name="Test Task", description="This is a test task.")

    assert isinstance(task.id, UUID)
    assert task.name == "Test Task"
    assert task.description == "This is a test task."
    assert task.parent_id is None
    assert task.subtasks == []


@pytest.mark.parametrize(
    ("name", "description"),
    [
        ("", "This is a test task."),
        ("Test Task", ""),
    ],
)
def test_task_creation_with_empty_fields(name, description) -> None:
    with pytest.raises(TaskValidationError):
        task = Task(name=name, description=description)


def test_add_subtask() -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    subtask = Task(name="Subtask", description="This is a subtask.")

    parent_task.add_subtask(subtask)

    assert len(parent_task.subtasks) == 1
    assert parent_task.subtasks[0].name == "Subtask"
    assert parent_task.subtasks[0].parent_id == parent_task.id


def test_remove_subtask() -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    subtask = Task(name="Subtask", description="This is a subtask.")

    parent_task.add_subtask(subtask)
    assert len(parent_task.subtasks) == 1

    parent_task.remove_subtask(subtask.id)

    assert len(parent_task.subtasks) == 0


def test_if_subtask_with_given_id_does_not_exist(faker: Faker) -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    some_subtask = Task(
        name="Subtask",
        description="This is a subtask.",
        parent_id=parent_task.id,
    )
    with pytest.raises(DomainError):
        parent_task.remove_subtask(some_subtask.id)


def test_add_subtask_with_parent_id() -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    subtask = Task(
        name="Subtask",
        description="This is a subtask.",
    )

    parent_task.add_subtask(subtask)

    assert len(parent_task.subtasks) == 1
    assert parent_task.subtasks[0].name == "Subtask"
    assert parent_task.subtasks[0].parent_id == parent_task.id


def test_add_subtask_with_parent_id() -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    subtask = Task(
        name="Subtask",
        description="This is a subtask.",
    )

    parent_task.add_subtask(subtask)

    assert len(parent_task.subtasks) == 1
    assert parent_task.subtasks[0].name == "Subtask"
    assert parent_task.subtasks[0].parent_id == parent_task.id


def test_add_subtask_with_parent_id() -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    subtask = Task(
        name="Subtask",
        description="This is a subtask.",
    )

    parent_task.add_subtask(subtask)

    assert len(parent_task.subtasks) == 1
    assert parent_task.subtasks[0].name == "Subtask"
    assert parent_task.subtasks[0].parent_id == parent_task.id


def test_if_parent_id_must_match_the_task_id(faker: Faker) -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    subtask = Task(
        name="Subtask",
        description="This is a subtask.",
        parent_id=faker.uuid4(),
    )

    with pytest.raises(TaskValidationError):
        parent_task.add_subtask(subtask)


def test_if_subtask_already_exists(faker: Faker) -> None:
    parent_task = Task(name="Parent Task", description="This is a parent task.")
    subtask = Task(
        name="Subtask",
        description="This is a subtask.",
        parent_id=parent_task.id,
    )

    parent_task.add_subtask(subtask)

    with pytest.raises(TaskValidationError):
        parent_task.add_subtask(subtask)
