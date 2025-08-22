from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from uuid import UUID

    from kairo.domain.entities.project import Project


class ProjectReader(Protocol):
    """ProjectReader defines the interface for reading project-related data."""

    def get_by_id(self, project_id: UUID) -> Project | None:
        """Retrieve a project by its unique identifier."""

    def get_by_user_id(self, user_id: UUID) -> list[Project]:
        """Retrieve all projects owned by a specific user."""


class ProjectWriter(Protocol):
    """ProjectWriter defines the interface for writing project-related data."""

    def create(self, project: Project) -> Project:
        """Create a new project."""

    def update(self, project: Project) -> Project:
        """Update an existing project."""

    def delete(self, project: Project) -> None:
        """Delete a project by its unique identifier."""


class ProjectGateway(ProjectReader, ProjectWriter, Protocol):
    """ProjectGateway defines the interface for project-related operations."""
