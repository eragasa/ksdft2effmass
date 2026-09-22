"""Explicit-input coding-standards conformance over identified source subjects.

Policies own requirement meaning, profiles bind every policy requirement to an
explicit compatible adapter and configuration, and adapters return the shared
immutable :class:`ValidationResult`.  This module performs no source discovery,
filesystem access, repair, behavioral test execution, promotion, or authority
selection.  A passing result establishes only the represented structural checks.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Protocol, runtime_checkable

from .validation import ValidationResult, ValidationRuleIdentity, ValidationStatus


class ConformanceInputRole(StrEnum):
    """Closed semantic roles for explicit conformance inputs."""

    SOURCE = "source"
    OWNERSHIP = "ownership"
    PROFILE = "profile"
    MIGRATION = "migration"
    AUTHORED_TEST_RESOURCE = "authored_test_resource"


class _ConformanceIdentity:
    """Own deterministic framed SHA-256 identities for conformance values."""

    __slots__ = ()
    _DIGEST = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)

    @classmethod
    def require_digest(cls, value: str, name: str) -> None:
        """Require one lowercase SHA-256 hexadecimal identity."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if cls._DIGEST.fullmatch(value) is None:
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")

    @staticmethod
    def require_text(value: str, name: str) -> None:
        """Require normalized nonempty single-line text."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")

    @staticmethod
    def digest(domain: str, values: tuple[str, ...]) -> str:
        """Return one domain-separated length-framed SHA-256 identity."""
        digest = hashlib.sha256()
        for value in (domain, *values):
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
        return digest.hexdigest()


@dataclass(frozen=True, slots=True, kw_only=True)
class ConformanceInput:
    """Represent one exact caller-supplied source or support input.

    Parameters
    ----------
    input_identity
        Stable identity unique within one subject.
    role
        Semantic input role selected by the caller.
    path
        Normalized repository-relative POSIX diagnostic path.
    expected_sha256, expected_byte_count
        Caller-supplied SHA-256 identity and exact byte size. The count accepts only a
        nonnegative built-in ``int`` excluding ``bool`` and has no fixed-width
        overflow boundary beyond Python's integer and available-memory limits.
    payload, read_error
        Exactly one successful byte payload or sanitized read failure.

    Notes
    -----
    Expected and observed bytes may disagree so the conformance action can return a
    closed error result rather than construction hiding the mismatch.
    """

    input_identity: str
    role: ConformanceInputRole
    path: PurePosixPath
    expected_sha256: str
    expected_byte_count: int
    payload: bytes | None
    read_error: str | None

    def __post_init__(self) -> None:
        _ConformanceIdentity.require_text(self.input_identity, "input_identity")
        if type(self.role) is not ConformanceInputRole:
            raise TypeError("role must be ConformanceInputRole")
        if type(self.path) is not PurePosixPath:
            raise TypeError("path must be PurePosixPath")
        path = self.path.as_posix()
        if (
            path in {"", "."}
            or self.path.is_absolute()
            or ".." in self.path.parts
            or "\\" in path
            or unicodedata.normalize("NFC", path) != path
        ):
            raise ValueError("path must be a normalized repository-relative POSIX path")
        _ConformanceIdentity.require_digest(self.expected_sha256, "expected_sha256")
        if type(self.expected_byte_count) is not int:
            raise TypeError("expected_byte_count must be a built-in int")
        if self.expected_byte_count < 0:
            raise ValueError("expected_byte_count must be nonnegative")
        if self.payload is not None and type(self.payload) is not bytes:
            raise TypeError("payload must be bytes or None")
        if self.read_error is not None:
            _ConformanceIdentity.require_text(self.read_error, "read_error")
        if (self.payload is None) == (self.read_error is None):
            raise ValueError("exactly one payload or read_error is required")

    @classmethod
    def from_payload(
        cls,
        *,
        input_identity: str,
        role: ConformanceInputRole,
        path: PurePosixPath,
        payload: bytes,
    ) -> ConformanceInput:
        """Construct one successful input with its observed exact identity."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        return cls(
            input_identity=input_identity,
            role=role,
            path=path,
            expected_sha256=hashlib.sha256(payload).hexdigest(),
            expected_byte_count=len(payload),
            payload=payload,
            read_error=None,
        )

    @property
    def observed_identity_matches(self) -> bool:
        """Return whether successful bytes match the caller's expected identity."""
        return bool(
            self.payload is not None
            and len(self.payload) == self.expected_byte_count
            and hashlib.sha256(self.payload).hexdigest() == self.expected_sha256
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ConformanceSubject:
    """Identify one closed source subject and its explicit input inventory."""

    subject_family_identity: str
    inputs: tuple[ConformanceInput, ...]
    subject_identity: str = ""

    def __post_init__(self) -> None:
        _ConformanceIdentity.require_text(
            self.subject_family_identity, "subject_family_identity"
        )
        if type(self.inputs) is not tuple or any(
            type(item) is not ConformanceInput for item in self.inputs
        ):
            raise TypeError("inputs must contain ConformanceInput values")
        if not self.inputs:
            raise ValueError("inputs must be nonempty")
        order = tuple(
            sorted(
                self.inputs,
                key=lambda item: (
                    item.input_identity,
                    item.role.value,
                    item.path.as_posix(),
                ),
            )
        )
        if self.inputs != order:
            raise ValueError("inputs must be deterministically sorted")
        input_ids = tuple(item.input_identity for item in self.inputs)
        paths = tuple(item.path for item in self.inputs)
        if len(set(input_ids)) != len(input_ids):
            raise ValueError("input identities must be unique")
        if len(set(paths)) != len(paths):
            raise ValueError("input paths must be unique")
        expected = _ConformanceIdentity.digest(
            "ksdft2effmass.harness.conformance-subject.v1",
            (
                self.subject_family_identity,
                *(
                    value
                    for item in self.inputs
                    for value in (
                        item.input_identity,
                        item.role.value,
                        item.path.as_posix(),
                        item.expected_sha256,
                        str(item.expected_byte_count),
                    )
                ),
            ),
        )
        if self.subject_identity == "":
            object.__setattr__(self, "subject_identity", expected)
        else:
            _ConformanceIdentity.require_digest(
                self.subject_identity, "subject_identity"
            )
            if self.subject_identity != expected:
                raise ValueError("subject_identity does not match the input inventory")

    def inputs_for_role(
        self, role: ConformanceInputRole
    ) -> tuple[ConformanceInput, ...]:
        """Return inputs with one exact role in canonical subject order."""
        if type(role) is not ConformanceInputRole:
            raise TypeError("role must be ConformanceInputRole")
        return tuple(item for item in self.inputs if item.role is role)


@dataclass(frozen=True, slots=True, kw_only=True)
class CodingStandardRequirement:
    """Bind one validation rule identity to its policy-owned meaning."""

    rule_identity: ValidationRuleIdentity
    description: str

    def __post_init__(self) -> None:
        if type(self.rule_identity) is not ValidationRuleIdentity:
            raise TypeError("rule_identity must be ValidationRuleIdentity")
        _ConformanceIdentity.require_text(self.description, "description")


@dataclass(frozen=True, slots=True, kw_only=True)
class CodingStandardsPolicy:
    """Represent one immutable identified coding-standards policy revision."""

    policy_identity: str
    policy_version: str
    requirements: tuple[CodingStandardRequirement, ...]
    content_identity: str = ""

    def __post_init__(self) -> None:
        _ConformanceIdentity.require_text(self.policy_identity, "policy_identity")
        _ConformanceIdentity.require_text(self.policy_version, "policy_version")
        if type(self.requirements) is not tuple or any(
            type(item) is not CodingStandardRequirement for item in self.requirements
        ):
            raise TypeError(
                "requirements must contain CodingStandardRequirement values"
            )
        if not self.requirements:
            raise ValueError("requirements must be nonempty")
        order = tuple(
            sorted(self.requirements, key=lambda item: item.rule_identity.sort_key)
        )
        if self.requirements != order:
            raise ValueError("requirements must be deterministically sorted")
        names = tuple(item.rule_identity.rule_identity for item in self.requirements)
        if len(set(names)) != len(names):
            raise ValueError("requirement rule identities must be unique")
        expected = _ConformanceIdentity.digest(
            "ksdft2effmass.harness.coding-standards-policy.v1",
            (
                self.policy_identity,
                self.policy_version,
                *(
                    value
                    for requirement in self.requirements
                    for value in (
                        requirement.rule_identity.requirement_identity,
                        requirement.rule_identity.rule_identity,
                        requirement.rule_identity.version_identity,
                        "required"
                        if requirement.rule_identity.required
                        else "optional",
                        "na-permitted"
                        if requirement.rule_identity.not_applicable_permitted
                        else "na-prohibited",
                        requirement.description,
                    )
                ),
            ),
        )
        if self.content_identity == "":
            object.__setattr__(self, "content_identity", expected)
        else:
            _ConformanceIdentity.require_digest(
                self.content_identity, "content_identity"
            )
            if self.content_identity != expected:
                raise ValueError("content_identity does not match policy semantics")

    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
        """Return policy rules in canonical order."""
        return tuple(item.rule_identity for item in self.requirements)


@dataclass(frozen=True, slots=True, kw_only=True)
class ConformanceAdapterConfiguration:
    """Represent exact immutable adapter configuration bytes."""

    configuration_identity: str
    adapter_identity: str
    adapter_version: str
    payload: bytes

    def __post_init__(self) -> None:
        _ConformanceIdentity.require_text(self.adapter_identity, "adapter_identity")
        _ConformanceIdentity.require_text(self.adapter_version, "adapter_version")
        if type(self.payload) is not bytes:
            raise TypeError("payload must be bytes")
        expected = hashlib.sha256(self.payload).hexdigest()
        if self.configuration_identity == "":
            object.__setattr__(self, "configuration_identity", expected)
        else:
            _ConformanceIdentity.require_digest(
                self.configuration_identity, "configuration_identity"
            )
            if self.configuration_identity != expected:
                raise ValueError("configuration_identity does not match payload")


@dataclass(frozen=True, slots=True, kw_only=True)
class ConformanceProfileBinding:
    """Bind one policy rule to an exact adapter and configuration revision."""

    rule_identity: str
    adapter_identity: str
    adapter_version: str
    configuration_identity: str

    def __post_init__(self) -> None:
        for name in ("rule_identity", "adapter_identity", "adapter_version"):
            _ConformanceIdentity.require_text(getattr(self, name), name)
        _ConformanceIdentity.require_digest(
            self.configuration_identity, "configuration_identity"
        )

    @property
    def sort_key(self) -> tuple[str, str, str, str]:
        """Return deterministic rule and adapter binding order."""
        return (
            self.rule_identity,
            self.adapter_identity,
            self.adapter_version,
            self.configuration_identity,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ConformanceProfile:
    """Map every policy rule to an adapter without changing requirement meaning."""

    profile_identity: str
    profile_version: str
    subject_family_identity: str
    policy_identity: str
    policy_version: str
    policy_content_identity: str
    bindings: tuple[ConformanceProfileBinding, ...]
    content_identity: str = ""

    def __post_init__(self) -> None:
        for name in (
            "profile_identity",
            "profile_version",
            "subject_family_identity",
            "policy_identity",
            "policy_version",
        ):
            _ConformanceIdentity.require_text(getattr(self, name), name)
        _ConformanceIdentity.require_digest(
            self.policy_content_identity, "policy_content_identity"
        )
        if type(self.bindings) is not tuple or any(
            type(item) is not ConformanceProfileBinding for item in self.bindings
        ):
            raise TypeError("bindings must contain ConformanceProfileBinding values")
        if not self.bindings:
            raise ValueError("bindings must be nonempty")
        if self.bindings != tuple(
            sorted(self.bindings, key=lambda item: item.sort_key)
        ):
            raise ValueError("bindings must be deterministically sorted")
        names = tuple(item.rule_identity for item in self.bindings)
        if len(set(names)) != len(names):
            raise ValueError("each rule must have exactly one profile binding")
        expected = _ConformanceIdentity.digest(
            "ksdft2effmass.harness.conformance-profile.v1",
            (
                self.profile_identity,
                self.profile_version,
                self.subject_family_identity,
                self.policy_identity,
                self.policy_version,
                self.policy_content_identity,
                *(value for binding in self.bindings for value in binding.sort_key),
            ),
        )
        if self.content_identity == "":
            object.__setattr__(self, "content_identity", expected)
        else:
            _ConformanceIdentity.require_digest(
                self.content_identity, "content_identity"
            )
            if self.content_identity != expected:
                raise ValueError("content_identity does not match profile semantics")


@runtime_checkable
class CodingStandardsAdapter(Protocol):
    """Structural contract for one explicit coding-standards adapter."""

    @property
    def adapter_identity(self) -> str:
        """Return the stable adapter identity."""
        ...

    @property
    def adapter_version(self) -> str:
        """Return the exact adapter behavior version."""
        ...

    @property
    def subject_family_identities(self) -> tuple[str, ...]:
        """Return supported subject families in canonical order."""
        ...

    @property
    def rule_identities(self) -> tuple[str, ...]:
        """Return supported policy rule identities in canonical order."""
        ...

    def execute(
        self,
        subject: ConformanceSubject,
        rules: tuple[ValidationRuleIdentity, ...],
        configuration: ConformanceAdapterConfiguration,
    ) -> ValidationResult:
        """Apply selected rules to one exact subject without mutation."""
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class ConformanceRequest:
    """Supply one complete explicit coding-standards conformance invocation."""

    subject: ConformanceSubject
    policy: CodingStandardsPolicy
    profile: ConformanceProfile
    adapters: tuple[CodingStandardsAdapter, ...]
    configurations: tuple[ConformanceAdapterConfiguration, ...]

    def __post_init__(self) -> None:
        if type(self.subject) is not ConformanceSubject:
            raise TypeError("subject must be ConformanceSubject")
        if type(self.policy) is not CodingStandardsPolicy:
            raise TypeError("policy must be CodingStandardsPolicy")
        if type(self.profile) is not ConformanceProfile:
            raise TypeError("profile must be ConformanceProfile")
        if type(self.adapters) is not tuple or any(
            not isinstance(item, CodingStandardsAdapter) for item in self.adapters
        ):
            raise TypeError("adapters must contain CodingStandardsAdapter values")
        if type(self.configurations) is not tuple or any(
            type(item) is not ConformanceAdapterConfiguration
            for item in self.configurations
        ):
            raise TypeError(
                "configurations must contain ConformanceAdapterConfiguration values"
            )
        adapter_order = tuple(
            sorted(
                self.adapters,
                key=lambda item: (item.adapter_identity, item.adapter_version),
            )
        )
        configuration_order = tuple(
            sorted(
                self.configurations,
                key=lambda item: (
                    item.adapter_identity,
                    item.adapter_version,
                    item.configuration_identity,
                ),
            )
        )
        if self.adapters != adapter_order or self.configurations != configuration_order:
            raise ValueError("adapters and configurations must be canonically sorted")
        adapters = tuple(
            (item.adapter_identity, item.adapter_version) for item in self.adapters
        )
        configurations = tuple(
            (
                item.adapter_identity,
                item.adapter_version,
                item.configuration_identity,
            )
            for item in self.configurations
        )
        if len(set(adapters)) != len(adapters):
            raise ValueError("adapter identity/version pairs must be unique")
        if len(set(configurations)) != len(configurations):
            raise ValueError("adapter configurations must be unique")


class CodingStandardsConformanceValidator:
    """Apply an explicit policy/profile/adapter composition deterministically."""

    __slots__ = ()
    _TOOL = "ksdft2effmass.harness.conformance:1"

    def execute(self, request: ConformanceRequest) -> ValidationResult:
        """Return one normalized result without discovery, repair, or authority."""
        if type(request) is not ConformanceRequest:
            raise TypeError("request must be ConformanceRequest")
        rules = request.policy.rule_identities
        input_problem = self._input_problem(request.subject)
        if input_problem is not None:
            return self._error(request, rules, input_problem)
        profile_problem = self._profile_problem(request)
        if profile_problem is not None:
            return self._error(request, rules, profile_problem)
        adapters = {
            (item.adapter_identity, item.adapter_version): item
            for item in request.adapters
        }
        configurations = {
            (
                item.adapter_identity,
                item.adapter_version,
                item.configuration_identity,
            ): item
            for item in request.configurations
        }
        rules_by_name = {rule.rule_identity: rule for rule in rules}
        groups: dict[tuple[str, str, str], list[ValidationRuleIdentity]] = {}
        for binding in request.profile.bindings:
            key = (
                binding.adapter_identity,
                binding.adapter_version,
                binding.configuration_identity,
            )
            groups.setdefault(key, []).append(rules_by_name[binding.rule_identity])
        results: list[ValidationResult] = []
        for key in sorted(groups):
            selected_rules = tuple(sorted(groups[key], key=lambda rule: rule.sort_key))
            adapter = adapters.get(key[:2])
            configuration = configurations.get(key)
            if adapter is None or configuration is None:
                results.append(
                    self._error(
                        request,
                        selected_rules,
                        "profile binding has no exact adapter and configuration",
                    )
                )
                continue
            if (
                request.subject.subject_family_identity
                not in adapter.subject_family_identities
                or any(
                    rule.rule_identity not in adapter.rule_identities
                    for rule in selected_rules
                )
            ):
                results.append(
                    self._error(
                        request,
                        selected_rules,
                        "adapter is incompatible with the selected subject or rules",
                    )
                )
                continue
            try:
                result = adapter.execute(request.subject, selected_rules, configuration)
            except Exception as exc:
                result = self._error(
                    request,
                    selected_rules,
                    f"adapter raised {type(exc).__name__}",
                )
            if (
                type(result) is not ValidationResult
                or result.subject_identity != request.subject.subject_identity
                or result.rule_identities != selected_rules
                or result.configuration_identity != configuration.configuration_identity
            ):
                result = self._error(
                    request,
                    selected_rules,
                    "adapter returned a mismatched normalized result",
                )
            results.append(result)
        return ValidationResult.composite(
            validator_identity="CodingStandardsConformanceValidator:1",
            summary="Explicit coding-standards conformance",
            subject_identity=request.subject.subject_identity,
            child_results=tuple(results),
            tool_identity=self._TOOL,
            configuration_identity=request.profile.content_identity,
            claim_boundary=(
                "structural coding-standards conformance only; excludes behavioral "
                "verification, scientific validity, promotion, authority, and "
                "acceptance"
            ),
        )

    @staticmethod
    def _input_problem(subject: ConformanceSubject) -> str | None:
        if any(item.read_error is not None for item in subject.inputs):
            return "one or more explicit inputs could not be read"
        if any(not item.observed_identity_matches for item in subject.inputs):
            return "one or more explicit input identities do not match supplied bytes"
        return None

    @staticmethod
    def _profile_problem(request: ConformanceRequest) -> str | None:
        profile = request.profile
        policy = request.policy
        if (
            profile.subject_family_identity != request.subject.subject_family_identity
            or profile.policy_identity != policy.policy_identity
            or profile.policy_version != policy.policy_version
            or profile.policy_content_identity != policy.content_identity
        ):
            return "profile does not identify the selected subject family and policy"
        policy_names = tuple(rule.rule_identity for rule in policy.rule_identities)
        binding_names = tuple(binding.rule_identity for binding in profile.bindings)
        if tuple(sorted(policy_names)) != binding_names:
            return "profile must bind every policy requirement exactly once"
        expected_adapters = {
            (binding.adapter_identity, binding.adapter_version)
            for binding in profile.bindings
        }
        actual_adapters = {
            (adapter.adapter_identity, adapter.adapter_version)
            for adapter in request.adapters
        }
        if actual_adapters != expected_adapters:
            return "adapters must exactly equal the profile-selected inventory"
        expected_configurations = {
            (
                binding.adapter_identity,
                binding.adapter_version,
                binding.configuration_identity,
            )
            for binding in profile.bindings
        }
        actual_configurations = {
            (
                configuration.adapter_identity,
                configuration.adapter_version,
                configuration.configuration_identity,
            )
            for configuration in request.configurations
        }
        if actual_configurations != expected_configurations:
            return "configurations must exactly equal the profile-selected inventory"
        return None

    def _error(
        self,
        request: ConformanceRequest,
        rules: tuple[ValidationRuleIdentity, ...],
        diagnostic: str,
    ) -> ValidationResult:
        return ValidationResult.error(
            validator_identity="CodingStandardsConformanceValidator:1",
            rule_identities=rules,
            summary="Coding-standards conformance could not establish pass or fail",
            subject_identity=request.subject.subject_identity,
            error_diagnostic=diagnostic,
            tool_identity=self._TOOL,
            configuration_identity=request.profile.content_identity,
            claim_boundary=(
                "structural coding-standards conformance only; excludes behavioral "
                "verification, scientific validity, promotion, authority, and "
                "acceptance"
            ),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ConformanceReport:
    """Derived immutable view over one identified normalized validation result."""

    source_result_identity: str
    subject_identity: str
    status: ValidationStatus
    blocking: bool
    rule_identities: tuple[str, ...]
    finding_identities: tuple[str, ...]
    affected_paths: tuple[str, ...]
    report_identity: str = ""

    def __post_init__(self) -> None:
        _ConformanceIdentity.require_digest(
            self.source_result_identity, "source_result_identity"
        )
        _ConformanceIdentity.require_text(self.subject_identity, "subject_identity")
        if type(self.status) is not ValidationStatus:
            raise TypeError("status must be ValidationStatus")
        if type(self.blocking) is not bool:
            raise TypeError("blocking must be bool")
        for name in ("rule_identities", "finding_identities", "affected_paths"):
            values = getattr(self, name)
            if type(values) is not tuple or any(
                type(value) is not str for value in values
            ):
                raise TypeError(f"{name} must contain built-in str values")
            if values != tuple(sorted(set(values))):
                raise ValueError(f"{name} must be sorted and unique")
        for value in self.finding_identities:
            _ConformanceIdentity.require_digest(value, "finding identity")
        expected = _ConformanceIdentity.digest(
            "ksdft2effmass.harness.conformance-report.v1",
            (
                self.source_result_identity,
                self.subject_identity,
                self.status.value,
                "blocking" if self.blocking else "nonblocking",
                *self.rule_identities,
                *self.finding_identities,
                *self.affected_paths,
            ),
        )
        if self.report_identity == "":
            object.__setattr__(self, "report_identity", expected)
        else:
            _ConformanceIdentity.require_digest(self.report_identity, "report_identity")
            if self.report_identity != expected:
                raise ValueError("report_identity does not match report semantics")


class ConformanceReportProjector:
    """Derive a report without replacing or mutating its source result."""

    __slots__ = ()

    def execute(self, result: ValidationResult) -> ConformanceReport:
        """Project one exact validation result into a compact immutable view."""
        if type(result) is not ValidationResult:
            raise TypeError("result must be ValidationResult")
        return ConformanceReport(
            source_result_identity=result.result_identity,
            subject_identity=result.subject_identity,
            status=result.status,
            blocking=result.blocking,
            rule_identities=tuple(
                sorted(rule.rule_identity for rule in result.rule_identities)
            ),
            finding_identities=tuple(
                sorted(finding.finding_identity for finding in result.findings)
            ),
            affected_paths=result.affected_paths,
        )
