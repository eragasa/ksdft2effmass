"""Immutable artifact, manifest, provenance, and lineage records.

The records in this module describe durable identities and relationships.  They
perform no storage discovery or input/output.  In particular,
:class:`ArtifactReference` identifies sealed content while
:class:`ArtifactLocation` separately describes a deployment location.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

_MAX_U64 = 18_446_744_073_709_551_615
_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:")
_WINDOWS_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}
_TIMESTAMP_PATTERN = re.compile(
    r"[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"
    r"T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z\Z"
)


def _require_text(value: object, name: str) -> str:
    """Return a nonempty, scalar-Unicode string owned by a record field."""
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if not value:
        raise ValueError(f"{name} must not be empty")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ValueError(f"{name} must not contain Unicode surrogate code points")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"{name} must be Unicode NFC")
    return value


def _require_identifier(value: object, name: str) -> str:
    """Validate a bounded portable identifier without interpreting its prefix."""
    text = _require_text(value, name)
    if _ID_PATTERN.fullmatch(text) is None:
        raise ValueError(f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}")
    return text


def _require_sha256(value: object, name: str) -> str:
    """Validate the lowercase hexadecimal representation of a SHA-256 digest."""
    text = _require_text(value, name)
    if _SHA256_PATTERN.fullmatch(text) is None:
        raise ValueError(f"{name} must be a 64-character lowercase SHA-256 digest")
    return text


def _require_root_relative_path(value: object, name: str) -> str:
    """Validate an NFC, root-relative, POSIX lexical path.

    The path is lexical only: this function never queries a filesystem or
    resolves symbolic links.
    """
    text = _require_text(value, name)
    if text.startswith("/") or _DRIVE_PATTERN.match(text):
        raise ValueError(f"{name} must not use absolute or Windows drive syntax")
    if "\\" in text or text.endswith("/") or "//" in text:
        raise ValueError(f"{name} must be a root-relative POSIX lexical path")
    parts = text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"{name} must not contain empty, '.' or '..' components")
    for part in parts:
        if part.split(".", 1)[0].upper() in _WINDOWS_DEVICE_NAMES:
            raise ValueError(f"{name} must not contain a Windows device name")
    if any(
        ord(character) < 0x20
        or 0x7F <= ord(character) <= 0x9F
        or ord(character) in {0x2028, 0x2029}
        for character in text
    ):
        raise ValueError(f"{name} must not contain C0/C1 or line controls")
    return text


def _require_identifier_tuple(value: object, name: str) -> tuple[str, ...]:
    """Require an immutable, unique tuple in deterministic lexical order."""
    if type(value) is not tuple:
        raise TypeError(f"{name} must be a built-in tuple")
    checked = tuple(
        _require_identifier(item, f"{name}[{index}]")
        for index, item in enumerate(value)
    )
    if checked != tuple(sorted(checked)) or len(set(checked)) != len(checked):
        raise ValueError(f"{name} must be unique and lexically sorted")
    return checked


class ArtifactLocationKind(StrEnum):
    """Closed set of deployment-location representations.

    Attributes
    ----------
    ROOT_RELATIVE
        A location named by an explicit ``root_id`` and lexical ``path``.
    EXTERNAL_DESCRIPTOR
        A location named only by an approved opaque descriptor identifier.
    """

    ROOT_RELATIVE = "root_relative"
    EXTERNAL_DESCRIPTOR = "external_descriptor"


class ManifestState(StrEnum):
    """Recorded lifecycle state of a run manifest.

    Attributes
    ----------
    DECLARED
        The attempt is declared and has no finish timestamp.
    COMPLETE
        External execution completed; no scientific acceptance is implied.
    FAILED
        The observed attempt terminated unsuccessfully.
    """

    DECLARED = "declared"
    COMPLETE = "complete"
    FAILED = "failed"


class LineageKind(StrEnum):
    """Closed vocabulary for a directed parent-to-child relationship.

    Attributes
    ----------
    DERIVED
        The child was derived from the parent.
    REPRESENTATION
        The child is a distinct representation of parent content.
    RETRY
        The child is a new attempt descended from a failed parent attempt.
    """

    DERIVED = "derived"
    REPRESENTATION = "representation"
    RETRY = "retry"


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """Stable identifier and exact byte identity of one sealed artifact.

    Parameters
    ----------
    artifact_id
        Opaque stable project identifier.
    sha256
        SHA-256 digest as exactly 64 lowercase hexadecimal characters.
    byte_size
        Exact size in bytes in the unsigned 64-bit range.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.  Booleans are not integers.
    ValueError
        If an identifier, digest, or size violates its stated invariant.
    """

    artifact_id: str
    sha256: str
    byte_size: int

    def __post_init__(self) -> None:
        _require_identifier(self.artifact_id, "artifact_id")
        _require_sha256(self.sha256, "sha256")
        if type(self.byte_size) is not int:
            raise TypeError("byte_size must be a built-in int excluding bool")
        if not 0 <= self.byte_size <= _MAX_U64:
            raise ValueError("byte_size must be in the unsigned 64-bit range")


@dataclass(frozen=True, slots=True)
class ArtifactSpecification:
    """Portable declared role and representation of an artifact.

    Parameters
    ----------
    logical_path
        NFC root-relative POSIX lexical path within a run or campaign.
    format
        Portable format identifier, such as ``json`` or ``qe-save-tree``.
    semantic_role
        Declared artifact role; this is metadata, not scientific acceptance.
    retention_policy
        Retention-policy identifier.  It never grants deletion authority.
    """

    logical_path: str
    format: str
    semantic_role: str
    retention_policy: str

    def __post_init__(self) -> None:
        _require_root_relative_path(self.logical_path, "logical_path")
        _require_identifier(self.format, "format")
        _require_identifier(self.semantic_role, "semantic_role")
        _require_identifier(self.retention_policy, "retention_policy")


@dataclass(frozen=True, slots=True)
class ArtifactReference:
    """Portable reference to sealed content and its producer manifest.

    Parameters
    ----------
    identity
        Exact content identity.
    specification
        Portable logical-path, format, role, and retention declaration.
    producer_manifest_id
        Opaque identity of the manifest that produced the artifact.

    Notes
    -----
    This object deliberately contains no deployment location.  The convenience
    properties expose the accepted flat reference vocabulary without duplicating
    stored state.
    """

    identity: ArtifactIdentity
    specification: ArtifactSpecification
    producer_manifest_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.identity, ArtifactIdentity):
            raise TypeError("identity must be an ArtifactIdentity")
        if not isinstance(self.specification, ArtifactSpecification):
            raise TypeError("specification must be an ArtifactSpecification")
        _require_identifier(self.producer_manifest_id, "producer_manifest_id")

    @property
    def artifact_id(self) -> str:
        """Return the stable artifact identifier."""
        return self.identity.artifact_id

    @property
    def logical_path(self) -> str:
        """Return the portable logical path, never a storage location."""
        return self.specification.logical_path

    @property
    def sha256(self) -> str:
        """Return the exact lowercase SHA-256 digest."""
        return self.identity.sha256

    @property
    def byte_size(self) -> int:
        """Return the exact unsigned 64-bit byte size."""
        return self.identity.byte_size


@dataclass(frozen=True, slots=True)
class ArtifactLocation:
    """Deployment location kept separate from portable artifact identity.

    Parameters
    ----------
    artifact_id
        Stable identifier of the located artifact.
    kind
        Location representation discriminator.
    root_id
        Explicit approved root identifier for ``ROOT_RELATIVE``.
    path
        NFC root-relative POSIX lexical path for ``ROOT_RELATIVE``.
    external_descriptor_id
        Opaque approved descriptor identifier for ``EXTERNAL_DESCRIPTOR``.

    Raises
    ------
    TypeError
        If values have incorrect types, including passing a string for ``kind``.
    ValueError
        If the selected representation is incomplete or contains fields from
        the other representation.

    Notes
    -----
    The record neither discovers an ambient root nor resolves the descriptor.
    """

    artifact_id: str
    kind: ArtifactLocationKind
    root_id: str | None = None
    path: str | None = None
    external_descriptor_id: str | None = None

    def __post_init__(self) -> None:
        _require_identifier(self.artifact_id, "artifact_id")
        if not isinstance(self.kind, ArtifactLocationKind):
            raise TypeError("kind must be an ArtifactLocationKind")
        if self.kind is ArtifactLocationKind.ROOT_RELATIVE:
            _require_identifier(self.root_id, "root_id")
            _require_root_relative_path(self.path, "path")
            if self.external_descriptor_id is not None:
                raise ValueError(
                    "external_descriptor_id must be absent for a root-relative location"
                )
        else:
            _require_identifier(self.external_descriptor_id, "external_descriptor_id")
            if self.root_id is not None or self.path is not None:
                raise ValueError(
                    "root_id and path must be absent for an external descriptor"
                )


@dataclass(frozen=True, slots=True)
class RunManifest:
    """Immutable manifest for one declared or observed execution attempt.

    Parameters
    ----------
    manifest_id
        Preallocated opaque manifest identifier.
    specification_id
        Identity of the immutable operation specification.
    input_artifact_ids, output_artifact_ids
        Ordered, duplicate-free artifact identifiers.
    started_at, finished_at
        UTC timestamps in ``YYYY-MM-DDTHH:MM:SSZ`` form. ``finished_at`` is
        absent only for ``DECLARED``.
    dependency_manifest_ids
        Ordered, duplicate-free manifest dependencies.
    state
        Manifest lifecycle state, distinct from scientific acceptance.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If an intrinsic manifest invariant is violated.
    """

    manifest_id: str
    specification_id: str
    input_artifact_ids: tuple[str, ...]
    started_at: str
    finished_at: str | None
    output_artifact_ids: tuple[str, ...]
    dependency_manifest_ids: tuple[str, ...]
    state: ManifestState

    def __post_init__(self) -> None:
        _require_identifier(self.manifest_id, "manifest_id")
        _require_identifier(self.specification_id, "specification_id")
        object.__setattr__(
            self,
            "input_artifact_ids",
            _require_identifier_tuple(self.input_artifact_ids, "input_artifact_ids"),
        )
        _require_text(self.started_at, "started_at")
        if _TIMESTAMP_PATTERN.fullmatch(self.started_at) is None:
            raise ValueError("started_at must be an RFC 3339 UTC second timestamp")
        try:
            started = datetime.strptime(self.started_at, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as error:
            raise ValueError(
                "started_at must be a real UTC calendar timestamp"
            ) from error
        if not isinstance(self.state, ManifestState):
            raise TypeError("state must be a ManifestState")
        if self.finished_at is None:
            if self.state is not ManifestState.DECLARED:
                raise ValueError("finished_at is required for a terminal manifest")
        else:
            _require_text(self.finished_at, "finished_at")
            if _TIMESTAMP_PATTERN.fullmatch(self.finished_at) is None:
                raise ValueError("finished_at must be an RFC 3339 UTC second timestamp")
            try:
                finished = datetime.strptime(self.finished_at, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError as error:
                raise ValueError(
                    "finished_at must be a real UTC calendar timestamp"
                ) from error
            if self.state is ManifestState.DECLARED:
                raise ValueError("finished_at must be absent for a declared manifest")
            if finished < started:
                raise ValueError("finished_at must not precede started_at")
        object.__setattr__(
            self,
            "output_artifact_ids",
            _require_identifier_tuple(self.output_artifact_ids, "output_artifact_ids"),
        )
        object.__setattr__(
            self,
            "dependency_manifest_ids",
            _require_identifier_tuple(
                self.dependency_manifest_ids, "dependency_manifest_ids"
            ),
        )


@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    """Durable provenance links for a manifest and its artifacts.

    Parameters
    ----------
    provenance_id
        Stable identity of this provenance record.
    manifest_id
        Manifest described by this record.
    parent_provenance_ids
        Ordered, duplicate-free direct provenance parents.
    artifact_ids
        Ordered, duplicate-free artifacts covered by this record.
    """

    provenance_id: str
    manifest_id: str
    parent_provenance_ids: tuple[str, ...]
    artifact_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.provenance_id, "provenance_id")
        _require_identifier(self.manifest_id, "manifest_id")
        parents = _require_identifier_tuple(
            self.parent_provenance_ids, "parent_provenance_ids"
        )
        if self.provenance_id in parents:
            raise ValueError("a provenance record must not be its own parent")
        object.__setattr__(self, "parent_provenance_ids", parents)
        object.__setattr__(
            self,
            "artifact_ids",
            _require_identifier_tuple(self.artifact_ids, "artifact_ids"),
        )


@dataclass(frozen=True, slots=True)
class LineageRelation:
    """One directed, immutable parent-to-child lineage edge.

    Parameters
    ----------
    lineage_id
        Stable identity of the relation.
    parent_id, child_id
        Opaque parent and child identities in the declared identity namespace.
    kind
        Meaning of the directed edge.
    provenance_id
        Provenance record supporting the relationship.
    """

    lineage_id: str
    parent_id: str
    child_id: str
    kind: LineageKind
    provenance_id: str

    def __post_init__(self) -> None:
        _require_identifier(self.lineage_id, "lineage_id")
        _require_identifier(self.parent_id, "parent_id")
        _require_identifier(self.child_id, "child_id")
        if self.parent_id == self.child_id:
            raise ValueError("parent_id and child_id must differ")
        if not isinstance(self.kind, LineageKind):
            raise TypeError("kind must be a LineageKind")
        _require_identifier(self.provenance_id, "provenance_id")
