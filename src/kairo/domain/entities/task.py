from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from uuid_extensions import uuid7

from kairo.domain.exceptions import (
    DomainError,
    TaskValidationError,
)

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(slots=True, kw_only=True)
class Task:
    """Represents a task in the system.

    Attributes
    ----------
        id (UUID): Unique identifier for the task, generated using uuid7.
        name (str): Name of the task.
        description (str): Description of the task.
        parent_id (UUID | None): Identifier of the parent task, if any.
        subtasks (list[Task]): List of subtasks associated with this task.

    """

    id: UUID = field(default_factory=lambda: uuid7())
    name: str
    description: str
    parent_id: UUID | None = field(default=None)

    subtasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            msg = "Task name cannot be empty."
            raise TaskValidationError(msg)

        if not self.description:
            msg = "Task description cannot be empty."
            raise TaskValidationError(msg)

    def add_subtask(self, subtask: Task) -> None:
        """Add a subtask to the task.

        :param subtask: The subtask to add.
        :raises DomainError: If the subtask's parent_id does not match the task's id,
            or if a subtask with the same id already exists in this task.
        """
        if subtask.parent_id is not None and subtask.parent_id != self.id:
            msg = "Subtask's parent_id must match the task's id."
            raise TaskValidationError(msg)

        if subtask.id in [s.id for s in self.subtasks]:
            msg = "Subtask with the same id already exists in this task."
            raise TaskValidationError(msg)

        if subtask.parent_id is None:
            subtask.parent_id = self.id

        self.subtasks.append(subtask)

    def remove_subtask(self, subtask_id: UUID) -> None:
        """Remove a subtask from the task.

        :param subtask_id: The id of the subtask to remove.
        :raises DomainException: If the subtask with the given id
            does not exist in this task.
        """
        for subtask in self.subtasks:
            if subtask.id == subtask_id:
                self.subtasks.remove(subtask)
                return

        msg = "Subtask with the given id does not exist in this task."
        raise DomainError(msg)
