from dataclasses import dataclass, field
from typing import Self
from uuid import UUID

from uuid_extensions import uuid7

from kairo.domain.entities.task import Task
from kairo.domain.entities.user import User
from kairo.domain.exceptions import ProjectValidationError


@dataclass(slots=True, kw_only=True)
class Project:
    """Represents a project entity.

    Attributes
    ----------
        id (UUID): Unique identifier for the project, generated using uuid7.
        name (str): Name of the project.
        description (str): Description of the project.
        owner (User): Owner of the project, represented by a User instance.

    Raises
    ------
        ProjectValidationError: If any of the required fields are
                                   empty or if owner is not a User instance.

    """

    id: UUID = field(default_factory=lambda: uuid7())
    name: str
    description: str
    owner: User
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self: Self) -> None:
        if not self.id:
            msg = "Project ID cannot be empty."
            raise ProjectValidationError(msg)
        if not self.name:
            msg = "Project name cannot be empty."
            raise ProjectValidationError(msg)
        if not self.description:
            msg = "Project description cannot be empty."
            raise ProjectValidationError(msg)
        if not self.owner:
            msg = "Owner cannot be empty."
            raise ProjectValidationError(msg)

    def transfer_ownership(self: Self, new_owner: User) -> None:
        """Transfers ownership of the project to a new user.

        :param new_owner: New owner of the project.
        :raises ProjectValidationError: If new_owner is not a User instance.
        """
        self.owner = new_owner

    def add_task(self: Self, task: Task) -> None:
        """Add a task to the project.

        :param task: The task to add.
        :raises DomainValidationException: If the task is not an instance of Task.
        """
        self.tasks.append(task)

    def remove_task(self: Self, task_id: str) -> None:
        """Remove a task from the project by its ID.

        :param task_id: ID of the task to remove.
        :raises DomainValidationException: If the task with the given
          ID does not exist in the project.
        """
        task_to_remove = next((task for task in self.tasks if task.id == task_id), None)
        if not task_to_remove:
            msg = f"Task with ID {task_id} does not exist in the project."
            raise ProjectValidationError(
                msg,
            )
        self.tasks.remove(task_to_remove)
