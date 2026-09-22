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
_WINDOWS_DEVICE_NAMES = frozenset(
    {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }
)
_TIMESTAMP_PATTERN = re.compile(
    r"[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"
    r"T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z\Z"
)


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
        """Validate this artifact's portable identifier and exact byte identity."""
        if type(self.artifact_id) is not str:
            raise TypeError("artifact_id must be a built-in str")
        if not self.artifact_id:
            raise ValueError("artifact_id must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.artifact_id):
            raise ValueError(
                "artifact_id must not contain Unicode surrogate code points"
            )
        if unicodedata.normalize("NFC", self.artifact_id) != self.artifact_id:
            raise ValueError("artifact_id must be Unicode NFC")
        if _ID_PATTERN.fullmatch(self.artifact_id) is None:
            raise ValueError("artifact_id must match [A-Za-z0-9][A-Za-z0-9._:-]{0,127}")

        if type(self.sha256) is not str:
            raise TypeError("sha256 must be a built-in str")
        if not self.sha256:
            raise ValueError("sha256 must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.sha256):
            raise ValueError("sha256 must not contain Unicode surrogate code points")
        if unicodedata.normalize("NFC", self.sha256) != self.sha256:
            raise ValueError("sha256 must be Unicode NFC")
        if _SHA256_PATTERN.fullmatch(self.sha256) is None:
            raise ValueError("sha256 must be a 64-character lowercase SHA-256 digest")

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

    Raises
    ------
    TypeError
        If any field is not a built-in string.
    ValueError
        If ``logical_path`` violates the root-relative POSIX lexical-path
        contract or any identifier is empty, non-NFC, contains a Unicode
        surrogate, or violates the portable identifier grammar.
    """

    logical_path: str
    format: str
    semantic_role: str
    retention_policy: str

    def __post_init__(self) -> None:
        """Validate this specification's lexical path and metadata identifiers."""
        if type(self.logical_path) is not str:
            raise TypeError("logical_path must be a built-in str")
        if not self.logical_path:
            raise ValueError("logical_path must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.logical_path):
            raise ValueError(
                "logical_path must not contain Unicode surrogate code points"
            )
        if unicodedata.normalize("NFC", self.logical_path) != self.logical_path:
            raise ValueError("logical_path must be Unicode NFC")
        if self.logical_path.startswith("/") or _DRIVE_PATTERN.match(self.logical_path):
            raise ValueError(
                "logical_path must not use absolute or Windows drive syntax"
            )
        if (
            "\\" in self.logical_path
            or self.logical_path.endswith("/")
            or "//" in self.logical_path
        ):
            raise ValueError("logical_path must be a root-relative POSIX lexical path")
        logical_path_parts = self.logical_path.split("/")
        if any(part in {"", ".", ".."} for part in logical_path_parts):
            raise ValueError(
                "logical_path must not contain empty, '.' or '..' components"
            )
        for part in logical_path_parts:
            if part.split(".", 1)[0].upper() in _WINDOWS_DEVICE_NAMES:
                raise ValueError("logical_path must not contain a Windows device name")
        if any(
            ord(character) < 0x20
            or 0x7F <= ord(character) <= 0x9F
            or ord(character) in {0x2028, 0x2029}
            for character in self.logical_path
        ):
            raise ValueError("logical_path must not contain C0/C1 or line controls")

        for name, value in (
            ("format", self.format),
            ("semantic_role", self.semantic_role),
            ("retention_policy", self.retention_policy),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(
                    f"{name} must not contain Unicode surrogate code points"
                )
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(
                    f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}"
                )


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

    Raises
    ------
    TypeError
        If ``identity`` or ``specification`` has the wrong record type, or if
        ``producer_manifest_id`` is not a built-in string.
    ValueError
        If ``producer_manifest_id`` is empty, non-NFC, contains a Unicode
        surrogate, or violates the portable identifier grammar.

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
        """Validate this reference's nested records and producer identity."""
        if not isinstance(self.identity, ArtifactIdentity):
            raise TypeError("identity must be an ArtifactIdentity")
        if not isinstance(self.specification, ArtifactSpecification):
            raise TypeError("specification must be an ArtifactSpecification")
        if type(self.producer_manifest_id) is not str:
            raise TypeError("producer_manifest_id must be a built-in str")
        if not self.producer_manifest_id:
            raise ValueError("producer_manifest_id must not be empty")
        if any(
            0xD800 <= ord(character) <= 0xDFFF
            for character in self.producer_manifest_id
        ):
            raise ValueError(
                "producer_manifest_id must not contain Unicode surrogate code points"
            )
        if (
            unicodedata.normalize("NFC", self.producer_manifest_id)
            != self.producer_manifest_id
        ):
            raise ValueError("producer_manifest_id must be Unicode NFC")
        if _ID_PATTERN.fullmatch(self.producer_manifest_id) is None:
            raise ValueError(
                "producer_manifest_id must match [A-Za-z0-9][A-Za-z0-9._:-]{0,127}"
            )

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
        """Validate this location's artifact identity and selected representation."""
        if type(self.artifact_id) is not str:
            raise TypeError("artifact_id must be a built-in str")
        if not self.artifact_id:
            raise ValueError("artifact_id must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.artifact_id):
            raise ValueError(
                "artifact_id must not contain Unicode surrogate code points"
            )
        if unicodedata.normalize("NFC", self.artifact_id) != self.artifact_id:
            raise ValueError("artifact_id must be Unicode NFC")
        if _ID_PATTERN.fullmatch(self.artifact_id) is None:
            raise ValueError("artifact_id must match [A-Za-z0-9][A-Za-z0-9._:-]{0,127}")
        if not isinstance(self.kind, ArtifactLocationKind):
            raise TypeError("kind must be an ArtifactLocationKind")

        if self.kind is ArtifactLocationKind.ROOT_RELATIVE:
            if type(self.root_id) is not str:
                raise TypeError("root_id must be a built-in str")
            if not self.root_id:
                raise ValueError("root_id must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in self.root_id):
                raise ValueError(
                    "root_id must not contain Unicode surrogate code points"
                )
            if unicodedata.normalize("NFC", self.root_id) != self.root_id:
                raise ValueError("root_id must be Unicode NFC")
            if _ID_PATTERN.fullmatch(self.root_id) is None:
                raise ValueError("root_id must match [A-Za-z0-9][A-Za-z0-9._:-]{0,127}")

            if type(self.path) is not str:
                raise TypeError("path must be a built-in str")
            if not self.path:
                raise ValueError("path must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in self.path):
                raise ValueError("path must not contain Unicode surrogate code points")
            if unicodedata.normalize("NFC", self.path) != self.path:
                raise ValueError("path must be Unicode NFC")
            if self.path.startswith("/") or _DRIVE_PATTERN.match(self.path):
                raise ValueError("path must not use absolute or Windows drive syntax")
            if "\\" in self.path or self.path.endswith("/") or "//" in self.path:
                raise ValueError("path must be a root-relative POSIX lexical path")
            path_parts = self.path.split("/")
            if any(part in {"", ".", ".."} for part in path_parts):
                raise ValueError("path must not contain empty, '.' or '..' components")
            for part in path_parts:
                if part.split(".", 1)[0].upper() in _WINDOWS_DEVICE_NAMES:
                    raise ValueError("path must not contain a Windows device name")
            if any(
                ord(character) < 0x20
                or 0x7F <= ord(character) <= 0x9F
                or ord(character) in {0x2028, 0x2029}
                for character in self.path
            ):
                raise ValueError("path must not contain C0/C1 or line controls")
            if self.external_descriptor_id is not None:
                raise ValueError(
                    "external_descriptor_id must be absent for a root-relative location"
                )
        else:
            if type(self.external_descriptor_id) is not str:
                raise TypeError("external_descriptor_id must be a built-in str")
            if not self.external_descriptor_id:
                raise ValueError("external_descriptor_id must not be empty")
            if any(
                0xD800 <= ord(character) <= 0xDFFF
                for character in self.external_descriptor_id
            ):
                raise ValueError(
                    "external_descriptor_id must not contain Unicode surrogate "
                    "code points"
                )
            if (
                unicodedata.normalize("NFC", self.external_descriptor_id)
                != self.external_descriptor_id
            ):
                raise ValueError("external_descriptor_id must be Unicode NFC")
            if _ID_PATTERN.fullmatch(self.external_descriptor_id) is None:
                raise ValueError(
                    "external_descriptor_id must match "
                    "[A-Za-z0-9][A-Za-z0-9._:-]{0,127}"
                )
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
    input_artifact_ids
        Ordered, duplicate-free identities of declared input artifacts.
    output_artifact_ids
        Ordered, duplicate-free, preallocated expected output identities.  A
        ``DECLARED`` manifest may contain them before the corresponding bytes
        or terminal execution outcome exist.
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
        """Validate this attempt's identifiers, times, lifecycle, and dependencies."""
        for name, value in (
            ("manifest_id", self.manifest_id),
            ("specification_id", self.specification_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(
                    f"{name} must not contain Unicode surrogate code points"
                )
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(
                    f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}"
                )

        if type(self.input_artifact_ids) is not tuple:
            raise TypeError("input_artifact_ids must be a built-in tuple")
        for index, artifact_id in enumerate(self.input_artifact_ids):
            name = f"input_artifact_ids[{index}]"
            if type(artifact_id) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not artifact_id:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in artifact_id):
                raise ValueError(
                    f"{name} must not contain Unicode surrogate code points"
                )
            if unicodedata.normalize("NFC", artifact_id) != artifact_id:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(artifact_id) is None:
                raise ValueError(
                    f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}"
                )
        if self.input_artifact_ids != tuple(sorted(self.input_artifact_ids)) or len(
            set(self.input_artifact_ids)
        ) != len(self.input_artifact_ids):
            raise ValueError("input_artifact_ids must be unique and lexically sorted")

        if type(self.started_at) is not str:
            raise TypeError("started_at must be a built-in str")
        if not self.started_at:
            raise ValueError("started_at must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.started_at):
            raise ValueError(
                "started_at must not contain Unicode surrogate code points"
            )
        if unicodedata.normalize("NFC", self.started_at) != self.started_at:
            raise ValueError("started_at must be Unicode NFC")
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
            if type(self.finished_at) is not str:
                raise TypeError("finished_at must be a built-in str")
            if not self.finished_at:
                raise ValueError("finished_at must not be empty")
            if any(
                0xD800 <= ord(character) <= 0xDFFF for character in self.finished_at
            ):
                raise ValueError(
                    "finished_at must not contain Unicode surrogate code points"
                )
            if unicodedata.normalize("NFC", self.finished_at) != self.finished_at:
                raise ValueError("finished_at must be Unicode NFC")
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

        for field_name, identifiers in (
            ("output_artifact_ids", self.output_artifact_ids),
            ("dependency_manifest_ids", self.dependency_manifest_ids),
        ):
            if type(identifiers) is not tuple:
                raise TypeError(f"{field_name} must be a built-in tuple")
            for index, identifier in enumerate(identifiers):
                name = f"{field_name}[{index}]"
                if type(identifier) is not str:
                    raise TypeError(f"{name} must be a built-in str")
                if not identifier:
                    raise ValueError(f"{name} must not be empty")
                if any(0xD800 <= ord(character) <= 0xDFFF for character in identifier):
                    raise ValueError(
                        f"{name} must not contain Unicode surrogate code points"
                    )
                if unicodedata.normalize("NFC", identifier) != identifier:
                    raise ValueError(f"{name} must be Unicode NFC")
                if _ID_PATTERN.fullmatch(identifier) is None:
                    raise ValueError(
                        f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}"
                    )
            if identifiers != tuple(sorted(identifiers)) or len(
                set(identifiers)
            ) != len(identifiers):
                raise ValueError(f"{field_name} must be unique and lexically sorted")

        if self.manifest_id in self.dependency_manifest_ids:
            raise ValueError("a run manifest must not depend on itself")


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

    Raises
    ------
    TypeError
        If an identity is not a built-in string, either collection is not a
        built-in tuple, or a tuple member is not a built-in string.
    ValueError
        If an identifier violates its lexical contract, either collection is
        not unique and lexically sorted, or the record names itself as a direct
        parent.
    """

    provenance_id: str
    manifest_id: str
    parent_provenance_ids: tuple[str, ...]
    artifact_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate this record's identifiers and direct-parent relationship."""
        for name, value in (
            ("provenance_id", self.provenance_id),
            ("manifest_id", self.manifest_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(
                    f"{name} must not contain Unicode surrogate code points"
                )
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(
                    f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}"
                )

        for field_name, identifiers in (
            ("parent_provenance_ids", self.parent_provenance_ids),
            ("artifact_ids", self.artifact_ids),
        ):
            if type(identifiers) is not tuple:
                raise TypeError(f"{field_name} must be a built-in tuple")
            for index, identifier in enumerate(identifiers):
                name = f"{field_name}[{index}]"
                if type(identifier) is not str:
                    raise TypeError(f"{name} must be a built-in str")
                if not identifier:
                    raise ValueError(f"{name} must not be empty")
                if any(0xD800 <= ord(character) <= 0xDFFF for character in identifier):
                    raise ValueError(
                        f"{name} must not contain Unicode surrogate code points"
                    )
                if unicodedata.normalize("NFC", identifier) != identifier:
                    raise ValueError(f"{name} must be Unicode NFC")
                if _ID_PATTERN.fullmatch(identifier) is None:
                    raise ValueError(
                        f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}"
                    )
            if identifiers != tuple(sorted(identifiers)) or len(
                set(identifiers)
            ) != len(identifiers):
                raise ValueError(f"{field_name} must be unique and lexically sorted")

        if self.provenance_id in self.parent_provenance_ids:
            raise ValueError("a provenance record must not be its own parent")


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

    Raises
    ------
    TypeError
        If an identity is not a built-in string or ``kind`` is not a
        :class:`LineageKind` member.
    ValueError
        If an identifier violates its lexical contract or ``parent_id`` and
        ``child_id`` are equal.
    """

    lineage_id: str
    parent_id: str
    child_id: str
    kind: LineageKind
    provenance_id: str

    def __post_init__(self) -> None:
        """Validate this directed edge's identifiers, direction, and vocabulary."""
        for name, value in (
            ("lineage_id", self.lineage_id),
            ("parent_id", self.parent_id),
            ("child_id", self.child_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(
                    f"{name} must not contain Unicode surrogate code points"
                )
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(
                    f"{name} must match [A-Za-z0-9][A-Za-z0-9._:-]{{0,127}}"
                )
        if self.parent_id == self.child_id:
            raise ValueError("parent_id and child_id must differ")
        if not isinstance(self.kind, LineageKind):
            raise TypeError("kind must be a LineageKind")

        if type(self.provenance_id) is not str:
            raise TypeError("provenance_id must be a built-in str")
        if not self.provenance_id:
            raise ValueError("provenance_id must not be empty")
        if any(0xD800 <= ord(character) <= 0xDFFF for character in self.provenance_id):
            raise ValueError(
                "provenance_id must not contain Unicode surrogate code points"
            )
        if unicodedata.normalize("NFC", self.provenance_id) != self.provenance_id:
            raise ValueError("provenance_id must be Unicode NFC")
        if _ID_PATTERN.fullmatch(self.provenance_id) is None:
            raise ValueError(
                "provenance_id must match [A-Za-z0-9][A-Za-z0-9._:-]{0,127}"
            )
