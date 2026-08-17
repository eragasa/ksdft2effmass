"""Project-local composition of accepted generic H2 validation actions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .. import ResourceResolver, SkillResourceValidator
from ..conformance.python import (
    PythonConformanceRequest,
    PythonConformanceValidator,
    PythonModuleSource,
)
from ..conformance.python.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from .checkpoint_validation import _CheckpointRepositoryValidator
from .conformance_inputs import _PythonConformanceInputResolver
from .context import LocalHarnessContextLoader
from .dbcontrol.verification import _HarnessProjectionVerifier
from .models import LocalHarnessContext, RepositoryRoots
from .resource_adapters import SkillInventoryAdapter
from .task_model import HarnessTaskDeserializer, HarnessTaskGraphValidator

_HARNESS_CHECK_ORDER = (
    "python_conformance",
    "resources",
    "task_graph",
    "checkpoints",
    "skills",
    "control_state",
)
_HARNESS_CLAIM_BOUNDARIES = (
    "does not execute or establish pytest success",
    "does not execute or establish Ruff conformance",
    "does not execute or establish mypy conformance",
    "does not execute or establish Sphinx conformance",
    "does not establish numerical verification",
    "does not establish scientific validation",
    "does not establish uncertainty quantification",
    "does not authorize protected execution",
    "does not establish human acceptance",
)


@dataclass(frozen=True, slots=True)
class HarnessValidationRequest:
    """Explicit repository boundary for deterministic structural validation.

    Parameters
    ----------
    repository_root
        Absolute existing project repository root. Existence and canonical source
        structure are checked by :class:`HarnessValidator`.
    """

    repository_root: Path

    def __post_init__(self) -> None:
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute() or ".." in self.repository_root.parts:
            raise ValueError(
                "repository_root must be absolute without parent traversal"
            )


@dataclass(frozen=True, slots=True)
class HarnessValidationCheck:
    """One stable repository structural check and its normalized findings.

    Findings are ``(code, repository_relative_path_or_none, message)`` triples. They
    preserve domain identities without introducing another public wire record kind.
    """

    name: str
    status: str
    findings: tuple[tuple[str, str | None, str], ...]

    def __post_init__(self) -> None:
        if type(self.name) is not str:
            raise TypeError("harness validation check name must be str")
        if self.name not in _HARNESS_CHECK_ORDER:
            raise ValueError("unsupported harness validation check name")
        if type(self.status) is not str:
            raise TypeError("harness validation check status must be str")
        if self.status not in {"PASS", "WARN", "FAIL"}:
            raise ValueError("invalid harness validation check status")
        if type(self.findings) is not tuple:
            raise TypeError("findings must be a tuple")
        for finding in self.findings:
            if (
                type(finding) is not tuple
                or len(finding) != 3
                or type(finding[0]) is not str
                or (finding[1] is not None and type(finding[1]) is not str)
                or type(finding[2]) is not str
            ):
                raise TypeError("findings must be structured string triples")
        if self.findings != tuple(sorted(set(self.findings), key=self._finding_key)):
            raise ValueError("findings must be unique and deterministically sorted")
        if self.status == "PASS" and self.findings:
            raise ValueError("PASS checks cannot contain findings")
        if self.status != "PASS" and not self.findings:
            raise ValueError("WARN and FAIL checks require findings")

    @staticmethod
    def _finding_key(
        finding: tuple[str, str | None, str],
    ) -> tuple[str, str, str]:
        return finding[0], finding[1] or "", finding[2]


@dataclass(frozen=True, slots=True)
class HarnessValidationResult:
    """Deterministic aggregate of project-local structural validation checks."""

    status: str
    checks: tuple[HarnessValidationCheck, ...]
    claim_boundaries: tuple[str, ...] = _HARNESS_CLAIM_BOUNDARIES

    def __post_init__(self) -> None:
        if type(self.status) is not str:
            raise TypeError("harness validation result status must be str")
        if self.status not in {"PASS", "WARN", "FAIL"}:
            raise ValueError("invalid harness validation result status")
        if type(self.checks) is not tuple or any(
            type(check) is not HarnessValidationCheck for check in self.checks
        ):
            raise TypeError("checks must contain HarnessValidationCheck values")
        if tuple(check.name for check in self.checks) != _HARNESS_CHECK_ORDER:
            raise ValueError("checks must use the complete stable semantic order")
        actual = (
            "FAIL"
            if any(check.status == "FAIL" for check in self.checks)
            else "WARN"
            if any(check.status == "WARN" for check in self.checks)
            else "PASS"
        )
        if self.status != actual:
            raise ValueError("result status does not agree with checks")
        if type(self.claim_boundaries) is not tuple or any(
            type(boundary) is not str for boundary in self.claim_boundaries
        ):
            raise TypeError("claim boundaries must be a tuple of strings")
        if self.claim_boundaries != _HARNESS_CLAIM_BOUNDARIES:
            raise ValueError("claim boundaries must use the complete stable contract")


class _PythonConformanceRepositoryValidator:
    """Invoke the Python conformance owner from canonical source inputs."""

    __slots__ = ()

    def execute(self, root: Path) -> HarnessValidationCheck:
        """Return direct Python-conformance findings for one repository root."""
        conformance_inputs = _PythonConformanceInputResolver().execute(root)
        sources: list[PythonModuleSource] = []
        module_inputs: list[_PythonTestModuleInput] = []
        for relative in conformance_inputs.module_paths:
            payload = (root / relative).read_bytes()
            path = relative.as_posix()
            sources.append(PythonModuleSource(path, payload))
            module_inputs.append(_PythonTestModuleInput(path, payload))
        corpus = _PythonTestModuleCorpusBuilder().execute(tuple(module_inputs))
        models = corpus.models
        ownership_entries: list[dict[str, object]] = []
        for model in models:
            entry: dict[str, object] = {
                "path": model.path,
                "mode": model.ownership_kind,
                "evidence_class": model.evidence_class,
                "evidence_profile": model.evidence_profile,
            }
            entry["sut" if model.ownership_kind == "class_owned" else "artifact"] = (
                model.owner_subject
            )
            ownership_entries.append(entry)
        if corpus.failures:
            first = corpus.failures[0]
            return HarnessValidationCheck(
                "python_conformance",
                "FAIL",
                (("TE.PARSE", first.path, first.message),),
            )
        conformance = PythonConformanceValidator().execute(
            PythonConformanceRequest(
                tuple(sources),
                "<source-embedded-module-declarations>",
                json.dumps(
                    {"schema_version": 1, "modules": ownership_entries},
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode(),
                migration_path=conformance_inputs.migration_path.as_posix(),
                migration_payload=(
                    root / conformance_inputs.migration_path
                ).read_bytes(),
                profile_path=conformance_inputs.profile_path.as_posix(),
                profile_payload=(root / conformance_inputs.profile_path).read_bytes(),
                _parsed_models=models,
            )
        )
        findings = tuple(
            sorted(
                (finding.code, finding.path, finding.message)
                for finding in conformance.findings
            )
        )
        return HarnessValidationCheck(
            "python_conformance", "FAIL" if findings else "PASS", findings
        )


class HarnessValidator:
    """Compose existing domain owners into structural repository validation.

    The Action owns deterministic sequencing and aggregation only. It does not invoke
    command-line interfaces, parse command output, execute development tools, absorb
    domain rules, or translate unexpected implementation exceptions into findings.
    """

    __slots__ = ()

    def execute(self, request: HarnessValidationRequest) -> HarnessValidationResult:
        """Validate one explicit repository and return ordered structural checks.

        Parameters
        ----------
        request
            Exact absolute repository boundary.

        Returns
        -------
        HarnessValidationResult
            Stable domain checks, findings, aggregate status, and claim boundaries.

        Raises
        ------
        TypeError
            If ``request`` has the wrong semantic type.
        ValueError
            If canonical request construction is invalid.
        Exception
            Unexpected domain or implementation failures propagate unchanged.
        """
        if type(request) is not HarnessValidationRequest:
            raise TypeError("request must be HarnessValidationRequest")
        root = request.repository_root.resolve(strict=True)
        conformance_check = _PythonConformanceRepositoryValidator().execute(root)
        context, resource_check = self._resource_check(root)
        task_check = self._task_check(root)
        checkpoint_check = self._checkpoint_check(root)
        skill_check = self._skill_check(root, context)
        control_result = _HarnessProjectionVerifier().execute(root)
        control_findings = tuple(
            sorted(
                (
                    f"control.{finding.code}",
                    finding.path,
                    finding.message,
                )
                for finding in control_result.findings
            )
        )
        control_failed = bool(control_findings) or not all(
            (
                control_result.integrity_check == "ok",
                control_result.foreign_key_issue_count == 0,
                control_result.semantic_digest
                == control_result.reconstructed_semantic_digest,
                control_result.schema_version_agrees,
                control_result.sql_identical,
                control_result.manifest_identical,
                control_result.projections_identical,
            )
        )
        control_check = HarnessValidationCheck(
            "control_state",
            "FAIL" if control_failed else "PASS",
            control_findings
            if control_findings
            else (
                (
                    "control.disagreement",
                    None,
                    "one or more represented control checks disagree",
                ),
            )
            if control_failed
            else (),
        )
        checks = (
            conformance_check,
            resource_check,
            task_check,
            checkpoint_check,
            skill_check,
            control_check,
        )
        status = (
            "FAIL"
            if any(check.status == "FAIL" for check in checks)
            else "WARN"
            if any(check.status == "WARN" for check in checks)
            else "PASS"
        )
        return HarnessValidationResult(status, checks)

    def _resource_check(
        self, root: Path
    ) -> tuple[LocalHarnessContext | None, HarnessValidationCheck]:
        roots = RepositoryRoots(root, root / "harness/pi", root / "harness/local")
        adapted = LocalHarnessContextLoader().execute(
            roots,
            (root / "harness/local/profiles/ksdft2effmass-v2.json").read_bytes(),
            (root / "harness/pi/resource-manifest.json").read_bytes(),
            (root / "harness/local/resource-manifest.json").read_bytes(),
        )
        if type(adapted.value) is not LocalHarnessContext:
            findings = tuple(
                (issue.code, issue.path, issue.detail)
                for issue in adapted.validation.issues
            )
            return None, HarnessValidationCheck("resources", "FAIL", findings)
        context = adapted.value
        issues: list[tuple[str, str | None, str]] = []
        resource_ids = tuple(
            sorted(
                reference.resource_id
                for manifest in (context.generic_manifest, context.local_manifest)
                for reference in manifest.resources
            )
        )
        for resource_id in resource_ids:
            result = ResourceResolver().execute(
                resource_id,
                roots.generic_resource_root,
                context.generic_manifest,
                context.generic_manifest_identity,
                roots.local_resource_root,
                context.local_manifest,
                context.local_manifest_identity,
                context.profile,
            )
            issues.extend(
                (issue.code, issue.path, issue.message)
                for issue in result.validation.issues
            )
        findings = tuple(sorted(set(issues)))
        return context, HarnessValidationCheck(
            "resources", "FAIL" if findings else "PASS", findings
        )

    def _task_check(self, root: Path) -> HarnessValidationCheck:
        tasks = []
        findings: list[tuple[str, str | None, str]] = []
        for path in sorted((root / "harness/tasks").glob("*.json")):
            try:
                tasks.append(HarnessTaskDeserializer().execute(path.read_bytes()))
            except (OSError, TypeError, ValueError) as exc:
                findings.append(
                    (
                        "task.invalid_record",
                        path.relative_to(root).as_posix(),
                        str(exc),
                    )
                )
        if tasks:
            graph = HarnessTaskGraphValidator().execute(tuple(tasks))
            findings.extend(
                (issue.code, issue.path, issue.detail) for issue in graph.issues
            )
        ordered = tuple(sorted(set(findings)))
        check = HarnessValidationCheck(
            "task_graph", "FAIL" if ordered else "PASS", ordered
        )
        return check

    def _checkpoint_check(self, root: Path) -> HarnessValidationCheck:
        result = _CheckpointRepositoryValidator().execute(root)
        findings = tuple(("checkpoint.invalid", None, error) for error in result.errors)
        return HarnessValidationCheck(
            "checkpoints", "FAIL" if findings else "PASS", findings
        )

    def _skill_check(
        self, root: Path, context: LocalHarnessContext | None
    ) -> HarnessValidationCheck:
        if context is None:
            return HarnessValidationCheck(
                "skills",
                "FAIL",
                (
                    (
                        "skill.resource_context_invalid",
                        None,
                        "resource context is invalid",
                    ),
                ),
            )
        descriptors = tuple(
            (
                path.relative_to(root).as_posix(),
                path.read_bytes(),
            )
            for path in sorted((root / "harness/pi/skills").glob("*/descriptor.json"))
        )
        adapted = SkillInventoryAdapter().execute(
            (root / ".pi/skills/skill-capability-inventory.json").read_bytes(),
            descriptors,
        )
        if type(adapted.value) is not tuple:
            findings = tuple(
                (issue.code, issue.path, issue.detail)
                for issue in adapted.validation.issues
            )
            return HarnessValidationCheck("skills", "FAIL", findings)
        result = SkillResourceValidator().execute(
            adapted.value,
            context.generic_manifest,
            context.generic_manifest_identity,
            context.local_manifest,
            context.local_manifest_identity,
            context.profile,
        )
        findings = tuple(
            (issue.code, issue.path, issue.message) for issue in result.issues
        )
        return HarnessValidationCheck(
            "skills", "FAIL" if findings else "PASS", findings
        )
