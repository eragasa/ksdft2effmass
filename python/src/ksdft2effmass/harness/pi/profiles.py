"""Explicit project-profile data and strict byte loader."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .identity import (
    ArtifactIdentity,
    Identifier,
    ResourcePath,
    Version,
    _require_identifier,
    _require_path,
    _require_sorted_unique,
    _require_tuple,
    _require_version,
)
from .ownership import OwnershipScope
from .validation import (
    DeserializeJsonRecord,
    ProjectProfileLoadResult,
    WireRecordKind,
    _issue,
    _result,
)


@dataclass(frozen=True, slots=True)
class ProjectProfile:
    """Data-only generic policy profile supplied explicitly to actions."""

    schema_version: int
    profile_id: Identifier
    public_contract_version: Version
    generic_manifest_id: Identifier
    generic_manifest_version: Version
    local_manifest_id: Identifier | None
    local_manifest_version: Version | None
    overlay_policy: str
    policy_reference_ids: tuple[Identifier, ...]
    supported_resource_formats: tuple[tuple[Identifier, Version], ...]
    supported_skill_behaviors: tuple[tuple[Identifier, Version], ...]
    evidence_namespace_rules: tuple[tuple[Identifier, int, int, int], ...]
    evidence_scope_rules: tuple[
        tuple[OwnershipScope, Identifier, tuple[Identifier, ...]], ...
    ]
    protected_unowned_functions: tuple[tuple[ResourcePath, Identifier], ...]
    pytest_markers: tuple[Identifier, ...]
    filename_policy_id: Identifier | None
    checkpoint_unresolved_statuses: tuple[Identifier, ...]
    checkpoint_resolved_statuses: tuple[Identifier, ...]
    task_active_statuses: tuple[Identifier, ...]
    task_blocked_statuses: tuple[Identifier, ...]
    task_satisfied_statuses: tuple[Identifier, ...]
    compatibility_adapter_version: Version | None
    local_extension_ids: tuple[Identifier, ...]

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        for name in ("profile_id", "generic_manifest_id"):
            _require_identifier(getattr(self, name), name)
        for name in ("public_contract_version", "generic_manifest_version"):
            _require_version(getattr(self, name), name)
        if self.local_manifest_id is not None:
            _require_identifier(self.local_manifest_id, "local_manifest_id")
        if self.local_manifest_version is not None:
            _require_version(self.local_manifest_version, "local_manifest_version")
        if (self.local_manifest_id is None) != (self.local_manifest_version is None):
            raise ValueError("local manifest ID/version must be jointly present")
        if type(self.overlay_policy) is not str:
            raise TypeError("overlay_policy must be str")
        if self.overlay_policy != "extend_only":
            raise ValueError("overlay_policy must be extend_only")
        for name in (
            "policy_reference_ids",
            "pytest_markers",
            "checkpoint_unresolved_statuses",
            "checkpoint_resolved_statuses",
            "task_active_statuses",
            "task_blocked_statuses",
            "task_satisfied_statuses",
            "local_extension_ids",
        ):
            values = getattr(self, name)
            _require_tuple(values, name)
            for x in values:
                _require_identifier(x, name)
            _require_sorted_unique(values, name)
        if (
            not self.checkpoint_unresolved_statuses
            or not self.checkpoint_resolved_statuses
            or not self.task_active_statuses
            or not self.task_blocked_statuses
        ):
            raise ValueError("required vocabularies must be nonempty")
        vocab = [
            set(self.checkpoint_unresolved_statuses),
            set(self.checkpoint_resolved_statuses),
        ]
        if vocab[0] & vocab[1]:
            raise ValueError("checkpoint vocabularies overlap")
        task_sets = [
            set(self.task_active_statuses),
            set(self.task_blocked_statuses),
            set(self.task_satisfied_statuses),
        ]
        if any(task_sets[i] & task_sets[j] for i in range(3) for j in range(i)):
            raise ValueError("task vocabularies overlap")
        for name in ("supported_resource_formats", "supported_skill_behaviors"):
            values = getattr(self, name)
            _require_tuple(values, name)
            if tuple(sorted(values)) != values or len(set(values)) != len(values):
                raise ValueError(f"{name} must be unique and sorted")
            for pair in values:
                if type(pair) is not tuple or len(pair) != 2:
                    raise TypeError(f"{name} entries must be pairs")
                _require_identifier(pair[0], name)
                _require_version(pair[1], name)
        _require_tuple(self.evidence_namespace_rules, "evidence_namespace_rules")
        prefixes = []
        for rule in self.evidence_namespace_rules:
            if type(rule) is not tuple or len(rule) != 4:
                raise TypeError("namespace rules must be 4-tuples")
            prefix, minimum, maximum, width = rule
            _require_identifier(prefix, "namespace_prefix")
            _require_version(minimum, "minimum", minimum=0)
            _require_version(maximum, "maximum", minimum=0)
            _require_version(width, "decimal_width", maximum=15)
            if minimum > maximum:
                raise ValueError("namespace minimum exceeds maximum")
            prefixes.append(prefix)
        if prefixes != sorted(prefixes) or len(set(prefixes)) != len(prefixes):
            raise ValueError("namespace prefixes must be unique and sorted")
        _require_tuple(self.evidence_scope_rules, "evidence_scope_rules")
        scopes: list[OwnershipScope] = []
        for scope_rule in self.evidence_scope_rules:
            if type(scope_rule) is not tuple or len(scope_rule) != 3:
                raise TypeError("scope rules must be triples")
            scope, marker, allowed = scope_rule
            if type(scope) is not OwnershipScope:
                raise TypeError("scope rule scope has wrong type")
            _require_identifier(marker, "required_marker")
            _require_tuple(allowed, "allowed_namespace_prefixes")
            if not allowed:
                raise ValueError("allowed namespaces must be nonempty")
            for p in allowed:
                _require_identifier(p, "allowed namespace")
            _require_sorted_unique(allowed, "allowed namespaces")
            if not set(allowed) <= set(prefixes):
                raise ValueError("scope uses undeclared namespace")
            if marker not in self.pytest_markers:
                raise ValueError("scope marker is undeclared")
            scopes.append(scope)
        for i, a in enumerate(scopes):
            for b in scopes[:i]:
                if a.contains(b.path) or b.contains(a.path):
                    raise ValueError("evidence scopes overlap")
        _require_tuple(self.protected_unowned_functions, "protected_unowned_functions")
        if tuple(
            sorted(self.protected_unowned_functions)
        ) != self.protected_unowned_functions or len(
            set(self.protected_unowned_functions)
        ) != len(self.protected_unowned_functions):
            raise ValueError("protected functions must be unique and sorted")
        for path, fn in self.protected_unowned_functions:
            _require_path(path, "protected path")
            _require_identifier(fn, "test function")
        if self.filename_policy_id is not None:
            _require_identifier(self.filename_policy_id, "filename_policy_id")
        if self.compatibility_adapter_version is not None:
            _require_version(
                self.compatibility_adapter_version, "compatibility_adapter_version"
            )


class LoadProjectProfile:
    """Load strict profile JSON from caller-supplied bytes only."""

    __slots__ = ()

    def execute(
        self,
        profile_bytes: bytes,
        expected_identity: ArtifactIdentity | None,
        supported_schema_versions: tuple[Version, ...],
        supported_contract_versions: tuple[Version, ...],
    ) -> ProjectProfileLoadResult:
        if type(profile_bytes) is not bytes:
            raise TypeError("profile_bytes must be bytes")
        if (
            expected_identity is not None
            and type(expected_identity) is not ArtifactIdentity
        ):
            raise TypeError("expected_identity has wrong type")
        for name, values in (
            ("supported_schema_versions", supported_schema_versions),
            ("supported_contract_versions", supported_contract_versions),
        ):
            _require_tuple(values, name)
            for v in values:
                _require_version(v, name)
        decoded = DeserializeJsonRecord().execute(
            WireRecordKind.ProjectProfile, profile_bytes
        )
        if decoded.validation.status == "FAIL":
            return ProjectProfileLoadResult(None, decoded.validation)
        profile = decoded.record
        if type(profile) is not ProjectProfile:
            raise AssertionError("profile decoder returned the wrong record kind")
        issues = []
        if expected_identity is not None:
            actual = ArtifactIdentity(
                1, "sha256", hashlib.sha256(profile_bytes).hexdigest()
            )
            if actual != expected_identity:
                issues.append(
                    _issue(
                        "PIH.PROFILE.IDENTITY_MISMATCH",
                        "Profile bytes differ from expected identity.",
                        profile.profile_id,
                    )
                )
        if profile.schema_version not in supported_schema_versions:
            issues.append(
                _issue(
                    "PIH.WIRE.UNSUPPORTED_VERSION",
                    "Profile schema version is unsupported.",
                    profile.profile_id,
                )
            )
        if profile.public_contract_version not in supported_contract_versions:
            issues.append(
                _issue(
                    "PIH.PROFILE.CONTRACT_INCOMPATIBLE",
                    "Public contract version is unsupported.",
                    profile.profile_id,
                )
            )
        validation = _result(tuple(issues))
        return ProjectProfileLoadResult(
            None if validation.status == "FAIL" else profile, validation
        )
