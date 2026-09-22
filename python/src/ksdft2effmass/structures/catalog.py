"""Canonical immutable structure-catalog records and atomic persistence.

The catalog retains exact canonical structure snapshot bytes, source provenance, and
explicitly parameterized derived symmetry. It composes the shared opaque revision
store and introduces no structure-specific SQL schema. Stored reference geometry does
not become a production geometry or establish scientific validity.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.persistence import (
    AtomicRevisionStore,
    Commit,
    CommitStatus,
    Revision,
    RevisionReadRequest,
    RevisionReadStatus,
    RevisionSelector,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type JsonObject = dict[str, JsonValue]

__all__ = [
    "StructureCatalogEntry",
    "StructureCatalogEntrySerializer",
    "StructureCatalogLoadResult",
    "StructureCatalogLoadStatus",
    "StructureCatalogRepository",
    "StructureCatalogRole",
    "StructureCatalogWriteResult",
    "StructureCatalogWriteStatus",
    "StructureSymmetry",
]


class StructureCatalogRole(StrEnum):
    """Scientific role of one retained geometry snapshot.

    Attributes
    ----------
    EXTERNAL_REFERENCE
        Geometry obtained from an external reference and not selected for production.
    PRODUCTION_RELAXED
        Geometry produced by an identified production relaxation.
    PROVISIONAL_INPUT
        Geometry retained as an input whose production status is not established.
    """

    EXTERNAL_REFERENCE = "external_reference"
    PRODUCTION_RELAXED = "production_relaxed"
    PROVISIONAL_INPUT = "provisional_input"


@dataclass(frozen=True, slots=True)
class StructureSymmetry:
    """Tolerance-qualified symmetry derived from one exact structure snapshot.

    Attributes
    ----------
    analyzer_identity
        Fully qualified analyzer implementation identity.
    analyzer_version
        Installed analyzer-distribution version used for derivation.
    symprec_angstrom
        Positive finite positional tolerance in angstrom.
    angle_tolerance_degree
        Positive finite angular tolerance in degrees.
    space_group_symbol
        International short Hermann--Mauguin symbol returned by the analyzer.
    space_group_number
        International space-group number from 1 through 230.
    hall_symbol
        Hall symbol returned by the analyzer.
    crystal_system
        Analyzer-reported crystal-system label.
    point_group_symbol
        Analyzer-reported point-group symbol.
    wyckoff_symbols
        Site-ordered Wyckoff symbols, one per retained structure site.
    equivalent_atoms
        Site-ordered nonnegative equivalence-class indices.

    Notes
    -----
    These fields describe derived numerical metadata. Their presence does not establish
    independent crystallographic or scientific validation.
    """

    analyzer_identity: str
    analyzer_version: str
    symprec_angstrom: float
    angle_tolerance_degree: float
    space_group_symbol: str
    space_group_number: int
    hall_symbol: str
    crystal_system: str
    point_group_symbol: str
    wyckoff_symbols: tuple[str, ...]
    equivalent_atoms: tuple[int, ...]

    def __post_init__(self) -> None:
        for name, text_value in (
            ("analyzer_identity", self.analyzer_identity),
            ("analyzer_version", self.analyzer_version),
            ("space_group_symbol", self.space_group_symbol),
            ("hall_symbol", self.hall_symbol),
            ("crystal_system", self.crystal_system),
            ("point_group_symbol", self.point_group_symbol),
        ):
            if type(text_value) is not str:
                raise TypeError(f"{name} must be str")
            if not text_value:
                raise ValueError(f"{name} must be nonempty")
        for name, tolerance_value in (
            ("symprec_angstrom", self.symprec_angstrom),
            ("angle_tolerance_degree", self.angle_tolerance_degree),
        ):
            if type(tolerance_value) is not float:
                raise TypeError(f"{name} must be built-in float")
            if not math.isfinite(tolerance_value) or tolerance_value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if type(self.space_group_number) is not int:
            raise TypeError("space_group_number must be built-in int")
        if not 1 <= self.space_group_number <= 230:
            raise ValueError("space_group_number must be in [1, 230]")
        if type(self.wyckoff_symbols) is not tuple or any(
            type(value) is not str or not value for value in self.wyckoff_symbols
        ):
            raise TypeError("wyckoff_symbols must contain nonempty str values")
        if type(self.equivalent_atoms) is not tuple or any(
            type(value) is not int or value < 0 for value in self.equivalent_atoms
        ):
            raise TypeError("equivalent_atoms must contain nonnegative int values")
        if not self.wyckoff_symbols or len(self.wyckoff_symbols) != len(
            self.equivalent_atoms
        ):
            raise ValueError("symmetry site arrays must be nonempty and equal length")


@dataclass(frozen=True, slots=True)
class StructureCatalogEntry:
    """Immutable canonical structure snapshot with provenance and symmetry.

    Attributes
    ----------
    identity
        Stable project catalog identity, such as ``materials-project:mp-149``.
    role
        Explicit scientific role of the retained geometry.
    source_database
        Human-readable external or project source name.
    source_record_id
        Source-owned record identifier.
    source_url
        Source record locator retained as provenance.
    source_content_id
        ``sha256:<hex>`` identity of the exact ``source_snapshot`` bytes.
    source_snapshot
        Exact credential-free canonical structure JSON bytes.
    symmetry
        Derived analyzer-, version-, and tolerance-qualified symmetry metadata.
    limitations
        Nonempty unique statements bounding interpretation of the entry.

    Raises
    ------
    TypeError
        A field has the wrong semantic type.
    ValueError
        A text or limitations field is empty, limitations repeat, or the SHA-256
        content identity does not authenticate the exact snapshot bytes.
    """

    identity: str
    role: StructureCatalogRole
    source_database: str
    source_record_id: str
    source_url: str
    source_content_id: str
    source_snapshot: bytes
    symmetry: StructureSymmetry
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("identity", self.identity),
            ("source_database", self.source_database),
            ("source_record_id", self.source_record_id),
            ("source_url", self.source_url),
            ("source_content_id", self.source_content_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be str")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.role) is not StructureCatalogRole:
            raise TypeError("role must be StructureCatalogRole")
        if type(self.source_snapshot) is not bytes:
            raise TypeError("source_snapshot must be bytes")
        expected = "sha256:" + hashlib.sha256(self.source_snapshot).hexdigest()
        if self.source_content_id != expected:
            raise ValueError("source_content_id must authenticate source_snapshot")
        if type(self.symmetry) is not StructureSymmetry:
            raise TypeError("symmetry must be StructureSymmetry")
        if type(self.limitations) is not tuple or any(
            type(value) is not str or not value for value in self.limitations
        ):
            raise TypeError("limitations must contain nonempty str values")
        if not self.limitations or len(set(self.limitations)) != len(self.limitations):
            raise ValueError("limitations must be nonempty and unique")


@dataclass(frozen=True, slots=True)
class StructureCatalogEntrySerializer:
    """Encode and reconstruct the closed catalog-entry wire format.

    Attributes
    ----------
    SCHEMA_ID
        Stable schema identity stored with every generic revision.

    Notes
    -----
    The schema uses canonical sorted UTF-8 JSON and base64 for exact source snapshot
    bytes. Unknown or missing fields are rejected during reconstruction.
    """

    SCHEMA_ID = "ksdft2effmass.structure-catalog-entry.v1"

    def serialize(self, value: StructureCatalogEntry) -> bytes:
        """Return stable canonical UTF-8 JSON bytes.

        Parameters
        ----------
        value
            Complete validated structure-catalog entry.

        Returns
        -------
        bytes
            Newline-terminated sorted JSON with the exact snapshot encoded as base64.

        Raises
        ------
        TypeError
            ``value`` is not exactly ``StructureCatalogEntry``.
        """
        if type(value) is not StructureCatalogEntry:
            raise TypeError("value must be StructureCatalogEntry")
        symmetry = value.symmetry
        payload: JsonObject = {
            "schema_version": 1,
            "identity": value.identity,
            "role": value.role.value,
            "source": {
                "database": value.source_database,
                "record_id": value.source_record_id,
                "url": value.source_url,
                "content_id": value.source_content_id,
                "snapshot_base64": base64.b64encode(value.source_snapshot).decode(
                    "ascii"
                ),
            },
            "symmetry": {
                "analyzer_identity": symmetry.analyzer_identity,
                "analyzer_version": symmetry.analyzer_version,
                "symprec_angstrom": symmetry.symprec_angstrom,
                "angle_tolerance_degree": symmetry.angle_tolerance_degree,
                "space_group_symbol": symmetry.space_group_symbol,
                "space_group_number": symmetry.space_group_number,
                "hall_symbol": symmetry.hall_symbol,
                "crystal_system": symmetry.crystal_system,
                "point_group_symbol": symmetry.point_group_symbol,
                "wyckoff_symbols": list(symmetry.wyckoff_symbols),
                "equivalent_atoms": list(symmetry.equivalent_atoms),
            },
            "limitations": list(value.limitations),
        }
        return (
            json.dumps(
                payload,
                allow_nan=False,
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")

    def deserialize(self, payload: bytes) -> StructureCatalogEntry:
        """Strictly reconstruct one catalog entry from its complete payload.

        Parameters
        ----------
        payload
            Complete UTF-8 JSON wire bytes for schema version 1.

        Returns
        -------
        StructureCatalogEntry
            Reconstructed immutable entry after all intrinsic validation.

        Raises
        ------
        TypeError
            The payload or a decoded field has the wrong semantic type.
        ValueError
            JSON, schema version, fields, base64, or domain invariants are invalid.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            decoded = json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("malformed structure catalog JSON") from error
        root = self._mapping(decoded, "catalog entry")
        self._keys(
            root,
            {"schema_version", "identity", "role", "source", "symmetry", "limitations"},
            "catalog entry",
        )
        if root["schema_version"] != 1:
            raise ValueError("unsupported structure catalog schema version")
        source = self._mapping(root["source"], "source")
        self._keys(
            source,
            {"database", "record_id", "url", "content_id", "snapshot_base64"},
            "source",
        )
        symmetry = self._mapping(root["symmetry"], "symmetry")
        self._keys(
            symmetry,
            {
                "analyzer_identity",
                "analyzer_version",
                "symprec_angstrom",
                "angle_tolerance_degree",
                "space_group_symbol",
                "space_group_number",
                "hall_symbol",
                "crystal_system",
                "point_group_symbol",
                "wyckoff_symbols",
                "equivalent_atoms",
            },
            "symmetry",
        )
        snapshot_text = self._string(source["snapshot_base64"], "snapshot_base64")
        try:
            snapshot = base64.b64decode(snapshot_text, validate=True)
        except ValueError as error:
            raise ValueError("invalid source snapshot base64") from error
        return StructureCatalogEntry(
            identity=self._string(root["identity"], "identity"),
            role=StructureCatalogRole(self._string(root["role"], "role")),
            source_database=self._string(source["database"], "database"),
            source_record_id=self._string(source["record_id"], "record_id"),
            source_url=self._string(source["url"], "url"),
            source_content_id=self._string(source["content_id"], "content_id"),
            source_snapshot=snapshot,
            symmetry=StructureSymmetry(
                analyzer_identity=self._string(
                    symmetry["analyzer_identity"], "analyzer_identity"
                ),
                analyzer_version=self._string(
                    symmetry["analyzer_version"], "analyzer_version"
                ),
                symprec_angstrom=self._float(
                    symmetry["symprec_angstrom"], "symprec_angstrom"
                ),
                angle_tolerance_degree=self._float(
                    symmetry["angle_tolerance_degree"], "angle_tolerance_degree"
                ),
                space_group_symbol=self._string(
                    symmetry["space_group_symbol"], "space_group_symbol"
                ),
                space_group_number=self._integer(
                    symmetry["space_group_number"], "space_group_number"
                ),
                hall_symbol=self._string(symmetry["hall_symbol"], "hall_symbol"),
                crystal_system=self._string(
                    symmetry["crystal_system"], "crystal_system"
                ),
                point_group_symbol=self._string(
                    symmetry["point_group_symbol"], "point_group_symbol"
                ),
                wyckoff_symbols=self._strings(
                    symmetry["wyckoff_symbols"], "wyckoff_symbols"
                ),
                equivalent_atoms=self._integers(
                    symmetry["equivalent_atoms"], "equivalent_atoms"
                ),
            ),
            limitations=self._strings(root["limitations"], "limitations"),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> JsonObject:
        if type(value) is not dict:
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def _keys(value: JsonObject, expected: set[str], name: str) -> None:
        if set(value) != expected:
            raise ValueError(f"{name} fields are not closed")

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{name} must be str")
        return value

    @staticmethod
    def _float(value: JsonValue, name: str) -> float:
        if type(value) is not float:
            raise TypeError(f"{name} must be built-in float")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{name} must be built-in int")
        return value

    @classmethod
    def _strings(cls, value: JsonValue, name: str) -> tuple[str, ...]:
        if type(value) is not list:
            raise TypeError(f"{name} must be a list")
        return tuple(cls._string(item, name) for item in value)

    @classmethod
    def _integers(cls, value: JsonValue, name: str) -> tuple[int, ...]:
        if type(value) is not list:
            raise TypeError(f"{name} must be a list")
        return tuple(cls._integer(item, name) for item in value)


class StructureCatalogWriteStatus(StrEnum):
    """Closed catalog write outcomes.

    ``COMMITTED`` denotes a new revision, ``UNCHANGED`` an exact current replay,
    ``CONFLICT`` a compare-and-swap loss, and ``FAILED`` an operational failure.
    """

    COMMITTED = "committed"
    UNCHANGED = "unchanged"
    CONFLICT = "conflict"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class StructureCatalogWriteResult:
    """Result of one exact structure-catalog write.

    Attributes
    ----------
    status
        Closed disposition of the attempted write.
    entry_identity
        Requested domain entry identity.
    revision_identity
        Committed or unchanged revision identity when available; otherwise ``None``.
    diagnostics
        Immutable store diagnostics; empty for ordinary committed or unchanged results.
    """

    status: StructureCatalogWriteStatus
    entry_identity: str
    revision_identity: str | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.status) is not StructureCatalogWriteStatus:
            raise TypeError("status must be StructureCatalogWriteStatus")
        if type(self.entry_identity) is not str:
            raise TypeError("entry_identity must be str")
        if not self.entry_identity:
            raise ValueError("entry_identity must be nonempty")
        if self.revision_identity is not None:
            if type(self.revision_identity) is not str:
                raise TypeError("revision_identity must be str or None")
            if not self.revision_identity:
                raise ValueError("revision_identity must be nonempty when present")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must contain str values")


