"""Complete source-derived repository Python-evidence conformance operation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.harness.pi.conformance.python.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from ksdft2effmass.harness.pi.conformance.python.nodes import _PythonTestNodeProjector

from .conformance_inputs import _PythonConformanceInputResolver
from .control.configuration_inputs import _HarnessConfigurationInputResolver
from .validation import HarnessValidationRequest, HarnessValidator

_CLAIM_BOUNDARY = (
    "semantic cohesion",
    "oracle independence",
    "field completeness beyond declared structural inventories",
    "mathematical correctness",
    "tolerance adequacy",
    "scientific validation",
    "uncertainty quantification",
    "human acceptance",
)


@dataclass(frozen=True, slots=True)
class _EvidenceRepositoryConformanceFinding:
    """Immutable normalized repository-conformance finding."""

    code: str
    path: str | None
    message: str
    severity: str = "error"


@dataclass(frozen=True, slots=True)
class _EvidenceRepositoryConformanceResult:
    """Immutable complete outcome rendered by the repository command adapter."""

    status: str
    claim_boundary: tuple[str, ...]
    baseline_modules: int
    baseline_collected_nodes: int
    discovered_modules: int
    collected_nodes: int
    unique_evidence_owners: int
    findings: tuple[_EvidenceRepositoryConformanceFinding, ...]


class _EvidenceRepositoryConformanceValidator:
    """Validate and summarize source-derived Python evidence for one repository."""

    __slots__ = ()

    def execute(
        self, request: HarnessValidationRequest
    ) -> _EvidenceRepositoryConformanceResult:
        """Return the complete structural repository-evidence result."""
        configuration = (
            _HarnessConfigurationInputResolver()
            .execute(request.repository_root)
            .configuration.python_conformance
        )
        inputs = _PythonConformanceInputResolver().execute(
            request.repository_root,
            pyproject_path=Path(configuration.pyproject_path),
            test_root_path=Path(configuration.test_root),
            profile_path=Path(configuration.profile_matrix_path),
            migration_path=Path(configuration.migration_map_path),
        )
        validation = HarnessValidator().execute(request)
        conformance = validation.checks[0]
        module_inputs = tuple(
            _PythonTestModuleInput(
                path.as_posix(), (inputs.repository_root / path).read_bytes()
            )
            for path in inputs.module_paths
        )
        corpus = _PythonTestModuleCorpusBuilder().execute(module_inputs)
        nodes = _PythonTestNodeProjector().execute(corpus.models)
        owner_count = sum(
            function.is_test for model in corpus.models for function in model.functions
        )
        findings = tuple(
            _EvidenceRepositoryConformanceFinding(code, path, message)
            for code, path, message in conformance.findings
        )
        return _EvidenceRepositoryConformanceResult(
            conformance.status,
            _CLAIM_BOUNDARY,
            182,
            2383,
            len(corpus.models),
            len(nodes),
            owner_count,
            findings,
        )
