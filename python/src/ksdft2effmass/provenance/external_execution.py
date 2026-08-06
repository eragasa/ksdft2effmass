"""Immutable requests and outcomes at an external-execution boundary.

This module owns the request/outcome layer of the external-tool lifecycle.  A
request records separately authorized intent; a result or failure records an
already-observed boundary outcome.  Frozen, slotted DataObjects store only their
constructor fields, and each record directly validates its intrinsic invariants
in ``__post_init__`` without a private or public validation-helper mechanism.

The module does not import declaration, observation, action, or serialization
layers.  Actions and serialization may depend on it, preserving an acyclic
outward dependency direction.  These records contain no commands, credentials,
processes, job-system handles, clients, or workflow state and perform no external
execution or input/output.  Completion is not solver convergence, numerical
acceptance, scientific validation, or uncertainty quantification.  Wrong
semantic Python types raise :class:`TypeError`; correctly typed values that
violate lexical, relational, or ordering invariants raise :class:`ValueError`.

Examples
--------
Construct a request through the supported package API::

    from ksdft2effmass.provenance import ExternalExecutionRequest

    request = ExternalExecutionRequest(
        "request-1", "correlation-1", "attempt-1", None,
        "qe", "execute-pw", "install-1", "authorization-1",
        ("input-1",), ("output",), "prov-1",
    )
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum

# Exact version-1 portable identifier and Windows-drive lexical grammars.
_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:")
# Reserved device stems are prohibited in every diagnostic-path component.
_WINDOWS_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


class ExternalExecutionStatus(StrEnum):
    """Successful-boundary status, distinct from scientific acceptance.

    Attributes
    ----------
    COMPLETED
        The external boundary completed and recorded its artifacts.

    Notes
    -----
    The declaration order and value are versioned wire vocabulary.  Completion
    does not assert solver convergence, output correctness, or scientific
    validity.
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

    Notes
    -----
    Declaration order and values are versioned wire vocabulary.  A stage
    classifies an observation and does not itself perform or retry work.
    """

    REQUEST_ACCEPTANCE = "request_acceptance"
    EXECUTION = "execution"
    RESULT_CAPTURE = "result_capture"


class ExternalFailureCode(StrEnum):
    """Closed version-1 classification for an external-operation failure.

    Attributes
    ----------
    UNAVAILABLE
        The required external boundary was unavailable.
    NOT_AUTHORIZED
        Required authorization was absent or rejected.
    REJECTED
        The boundary rejected the request.
    INTERRUPTED
        Accepted external activity was interrupted.
    MALFORMED_RESULT
        Captured output did not satisfy the boundary result contract.
    INTERNAL_ERROR
        The boundary reported an internal failure.

    Notes
    -----
    Declaration order and values are versioned wire vocabulary.  Codes do not
    classify scientific-model, numerical, or model-reduction error.
    """

    UNAVAILABLE = "unavailable"
    NOT_AUTHORIZED = "not_authorized"
    REJECTED = "rejected"
    INTERRUPTED = "interrupted"
    MALFORMED_RESULT = "malformed_result"
    INTERNAL_ERROR = "internal_error"


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
        Optional prior failed-request identity.  It records lineage only and
        never grants retry authorization; it must differ from ``request_id``.
    tool_id, capability_id, installation_id
        Declared tool, capability, and verified-installation identities.
    authorization_id
        Identity of a separate durable execution authorization.
    input_artifact_ids
        Built-in tuple of sealed input identifiers, unique and lexically sorted.
    expected_output_roles
        Built-in tuple of semantic role identifiers, unique and lexically
        sorted.
    provenance_id
        Provenance identity for request construction.

    Raises
    ------
    TypeError
        If an identifier is not a built-in :class:`str` or either tuple is not
        a built-in :class:`tuple` containing only built-in strings.
    ValueError
        If an identifier is not nonempty NFC portable text, retry lineage is
        self-referential, or a tuple is duplicated or not lexically sorted.

    Notes
    -----
    All state is stored unchanged.  The record contains no command, credential,
    client, or runtime handle and performs no authorization decision, execution,
    retry, artifact access, or input/output.
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
        """Validate request identifiers, retry lineage, and ordered tuples."""
        for value, name in (
            (self.request_id, "request_id"),
            (self.correlation_id, "correlation_id"),
            (self.attempt_id, "attempt_id"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} is not a portable identifier")
        if self.retry_parent_request_id is not None:
            value = self.retry_parent_request_id
            name = "retry_parent_request_id"
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} is not a portable identifier")
            if value == self.request_id:
                raise ValueError("retry_parent_request_id must differ from request_id")
        for value, name in (
            (self.tool_id, "tool_id"),
            (self.capability_id, "capability_id"),
            (self.installation_id, "installation_id"),
            (self.authorization_id, "authorization_id"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} is not a portable identifier")
        for tuple_value, tuple_name in (
            (self.input_artifact_ids, "input_artifact_ids"),
            (self.expected_output_roles, "expected_output_roles"),
        ):
            if type(tuple_value) is not tuple:
                raise TypeError(f"{tuple_name} must be a built-in tuple")
            checked: list[str] = []
            for index, item in enumerate(tuple_value):
                name = f"{tuple_name}[{index}]"
                if type(item) is not str:
                    raise TypeError(f"{name} must be a built-in str")
                if not item:
                    raise ValueError(f"{name} must not be empty")
                if any(0xD800 <= ord(character) <= 0xDFFF for character in item):
                    raise ValueError(f"{name} must not contain Unicode surrogates")
                if unicodedata.normalize("NFC", item) != item:
                    raise ValueError(f"{name} must be Unicode NFC")
                if _ID_PATTERN.fullmatch(item) is None:
                    raise ValueError(f"{name} is not a portable identifier")
                checked.append(item)
            checked_tuple = tuple(checked)
            if checked_tuple != tuple(sorted(checked_tuple)) or len(
                set(checked_tuple)
            ) != len(checked_tuple):
                raise ValueError(f"{tuple_name} must be unique and lexically sorted")
            object.__setattr__(self, tuple_name, checked_tuple)
        if type(self.provenance_id) is not str:
            raise TypeError("provenance_id must be a built-in str")
        if not self.provenance_id:
            raise ValueError("provenance_id must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.provenance_id):
            raise ValueError("provenance_id must not contain Unicode surrogates")
        if unicodedata.normalize("NFC", self.provenance_id) != self.provenance_id:
            raise ValueError("provenance_id must be Unicode NFC")
        if _ID_PATTERN.fullmatch(self.provenance_id) is None:
            raise ValueError("provenance_id is not a portable identifier")


@dataclass(frozen=True, slots=True)
class ExternalExecutionResult:
    """Immutable successful outcome correlated with an external request.

    Parameters
    ----------
    result_id, request_id, correlation_id, attempt_id
        Stable outcome, request, correlation, and attempt identities.
    status
        Exact :class:`ExternalExecutionStatus`; ``COMPLETED`` describes only the
        external boundary.
    output_artifact_ids
        Built-in tuple of sealed output identifiers, unique and lexically sorted.
    manifest_id, provenance_id
        Manifest and provenance identities supporting the outcome.

    Raises
    ------
    TypeError
        If identifier state has the wrong Python type, ``status`` is not an
        :class:`ExternalExecutionStatus`, or outputs are not a built-in tuple of
        built-in strings.
    ValueError
        If identifier text violates the nonempty NFC portable grammar or the
        output tuple is duplicated or not lexically sorted.

    Notes
    -----
    Constructor state is retained unchanged.  Completion is not solver
    convergence, numerical acceptance, scientific validation, or uncertainty
    quantification, and construction performs no execution or artifact access.
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
        """Validate outcome identifiers, exact status, and ordered outputs."""
        for value, name in (
            (self.result_id, "result_id"),
            (self.request_id, "request_id"),
            (self.correlation_id, "correlation_id"),
            (self.attempt_id, "attempt_id"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} is not a portable identifier")
        if not isinstance(self.status, ExternalExecutionStatus):
            raise TypeError("status must be an ExternalExecutionStatus")
        if type(self.output_artifact_ids) is not tuple:
            raise TypeError("output_artifact_ids must be a built-in tuple")
        checked: list[str] = []
        for index, item in enumerate(self.output_artifact_ids):
            name = f"output_artifact_ids[{index}]"
            if type(item) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not item:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in item):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", item) != item:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(item) is None:
                raise ValueError(f"{name} is not a portable identifier")
            checked.append(item)
        output_artifact_ids = tuple(checked)
        if output_artifact_ids != tuple(sorted(output_artifact_ids)) or len(
            set(output_artifact_ids)
        ) != len(output_artifact_ids):
            raise ValueError("output_artifact_ids must be unique and lexically sorted")
        object.__setattr__(self, "output_artifact_ids", output_artifact_ids)
        for value, name in (
            (self.manifest_id, "manifest_id"),
            (self.provenance_id, "provenance_id"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} is not a portable identifier")


@dataclass(frozen=True, slots=True)
class ExternalExecutionFailure:
    """Immutable structured failure correlated with an external request.

    Parameters
    ----------
    failure_id, request_id, correlation_id, attempt_id
        Stable failure, request, correlation, and attempt identities.
    stage
        Exact :class:`ExternalFailureStage` at which failure was observed.
    code
        Exact version-1 :class:`ExternalFailureCode`.
    diagnostic_paths
        Built-in tuple of unique, lexically sorted root-relative Unicode-NFC
        POSIX lexical paths.  Absolute paths, drive syntax, backslashes, empty,
        ``.`` and ``..`` components, trailing or repeated separators, Windows
        device names, and prohibited control characters are rejected.
    provenance_id
        Provenance identity supporting the failure observation.

    Raises
    ------
    TypeError
        If identifier or path state has the wrong semantic Python type, either
        enum has the wrong type, or ``diagnostic_paths`` is not a built-in tuple.
    ValueError
        If text violates its lexical grammar or paths are duplicated or unsorted.

    Notes
    -----
    The record stores a failure already observed elsewhere.  It does not expose
    diagnostics, retry work, execute a request, or classify scientific errors.
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
        """Validate failure identifiers, enums, and diagnostic path grammar."""
        for value, name in (
            (self.failure_id, "failure_id"),
            (self.request_id, "request_id"),
            (self.correlation_id, "correlation_id"),
            (self.attempt_id, "attempt_id"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} is not a portable identifier")
        if not isinstance(self.stage, ExternalFailureStage):
            raise TypeError("stage must be an ExternalFailureStage")
        if not isinstance(self.code, ExternalFailureCode):
            raise TypeError("code must be an ExternalFailureCode")
        if type(self.diagnostic_paths) is not tuple:
            raise TypeError("diagnostic_paths must be a built-in tuple")
        checked: list[str] = []
        for index, path in enumerate(self.diagnostic_paths):
            name = f"diagnostic_paths[{index}]"
            if type(path) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not path:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in path):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", path) != path:
                raise ValueError(f"{name} must be Unicode NFC")
            if path.startswith("/") or _DRIVE_PATTERN.match(path):
                raise ValueError(
                    f"{name} must not use absolute or Windows drive syntax"
                )
            if "\\" in path or path.endswith("/") or "//" in path:
                raise ValueError(f"{name} must be a root-relative POSIX lexical path")
            parts = path.split("/")
            if any(part in {"", ".", ".."} for part in parts):
                raise ValueError(f"{name} contains an invalid path component")
            if any(
                part.split(".", 1)[0].upper() in _WINDOWS_DEVICE_NAMES for part in parts
            ):
                raise ValueError(f"{name} contains a Windows device name")
            if any(
                ord(character) < 0x20
                or 0x7F <= ord(character) <= 0x9F
                or ord(character) in {0x2028, 0x2029}
                for character in path
            ):
                raise ValueError(f"{name} contains a prohibited control character")
            checked.append(path)
        diagnostic_paths = tuple(checked)
        if diagnostic_paths != tuple(sorted(diagnostic_paths)) or len(
            set(diagnostic_paths)
        ) != len(diagnostic_paths):
            raise ValueError("diagnostic_paths must be unique and lexically sorted")
        object.__setattr__(self, "diagnostic_paths", diagnostic_paths)
        if type(self.provenance_id) is not str:
            raise TypeError("provenance_id must be a built-in str")
        if not self.provenance_id:
            raise ValueError("provenance_id must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.provenance_id):
            raise ValueError("provenance_id must not contain Unicode surrogates")
        if unicodedata.normalize("NFC", self.provenance_id) != self.provenance_id:
            raise ValueError("provenance_id must be Unicode NFC")
        if _ID_PATTERN.fullmatch(self.provenance_id) is None:
            raise ValueError("provenance_id is not a portable identifier")


ExternalExecutionOutcome = ExternalExecutionResult | ExternalExecutionFailure
"""Type alias for the two immutable external-operation outcome forms.

The alias adds no runtime wrapper or stored state.  It supports action typing and
makes no claim that an outcome is successful, correlated, or scientifically
accepted.
"""