class StructureCatalogLoadStatus(StrEnum):
    """Closed catalog load outcomes.

    ``LOADED`` denotes a validated latest entry, ``ABSENT`` a missing stream, and
    ``FAILED`` an operational, schema, or payload-integrity failure.
    """

    LOADED = "loaded"
    ABSENT = "absent"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class StructureCatalogLoadResult:
    """Result of one latest structure-catalog load.

    Attributes
    ----------
    status
        Closed disposition of the load.
    entry_identity
        Requested domain entry identity.
    revision_identity
        Observed revision identity when available; otherwise ``None``.
    entry
        Reconstructed entry only when ``status`` is ``LOADED``.
    diagnostics
        Immutable failure diagnostics; empty for ordinary loaded or absent results.
    """

    status: StructureCatalogLoadStatus
    entry_identity: str
    revision_identity: str | None
    entry: StructureCatalogEntry | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.status) is not StructureCatalogLoadStatus:
            raise TypeError("status must be StructureCatalogLoadStatus")
        if type(self.entry_identity) is not str:
            raise TypeError("entry_identity must be str")
        if not self.entry_identity:
            raise ValueError("entry_identity must be nonempty")
        if self.revision_identity is not None:
            if type(self.revision_identity) is not str:
                raise TypeError("revision_identity must be str or None")
            if not self.revision_identity:
                raise ValueError("revision_identity must be nonempty when present")
        if self.entry is not None and type(self.entry) is not StructureCatalogEntry:
            raise TypeError("entry must be StructureCatalogEntry or None")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must contain str values")
        if self.status is StructureCatalogLoadStatus.LOADED:
            if self.revision_identity is None or self.entry is None or self.diagnostics:
                raise ValueError("loaded result fields are inconsistent")
        elif self.entry is not None:
            raise ValueError("non-loaded result must not contain an entry")


