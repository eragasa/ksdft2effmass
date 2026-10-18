"""Numerical backend exceptions and retained D1 disposition mapping."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

type HigherRankD1DocumentedBackendException = (
    ValueError | FloatingPointError | RuntimeError
)


class HigherRankD1BackendExceptionCode(StrEnum):
    """Stable serialized disposition for documented numerical backend failures."""

    ARITHMETIC_NONFINITE = "backend-arithmetic-nonfinite"
    NONCONVERGENCE = "backend-nonconvergence"
    VALIDATION_FAILED = "backend-validation-failed"


class HigherRankD1AlignmentBackendError(Exception):
    """Carry one alignment backend exception to the case boundary."""

    __slots__ = ("backend_exception",)

    def __init__(
        self, backend_exception: HigherRankD1DocumentedBackendException
    ) -> None:
        if not isinstance(
            backend_exception, (ValueError, FloatingPointError, RuntimeError)
        ):
            raise TypeError("backend_exception has an undocumented type")
        super().__init__("higher-rank D1 alignment backend failure")
        self.backend_exception = backend_exception


class HigherRankD1TransportBackendError(Exception):
    """Carry transport stage context and one backend exception to the case boundary."""

    __slots__ = ("stage", "attempted_link_count", "backend_exception")

    def __init__(
        self,
        stage: Literal["link", "closure"],
        attempted_link_count: int,
        backend_exception: HigherRankD1DocumentedBackendException,
    ) -> None:
        if stage not in ("link", "closure"):
            raise ValueError("stage is invalid")
        if type(attempted_link_count) is not int or attempted_link_count < 0:
            raise ValueError("attempted_link_count must be a nonnegative built-in int")
        if not isinstance(
            backend_exception, (ValueError, FloatingPointError, RuntimeError)
        ):
            raise TypeError("backend_exception has an undocumented type")
        super().__init__("higher-rank D1 transport backend failure")
        self.stage = stage
        self.attempted_link_count = attempted_link_count
        self.backend_exception = backend_exception


class HigherRankD1NumericalExceptionHandler:
    """Translate thrown documented backend exceptions into retained D1 codes."""

    __slots__ = ()

    @staticmethod
    def exception_code(
        error: HigherRankD1AlignmentBackendError | HigherRankD1TransportBackendError,
    ) -> HigherRankD1BackendExceptionCode:
        """Return the stable code without retaining exception text or traceback."""
        backend_exception = error.backend_exception
        if isinstance(backend_exception, FloatingPointError):
            return HigherRankD1BackendExceptionCode.ARITHMETIC_NONFINITE
        if isinstance(backend_exception, RuntimeError):
            return HigherRankD1BackendExceptionCode.NONCONVERGENCE
        return HigherRankD1BackendExceptionCode.VALIDATION_FAILED


__all__ = [
    "HigherRankD1AlignmentBackendError",
    "HigherRankD1BackendExceptionCode",
    "HigherRankD1DocumentedBackendException",
    "HigherRankD1NumericalExceptionHandler",
    "HigherRankD1TransportBackendError",
]
