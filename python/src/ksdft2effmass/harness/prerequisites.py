"""Explicit prerequisite-result contracts for the development Harness.

This module represents consumer-owned requirements separately from producer-owned
results.  Resolution is a pure software operation over explicit immutable inputs: it
performs no repository discovery, persistence, serialization, lifecycle inference,
selection, activation, authorization, repair, or successor choice.  A satisfied
resolution is therefore eligibility evidence only and grants no operation authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ._contract import require_identifier
from .identity import ContentIdentity
from .task import HarnessTask


def _version(value: object) -> None:
    if type(value) is not int:
        raise TypeError("schema_version must be a built-in int excluding bool")
    if value != 1:
        raise ValueError("schema_version must equal 1")


def _enum(value: object, enum_type: type[StrEnum], name: str) -> None:
    if type(value) is not enum_type:
        raise TypeError(f"{name} must be {enum_type.__name__}")


def _identity(value: object, name: str) -> None:
    require_identifier(value, name)


class DevelopmentPrerequisiteKind(StrEnum):
    """Distinguish canonical Task prerequisites from external prerequisites.

    Attributes
    ----------
    TASK
        A dependency on one canonical development Task result.
    EXTERNAL
        A dependency on an explicitly identified external result or event.
    """

    TASK = "task"
    EXTERNAL = "external"


class DevelopmentPrerequisiteLineage(StrEnum):
    """Describe the owner-reported effective state of one retained result.

    Attributes
    ----------
    EFFECTIVE
        The result is the owner's currently effective result.
    SUPERSEDED
        A named successor replaced the result.
    REVOKED
        A named revocation invalidated the result without a replacement claim.
    """

    EFFECTIVE = "effective"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"


class DevelopmentPrerequisiteLineagePolicy(StrEnum):
    """Select the accepted consumer policy for owner-reported result lineage.

    Attributes
    ----------
    EFFECTIVE_NOT_REVOKED
        Require exactly one effective result; superseded and revoked results do not
        satisfy the edge. This is the only accepted policy.
    """

    EFFECTIVE_NOT_REVOKED = "effective_not_revoked"


class DevelopmentPrerequisiteObservationStatus(StrEnum):
    """Describe one complete owner-bound observation of a prerequisite edge.

    Attributes
    ----------
    FOUND
        One or more retained result references were observed.
    ABSENT
        A complete successful observation established that no result exists.
    UNAVAILABLE
        An identified retained result could not be obtained.
    INDETERMINATE
        Observation, integrity, or version state could not be established.
    """

    FOUND = "found"
    ABSENT = "absent"
    UNAVAILABLE = "unavailable"
    INDETERMINATE = "indeterminate"


class DevelopmentPrerequisiteOutcome(StrEnum):
    """Closed outcome for one declared prerequisite edge.

    Attributes
    ----------
    SATISFIED
        Exactly one effective result matches every required binding.
    MISSING
        A complete owner observation established absence.
    CONFLICTING
        Effective candidates, observations, or lineage are contradictory.
    SUPERSEDED
        Only matching superseded results remain.
    REVOKED
        Only matching revoked results remain.
    UNAVAILABLE
        The correctly bound observation reports inaccessible retained state.
    INDETERMINATE
        Exact matching cannot be established.
    """

    SATISFIED = "satisfied"
    MISSING = "missing"
    CONFLICTING = "conflicting"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"
    UNAVAILABLE = "unavailable"
    INDETERMINATE = "indeterminate"


class DevelopmentPrerequisiteAggregateStatus(StrEnum):
    """Closed aggregate conclusion over every declared prerequisite edge.

    Attributes
    ----------
    SATISFIED
        Every declared edge is satisfied and no aggregate diagnostic exists.
    BLOCKED
        At least one edge is not satisfied or an aggregate diagnostic exists.
    """

    SATISFIED = "satisfied"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class DevelopmentPrerequisiteRequirement:
    """Define what owner-retained result satisfies one consumer prerequisite.

    Parameters
    ----------
    schema_version
        Built-in integer equal to 1.
    prerequisite_kind, prerequisite_id
        Exact kind and identity of the canonical Task edge.
    required_owner_id, required_result_kind, required_claim_id
        Exact domain owner, result type, and represented claim required by the
        consumer.
    required_producer_revision_id
        Exact producer or contract revision accepted by the consumer.
    retention_boundary_id
        Identity of the owner-controlled retention boundary from which the result
        observation was made.
    lineage_policy
        Exact accepted policy. Only ``effective_not_revoked`` is supported.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If the version or an identifier violates its accepted value grammar.
    """

    schema_version: int
    prerequisite_kind: DevelopmentPrerequisiteKind
    prerequisite_id: str
    required_owner_id: str
    required_result_kind: str
    required_claim_id: str
    required_producer_revision_id: str
    retention_boundary_id: str
    lineage_policy: DevelopmentPrerequisiteLineagePolicy

    def __post_init__(self) -> None:
        _version(self.schema_version)
        _enum(self.prerequisite_kind, DevelopmentPrerequisiteKind, "prerequisite_kind")
        _enum(
            self.lineage_policy,
            DevelopmentPrerequisiteLineagePolicy,
            "lineage_policy",
        )
        for name in (
            "prerequisite_id",
            "required_owner_id",
            "required_result_kind",
            "required_claim_id",
            "required_producer_revision_id",
            "retention_boundary_id",
        ):
            _identity(getattr(self, name), name)

    @property
    def edge_key(self) -> tuple[str, str]:
        """Return the deterministic represented edge key.

        Returns
        -------
        tuple[str, str]
            Exact ``(kind value, prerequisite identity)`` tuple.
        """
        return (self.prerequisite_kind.value, self.prerequisite_id)


@dataclass(frozen=True, slots=True)
class DevelopmentPrerequisiteContract:
    """Bind complete consumer requirements to one exact Task content identity.

    Parameters
    ----------
    schema_version
        Built-in integer equal to 1.
    contract_id
        Stable identity of this consumer-scoped contract.
    consumer_task_id
        Exact canonical consumer Task identity.
    consumer_task_content_identity
        SHA-256 identity of the exact consumer Task source bytes.
    requirements
        Built-in tuple of requirements in increasing edge-key order. Incomplete
        contracts are representable; exact coverage against the supplied Task is
        checked by :class:`DevelopmentPrerequisiteResolver`.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If the version, identifiers, requirement uniqueness, or ordering is invalid.
    """

    schema_version: int
    contract_id: str
    consumer_task_id: str
    consumer_task_content_identity: ContentIdentity
    requirements: tuple[DevelopmentPrerequisiteRequirement, ...]

    def __post_init__(self) -> None:
        _version(self.schema_version)
        _identity(self.contract_id, "contract_id")
        _identity(self.consumer_task_id, "consumer_task_id")
        if type(self.consumer_task_content_identity) is not ContentIdentity:
            raise TypeError("consumer_task_content_identity must be ContentIdentity")
        if type(self.requirements) is not tuple:
            raise TypeError("requirements must be a tuple")
        if any(
            type(item) is not DevelopmentPrerequisiteRequirement
            for item in self.requirements
        ):
            raise TypeError(
                "requirements must contain DevelopmentPrerequisiteRequirement"
            )
        keys = tuple(item.edge_key for item in self.requirements)
        if keys != tuple(sorted(set(keys))):
            raise ValueError("requirements must be unique and sorted by edge key")


@dataclass(frozen=True, slots=True)
class RetainedPrerequisiteResultReference:
    """Reference one exact owner-retained result without copying its payload.

    Parameters
    ----------
    schema_version
        Built-in integer equal to 1.
    prerequisite_kind, prerequisite_id
        Exact represented canonical edge.
    owner_id, result_id, result_kind, claim_id
        Exact domain owner, retained result identity and kind, and represented claim.
    producer_revision_id, retention_boundary_id
        Exact producer revision and owner-controlled retention boundary.
    content_identity
        SHA-256 identity of the exact retained result bytes.
    lineage
        Owner-reported effective, superseded, or revoked state. This represented state
        is not independently authenticated by the reference.
    superseding_result_id, revocation_id
        Optional built-in-string lineage companion identity. The former is present
        only for ``superseded``; the latter only for ``revoked``.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If version, identifier, or lineage companion invariants fail.
    """

    schema_version: int
    prerequisite_kind: DevelopmentPrerequisiteKind
    prerequisite_id: str
    owner_id: str
    result_id: str
    result_kind: str
    claim_id: str
    producer_revision_id: str
    retention_boundary_id: str
    content_identity: ContentIdentity
    lineage: DevelopmentPrerequisiteLineage
    superseding_result_id: str | None
    revocation_id: str | None

    def __post_init__(self) -> None:
        _version(self.schema_version)
        _enum(self.prerequisite_kind, DevelopmentPrerequisiteKind, "prerequisite_kind")
        _enum(self.lineage, DevelopmentPrerequisiteLineage, "lineage")
        for name in (
            "prerequisite_id",
            "owner_id",
            "result_id",
            "result_kind",
            "claim_id",
            "producer_revision_id",
            "retention_boundary_id",
        ):
            _identity(getattr(self, name), name)
        if type(self.content_identity) is not ContentIdentity:
            raise TypeError("content_identity must be ContentIdentity")
        if self.superseding_result_id is not None:
            _identity(self.superseding_result_id, "superseding_result_id")
        if self.revocation_id is not None:
            _identity(self.revocation_id, "revocation_id")
        expected = {
            DevelopmentPrerequisiteLineage.EFFECTIVE: (False, False),
            DevelopmentPrerequisiteLineage.SUPERSEDED: (True, False),
            DevelopmentPrerequisiteLineage.REVOKED: (False, True),
        }[self.lineage]
        observed = (
            self.superseding_result_id is not None,
            self.revocation_id is not None,
        )
        if observed != expected:
            raise ValueError(
                "lineage requires its exact supersession or revocation fields"
            )


@dataclass(frozen=True, slots=True)
class RetainedPrerequisiteObservation:
    """Represent one complete explicit observation for a declared edge.

    Parameters
    ----------
    schema_version
        Built-in integer equal to 1.
    prerequisite_kind, prerequisite_id
        Exact observed edge.
    owner_id, retention_boundary_id
        Exact result owner and owner-controlled retention boundary that performed the
        observation. These bind every status, including negative observations.
    status
        Closed found, absent, unavailable, or indeterminate observation state.
    references
        Owner-retained references; nonempty only for ``found``.
    diagnostic_id
        Owner-supplied diagnostic identity, required only for ``unavailable`` and
        ``indeterminate``.

    Notes
    -----
    ``absent`` means that the complete owner observation established no result. It is
    distinct from failure to observe a result.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If version, identifier, or status-dependent field invariants fail.
    """

    schema_version: int
    prerequisite_kind: DevelopmentPrerequisiteKind
    prerequisite_id: str
    owner_id: str
    retention_boundary_id: str
    status: DevelopmentPrerequisiteObservationStatus
    references: tuple[RetainedPrerequisiteResultReference, ...]
    diagnostic_id: str | None

    def __post_init__(self) -> None:
        _version(self.schema_version)
        _enum(self.prerequisite_kind, DevelopmentPrerequisiteKind, "prerequisite_kind")
        _enum(self.status, DevelopmentPrerequisiteObservationStatus, "status")
        _identity(self.prerequisite_id, "prerequisite_id")
        _identity(self.owner_id, "owner_id")
        _identity(self.retention_boundary_id, "retention_boundary_id")
        if type(self.references) is not tuple:
            raise TypeError("references must be a tuple")
        if any(
            type(item) is not RetainedPrerequisiteResultReference
            for item in self.references
        ):
            raise TypeError(
                "references must contain RetainedPrerequisiteResultReference"
            )
        if self.diagnostic_id is not None:
            _identity(self.diagnostic_id, "diagnostic_id")
        if self.status is DevelopmentPrerequisiteObservationStatus.FOUND:
            if not self.references or self.diagnostic_id is not None:
                raise ValueError(
                    "found observation requires references and no diagnostic"
                )
        elif self.status is DevelopmentPrerequisiteObservationStatus.ABSENT:
            if self.references or self.diagnostic_id is not None:
                raise ValueError(
                    "absent observation contains no references or diagnostic"
                )
        elif self.references or self.diagnostic_id is None:
            raise ValueError("unavailable or indeterminate requires only a diagnostic")

    @property
    def edge_key(self) -> tuple[str, str]:
        """Return the deterministic represented edge key.

        Returns
        -------
        tuple[str, str]
            Exact ``(kind value, prerequisite identity)`` tuple.
        """
        return (self.prerequisite_kind.value, self.prerequisite_id)


@dataclass(frozen=True, slots=True)
class DevelopmentPrerequisiteEdgeResult:
    """Record the resolver outcome for one exact declared edge.

    Parameters
    ----------
    prerequisite_kind, prerequisite_id
        Exact resolved canonical edge.
    outcome
        Closed satisfied, missing, conflicting, superseded, revoked, unavailable, or
        indeterminate conclusion.
    matched_result_id
        Exact effective result identity for ``satisfied``; otherwise ``None``.
    diagnostic_ids
        Built-in tuple of sorted unique diagnostic identities explaining
        non-satisfied conclusions.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If identifiers, ordering, or outcome-dependent result fields are invalid.
    """

    prerequisite_kind: DevelopmentPrerequisiteKind
    prerequisite_id: str
    outcome: DevelopmentPrerequisiteOutcome
    matched_result_id: str | None
    diagnostic_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _enum(self.prerequisite_kind, DevelopmentPrerequisiteKind, "prerequisite_kind")
        _enum(self.outcome, DevelopmentPrerequisiteOutcome, "outcome")
        _identity(self.prerequisite_id, "prerequisite_id")
        if self.matched_result_id is not None:
            _identity(self.matched_result_id, "matched_result_id")
        if type(self.diagnostic_ids) is not tuple:
            raise TypeError("diagnostic_ids must be a tuple")
        for item in self.diagnostic_ids:
            _identity(item, "diagnostic_id")
        if self.diagnostic_ids != tuple(sorted(set(self.diagnostic_ids))):
            raise ValueError("diagnostic_ids must be sorted and unique")
        if (self.outcome is DevelopmentPrerequisiteOutcome.SATISFIED) != (
            self.matched_result_id is not None
        ):
            raise ValueError("only satisfied outcomes contain a matched result")
        if (
            self.outcome is DevelopmentPrerequisiteOutcome.SATISFIED
            and self.diagnostic_ids
        ):
            raise ValueError("satisfied outcomes contain no diagnostics")


@dataclass(frozen=True, slots=True)
class DevelopmentPrerequisiteResolutionResult:
    """Record complete prerequisite resolution without granting authority.

    Parameters
    ----------
    consumer_task_id, consumer_task_content_identity
        Exact consumer Task identity and SHA-256 source-byte identity.
    contract_id
        Exact consumer sidecar contract identity.
    status
        ``satisfied`` only when every edge result is satisfied; otherwise ``blocked``.
    edge_results
        Complete unique edge-key-sorted resolution tuple.
    diagnostic_ids
        Built-in tuple of sorted unique aggregate diagnostics, including Task-binding,
        edge-coverage, and undeclared-observation failures.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If identifiers, ordering, or aggregate-status invariants fail.
    """

    consumer_task_id: str
    consumer_task_content_identity: ContentIdentity
    contract_id: str
    status: DevelopmentPrerequisiteAggregateStatus
    edge_results: tuple[DevelopmentPrerequisiteEdgeResult, ...]
    diagnostic_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _identity(self.consumer_task_id, "consumer_task_id")
        _identity(self.contract_id, "contract_id")
        if type(self.consumer_task_content_identity) is not ContentIdentity:
            raise TypeError("consumer_task_content_identity must be ContentIdentity")
        _enum(self.status, DevelopmentPrerequisiteAggregateStatus, "status")
        if type(self.edge_results) is not tuple or any(
            type(item) is not DevelopmentPrerequisiteEdgeResult
            for item in self.edge_results
        ):
            raise TypeError(
                "edge_results must contain DevelopmentPrerequisiteEdgeResult"
            )
        keys = tuple(
            (item.prerequisite_kind.value, item.prerequisite_id)
            for item in self.edge_results
        )
        if keys != tuple(sorted(set(keys))):
            raise ValueError("edge_results must be unique and sorted by edge key")
        if type(self.diagnostic_ids) is not tuple:
            raise TypeError("diagnostic_ids must be a tuple")
        for item in self.diagnostic_ids:
            _identity(item, "diagnostic_id")
        if self.diagnostic_ids != tuple(sorted(set(self.diagnostic_ids))):
            raise ValueError("diagnostic_ids must be sorted and unique")
        all_satisfied = not self.diagnostic_ids and all(
            item.outcome is DevelopmentPrerequisiteOutcome.SATISFIED
            for item in self.edge_results
        )
        expected = (
            DevelopmentPrerequisiteAggregateStatus.SATISFIED
            if all_satisfied
            else DevelopmentPrerequisiteAggregateStatus.BLOCKED
        )
        if self.status is not expected:
            raise ValueError("aggregate status must reflect every edge outcome")

    @property
    def is_satisfied(self) -> bool:
        """Return whether the aggregate is exactly satisfied.

        Returns
        -------
        bool
            ``True`` only when every edge is satisfied and no aggregate diagnostic
            exists.
        """
        return self.status is DevelopmentPrerequisiteAggregateStatus.SATISFIED


class DevelopmentPrerequisiteResolver:
    """Resolve explicit owner observations against one consumer sidecar contract.

    The fieldless ActionObject returns deterministic findings for incompatible Task
    binding, edge coverage, observation coverage, result matching, and lineage. It
    never inspects ``HarnessTask.status`` or ambient repository state.
    """

    __slots__ = ()

    def execute(
        self,
        task: HarnessTask,
        task_content_identity: ContentIdentity,
        contract: DevelopmentPrerequisiteContract,
        observations: tuple[RetainedPrerequisiteObservation, ...],
    ) -> DevelopmentPrerequisiteResolutionResult:
        """Return the complete resolution for one exact consumer Task.

        Parameters
        ----------
        task
            Exact canonical consumer Task. Its opaque lifecycle status is ignored.
        task_content_identity
            SHA-256 identity of the supplied Task source bytes.
        contract
            Consumer sidecar expected to bind exactly to ``task`` and every edge.
        observations
            Complete explicit owner observations; no ambient lookup is performed.

        Returns
        -------
        DevelopmentPrerequisiteResolutionResult
            Immutable edge outcomes and aggregate eligibility conclusion.

        Raises
        ------
        TypeError
            If an input has the wrong semantic public type.
        """
        if type(task) is not HarnessTask:
            raise TypeError("task must be HarnessTask")
        if type(task_content_identity) is not ContentIdentity:
            raise TypeError("task_content_identity must be ContentIdentity")
        if type(contract) is not DevelopmentPrerequisiteContract:
            raise TypeError("contract must be DevelopmentPrerequisiteContract")
        if type(observations) is not tuple or any(
            type(item) is not RetainedPrerequisiteObservation for item in observations
        ):
            raise TypeError("observations must contain RetainedPrerequisiteObservation")

        declared = tuple(
            sorted(
                (
                    *(
                        (DevelopmentPrerequisiteKind.TASK, item)
                        for item in task.task_prerequisite_ids
                    ),
                    *(
                        (DevelopmentPrerequisiteKind.EXTERNAL, item)
                        for item in task.external_prerequisite_ids
                    ),
                ),
                key=lambda item: (item[0].value, item[1]),
            )
        )
        declared_keys = tuple((kind.value, identifier) for kind, identifier in declared)
        requirement_by_key = {item.edge_key: item for item in contract.requirements}
        observation_by_key: dict[
            tuple[str, str], list[RetainedPrerequisiteObservation]
        ] = {}
        for item in observations:
            observation_by_key.setdefault(item.edge_key, []).append(item)

        global_diagnostics: set[str] = set()
        binding_ok = contract.consumer_task_id == task.task_id
        if not binding_ok:
            global_diagnostics.add("prerequisite.contract.task-id-mismatch")
        if contract.consumer_task_content_identity != task_content_identity:
            binding_ok = False
            global_diagnostics.add("prerequisite.contract.task-content-mismatch")
        if tuple(requirement_by_key) != declared_keys:
            binding_ok = False
            global_diagnostics.add("prerequisite.contract.edge-coverage-mismatch")
        extra_observations = set(observation_by_key) - set(declared_keys)
        if extra_observations:
            global_diagnostics.add("prerequisite.observation.undeclared-edge")

        edge_results: list[DevelopmentPrerequisiteEdgeResult] = []
        for kind, identifier in declared:
            key = (kind.value, identifier)
            if not binding_ok or key not in requirement_by_key:
                edge_results.append(
                    self._edge(
                        kind,
                        identifier,
                        DevelopmentPrerequisiteOutcome.INDETERMINATE,
                        "prerequisite.contract.invalid",
                    )
                )
                continue
            candidates = observation_by_key.get(key, [])
            if len(candidates) != 1:
                outcome = (
                    DevelopmentPrerequisiteOutcome.CONFLICTING
                    if len(candidates) > 1
                    else DevelopmentPrerequisiteOutcome.INDETERMINATE
                )
                code = (
                    "prerequisite.observation.duplicate"
                    if candidates
                    else "prerequisite.observation.missing"
                )
                edge_results.append(self._edge(kind, identifier, outcome, code))
                continue
            edge_results.append(
                self._resolve_edge(requirement_by_key[key], candidates[0])
            )

        status = (
            DevelopmentPrerequisiteAggregateStatus.SATISFIED
            if not global_diagnostics
            and all(
                item.outcome is DevelopmentPrerequisiteOutcome.SATISFIED
                for item in edge_results
            )
            else DevelopmentPrerequisiteAggregateStatus.BLOCKED
        )
        return DevelopmentPrerequisiteResolutionResult(
            task.task_id,
            task_content_identity,
            contract.contract_id,
            status,
            tuple(edge_results),
            tuple(sorted(global_diagnostics)),
        )

    @staticmethod
    def _edge(
        kind: DevelopmentPrerequisiteKind,
        identifier: str,
        outcome: DevelopmentPrerequisiteOutcome,
        diagnostic: str,
    ) -> DevelopmentPrerequisiteEdgeResult:
        return DevelopmentPrerequisiteEdgeResult(
            kind, identifier, outcome, None, (diagnostic,)
        )

    def _resolve_edge(
        self,
        requirement: DevelopmentPrerequisiteRequirement,
        observation: RetainedPrerequisiteObservation,
    ) -> DevelopmentPrerequisiteEdgeResult:
        if (
            observation.owner_id != requirement.required_owner_id
            or observation.retention_boundary_id != requirement.retention_boundary_id
        ):
            return self._edge(
                requirement.prerequisite_kind,
                requirement.prerequisite_id,
                DevelopmentPrerequisiteOutcome.INDETERMINATE,
                "prerequisite.observation.binding-mismatch",
            )
        status_map = {
            DevelopmentPrerequisiteObservationStatus.ABSENT: (
                DevelopmentPrerequisiteOutcome.MISSING
            ),
            DevelopmentPrerequisiteObservationStatus.UNAVAILABLE: (
                DevelopmentPrerequisiteOutcome.UNAVAILABLE
            ),
            DevelopmentPrerequisiteObservationStatus.INDETERMINATE: (
                DevelopmentPrerequisiteOutcome.INDETERMINATE
            ),
        }
        if observation.status is not DevelopmentPrerequisiteObservationStatus.FOUND:
            outcome = status_map[observation.status]
            diagnostics = (
                ()
                if observation.diagnostic_id is None
                else (observation.diagnostic_id,)
            )
            return DevelopmentPrerequisiteEdgeResult(
                requirement.prerequisite_kind,
                requirement.prerequisite_id,
                outcome,
                None,
                diagnostics,
            )

        references = observation.references
        if (
            requirement.lineage_policy
            is not DevelopmentPrerequisiteLineagePolicy.EFFECTIVE_NOT_REVOKED
        ):
            return self._edge(
                requirement.prerequisite_kind,
                requirement.prerequisite_id,
                DevelopmentPrerequisiteOutcome.INDETERMINATE,
                "prerequisite.requirement.unsupported-lineage-policy",
            )
        if any(
            reference.prerequisite_kind is not requirement.prerequisite_kind
            or reference.prerequisite_id != requirement.prerequisite_id
            or reference.owner_id != requirement.required_owner_id
            or reference.result_kind != requirement.required_result_kind
            or reference.claim_id != requirement.required_claim_id
            or reference.producer_revision_id
            != requirement.required_producer_revision_id
            or reference.retention_boundary_id != requirement.retention_boundary_id
            for reference in references
        ):
            return self._edge(
                requirement.prerequisite_kind,
                requirement.prerequisite_id,
                DevelopmentPrerequisiteOutcome.INDETERMINATE,
                "prerequisite.result.binding-mismatch",
            )
        if len({reference.result_id for reference in references}) != len(references):
            return self._edge(
                requirement.prerequisite_kind,
                requirement.prerequisite_id,
                DevelopmentPrerequisiteOutcome.CONFLICTING,
                "prerequisite.result.duplicate-identity",
            )
        effective = [
            item
            for item in references
            if item.lineage is DevelopmentPrerequisiteLineage.EFFECTIVE
        ]
        stale = {
            item.lineage
            for item in references
            if item.lineage is not DevelopmentPrerequisiteLineage.EFFECTIVE
        }
        if len(effective) > 1:
            return self._edge(
                requirement.prerequisite_kind,
                requirement.prerequisite_id,
                DevelopmentPrerequisiteOutcome.CONFLICTING,
                "prerequisite.result.multiple-effective",
            )
        if len(effective) == 1:
            return DevelopmentPrerequisiteEdgeResult(
                requirement.prerequisite_kind,
                requirement.prerequisite_id,
                DevelopmentPrerequisiteOutcome.SATISFIED,
                effective[0].result_id,
                (),
            )
        if stale == {DevelopmentPrerequisiteLineage.SUPERSEDED}:
            outcome = DevelopmentPrerequisiteOutcome.SUPERSEDED
            diagnostic = "prerequisite.result.superseded"
        elif stale == {DevelopmentPrerequisiteLineage.REVOKED}:
            outcome = DevelopmentPrerequisiteOutcome.REVOKED
            diagnostic = "prerequisite.result.revoked"
        else:
            outcome = DevelopmentPrerequisiteOutcome.CONFLICTING
            diagnostic = "prerequisite.result.lineage-conflict"
        return self._edge(
            requirement.prerequisite_kind,
            requirement.prerequisite_id,
            outcome,
            diagnostic,
        )
