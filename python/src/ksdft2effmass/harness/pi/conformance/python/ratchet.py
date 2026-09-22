"""Versioned production-source architecture conformance ratchet.

This unsupported implementation sibling composes the accepted explicit production
facts, callable/private rules, and named dependency-graph views. Every invocation
receives immutable subject, policy, profile, configuration, source, and inherited
baseline identities. The baseline remains a visible historical comparison input: it
is neither an approval nor a mutable or permanent waiver. Only newly introduced
syntax-deterministic violations fail the ratchet.

The component performs no ambient discovery, route-support classification, source
repair, export mutation, dependency change, runtime-semantic inference, scientific
assessment, Task acceptance, or successor activation. Structural software-verification
success establishes only the bounded represented contract.
"""

from __future__ import annotations

import base64
import hashlib
import json
import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import ClassVar

from .callable_private import (
    PythonArchitectureFinding,
    PythonArchitectureRuleClassification,
    PythonCallableIdentity,
    PythonCallablePrivateRuleEvaluator,
    PythonCallablePrivateRuleRequest,
    PythonHookCallableShape,
    PythonHookOwnerKind,
    PythonModuleHookException,
)
from .dependency_graph import (
    PythonAcceptedDependencyContract,
    PythonDependencyDirection,
    PythonDependencyDirectionCheck,
    PythonDependencyDirectionStatus,
    PythonDependencyGraphAnalyzer,
    PythonDependencyGraphRequest,
    PythonDependencyGraphResult,
    PythonDependencyGraphView,
    PythonDependencyModule,
)
from .production import (
    PythonProductionCallableKind,
    PythonProductionInspectionResult,
    PythonProductionLocation,
    PythonProductionSource,
    PythonProductionSourceInspector,
    PythonProductionSourceProfile,
)


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonProductionContentIdentity:
    """Identify exact bytes by SHA-256 and byte count.

    Parameters
    ----------
    sha256
        Lowercase hexadecimal SHA-256 digest.
    byte_count
        Exact nonnegative byte count.
    """

    sha256: str
    byte_count: int

    def __post_init__(self) -> None:
        """Require an exact SHA-256 identity and built-in integer count."""
        if type(self.sha256) is not str:
            raise TypeError("sha256 must be a built-in str")
        if len(self.sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256
        ):
            raise ValueError("sha256 must be lowercase SHA-256 hexadecimal")
        if type(self.byte_count) is not int:
            raise TypeError("byte_count must be a built-in int")
        if self.byte_count < 0:
            raise ValueError("byte_count must be nonnegative")

    @classmethod
    def from_bytes(cls, payload: bytes) -> PythonProductionContentIdentity:
        """Return the exact identity of one immutable byte payload."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        return cls(sha256=hashlib.sha256(payload).hexdigest(), byte_count=len(payload))


class PythonJsonStringSerializer:
    """Encode one exact Python string as a complete deterministic JSON string."""

    __slots__ = ()

    def execute(self, value: str) -> str:
        """Return RFC 8259-compatible JSON text for one built-in string."""
        if type(value) is not str:
            raise TypeError("value must be a built-in str")
        return json.dumps(
            value, ensure_ascii=True, allow_nan=False, separators=(",", ":")
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionConformanceSubject:
    """Identify one exact production-source subject independently of support status."""

    SUBJECT_FAMILY: ClassVar[str] = "python.production-source"
    SUBJECT_VERSION: ClassVar[str] = "1"

    subject_family: str
    subject_version: str
    subject_identity: str

    def __post_init__(self) -> None:
        """Require the versioned sibling family and normalized logical identity."""
        if (
            type(self.subject_family) is not str
            or type(self.subject_version) is not str
        ):
            raise TypeError("subject family and version must be built-in str values")
        if (self.subject_family, self.subject_version) != (
            self.SUBJECT_FAMILY,
            self.SUBJECT_VERSION,
        ):
            raise ValueError("production conformance subject identity is unsupported")
        self._require_text(self.subject_identity, "subject_identity")

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require normalized nonempty single-line built-in text."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionConformancePolicy:
    """Represent the exact version-one deterministic production ratchet policy.

    The policy includes source-input failures, the four accepted deterministic
    callable/private rule identities, and explicit dependency-direction outcomes.
    Structural observations and review-only signals remain visible but never become
    deterministic violations.
    """

    POLICY_IDENTITY: ClassVar[str] = "ksdft2effmass.python.production-conformance"
    POLICY_VERSION: ClassVar[str] = "1"
    SOURCE_FAILURE_RULE: ClassVar[str] = "python.production-source.input-failure.v1"
    DEPENDENCY_DIRECTION_RULE: ClassVar[str] = (
        "python.dependency-direction.exact-edge.v1"
    )
    DETERMINISTIC_RULES: ClassVar[tuple[str, ...]] = (
        SOURCE_FAILURE_RULE,
        "python.callable-private.hook-exception-integrity.v1",
        "python.callable-private.module-callable-owner.v1",
        "python.callable-private.top-level-class-name.v1",
        "python.callable-private.cross-owner-private-call.v1",
        DEPENDENCY_DIRECTION_RULE,
    )

    policy_identity: str = POLICY_IDENTITY
    policy_version: str = POLICY_VERSION
    deterministic_rule_identities: tuple[str, ...] = DETERMINISTIC_RULES

    def __post_init__(self) -> None:
        """Reject policy identity, version, omission, addition, or ordering changes."""
        if (
            type(self.policy_identity) is not str
            or type(self.policy_version) is not str
        ):
            raise TypeError("policy identity and version must be built-in str values")
        if (self.policy_identity, self.policy_version) != (
            self.POLICY_IDENTITY,
            self.POLICY_VERSION,
        ):
            raise ValueError("production conformance policy identity is unsupported")
        if self.deterministic_rule_identities != self.DETERMINISTIC_RULES:
            raise ValueError("deterministic rule inventory must equal policy version 1")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionConformanceProfile:
    """Bind exact subject, policy, and prerequisite profile versions."""

    PROFILE_IDENTITY: ClassVar[str] = "ksdft2effmass.python.production-ratchet"
    PROFILE_VERSION: ClassVar[str] = "1"

    profile_identity: str = PROFILE_IDENTITY
    profile_version: str = PROFILE_VERSION
    subject_family: str = PythonProductionConformanceSubject.SUBJECT_FAMILY
    subject_version: str = PythonProductionConformanceSubject.SUBJECT_VERSION
    policy_identity: str = PythonProductionConformancePolicy.POLICY_IDENTITY
    policy_version: str = PythonProductionConformancePolicy.POLICY_VERSION
    production_profile_identity: str = PythonProductionSourceProfile.PROFILE_IDENTITY
    production_profile_version: str = PythonProductionSourceProfile.PROFILE_VERSION

    def __post_init__(self) -> None:
        """Require the exact implemented production ratchet binding."""
        values = (
            self.profile_identity,
            self.profile_version,
            self.subject_family,
            self.subject_version,
            self.policy_identity,
            self.policy_version,
            self.production_profile_identity,
            self.production_profile_version,
        )
        if any(type(value) is not str for value in values):
            raise TypeError("profile binding identities must be built-in str values")
        expected = (
            self.PROFILE_IDENTITY,
            self.PROFILE_VERSION,
            PythonProductionConformanceSubject.SUBJECT_FAMILY,
            PythonProductionConformanceSubject.SUBJECT_VERSION,
            PythonProductionConformancePolicy.POLICY_IDENTITY,
            PythonProductionConformancePolicy.POLICY_VERSION,
            PythonProductionSourceProfile.PROFILE_IDENTITY,
            PythonProductionSourceProfile.PROFILE_VERSION,
        )
        if values != expected:
            raise ValueError("production conformance profile binding is unsupported")


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonProductionModuleBinding:
    """Bind one exact source input identity to a module and explicit facade status."""

    input_identity: str
    module_name: str
    is_package_facade: bool

    def __post_init__(self) -> None:
        """Require normalized identities, a dotted module name, and exact Boolean."""
        self._require_text(self.input_identity, "input_identity")
        self._require_text(self.module_name, "module_name")
        if any(not part.isidentifier() for part in self.module_name.split(".")):
            raise ValueError("module_name must contain dotted Python identifiers")
        if type(self.is_package_facade) is not bool:
            raise TypeError("is_package_facade must be a built-in bool")

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require one intrinsic normalized nonempty single-line text field."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionConformanceConfiguration:
    """Represent exact content-identified configuration for one ratchet invocation."""

    content_identity: PythonProductionContentIdentity
    subject: PythonProductionConformanceSubject
    policy: PythonProductionConformancePolicy
    profile: PythonProductionConformanceProfile
    module_bindings: tuple[PythonProductionModuleBinding, ...]
    hook_exceptions: tuple[PythonModuleHookException, ...]
    direction_checks: tuple[PythonDependencyDirectionCheck, ...]

    def __post_init__(self) -> None:
        """Require exact closed values and unambiguous canonical binding order."""
        if type(self.content_identity) is not PythonProductionContentIdentity:
            raise TypeError("content_identity must be PythonProductionContentIdentity")
        if type(self.subject) is not PythonProductionConformanceSubject:
            raise TypeError("subject must be PythonProductionConformanceSubject")
        if type(self.policy) is not PythonProductionConformancePolicy:
            raise TypeError("policy must be PythonProductionConformancePolicy")
        if type(self.profile) is not PythonProductionConformanceProfile:
            raise TypeError("profile must be PythonProductionConformanceProfile")
        if (
            self.profile.subject_family,
            self.profile.subject_version,
        ) != (self.subject.subject_family, self.subject.subject_version):
            raise ValueError("profile and subject identities mismatch")
        if (
            self.profile.policy_identity,
            self.profile.policy_version,
        ) != (self.policy.policy_identity, self.policy.policy_version):
            raise ValueError("profile and policy identities mismatch")
        if type(self.module_bindings) is not tuple or any(
            type(binding) is not PythonProductionModuleBinding
            for binding in self.module_bindings
        ):
            raise TypeError("module_bindings must contain module-binding values")
        if self.module_bindings != tuple(sorted(self.module_bindings)):
            raise ValueError("module_bindings must be in canonical order")
        if len(set(self.module_bindings)) != len(self.module_bindings):
            raise ValueError("module_bindings must be unique")
        if len({item.input_identity for item in self.module_bindings}) != len(
            self.module_bindings
        ):
            raise ValueError("module_bindings must have unique input identities")
        if len({item.module_name for item in self.module_bindings}) != len(
            self.module_bindings
        ):
            raise ValueError("module_bindings must have unique module names")
        if type(self.hook_exceptions) is not tuple or any(
            type(item) is not PythonModuleHookException for item in self.hook_exceptions
        ):
            raise TypeError("hook_exceptions must contain hook-exception values")
        if self.hook_exceptions != tuple(
            sorted(self.hook_exceptions, key=lambda item: item.sort_key)
        ):
            raise ValueError("hook_exceptions must be in canonical order")
        if len(set(self.hook_exceptions)) != len(self.hook_exceptions):
            raise ValueError("hook_exceptions must be unique")
        if type(self.direction_checks) is not tuple or any(
            type(item) is not PythonDependencyDirectionCheck
            for item in self.direction_checks
        ):
            raise TypeError("direction_checks must contain direction-check values")
        if self.direction_checks != tuple(
            sorted(self.direction_checks, key=lambda item: item.sort_key)
        ):
            raise ValueError("direction_checks must be in canonical order")
        if len({item.sort_key for item in self.direction_checks}) != len(
            self.direction_checks
        ):
            raise ValueError("direction_checks must be unique")


class PythonProductionConformanceConfigurationSerializer:
    """Decode and encode the complete canonical version-one configuration.

    Module bindings, exact hook exceptions, and direction checks with their optional
    accepted contracts are all represented in the content-identified bytes.
    """

    __slots__ = ()
    HEADER = "python.production-conformance-configuration\t1"

    def execute(
        self, payload: bytes, expected_identity: PythonProductionContentIdentity
    ) -> PythonProductionConformanceConfiguration:
        """Decode exact bytes and fail closed on content or profile mismatch."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        if type(expected_identity) is not PythonProductionContentIdentity:
            raise TypeError("expected_identity must be PythonProductionContentIdentity")
        actual = PythonProductionContentIdentity.from_bytes(payload)
        if actual != expected_identity:
            raise ValueError("configuration content identity mismatch")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("configuration must be UTF-8") from error
        if not text.endswith("\n"):
            raise ValueError("configuration must end with one newline")
        lines = text[:-1].split("\n")
        if not lines or lines[0] != self.HEADER:
            raise ValueError("configuration header or version mismatch")
        if len(lines) < 5:
            raise ValueError("configuration is incomplete")
        subject_fields = lines[1].split("\t")
        policy_fields = lines[2].split("\t")
        profile_fields = lines[3].split("\t")
        production_fields = lines[4].split("\t")
        if len(subject_fields) != 4 or subject_fields[0] != "subject":
            raise ValueError("configuration subject record is malformed")
        if len(policy_fields) != 3 or policy_fields[0] != "policy":
            raise ValueError("configuration policy record is malformed")
        if len(profile_fields) != 3 or profile_fields[0] != "profile":
            raise ValueError("configuration profile record is malformed")
        if len(production_fields) != 3 or production_fields[0] != "production":
            raise ValueError("configuration production profile record is malformed")
        subject = PythonProductionConformanceSubject(
            subject_family=self.decode_text(subject_fields[1]),
            subject_version=self.decode_text(subject_fields[2]),
            subject_identity=self.decode_text(subject_fields[3]),
        )
        policy = PythonProductionConformancePolicy(
            policy_identity=self.decode_text(policy_fields[1]),
            policy_version=self.decode_text(policy_fields[2]),
        )
        profile = PythonProductionConformanceProfile(
            profile_identity=self.decode_text(profile_fields[1]),
            profile_version=self.decode_text(profile_fields[2]),
            subject_family=subject.subject_family,
            subject_version=subject.subject_version,
            policy_identity=policy.policy_identity,
            policy_version=policy.policy_version,
            production_profile_identity=self.decode_text(production_fields[1]),
            production_profile_version=self.decode_text(production_fields[2]),
        )
        bindings: list[PythonProductionModuleBinding] = []
        hooks: list[PythonModuleHookException] = []
        checks: list[PythonDependencyDirectionCheck] = []
        for line in lines[5:]:
            fields = line.split("\t")
            if fields[0] == "module":
                bindings.append(self._module(fields))
            elif fields[0] == "hook":
                hooks.append(self._hook(fields))
            elif fields[0] == "direction":
                checks.append(self._direction(fields))
            else:
                raise ValueError("configuration record kind is unsupported")
        configuration = PythonProductionConformanceConfiguration(
            content_identity=actual,
            subject=subject,
            policy=policy,
            profile=profile,
            module_bindings=tuple(bindings),
            hook_exceptions=tuple(hooks),
            direction_checks=tuple(checks),
        )
        if self.encode(configuration, include_content_identity=False) != payload:
            raise ValueError("configuration is not in canonical representation")
        return configuration

    def encode(
        self,
        configuration: PythonProductionConformanceConfiguration,
        *,
        include_content_identity: bool = True,
    ) -> bytes:
        """Encode every consumed configuration field in canonical order."""
        if type(configuration) is not PythonProductionConformanceConfiguration:
            raise TypeError(
                "configuration must be PythonProductionConformanceConfiguration"
            )
        encode = self.encode_text
        lines = [
            self.HEADER,
            (
                f"subject\t{encode(configuration.subject.subject_family)}\t"
                f"{encode(configuration.subject.subject_version)}\t"
                f"{encode(configuration.subject.subject_identity)}"
            ),
            (
                f"policy\t{encode(configuration.policy.policy_identity)}\t"
                f"{encode(configuration.policy.policy_version)}"
            ),
            (
                f"profile\t{encode(configuration.profile.profile_identity)}\t"
                f"{encode(configuration.profile.profile_version)}"
            ),
            (
                "production\t"
                f"{encode(configuration.profile.production_profile_identity)}\t"
                f"{encode(configuration.profile.production_profile_version)}"
            ),
        ]
        lines.extend(
            self._encode_module(item) for item in configuration.module_bindings
        )
        lines.extend(self._encode_hook(item) for item in configuration.hook_exceptions)
        lines.extend(
            self._encode_direction(item) for item in configuration.direction_checks
        )
        payload = ("\n".join(lines) + "\n").encode("utf-8")
        if include_content_identity and (
            PythonProductionContentIdentity.from_bytes(payload)
            != configuration.content_identity
        ):
            raise ValueError("configuration fields disagree with content identity")
        return payload

    def _module(self, fields: list[str]) -> PythonProductionModuleBinding:
        """Decode one exact module-binding record."""
        if len(fields) != 4:
            raise ValueError("configuration module record is malformed")
        if fields[3] not in {"0", "1"}:
            raise ValueError("configuration facade flag must be 0 or 1")
        return PythonProductionModuleBinding(
            input_identity=self.decode_text(fields[1]),
            module_name=self.decode_text(fields[2]),
            is_package_facade=fields[3] == "1",
        )

    def _hook(self, fields: list[str]) -> PythonModuleHookException:
        """Decode one complete exact hook-exception record."""
        if len(fields) != 12:
            raise ValueError("configuration hook record is malformed")
        try:
            location = PythonProductionLocation(
                line=self._positive(fields[5], "hook line"),
                column=self._nonnegative(fields[6], "hook column"),
                end_line=self._positive(fields[7], "hook end line"),
                end_column=self._nonnegative(fields[8], "hook end column"),
            )
            callable_identity = PythonCallableIdentity(
                qualified_name=self.decode_text(fields[3]),
                kind=PythonProductionCallableKind(fields[4]),
                location=location,
            )
            return PythonModuleHookException(
                source_path=PurePosixPath(self.decode_text(fields[1])),
                source_sha256=fields[2],
                callable_identity=callable_identity,
                hook_owner=self.decode_text(fields[9]),
                hook_kind=PythonHookOwnerKind(fields[10]),
                applicable_shape=PythonHookCallableShape(fields[11]),
            )
        except ValueError as error:
            raise ValueError("configuration hook record is malformed") from error

    def _direction(self, fields: list[str]) -> PythonDependencyDirectionCheck:
        """Decode one exact direction check and optional accepted contract."""
        if len(fields) != 9:
            raise ValueError("configuration direction record is malformed")
        try:
            view = PythonDependencyGraphView(fields[1])
            source = self.decode_text(fields[2])
            target = self.decode_text(fields[3])
            contract_fields = fields[4:]
            contract: PythonAcceptedDependencyContract | None
            if contract_fields == ["-", "-", "-", "-", "-"]:
                contract = None
            elif any(value == "-" for value in contract_fields):
                raise ValueError("partial accepted contract")
            else:
                contract = PythonAcceptedDependencyContract(
                    contract_identity=self.decode_text(fields[4]),
                    view=PythonDependencyGraphView(fields[5]),
                    source_module=self.decode_text(fields[6]),
                    target_module=self.decode_text(fields[7]),
                    direction=PythonDependencyDirection(fields[8]),
                )
            return PythonDependencyDirectionCheck(
                view=view,
                source_module=source,
                target_module=target,
                accepted_contract=contract,
            )
        except ValueError as error:
            raise ValueError("configuration direction record is malformed") from error

    def _encode_module(self, binding: PythonProductionModuleBinding) -> str:
        """Encode one module binding."""
        return "\t".join(
            (
                "module",
                self.encode_text(binding.input_identity),
                self.encode_text(binding.module_name),
                "1" if binding.is_package_facade else "0",
            )
        )

    def _encode_hook(self, hook: PythonModuleHookException) -> str:
        """Encode one complete hook exception."""
        location = hook.callable_identity.location
        return "\t".join(
            (
                "hook",
                self.encode_text(hook.source_path.as_posix()),
                hook.source_sha256,
                self.encode_text(hook.callable_identity.qualified_name),
                hook.callable_identity.kind.value,
                str(location.line),
                str(location.column),
                str(location.end_line),
                str(location.end_column),
                self.encode_text(hook.hook_owner),
                hook.hook_kind.value,
                hook.applicable_shape.value,
            )
        )

    def _encode_direction(self, check: PythonDependencyDirectionCheck) -> str:
        """Encode one complete direction check and optional accepted contract."""
        contract = check.accepted_contract
        contract_fields = (
            ("-", "-", "-", "-", "-")
            if contract is None
            else (
                self.encode_text(contract.contract_identity),
                contract.view.value,
                self.encode_text(contract.source_module),
                self.encode_text(contract.target_module),
                contract.direction.value,
            )
        )
        return "\t".join(
            (
                "direction",
                check.view.value,
                self.encode_text(check.source_module),
                self.encode_text(check.target_module),
                *contract_fields,
            )
        )

    @staticmethod
    def _positive(value: str, name: str) -> int:
        """Decode one canonical positive decimal integer."""
        result = PythonProductionConformanceConfigurationSerializer._nonnegative(
            value, name
        )
        if result < 1:
            raise ValueError(f"{name} must be positive")
        return result

    @staticmethod
    def _nonnegative(value: str, name: str) -> int:
        """Decode one canonical nonnegative decimal integer."""
        if not value.isdecimal() or (len(value) > 1 and value.startswith("0")):
            raise ValueError(f"{name} must be canonical decimal text")
        return int(value)

    @staticmethod
    def encode_text(value: str) -> str:
        """Encode one normalized text field as unpadded URL-safe Base64."""
        if type(value) is not str:
            raise TypeError("encoded value must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(
                "encoded value must be normalized nonempty single-line text"
            )
        return (
            base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii").rstrip("=")
        )

    @staticmethod
    def decode_text(value: str) -> str:
        """Decode one canonical unpadded URL-safe Base64 text field."""
        if type(value) is not str or not value:
            raise ValueError("encoded configuration field must be nonempty")
        padding = "=" * (-len(value) % 4)
        try:
            decoded = base64.b64decode(
                value + padding, altchars=b"-_", validate=True
            ).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise ValueError(
                "configuration field is not canonical Base64 text"
            ) from error
        if (
            PythonProductionConformanceConfigurationSerializer.encode_text(decoded)
            != value
        ):
            raise ValueError("configuration field is not canonical Base64 text")
        return decoded


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonProductionRatchetFindingKey:
    """Identify one deterministic violation independently of source byte identity."""

    rule_identity: str
    subject_path: str
    line: int | None
    column: int | None
    owner_identity: str | None
    detail_identity: str
    message: str

    def __post_init__(self) -> None:
        """Require canonical policy rule and exact stable represented fields."""
        for name, value in (
            ("rule_identity", self.rule_identity),
            ("subject_path", self.subject_path),
            ("detail_identity", self.detail_identity),
            ("message", self.message),
        ):
            self._require_text(value, name)
        if (
            self.rule_identity
            not in PythonProductionConformancePolicy.DETERMINISTIC_RULES
        ):
            raise ValueError("finding rule is not in production policy version 1")
        if (self.line is None) != (self.column is None):
            raise ValueError("finding line and column must be present together")
        if self.line is not None and (type(self.line) is not int or self.line < 1):
            raise ValueError("finding line must be a positive built-in int or None")
        if self.column is not None and (
            type(self.column) is not int or self.column < 0
        ):
            raise ValueError("finding column must be nonnegative built-in int or None")
        if self.owner_identity is not None:
            self._require_text(self.owner_identity, "owner_identity")

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require one intrinsic normalized nonempty single-line text field."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonProductionRatchetFinding:
    """Represent one current deterministic violation with exact source identity."""

    key: PythonProductionRatchetFindingKey
    source_sha256: str | None

    def __post_init__(self) -> None:
        """Require one exact finding key and optional valid source SHA-256."""
        if type(self.key) is not PythonProductionRatchetFindingKey:
            raise TypeError("key must be PythonProductionRatchetFindingKey")
        if self.source_sha256 is not None and (
            type(self.source_sha256) is not str
            or len(self.source_sha256) != 64
            or any(
                character not in "0123456789abcdef" for character in self.source_sha256
            )
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256 or None")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionInheritedBaseline:
    """Represent a content-identified immutable historical finding baseline.

    The record makes inherited findings visible and binds their policy, profile,
    configuration, and historical source identities. It conveys no approval, waiver,
    sunset, or authority to mutate the represented findings.
    """

    content_identity: PythonProductionContentIdentity
    baseline_identity: str
    subject_family: str
    subject_version: str
    policy_identity: str
    policy_version: str
    profile_identity: str
    profile_version: str
    configuration_identity: PythonProductionContentIdentity
    source_identity: PythonProductionContentIdentity
    findings: tuple[PythonProductionRatchetFindingKey, ...]

    def __post_init__(self) -> None:
        """Require exact identities and a sorted unique inherited finding tuple."""
        if type(self.content_identity) is not PythonProductionContentIdentity:
            raise TypeError("content_identity must be PythonProductionContentIdentity")
        self._require_text(self.baseline_identity, "baseline_identity")
        expected = (
            PythonProductionConformanceSubject.SUBJECT_FAMILY,
            PythonProductionConformanceSubject.SUBJECT_VERSION,
            PythonProductionConformancePolicy.POLICY_IDENTITY,
            PythonProductionConformancePolicy.POLICY_VERSION,
            PythonProductionConformanceProfile.PROFILE_IDENTITY,
            PythonProductionConformanceProfile.PROFILE_VERSION,
        )
        actual = (
            self.subject_family,
            self.subject_version,
            self.policy_identity,
            self.policy_version,
            self.profile_identity,
            self.profile_version,
        )
        if actual != expected:
            raise ValueError("baseline subject, policy, or profile identity mismatch")
        if type(self.configuration_identity) is not PythonProductionContentIdentity:
            raise TypeError(
                "configuration_identity must be PythonProductionContentIdentity"
            )
        if type(self.source_identity) is not PythonProductionContentIdentity:
            raise TypeError("source_identity must be PythonProductionContentIdentity")
        if type(self.findings) is not tuple or any(
            type(item) is not PythonProductionRatchetFindingKey
            for item in self.findings
        ):
            raise TypeError("findings must contain ratchet finding keys")
        if self.findings != tuple(sorted(self.findings)):
            raise ValueError("baseline findings must be in canonical order")
        if len(set(self.findings)) != len(self.findings):
            raise ValueError("baseline findings must be unique")

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require one intrinsic normalized nonempty single-line text field."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")


