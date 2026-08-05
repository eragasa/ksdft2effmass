"""Immutable external-tool lifecycle, request, result, and failure records.

These records form a narrow durable boundary around external activity.  They do
not locate, import, probe, or execute tools and contain no runtime handles,
clients, credentials, or backend-specific scientific semantics.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum

_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_VERSION_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,63}\Z")
_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:")
_WINDOWS_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


def _require_text(value: object, name: str) -> str:
    """Validate narrow owner-local nonempty NFC text."""
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if not value:
        raise ValueError(f"{name} must not be empty")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ValueError(f"{name} must not contain Unicode surrogates")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"{name} must be Unicode NFC")
    return value


def _require_identifier(value: object, name: str) -> str:
    """Validate a bounded portable identifier owned by tool records."""
    text = _require_text(value, name)
    if _ID_PATTERN.fullmatch(text) is None:
        raise ValueError(f"{name} is not a portable identifier")
    return text


def _require_version(value: object, name: str) -> str:
    """Validate narrow portable version text without interpreting precedence."""
    text = _require_text(value, name)
    if _VERSION_PATTERN.fullmatch(text) is None:
        raise ValueError(f"{name} is not portable lexical version text")
    return text


def _require_sha256(value: object, name: str) -> str:
    """Validate a lowercase SHA-256 digest owned by an installation record."""
    text = _require_text(value, name)
    if _SHA256_PATTERN.fullmatch(text) is None:
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")
    return text


def _require_identifier_tuple(value: object, name: str) -> tuple[str, ...]:
    """Require a unique lexically sorted built-in tuple of identifiers."""
    if type(value) is not tuple:
        raise TypeError(f"{name} must be a built-in tuple")
    checked = tuple(
        _require_identifier(item, f"{name}[{index}]")
        for index, item in enumerate(value)
    )
    if checked != tuple(sorted(checked)) or len(set(checked)) != len(checked):
        raise ValueError(f"{name} must be unique and lexically sorted")
    return checked


def _require_root_relative_path(value: object, name: str) -> str:
    """Validate an owner-local NFC root-relative POSIX lexical path."""
    text = _require_text(value, name)
    if text.startswith("/") or _DRIVE_PATTERN.match(text):
        raise ValueError(f"{name} must not use absolute or Windows drive syntax")
    if "\\" in text or text.endswith("/") or "//" in text:
        raise ValueError(f"{name} must be a root-relative POSIX lexical path")
    parts = text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"{name} contains an invalid path component")
    if any(part.split(".", 1)[0].upper() in _WINDOWS_DEVICE_NAMES for part in parts):
        raise ValueError(f"{name} contains a Windows device name")
    if any(
        ord(character) < 0x20
        or 0x7F <= ord(character) <= 0x9F
        or ord(character) in {0x2028, 0x2029}
        for character in text
    ):
        raise ValueError(f"{name} contains a prohibited control character")
    return text


class CapabilityKind(StrEnum):
    """Closed version-1 categories of externally provided behavior.

    Attributes
    ----------
    EXECUTE, PARSE, RENDER, TRANSFER
        Execution, parsing, rendering, or artifact-transfer capability.
    """

    EXECUTE = "execute"
    PARSE = "parse"
    RENDER = "render"
    TRANSFER = "transfer"


class VerificationStatus(StrEnum):
    """Outcome of an observed tool-capability verification.

    Attributes
    ----------
    VERIFIED
        The declared capability was observed successfully.
    REJECTED
        Verification ran and rejected the capability.
    UNAVAILABLE
        Verification could not observe the capability.
    """

    VERIFIED = "verified"
    REJECTED = "rejected"
    UNAVAILABLE = "unavailable"


class ExternalExecutionStatus(StrEnum):
    """Successful-boundary status, distinct from scientific acceptance.

    Attributes
    ----------
    COMPLETED
        The external boundary completed and recorded its artifacts.
    """

    COMPLETED = "completed"


class ExternalFailureStage(StrEnum):
    """Closed lifecycle stage at which an external failure was observed.

    Attributes
    ----------
    REQUEST_ACCEPTANCE
        The boundary did not accept the immutable request.
    EXECUTION
        Failure occurred after request acceptance during external activity.
    RESULT_CAPTURE
        External activity ended but its result could not be captured.
    """

    REQUEST_ACCEPTANCE = "request_acceptance"
    EXECUTION = "execution"
    RESULT_CAPTURE = "result_capture"


class ExternalFailureCode(StrEnum):
    """Closed version-1 classification for an external-operation failure.

    Attributes
    ----------
    UNAVAILABLE, NOT_AUTHORIZED, REJECTED
        Availability, authorization, or boundary-rejection failures.
    INTERRUPTED, MALFORMED_RESULT, INTERNAL_ERROR
        Interrupted activity, malformed output, or internal boundary failure.
    """

    UNAVAILABLE = "unavailable"
    NOT_AUTHORIZED = "not_authorized"
    REJECTED = "rejected"
    INTERRUPTED = "interrupted"
    MALFORMED_RESULT = "malformed_result"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True, slots=True)
class ExternalToolIdentity:
    """Stable identity of an external tool family.

    Parameters
    ----------
    tool_id
        Stable project identity for the tool.
    implementation_family
        Portable implementation-family identifier.  This is not a dynamic
        import name or plugin registration key.
    """

    tool_id: str
    implementation_family: str

    def __post_init__(self) -> None:
        _require_identifier(self.tool_id, "tool_id")
        _require_identifier(self.implementation_family, "implementation_family")


@dataclass(frozen=True, slots=True)
class ExternalToolSpecification:
    """Immutable requested external-tool installation specification.

    Parameters
    ----------
    specification_id
        Stable identity of this declaration.
    tool_id
        Identity of the external-tool family.
    requested_version
        Exact project-declared version expression treated as opaque text.
    executable_or_package_id
        Declared executable or package identifier, never a runtime handle.
    """

    specification_id: str
    tool_id: str
    requested_version: str
    executable_or_package_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.specification_id, "specification_id")
        _require_identifier(self.tool_id, "tool_id")
        _require_version(self.requested_version, "requested_version")
        _require_identifier(self.executable_or_package_id, "executable_or_package_id")


@dataclass(frozen=True, slots=True)
class DeclaredCapability:
    """One immutable capability requested from an external tool.

    Parameters
    ----------
    capability_id
        Stable identity of the declaration.
    tool_id
        Declared provider tool identity.
    kind
        Version-1 capability category.
    name
        Narrow capability name within the category.
    specification_version
        Version of the capability's project-owned contract.
    """

    capability_id: str
    tool_id: str
    kind: CapabilityKind
    name: str
    specification_version: str

    def __post_init__(self) -> None:
        _require_identifier(self.capability_id, "capability_id")
        _require_identifier(self.tool_id, "tool_id")
        if not isinstance(self.kind, CapabilityKind):
            raise TypeError("kind must be a CapabilityKind")
        _require_identifier(self.name, "name")
        _require_identifier(self.specification_version, "specification_version")


@dataclass(frozen=True, slots=True)
class InstallationObservation:
    """Observed installation metadata without discovery or verification policy.

    Parameters
    ----------
    installation_id
        Stable identity of this observation.
    specification_id, tool_id
        Requested installation and tool identities.
    observed_version
        Version text reported by the observation boundary.
    executable_or_package_id
        Observed executable or package identifier.
    executable_sha256
        Optional exact executable/package digest when available.
    environment_record_id
        Identity of separately sanitized environment provenance.
    provenance_id
        Provenance record supporting the observation.
    """

    installation_id: str
    specification_id: str
    tool_id: str
    observed_version: str
    executable_or_package_id: str
    executable_sha256: str | None
    environment_record_id: str
    provenance_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.installation_id, "installation_id")
        _require_identifier(self.specification_id, "specification_id")
        _require_identifier(self.tool_id, "tool_id")
        _require_version(self.observed_version, "observed_version")
        _require_identifier(self.executable_or_package_id, "executable_or_package_id")
        if self.executable_sha256 is not None:
            _require_sha256(self.executable_sha256, "executable_sha256")
        _require_identifier(self.environment_record_id, "environment_record_id")
        _require_identifier(self.provenance_id, "provenance_id")


@dataclass(frozen=True, slots=True)
class VerificationObservation:
    """Observed result of verifying one declared capability.

    Parameters
    ----------
    verification_id
        Stable identity of the verification observation.
    installation_id, capability_id
        Correlated installation and capability identities.
    status
        Exact verification outcome.
    evidence_artifact_ids
        Ordered, duplicate-free evidence artifact identities.
    provenance_id
        Provenance record supporting this observation.

    Notes
    -----
    ``VERIFIED`` is software-capability evidence only.  It is not numerical
    acceptance, scientific validation, or uncertainty quantification.
    """

    verification_id: str
    installation_id: str
    capability_id: str
    status: VerificationStatus
    evidence_artifact_ids: tuple[str, ...]
    provenance_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.verification_id, "verification_id")
        _require_identifier(self.installation_id, "installation_id")
        _require_identifier(self.capability_id, "capability_id")
        if not isinstance(self.status, VerificationStatus):
            raise TypeError("status must be a VerificationStatus")
        object.__setattr__(
            self,
            "evidence_artifact_ids",
            _require_identifier_tuple(
                self.evidence_artifact_ids, "evidence_artifact_ids"
            ),
        )
        _require_identifier(self.provenance_id, "provenance_id")


@dataclass(frozen=True, slots=True)
class ExternalExecutionRequest:
    """Authorized immutable request presented to an external boundary.

    Parameters
    ----------
    request_id
        Stable request identity.
    correlation_id, attempt_id
        Correlation and attempt identities copied unchanged into outcomes.
    retry_parent_request_id
        Optional identity of a prior failed request.  It carries lineage only
        and never grants retry authorization.
    tool_id, capability_id, installation_id
        Declared tool, capability, and verified installation identities.
    authorization_id
        Identity of the separate durable execution authorization.
    input_artifact_ids
        Ordered, duplicate-free sealed input artifact identities.
    expected_output_roles
        Ordered, duplicate-free semantic role identifiers.
    provenance_id
        Provenance identity for request construction.

    Notes
    -----
    The record contains no command, credential, client, or runtime handle and
    performs no execution.
    """

    request_id: str
    correlation_id: str
    attempt_id: str
    retry_parent_request_id: str | None
    tool_id: str
    capability_id: str
    installation_id: str
    authorization_id: str
    input_artifact_ids: tuple[str, ...]
    expected_output_roles: tuple[str, ...]
    provenance_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.request_id, "request_id")
        _require_identifier(self.correlation_id, "correlation_id")
        _require_identifier(self.attempt_id, "attempt_id")
        if self.retry_parent_request_id is not None:
            _require_identifier(self.retry_parent_request_id, "retry_parent_request_id")
            if self.retry_parent_request_id == self.request_id:
                raise ValueError("retry_parent_request_id must differ from request_id")
        _require_identifier(self.tool_id, "tool_id")
        _require_identifier(self.capability_id, "capability_id")
        _require_identifier(self.installation_id, "installation_id")
        _require_identifier(self.authorization_id, "authorization_id")
        object.__setattr__(
            self,
            "input_artifact_ids",
            _require_identifier_tuple(self.input_artifact_ids, "input_artifact_ids"),
        )
        object.__setattr__(
            self,
            "expected_output_roles",
            _require_identifier_tuple(
                self.expected_output_roles, "expected_output_roles"
            ),
        )
        _require_identifier(self.provenance_id, "provenance_id")


@dataclass(frozen=True, slots=True)
class ExternalExecutionResult:
    """Immutable successful outcome correlated with an external request.

    Parameters
    ----------
    result_id, request_id, correlation_id, attempt_id
        Stable outcome, request, correlation, and attempt identities.
    status
        ``COMPLETED`` means the external boundary completed; it is not solver
        convergence, numerical acceptance, or scientific validation.
    output_artifact_ids
        Ordered, duplicate-free sealed output artifact identities.
    manifest_id, provenance_id
        Manifest and provenance identities supporting the outcome.
    """

    result_id: str
    request_id: str
    correlation_id: str
    attempt_id: str
    status: ExternalExecutionStatus
    output_artifact_ids: tuple[str, ...]
    manifest_id: str
    provenance_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.result_id, "result_id")
        _require_identifier(self.request_id, "request_id")
        _require_identifier(self.correlation_id, "correlation_id")
        _require_identifier(self.attempt_id, "attempt_id")
        if not isinstance(self.status, ExternalExecutionStatus):
            raise TypeError("status must be an ExternalExecutionStatus")
        object.__setattr__(
            self,
            "output_artifact_ids",
            _require_identifier_tuple(self.output_artifact_ids, "output_artifact_ids"),
        )
        _require_identifier(self.manifest_id, "manifest_id")
        _require_identifier(self.provenance_id, "provenance_id")


@dataclass(frozen=True, slots=True)
class ExternalExecutionFailure:
    """Immutable structured failure correlated with an external request.

    Parameters
    ----------
    failure_id, request_id, correlation_id, attempt_id
        Stable failure, request, correlation, and attempt identities.
    stage
        Exact lifecycle stage at which the failure was observed.
    code
        Exact version-1 failure class.
    diagnostic_paths
        Ordered, duplicate-free root-relative NFC POSIX lexical paths.
    provenance_id
        Provenance identity supporting the failure observation.
    """

    failure_id: str
    request_id: str
    correlation_id: str
    attempt_id: str
    stage: ExternalFailureStage
    code: ExternalFailureCode
    diagnostic_paths: tuple[str, ...]
    provenance_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.failure_id, "failure_id")
        _require_identifier(self.request_id, "request_id")
        _require_identifier(self.correlation_id, "correlation_id")
        _require_identifier(self.attempt_id, "attempt_id")
        if not isinstance(self.stage, ExternalFailureStage):
            raise TypeError("stage must be an ExternalFailureStage")
        if not isinstance(self.code, ExternalFailureCode):
            raise TypeError("code must be an ExternalFailureCode")
        if type(self.diagnostic_paths) is not tuple:
            raise TypeError("diagnostic_paths must be a built-in tuple")
        paths = tuple(self.diagnostic_paths)
        checked = tuple(
            _require_root_relative_path(path, f"diagnostic_paths[{index}]")
            for index, path in enumerate(paths)
        )
        if checked != tuple(sorted(checked)) or len(set(checked)) != len(checked):
            raise ValueError("diagnostic_paths must be unique and lexically sorted")
        object.__setattr__(self, "diagnostic_paths", checked)
        _require_identifier(self.provenance_id, "provenance_id")


ExternalExecutionOutcome = ExternalExecutionResult | ExternalExecutionFailure
"""Type alias for the two immutable external-operation outcome forms."""
