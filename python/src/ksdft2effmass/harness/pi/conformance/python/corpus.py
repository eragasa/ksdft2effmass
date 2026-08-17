"""Private immutable Python evidence corpus construction."""

from __future__ import annotations

from dataclasses import dataclass

from .model import (
    PythonTestModuleModel,
    _PythonTestModuleCorpus,
    _PythonTestModuleParseFailure,
)
from .parser import parse_module


@dataclass(frozen=True, slots=True)
class _PythonTestModuleInput:
    """One immutable source snapshot selected for corpus construction."""

    path: str
    payload: bytes


class _PythonTestModuleCorpusBuilder:
    """Build exactly one immutable corpus with one parse per source snapshot."""

    __slots__ = ()

    def execute(
        self,
        sources: tuple[_PythonTestModuleInput, ...],
        *,
        prebuilt: _PythonTestModuleCorpus | None = None,
    ) -> _PythonTestModuleCorpus:
        """Build or verify and reuse one caller-supplied private corpus."""
        snapshots = tuple(sources)
        if prebuilt is not None:
            represented = tuple(
                (model.path, model.source_bytes) for model in prebuilt.models
            )
            failure_paths = tuple(failure.path for failure in prebuilt.failures)
            expected_paths = tuple(source.path for source in snapshots)
            if (
                represented
                != tuple(
                    (source.path, source.payload)
                    for source in snapshots
                    if source.path not in failure_paths
                )
                or tuple(path for path in expected_paths if path in failure_paths)
                != failure_paths
            ):
                raise ValueError("prebuilt corpus must exactly cover source snapshots")
            return prebuilt
        models: list[PythonTestModuleModel] = []
        failures: list[_PythonTestModuleParseFailure] = []
        for source in snapshots:
            try:
                models.append(parse_module(source.path, source.payload))
            except (UnicodeError, SyntaxError) as exc:
                failures.append(_PythonTestModuleParseFailure(source.path, str(exc)))
        return _PythonTestModuleCorpus(tuple(models), tuple(failures))
