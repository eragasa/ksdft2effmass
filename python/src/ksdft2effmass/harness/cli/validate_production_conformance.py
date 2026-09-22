"""Bounded CLI adapter for explicit production-source conformance ratcheting.

The command reads only named configuration, baseline, and source files with exact
caller-supplied SHA-256 and byte-count identities. It emits one bounded deterministic
JSON report, performs no discovery or repair, and treats inherited findings as visible
history rather than approval or waiver state.
"""

from __future__ import annotations

import hashlib
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ksdft2effmass.harness.pi.conformance.python.production import (
    PythonProductionSource,
)
from ksdft2effmass.harness.pi.conformance.python.ratchet import (
    PythonJsonStringSerializer,
    PythonProductionConformanceConfigurationSerializer,
    PythonProductionContentIdentity,
    PythonProductionInheritedBaselineSerializer,
    PythonProductionRatchetReportSerializer,
    PythonProductionRatchetRequest,
    PythonProductionRatchetWorkflow,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionCommandSource:
    """Represent one explicit CLI source path and expected content identity."""

    input_identity: str
    diagnostic_path: PurePosixPath
    filesystem_path: Path
    content_identity: PythonProductionContentIdentity

    def __post_init__(self) -> None:
        """Require exact closed source-reference fields."""
        if type(self.input_identity) is not str or not self.input_identity:
            raise ValueError("input_identity must be nonempty built-in text")
        if type(self.diagnostic_path) is not PurePosixPath:
            raise TypeError("diagnostic_path must be PurePosixPath")
        if not isinstance(self.filesystem_path, Path):
            raise TypeError("filesystem_path must be a pathlib Path")
        if type(self.content_identity) is not PythonProductionContentIdentity:
            raise TypeError("content_identity must be PythonProductionContentIdentity")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionConformanceCommandRequest:
    """Represent fully parsed exact CLI inputs before file reads."""

    configuration_path: Path
    configuration_identity: PythonProductionContentIdentity
    baseline_path: Path
    baseline_identity: PythonProductionContentIdentity
    sources: tuple[PythonProductionCommandSource, ...]
    report_limit: int

    def __post_init__(self) -> None:
        """Require exact paths, identities, source tuple, and output bound."""
        if not isinstance(self.configuration_path, Path):
            raise TypeError("configuration_path must be a pathlib Path")
        if type(self.configuration_identity) is not PythonProductionContentIdentity:
            raise TypeError(
                "configuration_identity must be PythonProductionContentIdentity"
            )
        if not isinstance(self.baseline_path, Path):
            raise TypeError("baseline_path must be a pathlib Path")
        if type(self.baseline_identity) is not PythonProductionContentIdentity:
            raise TypeError("baseline_identity must be PythonProductionContentIdentity")
        if (
            type(self.sources) is not tuple
            or not self.sources
            or any(
                type(source) is not PythonProductionCommandSource
                for source in self.sources
            )
        ):
            raise TypeError("sources must contain command-source values")
        if type(self.report_limit) is not int:
            raise TypeError("report_limit must be a built-in int")
        if (
            not 0
            <= self.report_limit
            <= PythonProductionRatchetReportSerializer.MAX_FINDINGS
        ):
            raise ValueError("report_limit must be between 0 and 100")


class PythonProductionConformanceCommand:
    """Parse, load, validate, execute, and report one explicit bounded CLI request."""

    __slots__ = ()
    USAGE = (
        "validate-production-conformance "
        "--configuration PATH SHA256 BYTE_COUNT "
        "--baseline PATH SHA256 BYTE_COUNT "
        "--source INPUT_ID DIAGNOSTIC_PATH FILE_PATH SHA256 BYTE_COUNT "
        "[--source ...] [--limit 0..100]"
    )

    def execute(self, arguments: tuple[str, ...]) -> int:
        """Execute exact command arguments and map represented outcomes to status."""
        try:
            request = self._parse(arguments)
            configuration_bytes = self._read_exact(
                request.configuration_path, request.configuration_identity
            )
            baseline_bytes = self._read_exact(
                request.baseline_path, request.baseline_identity
            )
            configuration = (
                PythonProductionConformanceConfigurationSerializer().execute(
                    configuration_bytes, request.configuration_identity
                )
            )
            baseline = PythonProductionInheritedBaselineSerializer().execute(
                baseline_bytes, request.baseline_identity
            )
            sources = tuple(
                PythonProductionSource.from_payload(
                    input_identity=source.input_identity,
                    path=source.diagnostic_path,
                    payload=self._read_exact(
                        source.filesystem_path, source.content_identity
                    ),
                )
                for source in request.sources
            )
            result = PythonProductionRatchetWorkflow().execute(
                PythonProductionRatchetRequest(
                    configuration=configuration,
                    baseline=baseline,
                    sources=sources,
                )
            )
            print(
                PythonProductionRatchetReportSerializer().execute(
                    result, request.report_limit
                )
            )
            return 0 if result.passed else 1
        except (OSError, TypeError, ValueError) as error:
            print(self._error_json(str(error)))
            return 2

    def _parse(
        self, arguments: tuple[str, ...]
    ) -> PythonProductionConformanceCommandRequest:
        """Parse the closed option grammar without ambient defaults or discovery."""
        if type(arguments) is not tuple or any(
            type(argument) is not str for argument in arguments
        ):
            raise TypeError("arguments must be a tuple of built-in str values")
        configuration_path: Path | None = None
        configuration_identity: PythonProductionContentIdentity | None = None
        baseline_path: Path | None = None
        baseline_identity: PythonProductionContentIdentity | None = None
        sources: list[PythonProductionCommandSource] = []
        report_limit = 20
        report_limit_seen = False
        index = 0
        while index < len(arguments):
            option = arguments[index]
            if option == "--configuration":
                values = self._slice(arguments, index, 3, option)
                if configuration_path is not None:
                    raise ValueError("--configuration may be supplied exactly once")
                configuration_path = Path(values[0])
                configuration_identity = self._identity(values[1], values[2])
                index += 4
            elif option == "--baseline":
                values = self._slice(arguments, index, 3, option)
                if baseline_path is not None:
                    raise ValueError("--baseline may be supplied exactly once")
                baseline_path = Path(values[0])
                baseline_identity = self._identity(values[1], values[2])
                index += 4
            elif option == "--source":
                values = self._slice(arguments, index, 5, option)
                sources.append(
                    PythonProductionCommandSource(
                        input_identity=values[0],
                        diagnostic_path=PurePosixPath(values[1]),
                        filesystem_path=Path(values[2]),
                        content_identity=self._identity(values[3], values[4]),
                    )
                )
                index += 6
            elif option == "--limit":
                values = self._slice(arguments, index, 1, option)
                if report_limit_seen:
                    raise ValueError("--limit may be supplied at most once")
                report_limit_seen = True
                report_limit = self._count(values[0], "report limit")
                if report_limit > PythonProductionRatchetReportSerializer.MAX_FINDINGS:
                    raise ValueError("report limit must be between 0 and 100")
                index += 2
            elif option in {"-h", "--help"}:
                raise ValueError(self.USAGE)
            else:
                raise ValueError(f"unknown or misplaced argument: {option}")
        if configuration_path is None or configuration_identity is None:
            raise ValueError("one explicit --configuration is required")
        if baseline_path is None or baseline_identity is None:
            raise ValueError("one explicit --baseline is required")
        if not sources:
            raise ValueError("at least one explicit --source is required")
        source_identities = tuple(source.input_identity for source in sources)
        if len(set(source_identities)) != len(source_identities):
            raise ValueError("explicit source input identities must be unique")
        return PythonProductionConformanceCommandRequest(
            configuration_path=configuration_path,
            configuration_identity=configuration_identity,
            baseline_path=baseline_path,
            baseline_identity=baseline_identity,
            sources=tuple(sources),
            report_limit=report_limit,
        )

    @staticmethod
    def _slice(
        arguments: tuple[str, ...], index: int, count: int, option: str
    ) -> tuple[str, ...]:
        """Return the exact fixed number of values following one option."""
        end = index + 1 + count
        values = arguments[index + 1 : end]
        if len(values) != count or any(value.startswith("--") for value in values):
            raise ValueError(f"{option} requires exactly {count} values")
        return values

    @classmethod
    def _identity(cls, sha256: str, byte_count: str) -> PythonProductionContentIdentity:
        """Construct one exact CLI content identity without scalar coercion."""
        return PythonProductionContentIdentity(
            sha256=sha256, byte_count=cls._count(byte_count, "byte count")
        )

    @staticmethod
    def _count(value: str, name: str) -> int:
        """Decode one canonical nonnegative decimal integer."""
        if not value.isdecimal() or (len(value) > 1 and value.startswith("0")):
            raise ValueError(f"{name} must be canonical nonnegative decimal text")
        return int(value)

    @staticmethod
    def _read_exact(path: Path, identity: PythonProductionContentIdentity) -> bytes:
        """Read one explicit path and fail closed when its content identity differs."""
        payload = path.read_bytes()
        if len(payload) != identity.byte_count:
            raise ValueError(f"content byte count mismatch: {path}")
        if hashlib.sha256(payload).hexdigest() != identity.sha256:
            raise ValueError(f"content SHA-256 mismatch: {path}")
        return payload

    @staticmethod
    def _error_json(message: str) -> str:
        """Render one bounded deterministic invalid-input report."""
        bounded = PythonJsonStringSerializer().execute(message[:500])
        return f'{{"error":{bounded},"status":"invalid_input"}}'


# Packaging owns this exact command adapter; reusable behavior stays on the command.
def run(argv: Sequence[str] | None = None) -> int:
    """Adapt packaging arguments to :class:`PythonProductionConformanceCommand`."""
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    return PythonProductionConformanceCommand().execute(arguments)
