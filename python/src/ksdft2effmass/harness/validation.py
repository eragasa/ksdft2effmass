"""Immutable results and read-only validation of normalized Harness state.

The public result contract records one exact structural validation invocation. Domain
validators inspect one complete :class:`~ksdft2effmass.harness.HarnessState` without
mutating it, repairing sources, resolving authority, or inferring scientific meaning.
``HarnessStateValidator`` composes an explicit ordered validator tuple and owns only
aggregate decision-sequence and cross-domain closure rules.

This module provides software validation only. A passing result does not establish
pytest success, coding-standards conformance for another subject, numerical
verification, scientific validation, uncertainty quantification, protected authority,
or human acceptance. No public wire format is defined by this module.
"""

from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

from .compiler import HarnessState
from .task import HarnessTask


class ValidationApplicability(StrEnum):
    """Closed applicability state for one validation invocation."""

    APPLICABLE = "applicable"
    NOT_APPLICABLE = "not_applicable"


class ValidationStatus(StrEnum):
    """Closed outcome status for one validation invocation."""

    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    NOT_RUN = "not_run"
    NOT_APPLICABLE = "not_applicable"


class ActivationReferenceRequirement(StrEnum):
    """Explicit activation-reference applicability for a selected Task."""

    OPTIONAL = "optional"
    REQUIRED = "required"
    PROHIBITED = "prohibited"


@dataclass(frozen=True, slots=True, kw_only=True)
class DevelopmentTaskSelectionValidationPolicy:
    """Supply explicit selection-validation policy without granting authority.

    Parameters
    ----------
    policy_identity
        Exact nonempty identity of the supplied policy revision.
    activation_reference_requirement
        Whether a selected Task must, may, or must not carry activation-receipt
        references. The validator checks represented applicability only; it does not
        establish receipt existence, authenticity, or authority.
    eligible_task_statuses
        Strictly sorted unique opaque Task status values that this policy explicitly
        accepts for a selected Task. An empty tuple makes no lifecycle assertion.
    """

    policy_identity: str
    activation_reference_requirement: ActivationReferenceRequirement
    eligible_task_statuses: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.policy_identity) is not str:
            raise TypeError("policy_identity must be a built-in str")
        if (
            not self.policy_identity
            or "\n" in self.policy_identity
            or "\r" in self.policy_identity
        ):
            raise ValueError("policy_identity must be nonempty single-line text")
        if (
            type(self.activation_reference_requirement)
            is not ActivationReferenceRequirement
        ):
            raise TypeError("activation_reference_requirement must use its closed enum")
        if type(self.eligible_task_statuses) is not tuple or any(
            type(status) is not str for status in self.eligible_task_statuses
        ):
            raise TypeError("eligible_task_statuses must contain built-in str values")
        if any(
            not status or "\n" in status or "\r" in status
            for status in self.eligible_task_statuses
        ):
            raise ValueError(
                "eligible_task_statuses must contain nonempty single-line text"
            )
        if self.eligible_task_statuses != tuple(
            sorted(set(self.eligible_task_statuses))
        ):
            raise ValueError("eligible_task_statuses must be sorted and unique")


