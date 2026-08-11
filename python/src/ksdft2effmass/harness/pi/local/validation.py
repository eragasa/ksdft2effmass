"""Project-local composition of accepted generic H2 validation actions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from .. import (
    AgentDescriptorView,
    ChainStateEvaluator,
    ChainView,
    CheckpointRecord,
    CheckpointSetValidator,
    ChecksumManifest,
    ChecksumManifestValidator,
    OwnershipManifestValidator,
    OwnershipManifestView,
    ResourceManifestValidator,
    ResourceResolver,
    SkillDescriptor,
    SkillResourceValidator,
    ValidationResult,
)
from ..evidence import IdentifierAuditor
from .context import LocalHarnessContextLoader
from .dbcontrol import HarnessControlVerifier
from .models import LocalHarnessContext, RepositoryRoots
from .resource_adapters import SkillInventoryAdapter
from .task_model import HarnessTaskDeserializer, HarnessTaskGraphValidator


@dataclass(frozen=True, slots=True)
class AdaptedRepositoryRecords:
    """Explicit selected records consumed by local validation composition.

    Empty optional selections skip the corresponding generic action; they do
    not cause repository discovery.
    """

    chain: ChainView
    checkpoints: tuple[CheckpointRecord, ...]
    known_external_prerequisite_ids: tuple[str, ...]
    satisfied_external_prerequisite_ids: tuple[str, ...]
    agents: tuple[AgentDescriptorView, ...] = ()
    ownership: OwnershipManifestView | None = None
    checksum_root: Path | None = None
    checksums: ChecksumManifest | None = None
    skills: tuple[SkillDescriptor, ...] = ()
    evidence_modules: tuple[tuple[str, bytes], ...] = ()


@dataclass(frozen=True, slots=True)
class RepositoryValidationResult:
    """Ordered generic results with no local severity downgrade."""

    status: str
    results: tuple[tuple[str, ValidationResult], ...]

    def __post_init__(self) -> None:
        if self.status not in {"PASS", "WARN", "FAIL"}:
            raise ValueError("invalid status")
        if type(self.results) is not tuple or self.results != tuple(
            sorted(self.results)
        ):
            raise ValueError("results must be name sorted")
        actual = (
            "FAIL"
            if any(x.status == "FAIL" for _, x in self.results)
            else "WARN"
            if any(x.status == "WARN" for _, x in self.results)
            else "PASS"
        )
        if self.status != actual:
            raise ValueError("status does not agree with generic results")


class LocalRepositoryValidator:
    """Compose generic validators over explicit project-local selections."""

    __slots__ = ()

    def execute(
        self, context: LocalHarnessContext, adapted_records: AdaptedRepositoryRecords
    ) -> RepositoryValidationResult:
        """Run applicable generic actions without weakening their diagnostics."""
        if (
            type(context) is not LocalHarnessContext
            or type(adapted_records) is not AdaptedRepositoryRecords
        ):
            raise TypeError("context/records have wrong type")
        profile = context.profile
        values: list[tuple[str, ValidationResult]] = []
        values.append(
            (
                "resources",
                ResourceManifestValidator().execute(
                    context.generic_manifest,
                    context.generic_manifest_identity,
                    context.local_manifest,
                    context.local_manifest_identity,
                    profile,
                ),
            )
        )
        values.append(
            (
                "checkpoints",
                CheckpointSetValidator().execute(
                    adapted_records.checkpoints,
                    tuple(x.task_id for x in adapted_records.chain.tasks),
                    profile,
                ),
            )
        )
        chain_result = ChainStateEvaluator().execute(
            adapted_records.chain,
            adapted_records.checkpoints,
            adapted_records.known_external_prerequisite_ids,
            adapted_records.satisfied_external_prerequisite_ids,
            profile,
        )
        values.append(("chain", chain_result.validation))
        if adapted_records.ownership is not None:
            values.append(
                (
                    "ownership",
                    OwnershipManifestValidator().execute(
                        adapted_records.ownership,
                        adapted_records.chain,
                        adapted_records.agents,
                        profile,
                    ),
                )
            )
        if adapted_records.checksums is not None:
            if adapted_records.checksum_root is None:
                raise ValueError("checksum_root is required with checksums")
            values.append(
                (
                    "checksums",
                    ChecksumManifestValidator().execute(
                        adapted_records.checksum_root, adapted_records.checksums
                    ),
                )
            )
        if adapted_records.skills:
            values.append(
                (
                    "skills",
                    SkillResourceValidator().execute(
                        adapted_records.skills,
                        context.generic_manifest,
                        context.generic_manifest_identity,
                        context.local_manifest,
                        context.local_manifest_identity,
                        profile,
                    ),
                )
            )
        if adapted_records.evidence_modules:
            values.append(
                (
                    "evidence",
                    IdentifierAuditor()
                    .execute(adapted_records.evidence_modules, profile)
                    .validation,
                )
            )
        ordered = tuple(sorted(values))
        status = (
            "FAIL"
            if any(x.status == "FAIL" for _, x in ordered)
            else "WARN"
            if any(x.status == "WARN" for _, x in ordered)
            else "PASS"
        )
        return RepositoryValidationResult(status, ordered)


_HARNESS_CHECK_ORDER = (
    "python_evidence",
    "resources",
    "task_graph",
    "checkpoints",
    "skills",
    "ownership",
    "control_state",
    "external_gates",
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
        if type(self.name) is not str or self.name not in _HARNESS_CHECK_ORDER:
            raise ValueError("unsupported harness validation check name")
        if type(self.status) is not str or self.status not in {"PASS", "WARN", "FAIL"}:
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
        if type(self.status) is not str or self.status not in {"PASS", "WARN", "FAIL"}:
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
        if self.claim_boundaries != _HARNESS_CLAIM_BOUNDARIES:
            raise ValueError("claim boundaries must use the complete stable contract")


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
        context, resource_check = self._resource_check(root)
        task_check = self._task_check(root)
        checkpoint_check = self._checkpoint_check(root)
        skill_check = self._skill_check(root, context)
        ownership_check = self._ownership_check(root)
        control_result = HarnessControlVerifier().execute(root)
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
        evidence_findings = tuple(
            finding
            for finding in control_findings
            if finding[1] is None
            or finding[1].startswith("python/tests")
            or "python-conformance" in finding[1]
        )
        evidence_check = HarnessValidationCheck(
            "python_evidence",
            "FAIL" if evidence_findings else "PASS",
            evidence_findings,
        )
        external_check = HarnessValidationCheck(
            "external_gates",
            "WARN",
            (
                (
                    "external.development_tools",
                    None,
                    "pytest, Ruff, mypy, and Sphinx remain separately executed "
                    "final gates",
                ),
                (
                    "external.documentation_and_wire",
                    None,
                    "documentation projection and test-only wire checks remain "
                    "external final gates",
                ),
            ),
        )
        checks = (
            evidence_check,
            resource_check,
            task_check,
            checkpoint_check,
            skill_check,
            ownership_check,
            control_check,
            external_check,
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
                document = json.loads(path.read_text())
                if document.get("schema_version") == 3:
                    tasks.append(HarnessTaskDeserializer().execute(path.read_bytes()))
            except (
                OSError,
                UnicodeError,
                json.JSONDecodeError,
                TypeError,
                ValueError,
            ) as exc:
                findings.append(
                    (
                        "task.invalid_record",
                        path.relative_to(root).as_posix(),
                        str(exc),
                    )
                )
        if not findings:
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
        from ._commands import validate_checkpoints as owner

        checkpoint_root = root / ".pi/checkpoints"
        schema = owner.load_json(checkpoint_root / "checkpoint.schema.json")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        errors: list[str] = []
        for path in owner.checkpoint_paths(checkpoint_root, False):
            errors.extend(owner.validate_schema(owner.load_json(path), path, validator))
        errors.extend(owner.scan_duplicate_decisions(checkpoint_root))
        findings = tuple(
            sorted(
                (
                    "checkpoint.invalid",
                    None,
                    error,
                )
                for error in errors
            )
        )
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

    def _ownership_check(self, root: Path) -> HarnessValidationCheck:
        chain = json.loads(
            (root / ".pi/chains/harness-simplification.chain.json").read_text()
        )
        active = chain.get("active_task")
        entry = next(
            (
                item
                for item in chain.get("task_sequence", [])
                if item.get("id") == active
            ),
            None,
        )
        if entry is None:
            return HarnessValidationCheck(
                "ownership",
                "FAIL",
                (
                    (
                        "ownership.active_task_missing",
                        None,
                        "active Task is absent from chain",
                    ),
                ),
            )
        manifest = entry.get("ownership_manifest")
        if manifest is None:
            return HarnessValidationCheck(
                "ownership",
                "WARN",
                (
                    (
                        "ownership.not_declared",
                        None,
                        "active Task declares no ownership manifest",
                    ),
                ),
            )
        return HarnessValidationCheck(
            "ownership",
            "WARN",
            (
                (
                    "ownership.external_gate",
                    str(manifest),
                    "declared ownership remains validated by the maintained "
                    "ownership gate",
                ),
            ),
        )