class PythonProductionInheritedBaselineSerializer:
    """Decode and encode the canonical version-one inherited baseline text."""

    __slots__ = ()
    HEADER = "python.production-ratchet-baseline\t1"

    def execute(
        self, payload: bytes, expected_identity: PythonProductionContentIdentity
    ) -> PythonProductionInheritedBaseline:
        """Decode exact baseline bytes and reject malformed or mismatched identity."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        if type(expected_identity) is not PythonProductionContentIdentity:
            raise TypeError("expected_identity must be PythonProductionContentIdentity")
        actual_content = PythonProductionContentIdentity.from_bytes(payload)
        if actual_content != expected_identity:
            raise ValueError("baseline content identity mismatch")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("baseline must be UTF-8") from error
        if not text.endswith("\n"):
            raise ValueError("baseline must end with one newline")
        lines = text[:-1].split("\n")
        if len(lines) < 7 or lines[0] != self.HEADER:
            raise ValueError("baseline header, version, or fields mismatch")
        identity = self._fixed(lines[1], "baseline", 2)
        subject = self._fixed(lines[2], "subject", 3)
        policy = self._fixed(lines[3], "policy", 3)
        profile = self._fixed(lines[4], "profile", 3)
        configuration = self._fixed(lines[5], "configuration", 3)
        source = self._fixed(lines[6], "source", 3)
        findings: list[PythonProductionRatchetFindingKey] = []
        for line in lines[7:]:
            fields = line.split("\t")
            if len(fields) != 8 or fields[0] != "finding":
                raise ValueError("baseline finding record is malformed")
            line_value, column_value = self._position(fields[3], fields[4])
            owner = None if fields[5] == "-" else self._decode(fields[5])
            findings.append(
                PythonProductionRatchetFindingKey(
                    rule_identity=self._decode(fields[1]),
                    subject_path=self._decode(fields[2]),
                    line=line_value,
                    column=column_value,
                    owner_identity=owner,
                    detail_identity=self._decode(fields[6]),
                    message=self._decode(fields[7]),
                )
            )
        baseline = PythonProductionInheritedBaseline(
            content_identity=actual_content,
            baseline_identity=self._decode(identity[0]),
            subject_family=self._decode(subject[0]),
            subject_version=self._decode(subject[1]),
            policy_identity=self._decode(policy[0]),
            policy_version=self._decode(policy[1]),
            profile_identity=self._decode(profile[0]),
            profile_version=self._decode(profile[1]),
            configuration_identity=PythonProductionContentIdentity(
                sha256=configuration[0], byte_count=self._count(configuration[1])
            ),
            source_identity=PythonProductionContentIdentity(
                sha256=source[0], byte_count=self._count(source[1])
            ),
            findings=tuple(findings),
        )
        if self.encode(baseline, include_content_identity=False) != payload:
            raise ValueError("baseline is not in canonical representation")
        return baseline

    def encode(
        self,
        baseline: PythonProductionInheritedBaseline,
        *,
        include_content_identity: bool = True,
    ) -> bytes:
        """Encode one baseline canonically; the content identity is not serialized."""
        if type(baseline) is not PythonProductionInheritedBaseline:
            raise TypeError("baseline must be PythonProductionInheritedBaseline")
        lines = [
            self.HEADER,
            f"baseline\t{self._encode(baseline.baseline_identity)}",
            (
                f"subject\t{self._encode(baseline.subject_family)}\t"
                f"{self._encode(baseline.subject_version)}"
            ),
            (
                f"policy\t{self._encode(baseline.policy_identity)}\t"
                f"{self._encode(baseline.policy_version)}"
            ),
            (
                f"profile\t{self._encode(baseline.profile_identity)}\t"
                f"{self._encode(baseline.profile_version)}"
            ),
            (
                f"configuration\t{baseline.configuration_identity.sha256}\t"
                f"{baseline.configuration_identity.byte_count}"
            ),
            (
                f"source\t{baseline.source_identity.sha256}\t"
                f"{baseline.source_identity.byte_count}"
            ),
        ]
        for finding in baseline.findings:
            owner = (
                "-"
                if finding.owner_identity is None
                else self._encode(finding.owner_identity)
            )
            line = "-" if finding.line is None else str(finding.line)
            column = "-" if finding.column is None else str(finding.column)
            lines.append(
                "\t".join(
                    (
                        "finding",
                        self._encode(finding.rule_identity),
                        self._encode(finding.subject_path),
                        line,
                        column,
                        owner,
                        self._encode(finding.detail_identity),
                        self._encode(finding.message),
                    )
                )
            )
        payload = ("\n".join(lines) + "\n").encode("utf-8")
        if include_content_identity and (
            PythonProductionContentIdentity.from_bytes(payload)
            != baseline.content_identity
        ):
            raise ValueError("baseline fields disagree with content identity")
        return payload

    @staticmethod
    def _fixed(line: str, kind: str, size: int) -> tuple[str, ...]:
        """Return fields from one exact fixed-shape baseline record."""
        fields = line.split("\t")
        if len(fields) != size or fields[0] != kind:
            raise ValueError(f"baseline {kind} record is malformed")
        return tuple(fields[1:])

    @staticmethod
    def _position(line: str, column: str) -> tuple[int | None, int | None]:
        """Decode an absent or exact positive-line/nonnegative-column pair."""
        if line == "-" and column == "-":
            return (None, None)
        if not line.isdecimal() or not column.isdecimal():
            raise ValueError("baseline finding position is malformed")
        return (int(line), int(column))

    @staticmethod
    def _count(value: str) -> int:
        """Decode one canonical nonnegative decimal count."""
        if not value.isdecimal() or (len(value) > 1 and value.startswith("0")):
            raise ValueError("baseline byte count is malformed")
        return int(value)

    @staticmethod
    def _encode(value: str) -> str:
        """Encode one baseline text field canonically."""
        return PythonProductionConformanceConfigurationSerializer.encode_text(value)

    @staticmethod
    def _decode(value: str) -> str:
        """Decode one baseline text field canonically."""
        return PythonProductionConformanceConfigurationSerializer.decode_text(value)


class PythonProductionSourceSetIdentifier:
    """Derive one deterministic content identity from exact supplied source entries."""

    __slots__ = ()

    def execute(
        self, inspection: PythonProductionInspectionResult
    ) -> PythonProductionContentIdentity:
        """Identify outcomes without reading or discovering paths."""
        if type(inspection) is not PythonProductionInspectionResult:
            raise TypeError("inspection must be PythonProductionInspectionResult")
        lines: list[str] = ["python.production-source-set\t1"]
        encode = PythonProductionConformanceConfigurationSerializer.encode_text
        for module in inspection.modules:
            failure = module.failure
            lines.append(
                "\t".join(
                    (
                        "source",
                        encode(module.input_identity),
                        encode(module.path.as_posix()),
                        module.source_sha256 or "-",
                        "-"
                        if module.source_byte_count is None
                        else str(module.source_byte_count),
                        "-" if failure is None else failure.kind.value,
                        "-" if failure is None else encode(failure.message),
                        "-"
                        if failure is None or failure.line is None
                        else str(failure.line),
                        "-"
                        if failure is None or failure.column is None
                        else str(failure.column),
                    )
                )
            )
        return PythonProductionContentIdentity.from_bytes(
            ("\n".join(lines) + "\n").encode("utf-8")
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionRatchetRequest:
    """Represent every explicit immutable input to one production ratchet run."""

    configuration: PythonProductionConformanceConfiguration
    baseline: PythonProductionInheritedBaseline
    sources: tuple[PythonProductionSource, ...]

    def __post_init__(self) -> None:
        """Require exact configuration, baseline, and nonempty source values."""
        if type(self.configuration) is not PythonProductionConformanceConfiguration:
            raise TypeError(
                "configuration must be PythonProductionConformanceConfiguration"
            )
        if type(self.baseline) is not PythonProductionInheritedBaseline:
            raise TypeError("baseline must be PythonProductionInheritedBaseline")
        if (
            type(self.sources) is not tuple
            or not self.sources
            or any(
                type(source) is not PythonProductionSource for source in self.sources
            )
        ):
            raise TypeError("sources must be a nonempty tuple of production sources")
        identities = tuple(source.input_identity for source in self.sources)
        if len(set(identities)) != len(identities):
            raise ValueError("source input identities must be unique")


class PythonProductionRatchetStatus(StrEnum):
    """Represent the bounded deterministic ratchet outcome."""

    PASS = "pass"
    FAIL_NEW_VIOLATIONS = "fail_new_violations"


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionRatchetResult:
    """Represent one complete identified production conformance comparison."""

    subject: PythonProductionConformanceSubject
    policy: PythonProductionConformancePolicy
    profile: PythonProductionConformanceProfile
    configuration_identity: PythonProductionContentIdentity
    source_identity: PythonProductionContentIdentity
    baseline_identity: PythonProductionContentIdentity
    baseline_logical_identity: str
    production_facts: PythonProductionInspectionResult
    callable_rules: tuple[PythonArchitectureFinding, ...]
    dependency_graph: PythonDependencyGraphResult
    current_deterministic_findings: tuple[PythonProductionRatchetFinding, ...]
    baseline_findings: tuple[PythonProductionRatchetFindingKey, ...]
    inherited_present: tuple[PythonProductionRatchetFinding, ...]
    inherited_absent: tuple[PythonProductionRatchetFindingKey, ...]
    new_findings: tuple[PythonProductionRatchetFinding, ...]
    status: PythonProductionRatchetStatus

    def __post_init__(self) -> None:
        """Require canonical partitioning and status agreement without waiver state."""
        if type(self.subject) is not PythonProductionConformanceSubject:
            raise TypeError("subject has the wrong exact type")
        if type(self.policy) is not PythonProductionConformancePolicy:
            raise TypeError("policy has the wrong exact type")
        if type(self.profile) is not PythonProductionConformanceProfile:
            raise TypeError("profile has the wrong exact type")
        for identity in (
            self.configuration_identity,
            self.source_identity,
            self.baseline_identity,
        ):
            if type(identity) is not PythonProductionContentIdentity:
                raise TypeError("content identity has the wrong exact type")
        if type(self.production_facts) is not PythonProductionInspectionResult:
            raise TypeError("production_facts has the wrong exact type")
        if type(self.dependency_graph) is not PythonDependencyGraphResult:
            raise TypeError("dependency_graph has the wrong exact type")
        self._require_text(self.baseline_logical_identity, "baseline_logical_identity")
        if type(self.callable_rules) is not tuple or any(
            type(item) is not PythonArchitectureFinding for item in self.callable_rules
        ):
            raise TypeError("callable_rules must contain architecture findings")
        current_groups = (
            self.current_deterministic_findings,
            self.inherited_present,
            self.new_findings,
        )
        for values in current_groups:
            if type(values) is not tuple or any(
                type(item) is not PythonProductionRatchetFinding for item in values
            ):
                raise TypeError("current finding group contains an invalid value")
            if values != tuple(sorted(values)):
                raise ValueError("current finding group must be in canonical order")
        self._validate_key_group("baseline_findings", self.baseline_findings)
        self._validate_key_group("inherited_absent", self.inherited_absent)
        current_keys = tuple(item.key for item in self.current_deterministic_findings)
        if len(set(current_keys)) != len(current_keys):
            raise ValueError("current deterministic finding identities are ambiguous")
        current_by_key = {
            item.key: item for item in self.current_deterministic_findings
        }
        baseline_keys = frozenset(self.baseline_findings)
        expected_inherited = tuple(
            current_by_key[key]
            for key in sorted(frozenset(current_keys).intersection(baseline_keys))
        )
        expected_new = tuple(
            current_by_key[key]
            for key in sorted(frozenset(current_keys).difference(baseline_keys))
        )
        expected_absent = tuple(
            sorted(baseline_keys.difference(frozenset(current_keys)))
        )
        if self.inherited_present != expected_inherited:
            raise ValueError(
                "inherited_present must equal the exact current/baseline intersection"
            )
        if self.new_findings != expected_new:
            raise ValueError(
                "new_findings must equal the exact current/baseline difference"
            )
        if self.inherited_absent != expected_absent:
            raise ValueError(
                "inherited_absent must equal the exact baseline/current difference"
            )
        if type(self.status) is not PythonProductionRatchetStatus:
            raise TypeError("status must be PythonProductionRatchetStatus")
        expected_status = (
            PythonProductionRatchetStatus.FAIL_NEW_VIOLATIONS
            if self.new_findings
            else PythonProductionRatchetStatus.PASS
        )
        if self.status is not expected_status:
            raise ValueError("status must agree with newly introduced findings")

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require one intrinsic normalized nonempty single-line text field."""
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
    def _validate_key_group(
        name: str, values: tuple[PythonProductionRatchetFindingKey, ...]
    ) -> None:
        """Require one canonically ordered unique finding-key group."""
        if type(values) is not tuple or any(
            type(item) is not PythonProductionRatchetFindingKey for item in values
        ):
            raise TypeError(f"{name} contains an invalid value")
        if values != tuple(sorted(values)):
            raise ValueError(f"{name} must be in canonical order")
        if len(set(values)) != len(values):
            raise ValueError(f"{name} must contain unique finding keys")

    @property
    def passed(self) -> bool:
        """Return whether no newly introduced deterministic violation exists."""
        return self.status is PythonProductionRatchetStatus.PASS


