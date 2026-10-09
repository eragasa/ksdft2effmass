"""Thin structural and functional bases for provisional workflow v2."""

from __future__ import annotations

from abc import ABC, abstractmethod

__all__: tuple[str, ...] = (
    "DataObject",
    "DataObjectActionRequest",
    "DataObjectActionResult",
    "DataObjectActionizer",
    "DataObjectModel",
)


class DataObject(ABC):
    """Define the struct-like boundary for represented domain state."""

    __slots__ = ()

    @abstractmethod
    def __init__(self) -> None:
        """Initialize one complete represented value."""


class DataObjectModel(DataObject, ABC):
    """Identify an immutable data-object implementation."""

    __slots__ = ()


class DataObjectActionRequest(DataObjectModel, ABC):
    """Identify the immutable input to one data-object action."""

    __slots__ = ()


class DataObjectActionResult(DataObjectModel, ABC):
    """Identify the immutable result of one data-object action."""

    __slots__ = ()


class DataObjectActionizer[
    RequestT: DataObjectActionRequest,
    ResultT: DataObjectActionResult,
](ABC):
    """Define the function-like boundary for one data-object action."""

    __slots__ = ()

    @abstractmethod
    def action(self, *, request: RequestT) -> ResultT:
        """Return the result produced from one complete request."""