@dataclass(frozen=True, slots=True)
class StructureCatalogRepository:
    """Persist structure entries as append-only domain revisions.

    Parameters
    ----------
    store
        Atomic opaque revision store supplied by the application boundary.
    serializer
        Structure entry codec. The default implements schema version 1.

    Notes
    -----
    Each entry identity maps to one stream. Revision identity binds the canonical
    payload and its predecessor, allowing historical content to be restored as a new
    append-only revision. The repository owns no database location or SQL schema.
    """

    store: AtomicRevisionStore
    serializer: StructureCatalogEntrySerializer = StructureCatalogEntrySerializer()

    def __post_init__(self) -> None:
        if not isinstance(self.store, AtomicRevisionStore):
            raise TypeError("store must implement AtomicRevisionStore")
        if type(self.serializer) is not StructureCatalogEntrySerializer:
            raise TypeError("serializer must be StructureCatalogEntrySerializer")

    def write(self, entry: StructureCatalogEntry) -> StructureCatalogWriteResult:
        """Commit one entry after observing the exact current stream head.

        Parameters
        ----------
        entry
            Complete immutable catalog entry to append or replay.

        Returns
        -------
        StructureCatalogWriteResult
            Closed commit, unchanged, conflict, or failure result.

        Raises
        ------
        TypeError
            ``entry`` is not exactly ``StructureCatalogEntry``.
        """
        if type(entry) is not StructureCatalogEntry:
            raise TypeError("entry must be StructureCatalogEntry")
        stream_id = self._stream_id(entry.identity)
        observed = self.store.read(
            RevisionReadRequest(
                request_id=f"structure-catalog-read-before-write:{entry.identity}",
                stream_id=stream_id,
                selector=RevisionSelector.LATEST,
            )
        )
        if observed.status not in {RevisionReadStatus.FOUND, RevisionReadStatus.ABSENT}:
            return StructureCatalogWriteResult(
                StructureCatalogWriteStatus.FAILED,
                entry.identity,
                None,
                observed.diagnostics,
            )
        payload = self.serializer.serialize(entry)
        digest = hashlib.sha256(payload).hexdigest()
        predecessor = None
        if observed.status is RevisionReadStatus.FOUND:
            assert observed.revision is not None
            predecessor = observed.revision.revision_id
            if observed.revision.content_id == f"sha256:{digest}":
                return StructureCatalogWriteResult(
                    StructureCatalogWriteStatus.UNCHANGED,
                    entry.identity,
                    predecessor,
                    (),
                )
        revision_material = (
            stream_id + "\n" + (predecessor or "") + "\nsha256:" + digest
        ).encode("utf-8")
        revision_digest = hashlib.sha256(revision_material).hexdigest()
        revision_id = f"structure-catalog-revision:sha256:{revision_digest}"
        commit = self.store.commit(
            Commit(
                expected_revision_id=predecessor,
                candidate=Revision(
                    stream_id=stream_id,
                    revision_id=revision_id,
                    predecessor_revision_id=predecessor,
                    schema_id=self.serializer.SCHEMA_ID,
                    content_id=f"sha256:{digest}",
                    payload=payload,
                ),
                idempotency_id=f"structure-catalog-write:sha256:{revision_digest}",
            )
        )
        status = (
            StructureCatalogWriteStatus.COMMITTED
            if commit.status is CommitStatus.COMMITTED
            else StructureCatalogWriteStatus.CONFLICT
            if commit.status is CommitStatus.CONFLICT
            else StructureCatalogWriteStatus.FAILED
        )
        return StructureCatalogWriteResult(
            status,
            entry.identity,
            revision_id if status is StructureCatalogWriteStatus.COMMITTED else None,
            commit.diagnostics,
        )

    def load(self, entry_identity: str) -> StructureCatalogLoadResult:
        """Load and validate the latest revision of one explicit entry stream.

        Parameters
        ----------
        entry_identity
            Nonempty exact catalog entry identity.

        Returns
        -------
        StructureCatalogLoadResult
            Closed loaded, absent, or failure result. Payload and stream identity are
            validated before a loaded entry is returned.

        Raises
        ------
        TypeError
            ``entry_identity`` is not a built-in string.
        ValueError
            ``entry_identity`` is empty.
        """
        if type(entry_identity) is not str:
            raise TypeError("entry_identity must be str")
        if not entry_identity:
            raise ValueError("entry_identity must be nonempty")
        observed = self.store.read(
            RevisionReadRequest(
                request_id=f"structure-catalog-load:{entry_identity}",
                stream_id=self._stream_id(entry_identity),
                selector=RevisionSelector.LATEST,
            )
        )
        if observed.status is RevisionReadStatus.ABSENT:
            return StructureCatalogLoadResult(
                StructureCatalogLoadStatus.ABSENT, entry_identity, None, None, ()
            )
        if observed.status is not RevisionReadStatus.FOUND:
            return StructureCatalogLoadResult(
                StructureCatalogLoadStatus.FAILED,
                entry_identity,
                None,
                None,
                observed.diagnostics,
            )
        assert observed.revision is not None
        revision = observed.revision
        if revision.schema_id != self.serializer.SCHEMA_ID:
            return StructureCatalogLoadResult(
                StructureCatalogLoadStatus.FAILED,
                entry_identity,
                revision.revision_id,
                None,
                ("unsupported structure-catalog schema",),
            )
        try:
            entry = self.serializer.deserialize(revision.payload)
        except (TypeError, ValueError) as error:
            return StructureCatalogLoadResult(
                StructureCatalogLoadStatus.FAILED,
                entry_identity,
                revision.revision_id,
                None,
                (str(error),),
            )
        if entry.identity != entry_identity:
            return StructureCatalogLoadResult(
                StructureCatalogLoadStatus.FAILED,
                entry_identity,
                revision.revision_id,
                None,
                ("stored entry identity does not match stream identity",),
            )
        return StructureCatalogLoadResult(
            StructureCatalogLoadStatus.LOADED,
            entry_identity,
            revision.revision_id,
            entry,
            (),
        )

    @staticmethod
    def _stream_id(entry_identity: str) -> str:
        return f"ksdft2effmass.structure-catalog:{entry_identity}"