class PythonProductionRatchetWorkflow:
    """Compose all four Phase 2 slices over explicit immutable inputs."""

    __slots__ = ()

    def execute(
        self, request: PythonProductionRatchetRequest
    ) -> PythonProductionRatchetResult:
        """Inspect, evaluate, graph, and compare without discovery or mutation."""
        if type(request) is not PythonProductionRatchetRequest:
            raise TypeError("request must be PythonProductionRatchetRequest")
        configuration = request.configuration
        baseline = request.baseline
        PythonProductionConformanceConfigurationSerializer().encode(configuration)
        PythonProductionInheritedBaselineSerializer().encode(baseline)
        self._require_compatible_baseline(configuration, baseline)
        production = PythonProductionSourceInspector().execute(
            PythonProductionSourceProfile(
                subject_family_identity=configuration.profile.subject_family,
                profile_identity=configuration.profile.production_profile_identity,
                profile_version=configuration.profile.production_profile_version,
            ),
            request.sources,
        )
        source_identity = PythonProductionSourceSetIdentifier().execute(production)
        callable_result = PythonCallablePrivateRuleEvaluator().execute(
            PythonCallablePrivateRuleRequest(
                production_facts=production,
                hook_exceptions=configuration.hook_exceptions,
            )
        )
        graph = PythonDependencyGraphAnalyzer().execute(
            PythonDependencyGraphRequest(
                production_facts=production,
                modules=self._graph_modules(production, configuration.module_bindings),
                direction_checks=configuration.direction_checks,
            )
        )
        current = self._current_findings(production, callable_result.findings, graph)
        baseline_keys = frozenset(baseline.findings)
        inherited_present = tuple(item for item in current if item.key in baseline_keys)
        new_findings = tuple(item for item in current if item.key not in baseline_keys)
        current_keys = frozenset(item.key for item in current)
        inherited_absent = tuple(
            item for item in baseline.findings if item not in current_keys
        )
        status = (
            PythonProductionRatchetStatus.FAIL_NEW_VIOLATIONS
            if new_findings
            else PythonProductionRatchetStatus.PASS
        )
        return PythonProductionRatchetResult(
            subject=configuration.subject,
            policy=configuration.policy,
            profile=configuration.profile,
            configuration_identity=configuration.content_identity,
            source_identity=source_identity,
            baseline_identity=baseline.content_identity,
            baseline_logical_identity=baseline.baseline_identity,
            production_facts=production,
            callable_rules=callable_result.findings,
            dependency_graph=graph,
            current_deterministic_findings=current,
            baseline_findings=baseline.findings,
            inherited_present=inherited_present,
            inherited_absent=inherited_absent,
            new_findings=new_findings,
            status=status,
        )

    def _require_compatible_baseline(
        self,
        configuration: PythonProductionConformanceConfiguration,
        baseline: PythonProductionInheritedBaseline,
    ) -> None:
        """Fail closed when baseline and current contract identities disagree."""
        if (baseline.subject_family, baseline.subject_version) != (
            configuration.subject.subject_family,
            configuration.subject.subject_version,
        ):
            raise ValueError("baseline subject identity mismatch")
        if (baseline.policy_identity, baseline.policy_version) != (
            configuration.policy.policy_identity,
            configuration.policy.policy_version,
        ):
            raise ValueError("baseline policy identity mismatch")
        if (baseline.profile_identity, baseline.profile_version) != (
            configuration.profile.profile_identity,
            configuration.profile.profile_version,
        ):
            raise ValueError("baseline profile identity mismatch")
        if baseline.configuration_identity != configuration.content_identity:
            raise ValueError("baseline configuration identity mismatch")

    def _graph_modules(
        self,
        production: PythonProductionInspectionResult,
        bindings: tuple[PythonProductionModuleBinding, ...],
    ) -> tuple[PythonDependencyModule, ...]:
        """Resolve exact configured module bindings without path or name inference."""
        modules: list[PythonDependencyModule] = []
        for binding in bindings:
            matches = tuple(
                module
                for module in production.modules
                if module.input_identity == binding.input_identity
            )
            if len(matches) != 1:
                raise ValueError(
                    "each configured module binding must match one unambiguous "
                    "source outcome"
                )
            match = matches[0]
            if match.facts is None:
                continue
            source_sha256 = match.source_sha256
            if source_sha256 is None:
                raise AssertionError("successful production result requires SHA-256")
            modules.append(
                PythonDependencyModule(
                    module_name=binding.module_name,
                    is_package_facade=binding.is_package_facade,
                    input_identity=binding.input_identity,
                    source_path=match.path,
                    source_sha256=source_sha256,
                )
            )
        return tuple(modules)

    def _current_findings(
        self,
        production: PythonProductionInspectionResult,
        callable_findings: tuple[PythonArchitectureFinding, ...],
        graph: PythonDependencyGraphResult,
    ) -> tuple[PythonProductionRatchetFinding, ...]:
        """Normalize only policy-declared deterministic violations."""
        findings: list[PythonProductionRatchetFinding] = []
        for module in production.modules:
            failure = module.failure
            if failure is None:
                continue
            location = (
                None
                if failure.line is None or failure.column is None
                else PythonProductionLocation(
                    line=failure.line,
                    column=failure.column,
                    end_line=failure.line,
                    end_column=failure.column,
                )
            )
            findings.append(
                self._finding(
                    rule=PythonProductionConformancePolicy.SOURCE_FAILURE_RULE,
                    path=module.path.as_posix(),
                    location=location,
                    owner=None,
                    detail=failure.kind.value,
                    message=failure.message,
                    source_sha256=module.source_sha256,
                )
            )
        for finding in callable_findings:
            if (
                finding.rule.classification
                is not PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT
            ):
                continue
            findings.append(
                self._finding(
                    rule=finding.rule.rule_identity,
                    path=finding.source_path.as_posix(),
                    location=finding.location,
                    owner=finding.owner_identity,
                    detail=finding.callee_expression
                    or (
                        finding.hook_exception.hook_owner
                        if finding.hook_exception is not None
                        else "callable-owner"
                    ),
                    message=finding.message,
                    source_sha256=finding.source_sha256,
                )
            )
        for result in graph.direction_results:
            if result.status is PythonDependencyDirectionStatus.ALLOWED:
                continue
            findings.append(
                self._finding(
                    rule=PythonProductionConformancePolicy.DEPENDENCY_DIRECTION_RULE,
                    path=(
                        f"dependency/{result.view.value}/"
                        f"{result.source_module}-to-{result.target_module}"
                    ),
                    location=None,
                    owner=result.source_module,
                    detail=result.status.value,
                    message="explicit dependency direction check did not pass",
                    source_sha256=None,
                )
            )
        ordered = tuple(sorted(findings))
        keys = tuple(item.key for item in ordered)
        if len(set(keys)) != len(keys):
            raise ValueError("current deterministic findings have ambiguous duplicates")
        return ordered

    @staticmethod
    def _finding(
        *,
        rule: str,
        path: str,
        location: PythonProductionLocation | None,
        owner: str | None,
        detail: str,
        message: str,
        source_sha256: str | None,
    ) -> PythonProductionRatchetFinding:
        """Construct one exact normalized deterministic finding."""
        return PythonProductionRatchetFinding(
            key=PythonProductionRatchetFindingKey(
                rule_identity=rule,
                subject_path=path,
                line=None if location is None else location.line,
                column=None if location is None else location.column,
                owner_identity=owner,
                detail_identity=detail,
                message=message,
            ),
            source_sha256=source_sha256,
        )


