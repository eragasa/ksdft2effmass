"""Immutable observations of external-tool installations and capabilities.

This module owns the observation layer that follows external-tool declarations
and precedes immutable external-execution records.  Its frozen, slotted
DataObjects store already-observed metadata; each record validates every
intrinsic field directly in ``__post_init__`` without shared validation helpers,
hidden mutation, or derived persistent state.

The module is dependency-minimal and does not import actions, serialization, or
execution records.  Later action and serialization layers may import these
records.  Observation records do not discover installations, hash executables,
probe capabilities, read evidence, or execute tools.  They also do not establish
solver convergence, numerical acceptance, scientific validation, or uncertainty
quantification.  Wrong semantic Python types raise :class:`TypeError`; values of
the right type that violate lexical or ordering invariants raise
:class:`ValueError`.  Construction performs no input/output.

Examples
--------
Represent already-observed metadata through the supported package API::

    from ksdft2effmass.provenance import InstallationObservation

    observation = InstallationObservation(
        "install-1", "spec-1", "qe", "7.4", "pw.x", None, "env-1", "prov-1"
    )
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum

# Exact version-1 identifier, digest, and opaque-version lexical grammars.
_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_VERSION_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,63}\Z")


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

    Notes
    -----
    Declaration order and values are versioned wire vocabulary.  ``VERIFIED``
    is software-capability evidence only, not scientific or numerical
    acceptance and not uncertainty quantification.
    """

    VERIFIED = "verified"
    REJECTED = "rejected"
    UNAVAILABLE = "unavailable"


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
        Opaque version text matching
        ``[0-9A-Za-z][0-9A-Za-z._+-]{0,63}``.
    executable_or_package_id
        Observed executable or package identifier, not a runtime handle.
    executable_sha256
        Optional exact lowercase 64-hex-character SHA-256 digest.
    environment_record_id
        Identity of separately sanitized environment provenance.
    provenance_id
        Identity of provenance supporting the observation.

    Raises
    ------
    TypeError
        If any present textual field is not a built-in :class:`str`.
    ValueError
        If text is empty, contains Unicode surrogates, is not NFC, or violates
        its portable identifier, version, or digest grammar.

    Notes
    -----
    Every field is stored unchanged.  The record does not acquire the
    observation, verify digest bytes, resolve an environment, or prove that the
    installation can execute a capability.
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
        """Validate the installation observation's directly owned fields."""
        for value, name, pattern, grammar_message in (
            (
                self.installation_id,
                "installation_id",
                _ID_PATTERN,
                "is not a portable identifier",
            ),
            (
                self.specification_id,
                "specification_id",
                _ID_PATTERN,
                "is not a portable identifier",
            ),
            (self.tool_id, "tool_id", _ID_PATTERN, "is not a portable identifier"),
            (
                self.observed_version,
                "observed_version",
                _VERSION_PATTERN,
                "is not portable lexical version text",
            ),
            (
                self.executable_or_package_id,
                "executable_or_package_id",
                _ID_PATTERN,
                "is not a portable identifier",
            ),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if pattern.fullmatch(value) is None:
                raise ValueError(f"{name} {grammar_message}")
        if self.executable_sha256 is not None:
            if type(self.executable_sha256) is not str:
                raise TypeError("executable_sha256 must be a built-in str")
            if not self.executable_sha256:
                raise ValueError("executable_sha256 must not be empty")
            if any(
                0xD800 <= ord(character) <= 0xDFFF
                for character in self.executable_sha256
            ):
                raise ValueError(
                    "executable_sha256 must not contain Unicode surrogates"
                )
            if (
                unicodedata.normalize("NFC", self.executable_sha256)
                != self.executable_sha256
            ):
                raise ValueError("executable_sha256 must be Unicode NFC")
            if _SHA256_PATTERN.fullmatch(self.executable_sha256) is None:
                raise ValueError("executable_sha256 must be a lowercase SHA-256 digest")
        for value, name in (
            (self.environment_record_id, "environment_record_id"),
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
class VerificationObservation:
    """Observed result of verifying one declared capability.

    Parameters
    ----------
    verification_id
        Stable identity of the verification observation.
    installation_id, capability_id
        Correlated installation and capability identities.
    status
        Exact :class:`VerificationStatus` outcome.
    evidence_artifact_ids
        Built-in tuple of portable artifact identifiers, unique and sorted in
        ascending lexical order.  The empty tuple is permitted.
    provenance_id
        Provenance identity supporting this observation.

    Raises
    ------
    TypeError
        If an identifier is not a built-in :class:`str`, ``status`` is not a
        :class:`VerificationStatus`, ``evidence_artifact_ids`` is not a built-in
        :class:`tuple`, or a tuple member is not a built-in string.
    ValueError
        If identifier text violates the nonempty NFC portable grammar or the
        evidence tuple is duplicated or not lexically sorted.

    Notes
    -----
    All constructor state is retained unchanged; no evidence is opened or
    interpreted.  ``VERIFIED`` is software-capability evidence only and is not
    numerical acceptance, scientific validation, or uncertainty quantification.
    """

    verification_id: str
    installation_id: str
    capability_id: str
    status: VerificationStatus
    evidence_artifact_ids: tuple[str, ...]
    provenance_id: str

    def __post_init__(self) -> None:
        """Validate identifiers, status, and canonical evidence ordering."""
        for value, name in (
            (self.verification_id, "verification_id"),
            (self.installation_id, "installation_id"),
            (self.capability_id, "capability_id"),
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
        if not isinstance(self.status, VerificationStatus):
            raise TypeError("status must be a VerificationStatus")
        if type(self.evidence_artifact_ids) is not tuple:
            raise TypeError("evidence_artifact_ids must be a built-in tuple")
        checked: list[str] = []
        for index, item in enumerate(self.evidence_artifact_ids):
            name = f"evidence_artifact_ids[{index}]"
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
        evidence_artifact_ids = tuple(checked)
        if evidence_artifact_ids != tuple(sorted(evidence_artifact_ids)) or len(
            set(evidence_artifact_ids)
        ) != len(evidence_artifact_ids):
            raise ValueError(
                "evidence_artifact_ids must be unique and lexically sorted"
            )
        object.__setattr__(self, "evidence_artifact_ids", evidence_artifact_ids)
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
