"""Normalized ownership records and generic structural validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .identity import (
    Identifier,
    OwnershipScopePath,
    ResourcePath,
    _require_builtin_str,
    _require_identifier,
    _require_path,
    _require_tuple,
    _require_version,
)
from .validation import ValidationResult, _issue, _result

if TYPE_CHECKING:
    from .chains import ChainView
    from .profiles import ProjectProfile


@dataclass(frozen=True, slots=True)
class OwnershipScope:
    """One exact file or directory-tree ownership declaration."""

    schema_version: int
    path: OwnershipScopePath
    scope_kind: str

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_path(self.path, "path")
        _require_builtin_str(self.scope_kind, "scope_kind")
        if self.scope_kind not in {"file", "directory_tree"}:
            raise ValueError("invalid scope_kind")

    def contains(self, path: str) -> bool:
        """Return whether this scope contains a valid lexical path."""
        _require_path(path, "path")
        return path == self.path or (
            self.scope_kind == "directory_tree" and path.startswith(self.path + "/")
        )


@dataclass(frozen=True, slots=True)
class AgentDescriptorView:
    """Normalized agent identity and acceptance role."""

    schema_version: int
    agent_id: Identifier
    acceptance_role: str

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.agent_id, "agent_id")
        _require_builtin_str(self.acceptance_role, "acceptance_role")
        if self.acceptance_role not in {"writer", "read_only"}:
            raise ValueError("invalid acceptance_role")


@dataclass(frozen=True, slots=True)
class OwnershipManifestView:
    """Generic normalized version-2 ownership view."""

    schema_version: int
    task_id: Identifier
    task_record_path: ResourcePath
    writers: tuple[tuple[Identifier, Identifier, tuple[OwnershipScope, ...]], ...]
    reviewers: tuple[tuple[Identifier, Identifier], ...]
    completion_validator_path: ResourcePath
    completion_command: tuple[str, ...]
    orchestration_profile_id: Identifier | None

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.task_id, "task_id")
        _require_path(self.task_record_path, "task_record_path")
        _require_tuple(self.writers, "writers")
        _require_tuple(self.reviewers, "reviewers")
        if not self.writers or not self.reviewers:
            raise ValueError("writers and reviewers must be nonempty")
        if tuple(sorted(self.writers, key=lambda x: (x[0], x[1]))) != self.writers:
            raise ValueError("writers must be role/agent sorted")
        wr = []
        wa = []
        all_scopes: list[OwnershipScope] = []
        for role, agent, scopes in self.writers:
            _require_identifier(role, "writer role")
            _require_identifier(agent, "writer agent")
            _require_tuple(scopes, "owned_scopes")
            if not scopes or any(type(s) is not OwnershipScope for s in scopes):
                raise TypeError("owned_scopes must contain scopes")
            if tuple(sorted(scopes, key=lambda s: (s.path, s.scope_kind))) != scopes:
                raise ValueError("owned scopes must be sorted")
            for s in scopes:
                for prior in all_scopes:
                    if s.contains(prior.path) or prior.contains(s.path):
                        raise ValueError("writer scopes overlap")
                all_scopes.append(s)
            wr.append(role)
            wa.append(agent)
        if len(set(wr)) != len(wr) or len(set(wa)) != len(wa):
            raise ValueError("writer roles and agents must be unique")
        if tuple(sorted(self.reviewers)) != self.reviewers:
            raise ValueError("reviewers must be role/agent sorted")
        rr = []
        ra = []
        for role, agent in self.reviewers:
            _require_identifier(role, "reviewer role")
            _require_identifier(agent, "reviewer agent")
            rr.append(role)
            ra.append(agent)
        if len(set(rr)) != len(rr) or len(set(ra)) != len(ra):
            raise ValueError("reviewer roles and agents must be unique")
        if set(wa) & set(ra):
            raise ValueError("reviewers must be independent")
        _require_path(self.completion_validator_path, "completion_validator_path")
        _require_tuple(self.completion_command, "completion_command")
        if not self.completion_command:
            raise ValueError("completion_command must be nonempty")
        for arg in self.completion_command:
            _require_builtin_str(arg, "completion argv", nonempty=False)
        if self.orchestration_profile_id is not None:
            _require_identifier(
                self.orchestration_profile_id, "orchestration_profile_id"
            )


class OwnershipManifestValidator:
    """Validate ownership relations against explicit chain, agents, and profile."""

    __slots__ = ()

    def execute(
        self,
        manifest: OwnershipManifestView,
        chain: ChainView,
        agents: tuple[AgentDescriptorView, ...],
        profile: ProjectProfile,
    ) -> ValidationResult:
        from .chains import ChainView
        from .profiles import ProjectProfile

        if (
            type(manifest) is not OwnershipManifestView
            or type(chain) is not ChainView
            or type(profile) is not ProjectProfile
        ):
            raise TypeError("invalid ownership argument type")
        _require_tuple(agents, "agents")
        if any(type(a) is not AgentDescriptorView for a in agents):
            raise TypeError("agents must contain AgentDescriptorView")
        issues = []
        tasks = {t.task_id: t for t in chain.tasks}
        agentmap = {a.agent_id: a for a in agents}
        if manifest.task_id not in tasks or (
            manifest.task_id in tasks
            and tasks[manifest.task_id].record_path != manifest.task_record_path
        ):
            issues.append(
                _issue(
                    "PIH.OWNERSHIP.TASK_MISMATCH",
                    "Manifest task binding differs from chain.",
                    manifest.task_id,
                    manifest.task_record_path,
                )
            )
        for role, agent, _scopes in manifest.writers:
            if agent not in agentmap or agentmap[agent].acceptance_role != "writer":
                issues.append(
                    _issue(
                        "PIH.OWNERSHIP.AGENT_MISMATCH",
                        "Writer agent is absent or not writable.",
                        agent,
                        related_ids=(role,),
                    )
                )
        for role, agent in manifest.reviewers:
            if agent not in agentmap or agentmap[agent].acceptance_role != "read_only":
                issues.append(
                    _issue(
                        "PIH.OWNERSHIP.AGENT_MISMATCH",
                        "Reviewer agent is absent or not read-only.",
                        agent,
                        related_ids=(role,),
                    )
                )
        owners = [s for _, _, ss in manifest.writers for s in ss]
        if not any(
            s.scope_kind == "file" and s.path == manifest.completion_validator_path
            for s in owners
        ):
            issues.append(
                _issue(
                    "PIH.OWNERSHIP.COMPLETION_INVALID",
                    "Completion validator is not file-owned.",
                    manifest.task_id,
                    manifest.completion_validator_path,
                )
            )
        if manifest.completion_validator_path not in manifest.completion_command:
            issues.append(
                _issue(
                    "PIH.OWNERSHIP.COMPLETION_INVALID",
                    "Completion command does not bind validator path.",
                    manifest.task_id,
                    manifest.completion_validator_path,
                )
            )
        if (
            manifest.orchestration_profile_id is not None
            and manifest.orchestration_profile_id != profile.profile_id
        ):
            issues.append(
                _issue(
                    "PIH.OWNERSHIP.PROFILE_UNSUPPORTED",
                    "Orchestration profile is unsupported.",
                    manifest.task_id,
                    related_ids=(manifest.orchestration_profile_id,),
                )
            )
        return _result(tuple(issues))