class PythonProductionRatchetReportSerializer:
    """Render a bounded deterministic JSON report from one exact ratchet result."""

    __slots__ = ()
    MAX_FINDINGS = 100
    CLAIM_BOUNDARY = (
        "structural software verification only; inherited findings remain visible ",
        "and are not approvals or waivers; no route classification, repair, runtime ",
        "semantic conclusion, scientific validation, human acceptance, or successor ",
        "authority is established",
    )

    def execute(self, result: PythonProductionRatchetResult, limit: int) -> str:
        """Return canonical one-line JSON with at most ``limit`` findings per group."""
        if type(result) is not PythonProductionRatchetResult:
            raise TypeError("result must be PythonProductionRatchetResult")
        if type(limit) is not int:
            raise TypeError("limit must be a built-in int")
        if limit < 0 or limit > self.MAX_FINDINGS:
            raise ValueError("limit must be between 0 and 100")
        groups = (
            self._group("inherited_present", result.inherited_present, limit),
            self._key_group("inherited_absent", result.inherited_absent, limit),
            self._group("new", result.new_findings, limit),
        )
        claim = "".join(self.CLAIM_BOUNDARY)
        return (
            "{"
            f'"baseline":{self._content(result.baseline_identity)},'
            f'"baseline_logical_identity":{self._string(result.baseline_logical_identity)},'
            f'"claim_boundary":{self._string(claim)},'
            f'"configuration":{self._content(result.configuration_identity)},'
            f'"findings":{{{",".join(groups)}}},'
            f'"policy":{{"identity":{self._string(result.policy.policy_identity)},'
            f'"version":{self._string(result.policy.policy_version)}}},'
            f'"profile":{{"identity":{self._string(result.profile.profile_identity)},'
            f'"version":{self._string(result.profile.profile_version)}}},'
            '"schema_version":1,'
            f'"source":{self._content(result.source_identity)},'
            f'"status":{self._string(result.status.value)},'
            f'"subject":{{"family":{self._string(result.subject.subject_family)},'
            f'"identity":{self._string(result.subject.subject_identity)},'
            f'"version":{self._string(result.subject.subject_version)}}}'
            "}"
        )

    def _group(
        self,
        name: str,
        findings: tuple[PythonProductionRatchetFinding, ...],
        limit: int,
    ) -> str:
        """Render one bounded current-finding group with total and truncation state."""
        values = ",".join(self._finding(item) for item in findings[:limit])
        return (
            f'{self._string(name)}:{{"items":[{values}],"total":{len(findings)},'
            f'"truncated":{self._boolean(len(findings) > limit)}}}'
        )

    def _key_group(
        self,
        name: str,
        findings: tuple[PythonProductionRatchetFindingKey, ...],
        limit: int,
    ) -> str:
        """Render one bounded inherited-absent key group."""
        values = ",".join(self._key(item) for item in findings[:limit])
        return (
            f'{self._string(name)}:{{"items":[{values}],"total":{len(findings)},'
            f'"truncated":{self._boolean(len(findings) > limit)}}}'
        )

    def _finding(self, finding: PythonProductionRatchetFinding) -> str:
        """Render one current finding with exact optional source identity."""
        source = (
            "null"
            if finding.source_sha256 is None
            else self._string(finding.source_sha256)
        )
        return f'{{"key":{self._key(finding.key)},"source_sha256":{source}}}'

    def _key(self, key: PythonProductionRatchetFindingKey) -> str:
        """Render one stable deterministic finding key."""
        line = "null" if key.line is None else str(key.line)
        column = "null" if key.column is None else str(key.column)
        owner = (
            "null" if key.owner_identity is None else self._string(key.owner_identity)
        )
        return (
            "{"
            f'"column":{column},"detail_identity":{self._string(key.detail_identity)},'
            f'"line":{line},"message":{self._string(key.message)},'
            f'"owner_identity":{owner},"rule_identity":{self._string(key.rule_identity)},'
            f'"subject_path":{self._string(key.subject_path)}'
            "}"
        )

    @staticmethod
    def _content(identity: PythonProductionContentIdentity) -> str:
        """Render one content identity as canonical JSON."""
        return f'{{"byte_count":{identity.byte_count},"sha256":"{identity.sha256}"}}'

    @staticmethod
    def _string(value: str) -> str:
        """Render one string with complete deterministic JSON escaping."""
        return PythonJsonStringSerializer().execute(value)

    @staticmethod
    def _boolean(value: bool) -> str:
        """Render one exact Boolean as JSON."""
        return "true" if value else "false"