@dataclass(frozen=True, slots=True, kw_only=True)
class ValidationRuleIdentity:
    """Identify one versioned validation rule and its gate criticality.

    Parameters
    ----------
    requirement_identity
        Nonempty identity of the requirement represented by the rule.
    rule_identity
        Nonempty stable identity of the exact rule.
    version_identity
        Nonempty identity of the rule behavior version.
    required
        Whether ``fail``, ``error``, or ``not_run`` for this rule blocks its gate.
    not_applicable_permitted
        Whether the represented requirement permits a ``not_applicable`` outcome.
    """

    requirement_identity: str
    rule_identity: str
    version_identity: str
    required: bool
    not_applicable_permitted: bool

    def __post_init__(self) -> None:
        for name in (
            "requirement_identity",
            "rule_identity",
            "version_identity",
        ):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or "\n" in value or "\r" in value:
                raise ValueError(f"{name} must be nonempty single-line text")
        if type(self.required) is not bool:
            raise TypeError("required must be bool")
        if type(self.not_applicable_permitted) is not bool:
            raise TypeError("not_applicable_permitted must be bool")

    @property
    def sort_key(self) -> tuple[str, str, str]:
        """Return deterministic requirement, rule, and version order."""
        return (
            self.requirement_identity,
            self.rule_identity,
            self.version_identity,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ValidationFinding:
    """Represent one identified applicable validation-rule failure.

    Parameters
    ----------
    rule_identity
        Exact rule that produced the finding.
    code
        Stable nonempty machine-oriented finding code.
    subject_identity
        Exact identity of the normalized subject inspected by the rule.
    summary
        Sanitized nonempty single-line diagnostic.
    affected_paths
        Strictly sorted unique repository-relative paths associated with the finding.
        The tuple may be empty when the normalized state has no exact path binding.
    finding_identity
        Derived SHA-256 identity. An empty input is canonicalized to the identity of
        the other fields; a supplied value must match it exactly.
    """

    rule_identity: ValidationRuleIdentity
    code: str
    subject_identity: str
    summary: str
    affected_paths: tuple[str, ...]
    finding_identity: str = ""

    def __post_init__(self) -> None:
        if type(self.rule_identity) is not ValidationRuleIdentity:
            raise TypeError("rule_identity must be ValidationRuleIdentity")
        for name in ("code", "subject_identity", "summary"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or "\n" in value or "\r" in value:
                raise ValueError(f"{name} must be nonempty single-line text")
        if type(self.affected_paths) is not tuple or any(
            type(path) is not str for path in self.affected_paths
        ):
            raise TypeError("affected_paths must contain built-in str values")
        if self.affected_paths != tuple(sorted(set(self.affected_paths))):
            raise ValueError("affected_paths must be sorted and unique")
        for path in self.affected_paths:
            if (
                not path
                or path.startswith("/")
                or "\\" in path
                or path.endswith("/")
                or any(part in {"", ".", ".."} for part in path.split("/"))
                or unicodedata.normalize("NFC", path) != path
            ):
                raise ValueError(
                    "affected_paths must contain normalized repository-relative paths"
                )
        expected = self._derived_identity()
        if self.finding_identity == "":
            object.__setattr__(self, "finding_identity", expected)
        elif type(self.finding_identity) is not str:
            raise TypeError("finding_identity must be a built-in str")
        elif self.finding_identity != expected:
            raise ValueError("finding_identity does not match finding semantics")

    @classmethod
    def create(
        cls,
        *,
        rule_identity: ValidationRuleIdentity,
        code: str,
        subject_identity: str,
        summary: str,
        affected_paths: tuple[str, ...] = (),
    ) -> ValidationFinding:
        """Construct one finding with its exact derived identity."""
        return cls(
            rule_identity=rule_identity,
            code=code,
            subject_identity=subject_identity,
            summary=summary,
            affected_paths=affected_paths,
        )

    @property
    def sort_key(self) -> tuple[tuple[str, str, str], str, str, tuple[str, ...]]:
        """Return deterministic rule, code, subject, and path order."""
        return (
            self.rule_identity.sort_key,
            self.code,
            self.subject_identity,
            self.affected_paths,
        )

    def _derived_identity(self) -> str:
        digest = hashlib.sha256()
        values = (
            "ksdft2effmass.harness.validation-finding.v1",
            self.rule_identity.requirement_identity,
            self.rule_identity.rule_identity,
            self.rule_identity.version_identity,
            "required" if self.rule_identity.required else "optional",
            self.code,
            self.subject_identity,
            self.summary,
            *self.affected_paths,
        )
        for value in values:
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
        return digest.hexdigest()


@dataclass(frozen=True, slots=True, kw_only=True)
class ValidationResult:
    """Represent one complete leaf or composite validation outcome.

    Parameters
    ----------
    validator_identity
        Exact identity of the validator implementation and composition.
    rule_identities
        Strictly sorted unique rules represented by the result.
    summary
        Sanitized single-line invocation summary.
    applicability, not_applicable_reason
        Closed applicability and its required reason when not applicable.
    subject_identity
        Exact normalized-state identity inspected by the invocation.
    execution_completed
        Whether validation executed to a pass-or-fail conclusion.
    status
        Closed status. ``error`` and ``not_run`` are not successful execution.
    findings
        Strictly ordered identified applicable failures.
    error_diagnostic
        Sanitized diagnostic present exactly for ``error``.
    tool_identity, configuration_identity, environment_identity
        Exact invocation identities when represented, otherwise ``None``. Absence
        does not invent or imply an identity.
    evidence_references, affected_paths
        Strictly sorted unique retained references and repository-relative paths.
    child_results
        Explicit ordered child outcomes for a composite result. Leaf results use an
        empty tuple. ``child_result_identities`` exposes their exact identities.
    claim_boundary
        Nonempty statement delimiting what the result can establish.
    result_identity
        Derived SHA-256 identity. An empty input is canonicalized; a supplied value
        must match all represented result semantics.

    Notes
    -----
    ``blocking`` is derived from required rule failures and child outcomes. It is
    never selected independently. A pass is structural validation only.
    """

    validator_identity: str
    rule_identities: tuple[ValidationRuleIdentity, ...]
    summary: str
    applicability: ValidationApplicability
    not_applicable_reason: str | None
    subject_identity: str
    execution_completed: bool
    status: ValidationStatus
    findings: tuple[ValidationFinding, ...]
    error_diagnostic: str | None
    tool_identity: str | None
    configuration_identity: str | None
    environment_identity: str | None
    evidence_references: tuple[str, ...]
    affected_paths: tuple[str, ...]
    child_results: tuple[ValidationResult, ...]
    claim_boundary: str
    result_identity: str = ""

    def __post_init__(self) -> None:
        for name in (
            "validator_identity",
            "summary",
            "subject_identity",
            "claim_boundary",
        ):
            self._require_line(getattr(self, name), name)
        if type(self.rule_identities) is not tuple or any(
            type(rule) is not ValidationRuleIdentity for rule in self.rule_identities
        ):
            raise TypeError(
                "rule_identities must contain ValidationRuleIdentity values"
            )
        if not self.rule_identities:
            raise ValueError("rule_identities must be nonempty")
        if self.rule_identities != tuple(
            sorted(self.rule_identities, key=lambda rule: rule.sort_key)
        ):
            raise ValueError("rule_identities must be deterministically sorted")
        rule_names = tuple(rule.rule_identity for rule in self.rule_identities)
        if len(set(rule_names)) != len(rule_names):
            raise ValueError("rule_identity values must be unique")
        if type(self.applicability) is not ValidationApplicability:
            raise TypeError("applicability must be ValidationApplicability")
        if type(self.execution_completed) is not bool:
            raise TypeError("execution_completed must be bool")
        if type(self.status) is not ValidationStatus:
            raise TypeError("status must be ValidationStatus")
        if type(self.findings) is not tuple or any(
            type(finding) is not ValidationFinding for finding in self.findings
        ):
            raise TypeError("findings must contain ValidationFinding values")
        if self.findings != tuple(
            sorted(self.findings, key=lambda item: item.sort_key)
        ):
            raise ValueError("findings must be deterministically ordered")
        if len({item.finding_identity for item in self.findings}) != len(self.findings):
            raise ValueError("finding identities must be unique")
        rules = {rule.rule_identity: rule for rule in self.rule_identities}
        if any(
            finding.rule_identity != rules.get(finding.rule_identity.rule_identity)
            for finding in self.findings
        ):
            raise ValueError("every finding must name one exact represented rule")
        for name in (
            "tool_identity",
            "configuration_identity",
            "environment_identity",
            "error_diagnostic",
            "not_applicable_reason",
        ):
            value = getattr(self, name)
            if value is not None:
                self._require_line(value, name)
        for name in ("evidence_references", "affected_paths"):
            values = getattr(self, name)
            if type(values) is not tuple or any(
                type(value) is not str for value in values
            ):
                raise TypeError(f"{name} must contain built-in str values")
            if values != tuple(sorted(set(values))):
                raise ValueError(f"{name} must be sorted and unique")
        finding_paths = {
            path for finding in self.findings for path in finding.affected_paths
        }
        if not finding_paths <= set(self.affected_paths):
            raise ValueError("affected_paths must include every finding path")
        if type(self.child_results) is not tuple or any(
            type(result) is not ValidationResult for result in self.child_results
        ):
            raise TypeError("child_results must contain ValidationResult values")
        if len({result.result_identity for result in self.child_results}) != len(
            self.child_results
        ):
            raise ValueError("child result identities must be unique")
        if self.child_results:
            self._validate_composite()
        else:
            self._validate_leaf_status()
        expected = self._derived_identity()
        if self.result_identity == "":
            object.__setattr__(self, "result_identity", expected)
        elif type(self.result_identity) is not str:
            raise TypeError("result_identity must be a built-in str")
        elif self.result_identity != expected:
            raise ValueError("result_identity does not match result semantics")

    @property
    def blocking(self) -> bool:
        """Return whether required rule or child outcomes block their gate."""
        if self.child_results:
            return any(result.blocking for result in self.child_results)
        if self.status is ValidationStatus.FAIL:
            return any(finding.rule_identity.required for finding in self.findings)
        if self.status in {ValidationStatus.ERROR, ValidationStatus.NOT_RUN}:
            return any(rule.required for rule in self.rule_identities)
        return False

    @property
    def child_result_identities(self) -> tuple[str, ...]:
        """Return exact child-result identities in invocation order."""
        return tuple(result.result_identity for result in self.child_results)

    @classmethod
    def from_findings(
        cls,
        *,
        validator_identity: str,
        rule_identities: tuple[ValidationRuleIdentity, ...],
        summary: str,
        subject_identity: str,
        findings: tuple[ValidationFinding, ...],
        tool_identity: str | None,
        configuration_identity: str | None = None,
        environment_identity: str | None = None,
        evidence_references: tuple[str, ...] = (),
        claim_boundary: str = "development-harness structural validation only",
    ) -> ValidationResult:
        """Construct one executed leaf result from complete identified findings."""
        ordered_findings = tuple(sorted(findings, key=lambda finding: finding.sort_key))
        affected_paths = tuple(
            sorted(
                {
                    path
                    for finding in ordered_findings
                    for path in finding.affected_paths
                }
            )
        )
        return cls(
            validator_identity=validator_identity,
            rule_identities=tuple(
                sorted(rule_identities, key=lambda rule: rule.sort_key)
            ),
            summary=summary,
            applicability=ValidationApplicability.APPLICABLE,
            not_applicable_reason=None,
            subject_identity=subject_identity,
            execution_completed=True,
            status=ValidationStatus.FAIL if ordered_findings else ValidationStatus.PASS,
            findings=ordered_findings,
            error_diagnostic=None,
            tool_identity=tool_identity,
            configuration_identity=configuration_identity,
            environment_identity=environment_identity,
            evidence_references=tuple(sorted(set(evidence_references))),
            affected_paths=affected_paths,
            child_results=(),
            claim_boundary=claim_boundary,
        )

    @classmethod
    def error(
        cls,
        *,
        validator_identity: str,
        rule_identities: tuple[ValidationRuleIdentity, ...],
        summary: str,
        subject_identity: str,
        error_diagnostic: str,
        tool_identity: str | None,
        configuration_identity: str | None = None,
        environment_identity: str | None = None,
        claim_boundary: str = "development-harness structural validation only",
    ) -> ValidationResult:
        """Construct one leaf error without fabricated findings or success evidence."""
        return cls(
            validator_identity=validator_identity,
            rule_identities=tuple(
                sorted(rule_identities, key=lambda rule: rule.sort_key)
            ),
            summary=summary,
            applicability=ValidationApplicability.APPLICABLE,
            not_applicable_reason=None,
            subject_identity=subject_identity,
            execution_completed=False,
            status=ValidationStatus.ERROR,
            findings=(),
            error_diagnostic=error_diagnostic,
            tool_identity=tool_identity,
            configuration_identity=configuration_identity,
            environment_identity=environment_identity,
            evidence_references=(),
            affected_paths=(),
            child_results=(),
            claim_boundary=claim_boundary,
        )

    @classmethod
    def composite(
        cls,
        *,
        validator_identity: str,
        summary: str,
        subject_identity: str,
        child_results: tuple[ValidationResult, ...],
        tool_identity: str | None,
        configuration_identity: str | None = None,
        environment_identity: str | None = None,
        claim_boundary: str = "development-harness structural validation only",
    ) -> ValidationResult:
        """Construct a composite using deterministic status precedence and closure."""
        if type(child_results) is not tuple or not child_results:
            raise ValueError("child_results must be a nonempty tuple")
        if any(type(result) is not ValidationResult for result in child_results):
            raise TypeError("child_results must contain ValidationResult values")
        statuses = {result.status for result in child_results}
        applicable = any(
            result.applicability is ValidationApplicability.APPLICABLE
            for result in child_results
        )
        if ValidationStatus.ERROR in statuses:
            status = ValidationStatus.ERROR
        elif ValidationStatus.NOT_RUN in statuses:
            status = ValidationStatus.NOT_RUN
        elif ValidationStatus.FAIL in statuses:
            status = ValidationStatus.FAIL
        elif applicable:
            status = ValidationStatus.PASS
        else:
            status = ValidationStatus.NOT_APPLICABLE
        rules_by_identity: dict[str, ValidationRuleIdentity] = {}
        for result in child_results:
            for rule in result.rule_identities:
                previous = rules_by_identity.setdefault(rule.rule_identity, rule)
                if previous != rule:
                    raise ValueError("one rule identity has conflicting metadata")
        rules = tuple(
            sorted(rules_by_identity.values(), key=lambda rule: rule.sort_key)
        )
        findings = tuple(
            sorted(
                (finding for result in child_results for finding in result.findings),
                key=lambda finding: finding.sort_key,
            )
        )
        paths = tuple(
            sorted({path for result in child_results for path in result.affected_paths})
        )
        evidence = tuple(
            sorted(
                {
                    reference
                    for result in child_results
                    for reference in result.evidence_references
                }
            )
        )
        return cls(
            validator_identity=validator_identity,
            rule_identities=rules,
            summary=summary,
            applicability=(
                ValidationApplicability.APPLICABLE
                if applicable
                else ValidationApplicability.NOT_APPLICABLE
            ),
            not_applicable_reason=(
                None if applicable else "no child validation was applicable"
            ),
            subject_identity=subject_identity,
            execution_completed=status
            in {ValidationStatus.PASS, ValidationStatus.FAIL},
            status=status,
            findings=findings,
            error_diagnostic=(
                "one or more child validations ended in error"
                if status is ValidationStatus.ERROR
                else None
            ),
            tool_identity=tool_identity,
            configuration_identity=configuration_identity,
            environment_identity=environment_identity,
            evidence_references=evidence,
            affected_paths=paths,
            child_results=child_results,
            claim_boundary=claim_boundary,
        )

    @staticmethod
    def _require_line(value: str, field: str) -> None:
        if type(value) is not str:
            raise TypeError(f"{field} must be a built-in str")
        if not value or "\n" in value or "\r" in value:
            raise ValueError(f"{field} must be nonempty single-line text")

    def _validate_leaf_status(self) -> None:
        if self.applicability is ValidationApplicability.NOT_APPLICABLE:
            if self.status is not ValidationStatus.NOT_APPLICABLE:
                raise ValueError(
                    "not-applicable invocation must use not_applicable status"
                )
            if self.not_applicable_reason is None:
                raise ValueError("not-applicable invocation requires a reason")
            if not all(rule.not_applicable_permitted for rule in self.rule_identities):
                raise ValueError("represented rules do not permit not_applicable")
        elif self.not_applicable_reason is not None:
            raise ValueError(
                "applicable invocation must not carry a not-applicable reason"
            )
        elif self.status is ValidationStatus.NOT_APPLICABLE:
            raise ValueError("applicable invocation cannot use not_applicable status")
        if self.status is ValidationStatus.PASS:
            if (
                not self.execution_completed
                or self.findings
                or self.error_diagnostic is not None
            ):
                raise ValueError(
                    "pass requires completed execution without findings or error"
                )
        elif self.status is ValidationStatus.FAIL:
            if (
                not self.execution_completed
                or not self.findings
                or self.error_diagnostic is not None
            ):
                raise ValueError("fail requires completed execution and findings")
        elif self.status is ValidationStatus.ERROR:
            if (
                self.execution_completed
                or self.findings
                or self.error_diagnostic is None
            ):
                raise ValueError("error requires an error diagnostic and no findings")
        elif self.status is ValidationStatus.NOT_RUN:
            if (
                self.execution_completed
                or self.findings
                or self.error_diagnostic is not None
            ):
                raise ValueError(
                    "not_run carries no execution success, findings, or error"
                )
        elif self.status is ValidationStatus.NOT_APPLICABLE:
            if (
                self.execution_completed
                or self.findings
                or self.error_diagnostic is not None
            ):
                raise ValueError(
                    "not_applicable carries no execution result or findings"
                )

    def _validate_composite(self) -> None:
        if any(
            result.subject_identity != self.subject_identity
            for result in self.child_results
        ):
            raise ValueError("every child must validate the composite subject")
        expected_rules = tuple(
            sorted(
                {
                    rule
                    for result in self.child_results
                    for rule in result.rule_identities
                },
                key=lambda rule: rule.sort_key,
            )
        )
        expected_findings = tuple(
            sorted(
                (
                    finding
                    for result in self.child_results
                    for finding in result.findings
                ),
                key=lambda finding: finding.sort_key,
            )
        )
        if self.rule_identities != expected_rules or self.findings != expected_findings:
            raise ValueError("composite rules and findings must equal child closure")
        expected_paths = tuple(
            sorted(
                {
                    path
                    for result in self.child_results
                    for path in result.affected_paths
                }
            )
        )
        expected_evidence = tuple(
            sorted(
                {
                    reference
                    for result in self.child_results
                    for reference in result.evidence_references
                }
            )
        )
        if (
            self.affected_paths != expected_paths
            or self.evidence_references != expected_evidence
        ):
            raise ValueError("composite paths and evidence must equal child closure")
        statuses = {result.status for result in self.child_results}
        applicable = any(
            result.applicability is ValidationApplicability.APPLICABLE
            for result in self.child_results
        )
        expected_status = (
            ValidationStatus.ERROR
            if ValidationStatus.ERROR in statuses
            else ValidationStatus.NOT_RUN
            if ValidationStatus.NOT_RUN in statuses
            else ValidationStatus.FAIL
            if ValidationStatus.FAIL in statuses
            else ValidationStatus.PASS
            if applicable
            else ValidationStatus.NOT_APPLICABLE
        )
        if self.status is not expected_status:
            raise ValueError("composite status violates child precedence")
        expected_applicability = (
            ValidationApplicability.APPLICABLE
            if applicable
            else ValidationApplicability.NOT_APPLICABLE
        )
        if self.applicability is not expected_applicability:
            raise ValueError("composite applicability must agree with children")
        if self.execution_completed != (
            self.status
            in {
                ValidationStatus.PASS,
                ValidationStatus.FAIL,
            }
        ):
            raise ValueError("composite execution indicator must agree with status")
        if self.status is ValidationStatus.ERROR:
            if self.error_diagnostic is None or self.not_applicable_reason is not None:
                raise ValueError("composite error requires only an error diagnostic")
        elif self.status is ValidationStatus.NOT_APPLICABLE:
            if self.not_applicable_reason is None or self.error_diagnostic is not None:
                raise ValueError("composite not_applicable requires only its reason")
        elif (
            self.error_diagnostic is not None or self.not_applicable_reason is not None
        ):
            raise ValueError(
                "composite pass, fail, and not_run carry no reason or error"
            )

    def _derived_identity(self) -> str:
        digest = hashlib.sha256()
        values = [
            "ksdft2effmass.harness.validation-result.v1",
            self.validator_identity,
            self.summary,
            self.applicability.value,
            self.not_applicable_reason or "",
            self.subject_identity,
            "completed" if self.execution_completed else "incomplete",
            self.status.value,
            self.error_diagnostic or "",
            "blocking" if self.blocking else "nonblocking",
            self.tool_identity or "",
            self.configuration_identity or "",
            self.environment_identity or "",
            self.claim_boundary,
        ]
        for rule in self.rule_identities:
            values.extend(
                (
                    rule.requirement_identity,
                    rule.rule_identity,
                    rule.version_identity,
                    "required" if rule.required else "optional",
                    "permits-na"
                    if rule.not_applicable_permitted
                    else "requires-applicable",
                )
            )
        values.extend(finding.finding_identity for finding in self.findings)
        values.extend(self.evidence_references)
        values.extend(self.affected_paths)
        values.extend(self.child_result_identities)
        for value in values:
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
        return digest.hexdigest()


@runtime_checkable
class HarnessDomainValidator(Protocol):
    """Structural protocol for one normalized Harness-state domain validator."""

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return the complete deterministic rules owned by the validator."""
        ...

    def execute(self, state: HarnessState) -> ValidationResult:
        """Validate ``state`` without mutation, repair, discovery, or authority."""
        ...


class DevelopmentTaskSelectionValidator:
    """Validate selection against one explicit non-authorizing policy.

    Parameters
    ----------
    policy
        Exact policy that states activation-reference applicability and any accepted
        opaque lifecycle values. The policy grants no authority and authenticates no
        receipt.
    """

    __slots__ = ("_policy",)
    _TOOL = "ksdft2effmass.harness.validation:1"
    _RULES = tuple(
        ValidationRuleIdentity(
            requirement_identity="harness.selection.consistency",
            rule_identity=f"harness.selection.{name}",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        for name in (
            "activation-reference-applicable",
            "lifecycle-eligible",
            "selected-task-exists",
        )
    )

    def __init__(self, policy: DevelopmentTaskSelectionValidationPolicy) -> None:
        if type(policy) is not DevelopmentTaskSelectionValidationPolicy:
            raise TypeError("policy must be DevelopmentTaskSelectionValidationPolicy")
        self._policy = policy

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return selection-consistency rule identities."""
        return self._RULES

    def execute(self, state: HarnessState) -> ValidationResult:
        """Return policy-bound findings without inferring lifecycle or authority."""
        if type(state) is not HarnessState:
            raise TypeError("state must be HarnessState")
        findings: list[ValidationFinding] = []
        selected_id = state.selection.active_task_id
        if selected_id is not None:
            selected = next(
                (task for task in state.tasks.tasks if task.task_id == selected_id),
                None,
            )
            if selected is None:
                findings.append(
                    self._finding(
                        state,
                        "selected-task-exists",
                        "HV.SELECTION.UNKNOWN_TASK",
                        (
                            "The selected Task identity is absent from the "
                            "canonical registry."
                        ),
                    )
                )
            else:
                receipts = state.selection.explicit_activation_receipt_ids
                requirement = self._policy.activation_reference_requirement
                if (
                    requirement is ActivationReferenceRequirement.REQUIRED
                    and not receipts
                ):
                    findings.append(
                        self._finding(
                            state,
                            "activation-reference-applicable",
                            "HV.SELECTION.ACTIVATION_REFERENCE_REQUIRED",
                            "The supplied policy requires an activation reference.",
                        )
                    )
                elif (
                    requirement is ActivationReferenceRequirement.PROHIBITED
                    and receipts
                ):
                    findings.append(
                        self._finding(
                            state,
                            "activation-reference-applicable",
                            "HV.SELECTION.ACTIVATION_REFERENCE_PROHIBITED",
                            "The supplied policy prohibits activation references.",
                        )
                    )
                eligible = self._policy.eligible_task_statuses
                if eligible and selected.status not in eligible:
                    findings.append(
                        self._finding(
                            state,
                            "lifecycle-eligible",
                            "HV.SELECTION.LIFECYCLE_INELIGIBLE",
                            (
                                f"Task status {selected.status} is not eligible under "
                                f"policy {self._policy.policy_identity}."
                            ),
                        )
                    )
        return ValidationResult.from_findings(
            validator_identity="DevelopmentTaskSelectionValidator:1",
            rule_identities=self.rule_identities,
            summary="Development Task selection consistency",
            subject_identity=state.identity.sha256,
            findings=tuple(findings),
            tool_identity=self._TOOL,
            configuration_identity=self._policy.policy_identity,
        )

    def _finding(
        self,
        state: HarnessState,
        rule_name: str,
        code: str,
        summary: str,
    ) -> ValidationFinding:
        rule = next(
            rule
            for rule in self._RULES
            if rule.rule_identity == f"harness.selection.{rule_name}"
        )
        return ValidationFinding.create(
            rule_identity=rule,
            code=code,
            subject_identity=state.identity.sha256,
            summary=summary,
        )


class HarnessTaskGraphValidator:
    """Validate canonical Task references, closure, and acyclicity."""

    __slots__ = ()
    _TOOL = "ksdft2effmass.harness.validation:1"
    _RULE_NAMES = (
        "documentation-paths-unique",
        "intake-paths-unique",
        "parent-exists",
        "parent-acyclic",
        "prerequisite-exists",
        "prerequisite-acyclic",
        "supersession-exists",
        "supersession-acyclic",
    )
    _RULES = tuple(
        ValidationRuleIdentity(
            requirement_identity="harness.task-graph.closure",
            rule_identity=f"harness.task-graph.{name}",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        for name in _RULE_NAMES
    )

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return Task-graph closure rule identities."""
        return tuple(sorted(self._RULES, key=lambda rule: rule.sort_key))

    def execute(self, state: HarnessState) -> ValidationResult:
        """Return deterministic reference and cycle findings for canonical Tasks."""
        if type(state) is not HarnessState:
            raise TypeError("state must be HarnessState")
        tasks = state.tasks.tasks
        by_id = {task.task_id: task for task in tasks}
        findings: list[ValidationFinding] = []
        path_groups = (
            (
                tuple(
                    task.documentation_path
                    for task in tasks
                    if task.documentation_path is not None
                ),
                "documentation-paths-unique",
                "HV.TASK.DOCUMENTATION_PATH_DUPLICATE",
            ),
            (
                tuple(
                    task.intake_path for task in tasks if task.intake_path is not None
                ),
                "intake-paths-unique",
                "HV.TASK.INTAKE_PATH_DUPLICATE",
            ),
        )
        for values, rule_name, code in path_groups:
            for path in sorted({value for value in values if values.count(value) > 1}):
                findings.append(
                    self._finding(
                        state,
                        rule_name,
                        code,
                        f"Task resource path {path} occurs more than once.",
                        (path,),
                    )
                )
        relation_rules = (
            ("parent", "parent-exists", "HV.TASK.PARENT_MISSING"),
            ("prerequisite", "prerequisite-exists", "HV.TASK.PREREQUISITE_MISSING"),
            ("supersession", "supersession-exists", "HV.TASK.SUPERSESSION_MISSING"),
        )
        for task in tasks:
            for relation, rule_name, code in relation_rules:
                for target in self._targets(task, relation):
                    if target not in by_id:
                        findings.append(
                            self._finding(
                                state,
                                rule_name,
                                code,
                                (
                                    f"Task {task.task_id} references absent "
                                    f"{relation} {target}."
                                ),
                            )
                        )
        for relation, rule_name, code in (
            ("parent", "parent-acyclic", "HV.TASK.PARENT_CYCLE"),
            ("prerequisite", "prerequisite-acyclic", "HV.TASK.PREREQUISITE_CYCLE"),
            ("supersession", "supersession-acyclic", "HV.TASK.SUPERSESSION_CYCLE"),
        ):
            for cycle in self._cycles(tasks, relation):
                findings.append(
                    self._finding(
                        state,
                        rule_name,
                        code,
                        f"Task {relation} cycle: {','.join(cycle)}.",
                    )
                )
        return ValidationResult.from_findings(
            validator_identity="HarnessTaskGraphValidator:1",
            rule_identities=self.rule_identities,
            summary="Canonical Harness Task graph closure",
            subject_identity=state.identity.sha256,
            findings=tuple(findings),
            tool_identity=self._TOOL,
        )

    @staticmethod
    def _targets(task: HarnessTask, relation: str) -> tuple[str, ...]:
        if relation == "parent":
            return (task.parent_task_id,) if task.parent_task_id is not None else ()
        if relation == "prerequisite":
            return task.task_prerequisite_ids
        return task.superseded_by_task_ids

    @classmethod
    def _cycles(
        cls, tasks: tuple[HarnessTask, ...], relation: str
    ) -> tuple[tuple[str, ...], ...]:
        by_id = {task.task_id: task for task in tasks}
        graph = {
            task.task_id: tuple(
                target for target in cls._targets(task, relation) if target in by_id
            )
            for task in tasks
        }
        cycles: set[tuple[str, ...]] = set()
        completed: set[str] = set()
        for root in sorted(graph):
            if root in completed:
                continue
            path = [root]
            positions = {root: 0}
            stack: list[tuple[str, int]] = [(root, 0)]
            while stack:
                node, child_index = stack[-1]
                children = graph[node]
                if child_index >= len(children):
                    completed.add(node)
                    stack.pop()
                    positions.pop(node)
                    path.pop()
                    continue
                child = children[child_index]
                stack[-1] = (node, child_index + 1)
                if child in positions:
                    cycle = path[positions[child] :]
                    rotations = [
                        tuple(cycle[index:] + cycle[:index])
                        for index in range(len(cycle))
                    ]
                    cycles.add(min(rotations))
                elif child not in completed:
                    positions[child] = len(path)
                    path.append(child)
                    stack.append((child, 0))
        return tuple(sorted(cycles))

    def _finding(
        self,
        state: HarnessState,
        rule_name: str,
        code: str,
        summary: str,
        affected_paths: tuple[str, ...] = (),
    ) -> ValidationFinding:
        rule = next(
            rule
            for rule in self._RULES
            if rule.rule_identity == f"harness.task-graph.{rule_name}"
        )
        return ValidationFinding.create(
            rule_identity=rule,
            code=code,
            subject_identity=state.identity.sha256,
            summary=summary,
            affected_paths=affected_paths,
        )


class HarnessCapabilityCatalogValidator:
    """Validate capability and repository-agent identity relationships."""

    __slots__ = ()
    _TOOL = "ksdft2effmass.harness.validation:1"
    _RULES = tuple(
        ValidationRuleIdentity(
            requirement_identity="harness.capability-catalog.closure",
            rule_identity=f"harness.capability-catalog.{name}",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        for name in (
            "skill-identities-unique",
            "agent-identities-unique",
            "selected-skills-exist",
        )
    )

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return capability-catalog closure rule identities."""
        return tuple(sorted(self._RULES, key=lambda rule: rule.sort_key))

    def execute(self, state: HarnessState) -> ValidationResult:
        """Return findings for duplicate identities and absent selected skills."""
        if type(state) is not HarnessState:
            raise TypeError("state must be HarnessState")
        findings: list[ValidationFinding] = []
        skill_ids = tuple(skill.skill_id for skill in state.capabilities.capabilities)
        for skill_id in sorted(
            {value for value in skill_ids if skill_ids.count(value) > 1}
        ):
            findings.append(
                self._finding(
                    state,
                    "skill-identities-unique",
                    "HV.CAPABILITY.DUPLICATE_SKILL",
                    f"Skill identity {skill_id} occurs more than once.",
                )
            )
        runtime_names = tuple(
            agent.runtime_name for agent in state.capabilities.agent_definitions
        )
        for runtime_name in sorted(
            {value for value in runtime_names if runtime_names.count(value) > 1}
        ):
            findings.append(
                self._finding(
                    state,
                    "agent-identities-unique",
                    "HV.CAPABILITY.DUPLICATE_AGENT",
                    f"Agent runtime identity {runtime_name} occurs more than once.",
                )
            )
        known_skills = set(skill_ids)
        for agent in state.capabilities.agent_definitions:
            for selected_skill in agent.selected_skills:
                if selected_skill not in known_skills:
                    findings.append(
                        self._finding(
                            state,
                            "selected-skills-exist",
                            "HV.CAPABILITY.SELECTED_SKILL_MISSING",
                            (
                                f"Agent {agent.runtime_name} selects absent skill "
                                f"{selected_skill}."
                            ),
                        )
                    )
        return ValidationResult.from_findings(
            validator_identity="HarnessCapabilityCatalogValidator:1",
            rule_identities=self.rule_identities,
            summary="Harness capability catalog closure",
            subject_identity=state.identity.sha256,
            findings=tuple(findings),
            tool_identity=self._TOOL,
        )

    def _finding(
        self,
        state: HarnessState,
        rule_name: str,
        code: str,
        summary: str,
    ) -> ValidationFinding:
        rule = next(
            rule
            for rule in self._RULES
            if rule.rule_identity == f"harness.capability-catalog.{rule_name}"
        )
        return ValidationFinding.create(
            rule_identity=rule,
            code=code,
            subject_identity=state.identity.sha256,
            summary=summary,
        )


class HarnessResourceCatalogValidator:
    """Validate resource-manifest layering and dependency closure."""

    __slots__ = ()
    _TOOL = "ksdft2effmass.harness.validation:1"
    _RULES = tuple(
        ValidationRuleIdentity(
            requirement_identity="harness.resource-catalog.closure",
            rule_identity=f"harness.resource-catalog.{name}",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        for name in (
            "manifest-identities-unique",
            "local-base-exists",
            "local-base-is-generic",
            "resource-identities-unique",
            "resource-paths-unique",
            "dependencies-exist",
            "generic-layer-independent",
            "dependency-acyclic",
        )
    )

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return resource-catalog closure rule identities."""
        return tuple(sorted(self._RULES, key=lambda rule: rule.sort_key))

    def execute(self, state: HarnessState) -> ValidationResult:
        """Return deterministic resource identity, layering, and graph findings."""
        if type(state) is not HarnessState:
            raise TypeError("state must be HarnessState")
        manifests = state.resources.resources
        findings: list[ValidationFinding] = []
        manifest_ids = tuple(manifest.manifest_id for manifest in manifests)
        for manifest_id in sorted(
            {value for value in manifest_ids if manifest_ids.count(value) > 1}
        ):
            findings.append(
                self._finding(
                    state,
                    "manifest-identities-unique",
                    "HV.RESOURCE.DUPLICATE_MANIFEST",
                    f"Resource manifest identity {manifest_id} occurs more than once.",
                )
            )
        manifests_by_id = {manifest.manifest_id: manifest for manifest in manifests}
        for manifest in manifests:
            if manifest.layer != "local":
                continue
            base_id = manifest.extends_manifest_id
            base = None if base_id is None else manifests_by_id.get(base_id)
            if base is None:
                findings.append(
                    self._finding(
                        state,
                        "local-base-exists",
                        "HV.RESOURCE.BASE_MISSING",
                        (
                            f"Local manifest {manifest.manifest_id} extends an "
                            "absent base."
                        ),
                    )
                )
            elif base.layer != "generic":
                findings.append(
                    self._finding(
                        state,
                        "local-base-is-generic",
                        "HV.RESOURCE.BASE_NOT_GENERIC",
                        (
                            f"Local manifest {manifest.manifest_id} does not extend "
                            "a generic manifest."
                        ),
                    )
                )
        resources = tuple(
            (manifest.layer, resource)
            for manifest in manifests
            for resource in manifest.resources
        )
        resource_ids = tuple(resource.resource_id for _, resource in resources)
        for resource_id in sorted(
            {value for value in resource_ids if resource_ids.count(value) > 1}
        ):
            findings.append(
                self._finding(
                    state,
                    "resource-identities-unique",
                    "HV.RESOURCE.DUPLICATE_ID",
                    f"Resource identity {resource_id} occurs more than once.",
                )
            )
        resource_paths = tuple(resource.path for _, resource in resources)
        for path in sorted(
            {value for value in resource_paths if resource_paths.count(value) > 1}
        ):
            findings.append(
                self._finding(
                    state,
                    "resource-paths-unique",
                    "HV.RESOURCE.DUPLICATE_PATH",
                    f"Resource path {path} occurs more than once.",
                    (path,),
                )
            )
        all_ids = set(resource_ids)
        local_ids = {
            resource.resource_id for layer, resource in resources if layer == "local"
        }
        graph: dict[str, tuple[str, ...]] = {}
        for layer, resource in resources:
            valid_dependencies: list[str] = []
            for dependency in resource.dependency_ids:
                if dependency not in all_ids:
                    findings.append(
                        self._finding(
                            state,
                            "dependencies-exist",
                            "HV.RESOURCE.DEPENDENCY_MISSING",
                            (
                                f"Resource {resource.resource_id} depends on absent "
                                f"{dependency}."
                            ),
                            (resource.path,),
                        )
                    )
                elif layer == "generic" and dependency in local_ids:
                    findings.append(
                        self._finding(
                            state,
                            "generic-layer-independent",
                            "HV.RESOURCE.GENERIC_TO_LOCAL_DEPENDENCY",
                            (
                                f"Generic resource {resource.resource_id} depends on "
                                f"local {dependency}."
                            ),
                            (resource.path,),
                        )
                    )
                else:
                    valid_dependencies.append(dependency)
            graph[resource.resource_id] = tuple(valid_dependencies)
        for cycle in self._cycles(graph):
            findings.append(
                self._finding(
                    state,
                    "dependency-acyclic",
                    "HV.RESOURCE.DEPENDENCY_CYCLE",
                    f"Resource dependency cycle: {','.join(cycle)}.",
                )
            )
        return ValidationResult.from_findings(
            validator_identity="HarnessResourceCatalogValidator:1",
            rule_identities=self.rule_identities,
            summary="Harness resource catalog closure",
            subject_identity=state.identity.sha256,
            findings=tuple(findings),
            tool_identity=self._TOOL,
        )

    @staticmethod
    def _cycles(graph: dict[str, tuple[str, ...]]) -> tuple[tuple[str, ...], ...]:
        cycles: set[tuple[str, ...]] = set()
        completed: set[str] = set()
        for root in sorted(graph):
            if root in completed:
                continue
            path = [root]
            positions = {root: 0}
            stack: list[tuple[str, int]] = [(root, 0)]
            while stack:
                node, child_index = stack[-1]
                children = graph.get(node, ())
                if child_index >= len(children):
                    completed.add(node)
                    stack.pop()
                    positions.pop(node)
                    path.pop()
                    continue
                child = children[child_index]
                stack[-1] = (node, child_index + 1)
                if child in positions:
                    cycle = path[positions[child] :]
                    rotations = [
                        tuple(cycle[index:] + cycle[:index])
                        for index in range(len(cycle))
                    ]
                    cycles.add(min(rotations))
                elif child in graph and child not in completed:
                    positions[child] = len(path)
                    path.append(child)
                    stack.append((child, 0))
        return tuple(sorted(cycles))

    def _finding(
        self,
        state: HarnessState,
        rule_name: str,
        code: str,
        summary: str,
        affected_paths: tuple[str, ...] = (),
    ) -> ValidationFinding:
        rule = next(
            rule
            for rule in self._RULES
            if rule.rule_identity == f"harness.resource-catalog.{rule_name}"
        )
        return ValidationFinding.create(
            rule_identity=rule,
            code=code,
            subject_identity=state.identity.sha256,
            summary=summary,
            affected_paths=affected_paths,
        )


class HarnessEvidenceCatalogValidator:
    """Validate exact source-level evidence catalog identity closure.

    Evidence ownership, evidence identifiers, and semantic claim boundaries remain
    with downstream coding-standards conformance. This validator does not parse source
    payloads or reinterpret test evidence.
    """

    __slots__ = ()
    _TOOL = "ksdft2effmass.harness.validation:1"
    _RULES = tuple(
        ValidationRuleIdentity(
            requirement_identity="harness.evidence-catalog.source-closure",
            rule_identity=f"harness.evidence-catalog.{name}",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        for name in (
            "paths-unique",
            "source-identities-unique",
            "sources-match-identities",
        )
    )

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return source-level evidence closure rule identities."""
        return self._RULES

    def execute(self, state: HarnessState) -> ValidationResult:
        """Return exact path, identity, and payload-binding findings."""
        if type(state) is not HarnessState:
            raise TypeError("state must be HarnessState")
        findings: list[ValidationFinding] = []
        sources = state.evidence.evidence
        identities = state.evidence.source_identities
        paths = tuple(source.path for source in sources)
        for path in sorted({value for value in paths if paths.count(value) > 1}):
            findings.append(
                self._finding(
                    state,
                    "paths-unique",
                    "HV.EVIDENCE.DUPLICATE_PATH",
                    f"Evidence source path {path} occurs more than once.",
                    (path,),
                )
            )
        identity_keys = tuple(
            (identity.relative_path.as_posix(), identity.sha256)
            for identity in identities
        )
        for path, _digest in sorted(
            {value for value in identity_keys if identity_keys.count(value) > 1}
        ):
            findings.append(
                self._finding(
                    state,
                    "source-identities-unique",
                    "HV.EVIDENCE.DUPLICATE_SOURCE_IDENTITY",
                    f"Evidence source identity for {path} occurs more than once.",
                    (path,),
                )
            )
        for source, identity in zip(sources, identities, strict=True):
            payload = source.payload
            if (
                payload is None
                or source.path != identity.relative_path.as_posix()
                or hashlib.sha256(payload).hexdigest() != identity.sha256
                or len(payload) != identity.byte_count
            ):
                findings.append(
                    self._finding(
                        state,
                        "sources-match-identities",
                        "HV.EVIDENCE.SOURCE_IDENTITY_MISMATCH",
                        (
                            f"Evidence source {source.path} differs from its exact "
                            "identity."
                        ),
                        (source.path,),
                    )
                )
        return ValidationResult.from_findings(
            validator_identity="HarnessEvidenceCatalogValidator:1",
            rule_identities=self.rule_identities,
            summary="Harness evidence source catalog closure",
            subject_identity=state.identity.sha256,
            findings=tuple(findings),
            tool_identity=self._TOOL,
            evidence_references=tuple(identity.sha256 for identity in identities),
            claim_boundary=(
                "exact evidence source identity closure only; evidence ownership and "
                "claim semantics are excluded"
            ),
        )

    def _finding(
        self,
        state: HarnessState,
        rule_name: str,
        code: str,
        summary: str,
        affected_paths: tuple[str, ...] = (),
    ) -> ValidationFinding:
        rule = next(
            rule
            for rule in self._RULES
            if rule.rule_identity == f"harness.evidence-catalog.{rule_name}"
        )
        return ValidationFinding.create(
            rule_identity=rule,
            code=code,
            subject_identity=state.identity.sha256,
            summary=summary,
            affected_paths=affected_paths,
        )


class HarnessStateValidator:
    """Compose explicit domain validators and aggregate-level Harness rules.

    Parameters
    ----------
    validators
        Ordered tuple of structural :class:`HarnessDomainValidator` objects. No
        registry or default validator set is discovered. Decision-sequence and
        cross-domain resource closure rules are always applied by this coordinator.

    Notes
    -----
    The coordinator applies every validator. An unexpected child exception becomes an
    identified ``error`` result without copying exception text or fabricating success.
    """

    __slots__ = ("_validators",)
    _TOOL = "ksdft2effmass.harness.validation:1"
    _DECISION_RULES = tuple(
        ValidationRuleIdentity(
            requirement_identity="harness.decision-sequence.closure",
            rule_identity=f"harness.decision-sequence.{name}",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        for name in (
            "identities-unique",
            "predecessors-exist",
            "predecessors-acyclic",
            "task-references-exist",
            "canonical-order",
        )
    )
    _CLOSURE_RULES = (
        ValidationRuleIdentity(
            requirement_identity="harness.cross-domain.closure",
            rule_identity="harness.cross-domain.skill-resources-exist",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        ),
    )

    def __init__(self, validators: tuple[HarnessDomainValidator, ...]) -> None:
        if type(validators) is not tuple or any(
            not isinstance(validator, HarnessDomainValidator)
            for validator in validators
        ):
            raise TypeError("validators must contain HarnessDomainValidator values")
        for validator in validators:
            rules = validator.rule_identities
            if type(rules) is not tuple or any(
                type(rule) is not ValidationRuleIdentity for rule in rules
            ):
                raise TypeError(
                    "each validator must expose a ValidationRuleIdentity tuple"
                )
            if rules != tuple(sorted(rules, key=lambda rule: rule.sort_key)):
                raise ValueError("validator rule identities must be sorted")
            names = tuple(rule.rule_identity for rule in rules)
            if len(set(names)) != len(names):
                raise ValueError("one validator must not repeat a rule identity")
        rule_ids = tuple(
            rule.rule_identity
            for validator in validators
            for rule in validator.rule_identities
        )
        internal_ids = tuple(
            rule.rule_identity for rule in self._DECISION_RULES + self._CLOSURE_RULES
        )
        if len(set(rule_ids + internal_ids)) != len(rule_ids + internal_ids):
            raise ValueError("validator rule identities must be globally unique")
        self._validators = validators

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return every composed domain and aggregate rule in canonical order."""
        domain_rules = tuple(
            rule for validator in self._validators for rule in validator.rule_identities
        )
        return tuple(
            sorted(
                domain_rules + self._DECISION_RULES + self._CLOSURE_RULES,
                key=lambda rule: rule.sort_key,
            )
        )

    def execute(self, state: HarnessState) -> ValidationResult:
        """Apply all explicit validators and aggregate rules deterministically."""
        if type(state) is not HarnessState:
            raise TypeError("state must be HarnessState")
        children: list[ValidationResult] = []
        for validator in self._validators:
            try:
                result = validator.execute(state)
            except Exception as exc:
                result = ValidationResult.error(
                    validator_identity=type(validator).__name__,
                    rule_identities=validator.rule_identities,
                    summary="Domain validation could not establish pass or fail",
                    subject_identity=state.identity.sha256,
                    error_diagnostic=f"validator raised {type(exc).__name__}",
                    tool_identity=self._TOOL,
                )
            expected_rules = validator.rule_identities
            if type(result) is not ValidationResult:
                result = ValidationResult.error(
                    validator_identity=type(validator).__name__,
                    rule_identities=expected_rules,
                    summary="Domain validation returned the wrong result type",
                    subject_identity=state.identity.sha256,
                    error_diagnostic="child did not return ValidationResult",
                    tool_identity=self._TOOL,
                )
            elif result.subject_identity != state.identity.sha256:
                result = ValidationResult.error(
                    validator_identity=type(validator).__name__,
                    rule_identities=expected_rules,
                    summary="Domain validation returned a mismatched subject",
                    subject_identity=state.identity.sha256,
                    error_diagnostic="child result subject identity mismatch",
                    tool_identity=self._TOOL,
                )
            elif result.rule_identities != expected_rules:
                result = ValidationResult.error(
                    validator_identity=type(validator).__name__,
                    rule_identities=expected_rules,
                    summary="Domain validation returned mismatched rules",
                    subject_identity=state.identity.sha256,
                    error_diagnostic="child result rule identity mismatch",
                    tool_identity=self._TOOL,
                )
            children.append(result)
        children.append(self._decision_result(state))
        children.append(self._closure_result(state))
        return ValidationResult.composite(
            validator_identity="HarnessStateValidator:1",
            summary="Complete normalized Harness state validation",
            subject_identity=state.identity.sha256,
            child_results=tuple(children),
            tool_identity=self._TOOL,
        )

    def _decision_result(self, state: HarnessState) -> ValidationResult:
        decisions = state.decisions
        findings: list[ValidationFinding] = []
        decision_ids = tuple(decision.decision_id for decision in decisions)
        for decision_id in sorted(
            {value for value in decision_ids if decision_ids.count(value) > 1}
        ):
            findings.append(
                self._decision_finding(
                    state,
                    "identities-unique",
                    "HV.DECISION.DUPLICATE_ID",
                    f"Decision identity {decision_id} occurs more than once.",
                )
            )
        known_decisions = set(decision_ids)
        known_tasks = set(state.tasks.task_ids)
        for decision in decisions:
            predecessor = decision.predecessor_decision_id
            if predecessor is not None and predecessor not in known_decisions:
                findings.append(
                    self._decision_finding(
                        state,
                        "predecessors-exist",
                        "HV.DECISION.PREDECESSOR_MISSING",
                        (
                            f"Decision {decision.decision_id} names absent "
                            f"predecessor {predecessor}."
                        ),
                    )
                )
            if decision.task_id is not None and decision.task_id not in known_tasks:
                findings.append(
                    self._decision_finding(
                        state,
                        "task-references-exist",
                        "HV.DECISION.TASK_MISSING",
                        (
                            f"Decision {decision.decision_id} names absent Task "
                            f"{decision.task_id}."
                        ),
                    )
                )
        predecessors: dict[str, str | None] = {
            decision.decision_id: decision.predecessor_decision_id
            for decision in decisions
            if decision.predecessor_decision_id in known_decisions
        }
        for cycle in self._decision_cycles(predecessors):
            findings.append(
                self._decision_finding(
                    state,
                    "predecessors-acyclic",
                    "HV.DECISION.PREDECESSOR_CYCLE",
                    f"Decision predecessor cycle: {','.join(cycle)}.",
                )
            )
        canonical = tuple(
            sorted(
                decisions,
                key=lambda decision: (
                    (decision.predecessor_decision_id or "").encode("utf-8"),
                    decision.decision_id.encode("utf-8"),
                ),
            )
        )
        if decisions != canonical:
            findings.append(
                self._decision_finding(
                    state,
                    "canonical-order",
                    "HV.DECISION.NONCANONICAL_ORDER",
                    (
                        "Development decisions are not in canonical predecessor "
                        "and identity order."
                    ),
                )
            )
        return ValidationResult.from_findings(
            validator_identity="HarnessStateValidator.decision-sequence:1",
            rule_identities=self._DECISION_RULES,
            summary="Harness decision sequence closure",
            subject_identity=state.identity.sha256,
            findings=tuple(findings),
            tool_identity=self._TOOL,
        )

    def _closure_result(self, state: HarnessState) -> ValidationResult:
        findings: list[ValidationFinding] = []
        resource_ids = {
            resource.resource_id
            for manifest in state.resources.resources
            for resource in manifest.resources
        }
        rule = self._CLOSURE_RULES[0]
        for skill in state.capabilities.capabilities:
            for resource_id in skill.required_resource_ids:
                if resource_id not in resource_ids:
                    findings.append(
                        ValidationFinding.create(
                            rule_identity=rule,
                            code="HV.CLOSURE.SKILL_RESOURCE_MISSING",
                            subject_identity=state.identity.sha256,
                            summary=(
                                f"Skill {skill.skill_id} requires absent resource "
                                f"{resource_id}."
                            ),
                        )
                    )
        return ValidationResult.from_findings(
            validator_identity="HarnessStateValidator.cross-domain:1",
            rule_identities=self._CLOSURE_RULES,
            summary="Harness cross-domain closure",
            subject_identity=state.identity.sha256,
            findings=tuple(findings),
            tool_identity=self._TOOL,
        )

    def _decision_finding(
        self,
        state: HarnessState,
        rule_name: str,
        code: str,
        summary: str,
    ) -> ValidationFinding:
        rule = next(
            rule
            for rule in self._DECISION_RULES
            if rule.rule_identity == f"harness.decision-sequence.{rule_name}"
        )
        return ValidationFinding.create(
            rule_identity=rule,
            code=code,
            subject_identity=state.identity.sha256,
            summary=summary,
        )

    @staticmethod
    def _decision_cycles(
        predecessors: dict[str, str | None],
    ) -> tuple[tuple[str, ...], ...]:
        cycles: set[tuple[str, ...]] = set()
        for root in sorted(predecessors):
            path: list[str] = []
            positions: dict[str, int] = {}
            current: str | None = root
            while current is not None and current in predecessors:
                if current in positions:
                    cycle = path[positions[current] :]
                    rotations = [
                        tuple(cycle[index:] + cycle[:index])
                        for index in range(len(cycle))
                    ]
                    cycles.add(min(rotations))
                    break
                positions[current] = len(path)
                path.append(current)
                current = predecessors[current]
        return tuple(sorted(cycles))


__all__ = (
    "ValidationApplicability",
    "ValidationStatus",
    "ActivationReferenceRequirement",
    "DevelopmentTaskSelectionValidationPolicy",
    "ValidationRuleIdentity",
    "ValidationFinding",
    "ValidationResult",
    "HarnessDomainValidator",
    "DevelopmentTaskSelectionValidator",
    "HarnessTaskGraphValidator",
    "HarnessCapabilityCatalogValidator",
    "HarnessResourceCatalogValidator",
    "HarnessEvidenceCatalogValidator",
    "HarnessStateValidator",
)
