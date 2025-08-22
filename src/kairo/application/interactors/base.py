from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class Interactor(Generic[TInput, TOutput], ABC):
    """Base class for all interactors."""

    @abstractmethod
    def __call__(self, input_data: TInput) -> TOutput:
        """Execute the interactor."""


class Command(Generic[TInput], ABC):
    """Base class for commands (operations without return values)."""

    @abstractmethod
    def __call__(self, input_data: TInput) -> None:
        """Execute the command."""


class Query(Generic[TInput, TOutput], ABC):
    """Base class for queries (read-only operations)."""

    @abstractmethod
    def __call__(self, input_data: TInput) -> TOutput:
        """Execute the query."""
