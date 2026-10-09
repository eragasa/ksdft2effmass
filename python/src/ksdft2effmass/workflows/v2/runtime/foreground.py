"""Typed foreground effect records and application-owned worker boundaries.

The records in this module describe one bounded foreground effect attempt.  They
contain compact identities and evidence references only.  Application packages
implement workers and reconcilers; this module does not import providers,
scientific packages, subprocesses, networks, clocks, or filesystem APIs.
"""

from __future__ import annotations

import hashlib
import json
import re
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import final

from ksdft2effmass.base import (
    DataObjectActionizer,
    DataObjectActionRequest,
    DataObjectActionResult,
)
from ksdft2effmass.base.identity import AbstractIdentity
from ksdft2effmass.base.immutable import AbstractImmutableDataObject
from ksdft2effmass.workflows.v2.core import (
    WorkflowAdapterIdentity,
    WorkflowAuthorityReferenceIdentity,
    WorkflowDefinitionIdentity,
)

from .records import (
    WORKFLOW_RUNTIME_CONTRACT_VERSION,
    WorkflowOccurrenceIdentity,
    WorkflowRuntimeEvidenceReference,
)

_MAX_REFERENCES = 256
_MAX_PLAN_EFFECT_INTENTS = 251
_MAX_EXECUTION_REFERENCES = 251
_MAX_RECONCILIATION_REFERENCES = 253
_MAX_REASONS = 64
_MAX_EVIDENCE_REASONS = 63
_MAX_ATTEMPTS = 64
_RUNTIME_REFERENCE_KINDS = frozenset(
    {
        "adapter",
        "adapter-configuration",
        "authority-verification",
        "dispatch-authorization",
        "effect-intent",
        "execution-evidence",
        "final-effect-intent",
        "foreground-plan",
        "reconciliation-evidence",
        "workflow-attempt",
        "workflow-definition",
        "workflow-reconciler",
        "workflow-worker",
    }
)
_NAMED_IDENTITY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{0,511}$", re.ASCII)
_DIGEST = re.compile(r"[0-9a-f]{64}", re.ASCII)


