"""Project-local composition of accepted generic H2 validation actions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .. import (
    AgentDescriptorView,
    AuditEvidenceIdentifiers,
    ChainStateEvaluator,
    ChainView,
    CheckpointRecord,
    CheckpointSetValidator,
    ChecksumManifest,
    ChecksumManifestValidator,
    OwnershipManifestValidator,
    OwnershipManifestView,
    ResourceManifestValidator,
    SkillDescriptor,
    SkillResourceValidator,
    ValidationResult,
)
from .models import LocalHarnessContext


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
                    AuditEvidenceIdentifiers()
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
