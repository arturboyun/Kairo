class DomainError(Exception):
    """Base class for all domain exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"


class DomainValidationError(DomainError):
    """Exception raised for validation errors in the domain."""


class UserValidationError(DomainValidationError):
    """Exception raised for validation errors related to users."""


class ProjectValidationError(DomainValidationError):
    """Exception raised for validation errors related to projects."""


class TaskValidationError(DomainValidationError):
    """Exception raised for validation errors related to tasks."""