def _named_identity(value: str, field: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    if _NAMED_IDENTITY.fullmatch(value) is None:
        raise ValueError(f"{field} has an invalid identity grammar")


def _digest_identity(value: str, field: str) -> None:
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        raise ValueError(f"{field} must be 64 lowercase hexadecimal characters")


def _content_identity(domain: str, parts: list[object]) -> str:
    payload = json.dumps(
        {"domain": domain, "parts": parts},
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _references(
    values: tuple[WorkflowRuntimeEvidenceReference, ...],
    field: str,
) -> tuple[WorkflowRuntimeEvidenceReference, ...]:
    if type(values) is not tuple:
        raise TypeError(f"{field} must be a tuple")
    if len(values) > _MAX_REFERENCES:
        raise ValueError(f"{field} exceeds its bound")
    if any(type(value) is not WorkflowRuntimeEvidenceReference for value in values):
        raise TypeError(f"{field} must contain WorkflowRuntimeEvidenceReference")
    canonical = tuple(sorted(set(values)))
    if canonical != values:
        raise ValueError(f"{field} must be unique and canonical")
    return values


def _reasons(values: tuple[str, ...]) -> tuple[str, ...]:
    if type(values) is not tuple:
        raise TypeError("reason_codes must be a tuple")
    if not values or len(values) > _MAX_REASONS:
        raise ValueError("reason_codes must be nonempty and bounded")
    for value in values:
        _named_identity(value, "reason_code")
    canonical = tuple(sorted(set(values)))
    if canonical != values:
        raise ValueError("reason_codes must be unique and canonical")
    return values


def _application_evidence(
    values: tuple[WorkflowRuntimeEvidenceReference, ...],
    *,
    maximum: int,
    field: str,
) -> tuple[WorkflowRuntimeEvidenceReference, ...]:
    references = _references(values, field)
    if len(references) > maximum:
        raise ValueError(f"{field} exceeds its event-envelope bound")
    if any(
        reference.reference_kind in _RUNTIME_REFERENCE_KINDS for reference in references
    ):
        raise ValueError(f"{field} uses a runtime-reserved reference kind")
    return references


def _evidence_reasons(
    values: tuple[str, ...],
    *,
    reserved_outcomes: frozenset[str],
) -> tuple[str, ...]:
    reasons = _reasons(values)
    if len(reasons) > _MAX_EVIDENCE_REASONS:
        raise ValueError("reason_codes exceed their event-envelope bound")
    if reserved_outcomes.intersection(reasons):
        raise ValueError("reason_codes use a runtime-reserved outcome code")
    return reasons


def _reference_parts(
    values: tuple[WorkflowRuntimeEvidenceReference, ...],
) -> list[list[str]]:
    return [
        [reference.reference_kind, reference.reference_identity] for reference in values
    ]


@dataclass(frozen=True, slots=True)
class WorkflowAdapterConfigurationIdentity(AbstractIdentity):
    """Identity of one immutable application adapter configuration."""

    value: str

    def __post_init__(self) -> None:
        _named_identity(self.value, "adapter configuration identity")


@dataclass(frozen=True, slots=True)
class WorkflowForegroundWorkerIdentity(AbstractIdentity):
    """Identity of one exact foreground worker implementation or class."""

    value: str

    def __post_init__(self) -> None:
        _named_identity(self.value, "foreground worker identity")


@dataclass(frozen=True, slots=True)
class WorkflowEffectReconcilerIdentity(AbstractIdentity):
    """Nominal identity of one application-owned query-only reconciler."""

    value: str

    def __post_init__(self) -> None:
        _named_identity(self.value, "workflow effect reconciler identity")


@dataclass(frozen=True, slots=True)
class WorkflowEffectIntentIdentity(AbstractIdentity):
    """Content identity of one effect intent."""

    value: str

    def __post_init__(self) -> None:
        _digest_identity(self.value, "effect intent identity")


@dataclass(frozen=True, slots=True)
class WorkflowPlanIdentity(AbstractIdentity):
    """Content identity of one deterministic foreground plan."""

    value: str

    def __post_init__(self) -> None:
        _digest_identity(self.value, "plan identity")


@dataclass(frozen=True, slots=True)
class WorkflowAttemptIdentity(AbstractIdentity):
    """Content identity of one ordinal effect attempt."""

    value: str

    def __post_init__(self) -> None:
        _digest_identity(self.value, "attempt identity")

    @classmethod
    def create(
        cls,
        *,
        occurrence_identity: WorkflowOccurrenceIdentity,
        effect_intent_identity: WorkflowEffectIntentIdentity,
        attempt_ordinal: int,
    ) -> WorkflowAttemptIdentity:
        """Derive an attempt identity from one occurrence and intent."""
        if type(occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(effect_intent_identity) is not WorkflowEffectIntentIdentity:
            raise TypeError(
                "effect_intent_identity must be WorkflowEffectIntentIdentity"
            )
        if type(attempt_ordinal) is not int or attempt_ordinal < 1:
            raise ValueError("attempt_ordinal must be a positive built-in int")
        return cls(
            _content_identity(
                "workflow-attempt:1",
                [
                    occurrence_identity.value,
                    effect_intent_identity.value,
                    attempt_ordinal,
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )


@dataclass(frozen=True, slots=True)
class WorkflowAuthorityVerificationIdentity(AbstractIdentity):
    """Content identity of one application-owned authority verification."""

    value: str

    def __post_init__(self) -> None:
        _digest_identity(self.value, "authority verification identity")


@dataclass(frozen=True, slots=True)
class WorkflowDispatchAuthorizationIdentity(AbstractIdentity):
    """Content identity of one attempt-bound dispatch authorization."""

    value: str

    def __post_init__(self) -> None:
        _digest_identity(self.value, "dispatch authorization identity")


@dataclass(frozen=True, slots=True)
class WorkflowExecutionEvidenceIdentity(AbstractIdentity):
    """Content identity of one foreground worker report."""

    value: str

    def __post_init__(self) -> None:
        _digest_identity(self.value, "execution evidence identity")


@dataclass(frozen=True, slots=True)
class WorkflowReconciliationEvidenceIdentity(AbstractIdentity):
    """Content identity of one query-only reconciliation report."""

    value: str

    def __post_init__(self) -> None:
        _digest_identity(self.value, "reconciliation evidence identity")


class WorkflowEffectCapability(StrEnum):
    """Closed external idempotency and lookup capability declaration."""

    IDEMPOTENT_EXECUTION = "idempotent_execution"
    LOOKUP = "lookup"
    IDEMPOTENT_EXECUTION_AND_LOOKUP = "idempotent_execution_and_lookup"
    NEITHER = "neither"


@dataclass(frozen=True, slots=True)
class WorkflowEffectIntent(AbstractImmutableDataObject):
    """Bounded effect proposal produced by an application planner."""

    identity: WorkflowEffectIntentIdentity
    occurrence_identity: WorkflowOccurrenceIdentity
    ordinal: int
    operation_kind: str
    adapter_identity: WorkflowAdapterIdentity
    adapter_configuration_identity: WorkflowAdapterConfigurationIdentity
    input_references: tuple[WorkflowRuntimeEvidenceReference, ...]
    expected_output_contract: str
    capability: WorkflowEffectCapability
    external_idempotency_token: str
    contract_version: str = WORKFLOW_RUNTIME_CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        occurrence_identity: WorkflowOccurrenceIdentity,
        ordinal: int,
        operation_kind: str,
        adapter_identity: WorkflowAdapterIdentity,
        adapter_configuration_identity: WorkflowAdapterConfigurationIdentity,
        input_references: tuple[WorkflowRuntimeEvidenceReference, ...],
        expected_output_contract: str,
        capability: WorkflowEffectCapability,
    ) -> WorkflowEffectIntent:
        """Create one content-identified effect intent without executing it."""
        if type(occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(ordinal) is not int or ordinal < 0:
            raise ValueError("ordinal must be a nonnegative built-in int")
        _named_identity(operation_kind, "operation_kind")
        if type(adapter_identity) is not WorkflowAdapterIdentity:
            raise TypeError("adapter_identity must be WorkflowAdapterIdentity")
        if (
            type(adapter_configuration_identity)
            is not WorkflowAdapterConfigurationIdentity
        ):
            raise TypeError(
                "adapter_configuration_identity must be "
                "WorkflowAdapterConfigurationIdentity"
            )
        references = _references(input_references, "input_references")
        _named_identity(expected_output_contract, "expected_output_contract")
        if type(capability) is not WorkflowEffectCapability:
            raise TypeError("capability must be WorkflowEffectCapability")
        parts: list[object] = [
            occurrence_identity.value,
            ordinal,
            operation_kind,
            adapter_identity.value,
            adapter_configuration_identity.value,
            _reference_parts(references),
            expected_output_contract,
            capability.value,
            WORKFLOW_RUNTIME_CONTRACT_VERSION,
        ]
        identity = WorkflowEffectIntentIdentity(
            _content_identity("workflow-effect-intent:1", parts)
        )
        token = hashlib.sha256(
            (
                "workflow-external-idempotency:1\0"
                + occurrence_identity.value
                + "\0"
                + identity.value
            ).encode("utf-8")
        ).hexdigest()
        return cls(
            identity,
            occurrence_identity,
            ordinal,
            operation_kind,
            adapter_identity,
            adapter_configuration_identity,
            references,
            expected_output_contract,
            capability,
            token,
        )

    def __post_init__(self) -> None:
        if type(self.identity) is not WorkflowEffectIntentIdentity:
            raise TypeError("identity must be WorkflowEffectIntentIdentity")
        if type(self.occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(self.ordinal) is not int or self.ordinal < 0:
            raise ValueError("ordinal must be a nonnegative built-in int")
        _named_identity(self.operation_kind, "operation_kind")
        if type(self.adapter_identity) is not WorkflowAdapterIdentity:
            raise TypeError("adapter_identity must be WorkflowAdapterIdentity")
        if (
            type(self.adapter_configuration_identity)
            is not WorkflowAdapterConfigurationIdentity
        ):
            raise TypeError(
                "adapter_configuration_identity must be "
                "WorkflowAdapterConfigurationIdentity"
            )
        references = _references(self.input_references, "input_references")
        _named_identity(self.expected_output_contract, "expected_output_contract")
        if type(self.capability) is not WorkflowEffectCapability:
            raise TypeError("capability must be WorkflowEffectCapability")
        expected_identity = WorkflowEffectIntentIdentity(
            _content_identity(
                "workflow-effect-intent:1",
                [
                    self.occurrence_identity.value,
                    self.ordinal,
                    self.operation_kind,
                    self.adapter_identity.value,
                    self.adapter_configuration_identity.value,
                    _reference_parts(references),
                    self.expected_output_contract,
                    self.capability.value,
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        expected_token = hashlib.sha256(
            (
                "workflow-external-idempotency:1\0"
                + self.occurrence_identity.value
                + "\0"
                + expected_identity.value
            ).encode("utf-8")
        ).hexdigest()
        if (
            self.identity != expected_identity
            or self.external_idempotency_token != expected_token
            or self.contract_version != WORKFLOW_RUNTIME_CONTRACT_VERSION
        ):
            raise ValueError("effect intent content is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowForegroundPlan(AbstractImmutableDataObject):
    """Deterministic ordered plan for one reserved occurrence."""

    identity: WorkflowPlanIdentity
    occurrence_identity: WorkflowOccurrenceIdentity
    definition_identity: WorkflowDefinitionIdentity
    adapter_identity: WorkflowAdapterIdentity
    adapter_configuration_identity: WorkflowAdapterConfigurationIdentity
    effect_intents: tuple[WorkflowEffectIntent, ...]
    maximum_attempts_per_intent: int
    contract_version: str = WORKFLOW_RUNTIME_CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        occurrence_identity: WorkflowOccurrenceIdentity,
        definition_identity: WorkflowDefinitionIdentity,
        adapter_identity: WorkflowAdapterIdentity,
        adapter_configuration_identity: WorkflowAdapterConfigurationIdentity,
        effect_intents: tuple[WorkflowEffectIntent, ...],
        maximum_attempts_per_intent: int,
    ) -> WorkflowForegroundPlan:
        """Create a nonempty plan from exact ordered intent identities."""
        if type(occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(definition_identity) is not WorkflowDefinitionIdentity:
            raise TypeError("definition_identity must be WorkflowDefinitionIdentity")
        if type(adapter_identity) is not WorkflowAdapterIdentity:
            raise TypeError("adapter_identity must be WorkflowAdapterIdentity")
        if (
            type(adapter_configuration_identity)
            is not WorkflowAdapterConfigurationIdentity
        ):
            raise TypeError(
                "adapter_configuration_identity must be "
                "WorkflowAdapterConfigurationIdentity"
            )
        if type(effect_intents) is not tuple or not effect_intents:
            raise ValueError("effect_intents must be a nonempty tuple")
        if len(effect_intents) > _MAX_PLAN_EFFECT_INTENTS:
            raise ValueError("effect_intents exceed their event-envelope bound")
        if any(type(value) is not WorkflowEffectIntent for value in effect_intents):
            raise TypeError("effect_intents must contain WorkflowEffectIntent")
        if any(
            value.occurrence_identity != occurrence_identity
            or value.adapter_identity != adapter_identity
            or value.adapter_configuration_identity != adapter_configuration_identity
            or value.ordinal != ordinal
            for ordinal, value in enumerate(effect_intents)
        ):
            raise ValueError("effect intents do not form one canonical plan")
        if len({value.identity for value in effect_intents}) != len(effect_intents):
            raise ValueError("effect intent identities must be unique")
        if (
            type(maximum_attempts_per_intent) is not int
            or not 1 <= maximum_attempts_per_intent <= _MAX_ATTEMPTS
        ):
            raise ValueError("maximum_attempts_per_intent is outside its bound")
        identity = WorkflowPlanIdentity(
            _content_identity(
                "workflow-foreground-plan:1",
                [
                    occurrence_identity.value,
                    definition_identity.value,
                    adapter_identity.value,
                    adapter_configuration_identity.value,
                    [value.identity.value for value in effect_intents],
                    maximum_attempts_per_intent,
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        return cls(
            identity,
            occurrence_identity,
            definition_identity,
            adapter_identity,
            adapter_configuration_identity,
            effect_intents,
            maximum_attempts_per_intent,
        )

    def __post_init__(self) -> None:
        if type(self.identity) is not WorkflowPlanIdentity:
            raise TypeError("identity must be WorkflowPlanIdentity")
        if type(self.occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(self.definition_identity) is not WorkflowDefinitionIdentity:
            raise TypeError("definition_identity must be WorkflowDefinitionIdentity")
        if type(self.adapter_identity) is not WorkflowAdapterIdentity:
            raise TypeError("adapter_identity must be WorkflowAdapterIdentity")
        if (
            type(self.adapter_configuration_identity)
            is not WorkflowAdapterConfigurationIdentity
        ):
            raise TypeError(
                "adapter_configuration_identity must be "
                "WorkflowAdapterConfigurationIdentity"
            )
        if type(self.effect_intents) is not tuple or not self.effect_intents:
            raise ValueError("effect_intents must be a nonempty tuple")
        if len(self.effect_intents) > _MAX_PLAN_EFFECT_INTENTS:
            raise ValueError("effect_intents exceed their event-envelope bound")
        if any(
            type(value) is not WorkflowEffectIntent for value in self.effect_intents
        ):
            raise TypeError("effect_intents must contain WorkflowEffectIntent")
        if any(
            value.occurrence_identity != self.occurrence_identity
            or value.adapter_identity != self.adapter_identity
            or value.adapter_configuration_identity
            != self.adapter_configuration_identity
            or value.ordinal != ordinal
            for ordinal, value in enumerate(self.effect_intents)
        ):
            raise ValueError("effect intents do not form one canonical plan")
        if len({value.identity for value in self.effect_intents}) != len(
            self.effect_intents
        ):
            raise ValueError("effect intent identities must be unique")
        if (
            type(self.maximum_attempts_per_intent) is not int
            or not 1 <= self.maximum_attempts_per_intent <= _MAX_ATTEMPTS
        ):
            raise ValueError("maximum_attempts_per_intent is outside its bound")
        expected = WorkflowPlanIdentity(
            _content_identity(
                "workflow-foreground-plan:1",
                [
                    self.occurrence_identity.value,
                    self.definition_identity.value,
                    self.adapter_identity.value,
                    self.adapter_configuration_identity.value,
                    [value.identity.value for value in self.effect_intents],
                    self.maximum_attempts_per_intent,
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        if (
            self.identity != expected
            or self.contract_version != WORKFLOW_RUNTIME_CONTRACT_VERSION
        ):
            raise ValueError("foreground plan content is inconsistent")


class WorkflowAuthorityVerificationKind(StrEnum):
    """Closed application-policy authority decision."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class WorkflowAuthorityVerification(AbstractImmutableDataObject):
    """Application-owned authority verification made before dispatch."""

    identity: WorkflowAuthorityVerificationIdentity
    occurrence_identity: WorkflowOccurrenceIdentity
    plan_identity: WorkflowPlanIdentity
    effect_intent_identity: WorkflowEffectIntentIdentity
    attempt_identity: WorkflowAttemptIdentity
    authority_reference_identity: WorkflowAuthorityReferenceIdentity
    authority_version: str
    policy_decision_identity: str
    validity_observation_identity: str
    kind: WorkflowAuthorityVerificationKind
    reason_codes: tuple[str, ...]
    contract_version: str = WORKFLOW_RUNTIME_CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        occurrence_identity: WorkflowOccurrenceIdentity,
        plan_identity: WorkflowPlanIdentity,
        effect_intent_identity: WorkflowEffectIntentIdentity,
        attempt_identity: WorkflowAttemptIdentity,
        authority_reference_identity: WorkflowAuthorityReferenceIdentity,
        authority_version: str,
        policy_decision_identity: str,
        validity_observation_identity: str,
        kind: WorkflowAuthorityVerificationKind,
        reason_codes: tuple[str, ...],
    ) -> WorkflowAuthorityVerification:
        """Create policy evidence without granting new authority."""
        if type(occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(plan_identity) is not WorkflowPlanIdentity:
            raise TypeError("plan_identity must be WorkflowPlanIdentity")
        if type(effect_intent_identity) is not WorkflowEffectIntentIdentity:
            raise TypeError(
                "effect_intent_identity must be WorkflowEffectIntentIdentity"
            )
        if type(attempt_identity) is not WorkflowAttemptIdentity:
            raise TypeError("attempt_identity must be WorkflowAttemptIdentity")
        if type(authority_reference_identity) is not WorkflowAuthorityReferenceIdentity:
            raise TypeError(
                "authority_reference_identity must be "
                "WorkflowAuthorityReferenceIdentity"
            )
        _named_identity(authority_version, "authority_version")
        _named_identity(policy_decision_identity, "policy_decision_identity")
        _named_identity(validity_observation_identity, "validity_observation_identity")
        if type(kind) is not WorkflowAuthorityVerificationKind:
            raise TypeError("kind must be WorkflowAuthorityVerificationKind")
        reasons = _reasons(reason_codes)
        if _RESERVED_FOREGROUND_OUTCOME_CODES.intersection(reasons):
            raise ValueError("reason_codes use a runtime-reserved outcome code")
        identity = WorkflowAuthorityVerificationIdentity(
            _content_identity(
                "workflow-authority-verification:2",
                [
                    occurrence_identity.value,
                    plan_identity.value,
                    effect_intent_identity.value,
                    attempt_identity.value,
                    authority_reference_identity.value,
                    authority_version,
                    policy_decision_identity,
                    validity_observation_identity,
                    kind.value,
                    list(reasons),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        return cls(
            identity,
            occurrence_identity,
            plan_identity,
            effect_intent_identity,
            attempt_identity,
            authority_reference_identity,
            authority_version,
            policy_decision_identity,
            validity_observation_identity,
            kind,
            reasons,
        )

    def __post_init__(self) -> None:
        if type(self.identity) is not WorkflowAuthorityVerificationIdentity:
            raise TypeError("identity must be WorkflowAuthorityVerificationIdentity")
        if type(self.occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(self.plan_identity) is not WorkflowPlanIdentity:
            raise TypeError("plan_identity must be WorkflowPlanIdentity")
        if type(self.effect_intent_identity) is not WorkflowEffectIntentIdentity:
            raise TypeError(
                "effect_intent_identity must be WorkflowEffectIntentIdentity"
            )
        if type(self.attempt_identity) is not WorkflowAttemptIdentity:
            raise TypeError("attempt_identity must be WorkflowAttemptIdentity")
        if (
            type(self.authority_reference_identity)
            is not WorkflowAuthorityReferenceIdentity
        ):
            raise TypeError(
                "authority_reference_identity must be "
                "WorkflowAuthorityReferenceIdentity"
            )
        _named_identity(self.authority_version, "authority_version")
        _named_identity(self.policy_decision_identity, "policy_decision_identity")
        _named_identity(
            self.validity_observation_identity,
            "validity_observation_identity",
        )
        if type(self.kind) is not WorkflowAuthorityVerificationKind:
            raise TypeError("kind must be WorkflowAuthorityVerificationKind")
        reasons = _reasons(self.reason_codes)
        if _RESERVED_FOREGROUND_OUTCOME_CODES.intersection(reasons):
            raise ValueError("reason_codes use a runtime-reserved outcome code")
        expected = WorkflowAuthorityVerificationIdentity(
            _content_identity(
                "workflow-authority-verification:2",
                [
                    self.occurrence_identity.value,
                    self.plan_identity.value,
                    self.effect_intent_identity.value,
                    self.attempt_identity.value,
                    self.authority_reference_identity.value,
                    self.authority_version,
                    self.policy_decision_identity,
                    self.validity_observation_identity,
                    self.kind.value,
                    list(reasons),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        if (
            self.identity != expected
            or self.contract_version != WORKFLOW_RUNTIME_CONTRACT_VERSION
        ):
            raise ValueError("authority verification content is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowDispatchAuthorization(AbstractImmutableDataObject):
    """Attempt-bound authorization retained before one worker handoff."""

    identity: WorkflowDispatchAuthorizationIdentity
    occurrence_identity: WorkflowOccurrenceIdentity
    plan_identity: WorkflowPlanIdentity
    effect_intent_identity: WorkflowEffectIntentIdentity
    attempt_identity: WorkflowAttemptIdentity
    worker_identity: WorkflowForegroundWorkerIdentity
    external_idempotency_token: str
    authority_verification_identity: WorkflowAuthorityVerificationIdentity
    authority_verification_kind: WorkflowAuthorityVerificationKind
    limit_references: tuple[WorkflowRuntimeEvidenceReference, ...]
    contract_version: str = WORKFLOW_RUNTIME_CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        plan: WorkflowForegroundPlan,
        effect_intent: WorkflowEffectIntent,
        attempt_ordinal: int,
        worker_identity: WorkflowForegroundWorkerIdentity,
        authority_verification: WorkflowAuthorityVerification,
        limit_references: tuple[WorkflowRuntimeEvidenceReference, ...],
    ) -> WorkflowDispatchAuthorization:
        """Create authorization from accepted correlated evidence."""
        if type(plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        if type(effect_intent) is not WorkflowEffectIntent:
            raise TypeError("effect_intent must be WorkflowEffectIntent")
        if type(attempt_ordinal) is not int or attempt_ordinal < 1:
            raise ValueError("attempt_ordinal must be a positive built-in int")
        if attempt_ordinal > plan.maximum_attempts_per_intent:
            raise ValueError("attempt_ordinal exceeds the plan bound")
        attempt_identity = WorkflowAttemptIdentity.create(
            occurrence_identity=plan.occurrence_identity,
            effect_intent_identity=effect_intent.identity,
            attempt_ordinal=attempt_ordinal,
        )
        if type(worker_identity) is not WorkflowForegroundWorkerIdentity:
            raise TypeError("worker_identity must be WorkflowForegroundWorkerIdentity")
        if type(authority_verification) is not WorkflowAuthorityVerification:
            raise TypeError(
                "authority_verification must be WorkflowAuthorityVerification"
            )
        limits = _references(limit_references, "limit_references")
        if effect_intent not in plan.effect_intents:
            raise ValueError("effect intent is not a plan member")
        if (
            authority_verification.kind
            is not WorkflowAuthorityVerificationKind.ACCEPTED
            or authority_verification.occurrence_identity != plan.occurrence_identity
            or authority_verification.plan_identity != plan.identity
            or authority_verification.effect_intent_identity != effect_intent.identity
            or authority_verification.attempt_identity != attempt_identity
        ):
            raise ValueError("authority verification does not authorize this intent")
        identity = WorkflowDispatchAuthorizationIdentity(
            _content_identity(
                "workflow-dispatch-authorization:1",
                [
                    plan.occurrence_identity.value,
                    plan.identity.value,
                    effect_intent.identity.value,
                    attempt_identity.value,
                    worker_identity.value,
                    effect_intent.external_idempotency_token,
                    authority_verification.identity.value,
                    authority_verification.kind.value,
                    _reference_parts(limits),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        return cls(
            identity,
            plan.occurrence_identity,
            plan.identity,
            effect_intent.identity,
            attempt_identity,
            worker_identity,
            effect_intent.external_idempotency_token,
            authority_verification.identity,
            authority_verification.kind,
            limits,
        )

    def __post_init__(self) -> None:
        if type(self.identity) is not WorkflowDispatchAuthorizationIdentity:
            raise TypeError("identity must be WorkflowDispatchAuthorizationIdentity")
        if type(self.occurrence_identity) is not WorkflowOccurrenceIdentity:
            raise TypeError("occurrence_identity must be WorkflowOccurrenceIdentity")
        if type(self.plan_identity) is not WorkflowPlanIdentity:
            raise TypeError("plan_identity must be WorkflowPlanIdentity")
        if type(self.effect_intent_identity) is not WorkflowEffectIntentIdentity:
            raise TypeError(
                "effect_intent_identity must be WorkflowEffectIntentIdentity"
            )
        if type(self.attempt_identity) is not WorkflowAttemptIdentity:
            raise TypeError("attempt_identity must be WorkflowAttemptIdentity")
        if type(self.worker_identity) is not WorkflowForegroundWorkerIdentity:
            raise TypeError("worker_identity must be WorkflowForegroundWorkerIdentity")
        _digest_identity(self.external_idempotency_token, "external_idempotency_token")
        if (
            type(self.authority_verification_identity)
            is not WorkflowAuthorityVerificationIdentity
        ):
            raise TypeError(
                "authority_verification_identity must be "
                "WorkflowAuthorityVerificationIdentity"
            )
        if (
            self.authority_verification_kind
            is not WorkflowAuthorityVerificationKind.ACCEPTED
        ):
            raise ValueError("dispatch requires accepted authority verification")
        limits = _references(self.limit_references, "limit_references")
        expected = WorkflowDispatchAuthorizationIdentity(
            _content_identity(
                "workflow-dispatch-authorization:1",
                [
                    self.occurrence_identity.value,
                    self.plan_identity.value,
                    self.effect_intent_identity.value,
                    self.attempt_identity.value,
                    self.worker_identity.value,
                    self.external_idempotency_token,
                    self.authority_verification_identity.value,
                    self.authority_verification_kind.value,
                    _reference_parts(limits),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        if (
            self.identity != expected
            or self.contract_version != WORKFLOW_RUNTIME_CONTRACT_VERSION
        ):
            raise ValueError("dispatch authorization content is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowForegroundExecutionRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Exact application-to-worker handoff retained by the runtime."""

    plan: WorkflowForegroundPlan
    effect_intent: WorkflowEffectIntent
    attempt_ordinal: int
    authorization: WorkflowDispatchAuthorization

    def __post_init__(self) -> None:
        if type(self.plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        if type(self.effect_intent) is not WorkflowEffectIntent:
            raise TypeError("effect_intent must be WorkflowEffectIntent")
        if type(self.attempt_ordinal) is not int or self.attempt_ordinal < 1:
            raise ValueError("attempt_ordinal must be a positive built-in int")
        if self.attempt_ordinal > self.plan.maximum_attempts_per_intent:
            raise ValueError("attempt_ordinal exceeds the plan bound")
        if type(self.authorization) is not WorkflowDispatchAuthorization:
            raise TypeError("authorization must be WorkflowDispatchAuthorization")
        expected_attempt = WorkflowAttemptIdentity.create(
            occurrence_identity=self.plan.occurrence_identity,
            effect_intent_identity=self.effect_intent.identity,
            attempt_ordinal=self.attempt_ordinal,
        )
        if (
            self.effect_intent not in self.plan.effect_intents
            or self.authorization.occurrence_identity != self.plan.occurrence_identity
            or self.authorization.plan_identity != self.plan.identity
            or self.authorization.effect_intent_identity != self.effect_intent.identity
            or self.authorization.attempt_identity != expected_attempt
            or self.authorization.external_idempotency_token
            != self.effect_intent.external_idempotency_token
        ):
            raise ValueError("foreground execution request is not correlated")


class WorkflowEffectOutcomeKind(StrEnum):
    """Closed worker effect outcome classification."""

    SUCCEEDED = "succeeded"
    KNOWN_NOT_APPLIED = "known_not_applied"
    KNOWN_APPLIED_WITH_FAILURE = "known_applied_with_failure"
    AMBIGUOUS = "ambiguous"
    REJECTED_BEFORE_EFFECT = "rejected_before_effect"


@dataclass(frozen=True, slots=True)
class WorkflowExecutionEvidence(
    AbstractImmutableDataObject,
    DataObjectActionResult,
):
    """Immutable bounded worker evidence for one exact foreground attempt."""

    identity: WorkflowExecutionEvidenceIdentity
    occurrence_identity: WorkflowOccurrenceIdentity
    plan_identity: WorkflowPlanIdentity
    effect_intent_identity: WorkflowEffectIntentIdentity
    attempt_identity: WorkflowAttemptIdentity
    dispatch_authorization_identity: WorkflowDispatchAuthorizationIdentity
    worker_identity: WorkflowForegroundWorkerIdentity
    outcome: WorkflowEffectOutcomeKind
    evidence_references: tuple[WorkflowRuntimeEvidenceReference, ...]
    reason_codes: tuple[str, ...]
    contract_version: str = WORKFLOW_RUNTIME_CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        request: WorkflowForegroundExecutionRequest,
        outcome: WorkflowEffectOutcomeKind,
        evidence_references: tuple[WorkflowRuntimeEvidenceReference, ...],
        reason_codes: tuple[str, ...],
    ) -> WorkflowExecutionEvidence:
        """Create a report bound to one exact worker attempt."""
        if type(request) is not WorkflowForegroundExecutionRequest:
            raise TypeError("request must be WorkflowForegroundExecutionRequest")
        if type(outcome) is not WorkflowEffectOutcomeKind:
            raise TypeError("outcome must be WorkflowEffectOutcomeKind")
        evidence = _application_evidence(
            evidence_references,
            maximum=_MAX_EXECUTION_REFERENCES,
            field="evidence_references",
        )
        reasons = _evidence_reasons(
            reason_codes,
            reserved_outcomes=_RESERVED_FOREGROUND_OUTCOME_CODES,
        )
        authorization = request.authorization
        identity = WorkflowExecutionEvidenceIdentity(
            _content_identity(
                "workflow-execution-evidence:1",
                [
                    request.plan.occurrence_identity.value,
                    request.plan.identity.value,
                    request.effect_intent.identity.value,
                    authorization.attempt_identity.value,
                    authorization.identity.value,
                    authorization.worker_identity.value,
                    outcome.value,
                    _reference_parts(evidence),
                    list(reasons),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        return cls(
            identity,
            request.plan.occurrence_identity,
            request.plan.identity,
            request.effect_intent.identity,
            authorization.attempt_identity,
            authorization.identity,
            authorization.worker_identity,
            outcome,
            evidence,
            reasons,
        )

    def __post_init__(self) -> None:
        for value, expected_type, field in (
            (self.identity, WorkflowExecutionEvidenceIdentity, "identity"),
            (
                self.occurrence_identity,
                WorkflowOccurrenceIdentity,
                "occurrence_identity",
            ),
            (self.plan_identity, WorkflowPlanIdentity, "plan_identity"),
            (
                self.effect_intent_identity,
                WorkflowEffectIntentIdentity,
                "effect_intent_identity",
            ),
            (
                self.attempt_identity,
                WorkflowAttemptIdentity,
                "attempt_identity",
            ),
            (
                self.dispatch_authorization_identity,
                WorkflowDispatchAuthorizationIdentity,
                "dispatch_authorization_identity",
            ),
            (
                self.worker_identity,
                WorkflowForegroundWorkerIdentity,
                "worker_identity",
            ),
        ):
            if type(value) is not expected_type:
                raise TypeError(f"{field} has an invalid nominal type")
        if type(self.outcome) is not WorkflowEffectOutcomeKind:
            raise TypeError("outcome must be WorkflowEffectOutcomeKind")
        evidence = _application_evidence(
            self.evidence_references,
            maximum=_MAX_EXECUTION_REFERENCES,
            field="evidence_references",
        )
        reasons = _evidence_reasons(
            self.reason_codes,
            reserved_outcomes=_RESERVED_FOREGROUND_OUTCOME_CODES,
        )
        expected = WorkflowExecutionEvidenceIdentity(
            _content_identity(
                "workflow-execution-evidence:1",
                [
                    self.occurrence_identity.value,
                    self.plan_identity.value,
                    self.effect_intent_identity.value,
                    self.attempt_identity.value,
                    self.dispatch_authorization_identity.value,
                    self.worker_identity.value,
                    self.outcome.value,
                    _reference_parts(evidence),
                    list(reasons),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        if (
            self.identity != expected
            or self.contract_version != WORKFLOW_RUNTIME_CONTRACT_VERSION
        ):
            raise ValueError("execution evidence content is inconsistent")


class WorkflowReconciliationOutcomeKind(StrEnum):
    """Closed query-only reconciliation outcome."""

    CONFIRMED_APPLIED = "confirmed_applied"
    CONFIRMED_NOT_APPLIED = "confirmed_not_applied"
    CONFIRMED_PARTIAL = "confirmed_partial"
    STILL_AMBIGUOUS = "still_ambiguous"
    EVIDENCE_INVALID = "evidence_invalid"


_RESERVED_FOREGROUND_OUTCOME_CODES = frozenset(
    value.value
    for value in (
        *WorkflowEffectOutcomeKind,
        *WorkflowReconciliationOutcomeKind,
    )
)


@dataclass(frozen=True, slots=True)
class WorkflowReconciliationRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Exact query-only request for one ambiguous execution report."""

    execution_request: WorkflowForegroundExecutionRequest
    execution_evidence: WorkflowExecutionEvidence

    def __post_init__(self) -> None:
        if type(self.execution_request) is not WorkflowForegroundExecutionRequest:
            raise TypeError(
                "execution_request must be WorkflowForegroundExecutionRequest"
            )
        if type(self.execution_evidence) is not WorkflowExecutionEvidence:
            raise TypeError("execution_evidence must be WorkflowExecutionEvidence")
        request = self.execution_request
        evidence = self.execution_evidence
        if (
            evidence.outcome is not WorkflowEffectOutcomeKind.AMBIGUOUS
            or evidence.occurrence_identity != request.plan.occurrence_identity
            or evidence.plan_identity != request.plan.identity
            or evidence.effect_intent_identity != request.effect_intent.identity
            or evidence.attempt_identity != request.authorization.attempt_identity
            or evidence.dispatch_authorization_identity
            != request.authorization.identity
        ):
            raise ValueError("reconciliation requires exact ambiguous evidence")


@dataclass(frozen=True, slots=True)
class WorkflowReconciliationEvidence(
    AbstractImmutableDataObject,
    DataObjectActionResult,
):
    """Immutable evidence returned by a query-only reconciler."""

    identity: WorkflowReconciliationEvidenceIdentity
    execution_evidence_identity: WorkflowExecutionEvidenceIdentity
    reconciler_identity: WorkflowEffectReconcilerIdentity
    outcome: WorkflowReconciliationOutcomeKind
    evidence_references: tuple[WorkflowRuntimeEvidenceReference, ...]
    reason_codes: tuple[str, ...]
    contract_version: str = WORKFLOW_RUNTIME_CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        request: WorkflowReconciliationRequest,
        reconciler_identity: WorkflowEffectReconcilerIdentity,
        outcome: WorkflowReconciliationOutcomeKind,
        evidence_references: tuple[WorkflowRuntimeEvidenceReference, ...],
        reason_codes: tuple[str, ...],
    ) -> WorkflowReconciliationEvidence:
        """Create reconciliation evidence for one ambiguous report."""
        if type(request) is not WorkflowReconciliationRequest:
            raise TypeError("request must be WorkflowReconciliationRequest")
        if type(reconciler_identity) is not WorkflowEffectReconcilerIdentity:
            raise TypeError(
                "reconciler_identity must be WorkflowEffectReconcilerIdentity"
            )
        if type(outcome) is not WorkflowReconciliationOutcomeKind:
            raise TypeError("outcome must be WorkflowReconciliationOutcomeKind")
        evidence = _application_evidence(
            evidence_references,
            maximum=_MAX_RECONCILIATION_REFERENCES,
            field="evidence_references",
        )
        reasons = _evidence_reasons(
            reason_codes,
            reserved_outcomes=_RESERVED_FOREGROUND_OUTCOME_CODES,
        )
        identity = WorkflowReconciliationEvidenceIdentity(
            _content_identity(
                "workflow-reconciliation-evidence:1",
                [
                    request.execution_evidence.identity.value,
                    reconciler_identity.value,
                    outcome.value,
                    _reference_parts(evidence),
                    list(reasons),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        return cls(
            identity,
            request.execution_evidence.identity,
            reconciler_identity,
            outcome,
            evidence,
            reasons,
        )

    def __post_init__(self) -> None:
        if type(self.identity) is not WorkflowReconciliationEvidenceIdentity:
            raise TypeError("identity must be WorkflowReconciliationEvidenceIdentity")
        if (
            type(self.execution_evidence_identity)
            is not WorkflowExecutionEvidenceIdentity
        ):
            raise TypeError(
                "execution_evidence_identity must be WorkflowExecutionEvidenceIdentity"
            )
        if type(self.reconciler_identity) is not WorkflowEffectReconcilerIdentity:
            raise TypeError(
                "reconciler_identity must be WorkflowEffectReconcilerIdentity"
            )
        if type(self.outcome) is not WorkflowReconciliationOutcomeKind:
            raise TypeError("outcome must be WorkflowReconciliationOutcomeKind")
        evidence = _application_evidence(
            self.evidence_references,
            maximum=_MAX_RECONCILIATION_REFERENCES,
            field="evidence_references",
        )
        reasons = _evidence_reasons(
            self.reason_codes,
            reserved_outcomes=_RESERVED_FOREGROUND_OUTCOME_CODES,
        )
        expected = WorkflowReconciliationEvidenceIdentity(
            _content_identity(
                "workflow-reconciliation-evidence:1",
                [
                    self.execution_evidence_identity.value,
                    self.reconciler_identity.value,
                    self.outcome.value,
                    _reference_parts(evidence),
                    list(reasons),
                    WORKFLOW_RUNTIME_CONTRACT_VERSION,
                ],
            )
        )
        if (
            self.identity != expected
            or self.contract_version != WORKFLOW_RUNTIME_CONTRACT_VERSION
        ):
            raise ValueError("reconciliation evidence content is inconsistent")


class AbstractWorkflowForegroundWorker(
    DataObjectActionizer[
        WorkflowForegroundExecutionRequest,
        WorkflowExecutionEvidence,
    ],
):
    """Application-owned worker invoked only after retained authorization."""

    __slots__ = ()

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if "action" in cls.__dict__:
            raise TypeError("foreground workers cannot override fixed action")

    @property
    @abstractmethod
    def identity(self) -> WorkflowForegroundWorkerIdentity:
        """Return the exact worker identity bound by dispatch authorization."""
        raise NotImplementedError

    @final
    def action(
        self,
        *,
        request: WorkflowForegroundExecutionRequest,
    ) -> WorkflowExecutionEvidence:
        """Perform the fixed worker action for one exact request."""
        if type(request) is not WorkflowForegroundExecutionRequest:
            raise TypeError("request must be WorkflowForegroundExecutionRequest")
        return self.execute(request=request)

    @abstractmethod
    def execute(
        self,
        *,
        request: WorkflowForegroundExecutionRequest,
    ) -> WorkflowExecutionEvidence:
        """Perform at most the authorized effect and return bounded evidence."""
        raise NotImplementedError


class AbstractWorkflowEffectReconciler(
    DataObjectActionizer[
        WorkflowReconciliationRequest,
        WorkflowReconciliationEvidence,
    ],
):
    """Application-owned query-only reconciler for ambiguous effects."""

    __slots__ = ()

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if "action" in cls.__dict__:
            raise TypeError("reconcilers cannot override fixed action")

    @property
    @abstractmethod
    def identity(self) -> WorkflowEffectReconcilerIdentity:
        """Return the exact query-only reconciler implementation identity."""
        raise NotImplementedError

    @final
    def action(
        self,
        *,
        request: WorkflowReconciliationRequest,
    ) -> WorkflowReconciliationEvidence:
        """Perform the fixed query-only action for one exact request."""
        if type(request) is not WorkflowReconciliationRequest:
            raise TypeError("request must be WorkflowReconciliationRequest")
        return self.reconcile(request=request)

    @abstractmethod
    def reconcile(
        self,
        *,
        request: WorkflowReconciliationRequest,
    ) -> WorkflowReconciliationEvidence:
        """Inspect evidence without invoking the original effect."""
        raise NotImplementedError
