"""Explicit-input structural validation of Python test evidence.

The module represents caller-supplied source and JSON bytes; it never reads a
filesystem or discovers a repository, root, current directory, Git checkout, or
process state.  :class:`PythonConformanceValidator` checks the maintained static
syntax, documentation, ownership, evidence-identifier, parameter-inventory, and
optional migration-map conventions inherited from the compatibility command.
Its findings are deterministic software-verification diagnostics for the
supplied representation.  A passing result does not establish oracle
independence, mathematical correctness, test cohesion, tolerance adequacy,
scientific validity, uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...identity import _require_builtin_str, _require_tuple
from .corpus import _PythonTestModuleCorpusBuilder, _PythonTestModuleInput
from .documentation import _PythonDocumentationRule
from .evidence import _PythonEvidenceIdentifierRule
from .migration import _PythonEvidencePredecessorRule
from .model import PythonTestModuleModel, _PythonTestModuleCorpus
from .naming import _PythonNamingRule
from .ownership import _PythonOwnershipInputLoader, _PythonOwnershipRule
from .parameterization import (
    _PythonParameterizationRule,
    _PythonParameterizationRuleResult,
)
from .profile import (
    EvidenceProfileMatrix,
    _EvidenceProfileCombinationRule,
    _EvidenceProfileMatrixLoader,
)
from .repository import (
    _PythonRepositoryConformanceRule,
    _PythonRepositoryConformanceRuleResult,
    _PythonRepositoryUniquenessRule,
)

EVIDENCE_OPENINGS = frozenset(
    {
        "software_verification",
        "numerical_verification",
        "scientific_validation",
        "uncertainty_quantification",
    }
)


@dataclass(frozen=True, slots=True)
class PythonModuleSource:
    """One explicitly supplied module and its caller-observed read outcome.

    Attributes
    ----------
    path
        Caller-supplied diagnostic path.  Absolute paths are accepted because
        the generic validator assigns no repository-root meaning to the value.
    payload
        Exact module bytes, or ``None`` when the caller could not supply bytes.
    is_regular_file
        Whether the caller observed a regular, nonsymlink file.  Generic code
        trusts this explicit observation and performs no filesystem query.
    read_error
        Caller-rendered read failure, or ``None``.  A regular source has exactly
        one of ``payload`` and ``read_error``; a nonregular source has neither.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a string is empty or the represented read outcome is contradictory.
    """

    path: str
    payload: bytes | None
    is_regular_file: bool = True
    read_error: str | None = None

    def __post_init__(self) -> None:
        _require_builtin_str(self.path, "path")
        if type(self.is_regular_file) is not bool:
            raise TypeError("is_regular_file must be a bool")
        if self.payload is not None and type(self.payload) is not bytes:
            raise TypeError("payload must be bytes or None")
        if self.read_error is not None:
            _require_builtin_str(self.read_error, "read_error")
        if not self.is_regular_file and (self.payload is not None or self.read_error):
            raise ValueError(
                "a non-regular source cannot contain payload or read_error"
            )
        if self.is_regular_file and (self.payload is None) == (self.read_error is None):
            raise ValueError(
                "a regular source requires exactly one payload or read_error"
            )


@dataclass(frozen=True, slots=True)
class PythonConformanceRequest:
    """Closed explicit inputs for one test-evidence validation.

    Attributes
    ----------
    sources
        Nonempty tuple of explicitly supplied module inputs, in command order.
        Duplicate paths remain representable and produce a validation finding.
    ownership_path
        Diagnostic path for the ownership input.
    ownership_payload
        Exact ownership JSON bytes, or ``None`` after a caller read failure.
    ownership_read_error
        Caller-rendered ownership read failure, or ``None`` when bytes exist.
    migration_path
        Diagnostic path for an optional migration map.
    migration_payload
        Exact optional migration-map JSON bytes.
    migration_read_error
        Caller-rendered optional migration-map read failure.
    profile_path
        Diagnostic path for the optional generic evidence-profile matrix.
    profile_payload
        Exact optional profile-matrix JSON bytes.
    profile_read_error
        Caller-rendered optional profile-matrix read failure.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If required input is absent or a payload/read-error state conflicts.
    """

    sources: tuple[PythonModuleSource, ...]
    ownership_path: str
    ownership_payload: bytes | None
    ownership_read_error: str | None = None
    migration_path: str | None = None
    migration_payload: bytes | None = None
    migration_read_error: str | None = None
    profile_path: str | None = None
    profile_payload: bytes | None = None
    profile_read_error: str | None = None
    _parsed_models: tuple[PythonTestModuleModel, ...] = ()

    def __post_init__(self) -> None:
        _require_tuple(self.sources, "sources")
        if not self.sources:
            raise ValueError("sources must be nonempty")
        if any(type(source) is not PythonModuleSource for source in self.sources):
            raise TypeError("sources must contain PythonModuleSource values")
        _require_builtin_str(self.ownership_path, "ownership_path")
        if (
            self.ownership_payload is not None
            and type(self.ownership_payload) is not bytes
        ):
            raise TypeError("ownership_payload must be bytes or None")
        if self.ownership_read_error is not None:
            _require_builtin_str(self.ownership_read_error, "ownership_read_error")
        if (self.ownership_payload is None) == (self.ownership_read_error is None):
            raise ValueError("ownership requires exactly one payload or read error")
        if self.migration_path is None:
            if (
                self.migration_payload is not None
                or self.migration_read_error is not None
            ):
                raise ValueError("migration data requires migration_path")
        else:
            _require_builtin_str(self.migration_path, "migration_path")
            if (
                self.migration_payload is not None
                and type(self.migration_payload) is not bytes
            ):
                raise TypeError("migration_payload must be bytes or None")
            if self.migration_read_error is not None:
                _require_builtin_str(self.migration_read_error, "migration_read_error")
            if (self.migration_payload is None) == (self.migration_read_error is None):
                raise ValueError("migration requires exactly one payload or read error")
        _require_tuple(self._parsed_models, "_parsed_models")
        if any(
            type(model) is not PythonTestModuleModel for model in self._parsed_models
        ):
            raise TypeError("_parsed_models must contain PythonTestModuleModel values")
        if self._parsed_models and (
            tuple(model.path for model in self._parsed_models)
            != tuple(source.path for source in self.sources)
            or any(
                model.source_bytes != source.payload
                for model, source in zip(self._parsed_models, self.sources, strict=True)
            )
        ):
            raise ValueError(
                "_parsed_models must exactly cover source paths and bytes in request order"  # noqa: E501
            )
        if self.profile_path is None:
            if self.profile_payload is not None or self.profile_read_error is not None:
                raise ValueError("profile data requires profile_path")
        else:
            _require_builtin_str(self.profile_path, "profile_path")
            if (
                self.profile_payload is not None
                and type(self.profile_payload) is not bytes
            ):
                raise TypeError("profile_payload must be bytes or None")
            if self.profile_read_error is not None:
                _require_builtin_str(self.profile_read_error, "profile_read_error")
            if (self.profile_payload is None) == (self.profile_read_error is None):
                raise ValueError("profile requires exactly one payload or read error")


@dataclass(frozen=True, slots=True)
class PythonConformanceFinding:
    """One expected-invalidity finding for supplied evidence.

    Attributes
    ----------
    code
        Stable compatibility diagnostic code in the ``TE.`` namespace.
    path
        Caller-supplied diagnostic path associated with the finding.
    message
        Deterministic human-readable diagnostic detail.
    severity
        Compatibility severity, currently fixed to ``"error"``.
    line
        Optional one-based source line.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a value violates its intrinsic lexical or range invariant.
    """

    code: str
    path: str
    message: str
    severity: str = "error"
    line: int | None = None

    def __post_init__(self) -> None:
        _require_builtin_str(self.code, "code")
        if not self.code.startswith("TE."):
            raise ValueError("code must use the TE namespace")
        _require_builtin_str(self.path, "path")
        _require_builtin_str(self.message, "message")
        _require_builtin_str(self.severity, "severity")
        if self.severity != "error":
            raise ValueError("severity must equal 'error'")
        if self.line is not None:
            if type(self.line) is not int:
                raise TypeError("line must be an int excluding bool or None")
            if self.line < 1:
                raise ValueError("line must be positive")


def _finding(
    code: str, path: str, message: str, line: int | None = None
) -> PythonConformanceFinding:
    """Construct one public finding from an independent rule result."""
    return PythonConformanceFinding(code, path, message, "error", line)


@dataclass(frozen=True, slots=True)
class PythonConformanceResult:
    """Immutable compatibility-complete structural validation result.

    The scalar count fields and sorted key/count tuples represent the legacy
    command's ``counts`` object without exposing mutable dictionaries.  ``paths``
    preserves request order, and ``findings`` preserves the deterministic rule
    and source traversal order.

    Attributes
    ----------
    schema_version
        Result contract version, fixed to ``1``.
    status
        ``"PASS"`` when ``findings`` is empty, otherwise ``"FAIL"``.
    claim_boundary
        Ordered tuple of conclusions explicitly not established by this result.
    paths
        Supplied module paths in request order.
    findings
        Structured expected-invalidity findings in deterministic traversal order.
    artifact_owned_modules, class_owned_modules
        Counts derived from all syntactically object-shaped ownership entries.
    evidence_class_modules
        Sorted evidence-class/count pairs.
    findings_by_code
        Sorted finding-code/count pairs.
    helper_functions, modules, parameterized_functions, test_functions
        Static module and top-level-function inventory counts.
    static_collected_parameter_cases
        Static parameter-case count, or ``None`` if any count is unresolved.
    unique_evidence_owners
        Number of unique evidence identifiers retained during validation.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If status, ordering, version, or a nonnegative-count invariant fails.
    """

    schema_version: int
    status: str
    claim_boundary: tuple[str, ...]
    paths: tuple[str, ...]
    findings: tuple[PythonConformanceFinding, ...]
    artifact_owned_modules: int
    class_owned_modules: int
    evidence_class_modules: tuple[tuple[str, int], ...]
    findings_by_code: tuple[tuple[str, int], ...]
    helper_functions: int
    modules: int
    parameterized_functions: int
    static_collected_parameter_cases: int | None
    test_functions: int
    unique_evidence_owners: int

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an int excluding bool")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        _require_builtin_str(self.status, "status")
        _require_tuple(self.claim_boundary, "claim_boundary")
        _require_tuple(self.paths, "paths")
        _require_tuple(self.findings, "findings")
        _require_tuple(self.evidence_class_modules, "evidence_class_modules")
        _require_tuple(self.findings_by_code, "findings_by_code")
        if any(type(item) is not str for item in self.claim_boundary + self.paths):
            raise TypeError("claim_boundary and paths must contain strings")
        if any(type(item) is not PythonConformanceFinding for item in self.findings):
            raise TypeError("findings must contain PythonConformanceFinding values")
        if self.status != ("PASS" if not self.findings else "FAIL"):
            raise ValueError("status must agree with findings")
        for name in (
            "artifact_owned_modules",
            "class_owned_modules",
            "helper_functions",
            "modules",
            "parameterized_functions",
            "test_functions",
            "unique_evidence_owners",
        ):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be an int excluding bool")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.static_collected_parameter_cases is not None:
            if type(self.static_collected_parameter_cases) is not int:
                raise TypeError(
                    "static_collected_parameter_cases must be an int excluding "
                    "bool or None"
                )
            if self.static_collected_parameter_cases < 0:
                raise ValueError("static_collected_parameter_cases must be nonnegative")
        for name in ("evidence_class_modules", "findings_by_code"):
            values = getattr(self, name)
            if tuple(sorted(values)) != values:
                raise ValueError(f"{name} must be sorted")
            if any(
                type(key) is not str or type(count) is not int or count < 0
                for key, count in values
            ):
                raise TypeError(f"{name} must contain str/nonnegative-int pairs")


class PythonConformanceValidator:
    """Validate explicit Python source and metadata bytes without performing I/O."""

    __slots__ = ()

    @staticmethod
    def _module_findings(
        model: PythonTestModuleModel,
        owner: dict[str, Any],
        seen: dict[str, str],
        profile_matrix: EvidenceProfileMatrix | None,
    ) -> tuple[
        tuple[PythonConformanceFinding, ...],
        _PythonParameterizationRuleResult,
        _PythonRepositoryConformanceRuleResult,
    ]:
        """Orchestrate independent named rule owners in compatibility order."""
        profile = owner.get("evidence_profile")
        documentation = _PythonDocumentationRule().execute(
            model, profile, profile_matrix
        )
        parameterization = _PythonParameterizationRule().execute(model)
        repository = _PythonRepositoryConformanceRule().execute(model)
        raw = (
            *_PythonOwnershipRule().execute(model, owner),
            *documentation.module_findings,
            *_PythonNamingRule().execute(model),
            *parameterization.findings,
            *documentation.function_findings,
            *_PythonEvidenceIdentifierRule().execute(model, seen),
            *repository.findings,
        )
        return (
            tuple(
                _finding(code, model.path, message, line) for code, message, line in raw
            ),
            parameterization,
            repository,
        )

    def execute(self, request: PythonConformanceRequest) -> PythonConformanceResult:
        """Validate one closed request while preserving the public signature."""
        return self._execute(request)

    def _execute(
        self,
        request: PythonConformanceRequest,
        corpus: _PythonTestModuleCorpus | None = None,
    ) -> PythonConformanceResult:
        """Validate with an optional internally prebuilt immutable corpus."""
        if type(request) is not PythonConformanceRequest:
            raise TypeError("request must be PythonConformanceRequest")
        findings: list[PythonConformanceFinding] = []
        profile_matrix: EvidenceProfileMatrix | None = None
        if request.profile_path is not None:
            if request.profile_read_error is not None:
                findings.append(
                    _finding(
                        "TE.PROFILE_INPUT",
                        request.profile_path,
                        request.profile_read_error,
                    )
                )
            else:
                assert request.profile_payload is not None
                profile_matrix, profile_problem = (
                    _EvidenceProfileMatrixLoader().execute(request.profile_payload)
                )
                if profile_problem is not None:
                    findings.append(
                        _finding(
                            "TE.PROFILE_INPUT",
                            request.profile_path,
                            profile_problem,
                        )
                    )
        supplied = tuple(source.path for source in request.sources)
        findings.extend(
            _finding(code, request.ownership_path, message)
            for code, message in _PythonRepositoryUniquenessRule().execute(supplied)
        )
        entries, by_path, ownership_findings = _PythonOwnershipInputLoader().execute(
            request.ownership_path,
            request.ownership_payload,
            request.ownership_read_error,
            supplied,
        )
        findings.extend(
            _finding(code, path, message, line)
            for code, path, message, line in ownership_findings
        )
        if profile_matrix is not None:
            findings.extend(
                _finding(code, request.ownership_path, message)
                for code, message in _EvidenceProfileCombinationRule().execute(
                    entries, profile_matrix
                )
            )
        selected = tuple(
            _PythonTestModuleInput(source.path, source.payload)
            for source in request.sources
            if source.path in by_path
            and source.is_regular_file
            and source.payload is not None
        )
        if corpus is None and request._parsed_models:
            corpus = _PythonTestModuleCorpus(tuple(request._parsed_models), ())
        built = _PythonTestModuleCorpusBuilder().execute(selected, prebuilt=corpus)
        seen: dict[str, str] = {}
        models: list[PythonTestModuleModel] = []
        parameter_results: list[_PythonParameterizationRuleResult] = []
        repository_results: list[_PythonRepositoryConformanceRuleResult] = []
        failures = {failure.path: failure.message for failure in built.failures}
        for source in request.sources:
            if not source.is_regular_file:
                findings.append(
                    _finding(
                        "TE.EXPLICIT_PATH",
                        source.path,
                        "supplied path must be a regular file",
                    )
                )
                continue
            owner = by_path.get(source.path)
            if owner is None:
                continue
            if source.read_error is not None:
                findings.append(_finding("TE.PARSE", source.path, source.read_error))
                continue
            if source.path in failures:
                findings.append(
                    _finding("TE.PARSE", source.path, failures[source.path])
                )
                continue
            model = built.model_for(source.path)
            assert model is not None
            models.append(model)
            module_findings, parameterization, repository = self._module_findings(
                model, owner, seen, profile_matrix
            )
            findings.extend(module_findings)
            parameter_results.append(parameterization)
            repository_results.append(repository)
        if request.migration_path is not None:
            predecessor = _PythonEvidencePredecessorRule().execute(
                request.migration_path,
                request.migration_payload,
                request.migration_read_error,
            )
            findings.extend(
                _finding(code, path, message, line)
                for code, path, message, line in predecessor.findings
            )
        tests = sum(result.test_functions for result in repository_results)
        helpers = sum(result.helper_functions for result in repository_results)
        parameterized = sum(
            result.parameterized_functions for result in parameter_results
        )
        static_known = all(
            result.static_case_count is not None for result in parameter_results
        )
        static_cases = (
            sum(result.static_case_count or 0 for result in parameter_results)
            if static_known
            else None
        )
        findings_by_code: dict[str, int] = {}
        for item in findings:
            findings_by_code[item.code] = findings_by_code.get(item.code, 0) + 1
        ownership_counts = {
            kind: sum(
                item.get("mode") == kind for item in entries if isinstance(item, dict)
            )
            for kind in ("class_owned", "artifact_owned")
        }
        evidence_class_counts = {
            kind: sum(
                item.get("evidence_class") == kind
                for item in entries
                if isinstance(item, dict)
            )
            for kind in EVIDENCE_OPENINGS
        }
        return PythonConformanceResult(
            1,
            "PASS" if not findings else "FAIL",
            (
                "oracle independence",
                "mathematical correctness",
                "property/surface correctness",
                "test cohesion",
                "tolerance adequacy",
                "scientific validity",
                "uncertainty quantification",
                "human acceptance",
            ),
            supplied,
            tuple(findings),
            ownership_counts["artifact_owned"],
            ownership_counts["class_owned"],
            tuple(sorted(evidence_class_counts.items())),
            tuple(sorted(findings_by_code.items())),
            helpers,
            len(request.sources),
            parameterized,
            static_cases,
            tests,
            len(seen),
        )
