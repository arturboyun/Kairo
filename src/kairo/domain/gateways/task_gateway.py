from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from uuid import UUID

    from kairo.domain.entities.task import Task


class TaskReader(Protocol):
    """TaskReader defines the interface for reading user-related data."""

    def get_by_id(self, task_id: UUID) -> Task | None:
        """Retrieve a task by its unique identifier."""

    def get_by_project_id(self, project_id: UUID) -> list[Task]:
        """Retrieve all tasks belonging to a specific project."""

    def get_by_parent_id(self, parent_id: UUID) -> list[Task]:
        """Retrieve all subtasks of a specific parent task."""


class TaskWriter(Protocol):
    """TaskWriter defines the interface for writing task-related data."""

    def create(self, task: Task) -> Task:
        """Create a new task."""

    def update(self, task: Task) -> Task:
        """Update an existing task."""

    def delete(self, task: Task) -> None:
        """Delete a task by its unique identifier."""


class TaskGateway(TaskReader, TaskWriter, Protocol):
    """TaskGateway defines the interface for task-related operations."""
