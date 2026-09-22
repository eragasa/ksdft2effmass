"""Backend-neutral pseudopotential identity, storage, and catalog contracts.

This module separates a library source entry from each calculator-specific file that
represents it.  Artifacts are stored outside the repository by complete SHA-256
identity, while a SQLite catalog records compact metadata and relative locations.
The catalog stores no pseudopotential payload bytes and establishes neither physical
equivalence between formats nor scientific validation.

Catalog initialization and recording are explicit local filesystem operations.  They
perform no network access, download, format conversion, calculator execution, or
scientific selection.  Recording accepts only an artifact already placed at its
content-addressed location and verifies its size and SHA-256 before inserting
metadata.  Resolution returns recorded metadata; callers use
:class:`PseudopotentialArtifactVerifier` when current local-byte integrity matters.
"""

from __future__ import annotations

import hashlib
import math
import re
import sqlite3
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from urllib.parse import urlsplit

_MAX_U64 = 18_446_744_073_709_551_615
_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]{0,255}\Z", re.ASCII)
_VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,127}\Z", re.ASCII)
_ELEMENT_PATTERN = re.compile(r"[A-Z][a-z]?\Z", re.ASCII)
_FILENAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,255}\Z", re.ASCII)
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)


type SqliteScalar = None | int | float | str | bytes
"""Closed scalar representation returned by the maintained SQLite schema."""


class PseudopotentialFormalism(StrEnum):
    """Electron--ion representation formalism declared by an artifact family.

    Attributes
    ----------
    NORM_CONSERVING
        Norm-conserving pseudopotential.
    ULTRASOFT
        Ultrasoft pseudopotential.
    PAW
        Projector-augmented-wave dataset.
    """

    NORM_CONSERVING = "norm_conserving"
    ULTRASOFT = "ultrasoft"
    PAW = "paw"


class PseudopotentialRelativity(StrEnum):
    """Relativistic treatment represented by one source entry.

    Attributes
    ----------
    NONRELATIVISTIC
        No relativistic treatment is represented.
    SCALAR_RELATIVISTIC
        Scalar-relativistic effects are represented without explicit spinors.
    FULLY_RELATIVISTIC
        A spinor-capable fully relativistic representation is declared.
    """

    NONRELATIVISTIC = "nonrelativistic"
    SCALAR_RELATIVISTIC = "scalar_relativistic"
    FULLY_RELATIVISTIC = "fully_relativistic"


class PseudopotentialArtifactFormat(StrEnum):
    """Closed native file formats admitted by catalog schema version 1.

    Attributes
    ----------
    UPF2
        Unified Pseudopotential Format version 2 representation.
    PSP8
        ABINIT PSP8 norm-conserving representation.
    PSML
        Pseudopotential Markup Language representation.
    ABINIT_PAW_XML
        ABINIT-native PAW XML dataset.
    """

    UPF2 = "upf2"
    PSP8 = "psp8"
    PSML = "psml"
    ABINIT_PAW_XML = "abinit_paw_xml"


class PseudopotentialVerificationStatus(StrEnum):
    """Outcome of checking recorded metadata against current local bytes.

    Attributes
    ----------
    MATCH
        The path is a regular file with the recorded size and SHA-256.
    MISSING
        The recorded path does not exist.
    NOT_REGULAR_FILE
        The recorded path exists but is not a regular non-symlink file.
    SIZE_MISMATCH
        The current byte count differs from the recorded byte count.
    SHA256_MISMATCH
        The size agrees but the current SHA-256 differs.
    """

    MATCH = "match"
    MISSING = "missing"
    NOT_REGULAR_FILE = "not_regular_file"
    SIZE_MISMATCH = "size_mismatch"
    SHA256_MISMATCH = "sha256_mismatch"


@dataclass(frozen=True, slots=True)
class PseudopotentialSha256:
    """Represent one complete lowercase SHA-256 content identity.

    Parameters
    ----------
    digest
        Exactly 64 lowercase hexadecimal characters.
    """

    digest: str

    def __post_init__(self) -> None:
        """Validate the complete digest without reading artifact bytes."""
        if type(self.digest) is not str:
            raise TypeError("digest must be a built-in str")
        if _SHA256_PATTERN.fullmatch(self.digest) is None:
            raise ValueError("digest must be a lowercase SHA-256 value")


@dataclass(frozen=True, slots=True, kw_only=True)
class PseudopotentialCutoffHints:
    """Represent library-provided plane-wave cutoff hints in Hartree.

    Parameters
    ----------
    low_hartree
        Positive finite low-accuracy hint in Hartree.
    normal_hartree
        Positive finite routine-use hint in Hartree, not below ``low_hartree``.
    high_hartree
        Positive finite high-accuracy hint in Hartree, not below
        ``normal_hartree``.

    Notes
    -----
    Fields accept built-in :class:`float` values only.  Booleans, integers, numeric
    strings, nonfinite values, and nonpositive values are rejected.  These values are
    source-library guidance, not project convergence results or acceptance limits.
    """

    low_hartree: float
    normal_hartree: float
    high_hartree: float

    def __post_init__(self) -> None:
        """Validate exact floating-point types, finiteness, and monotone ordering."""
        for value, name in (
            (self.low_hartree, "low_hartree"),
            (self.normal_hartree, "normal_hartree"),
            (self.high_hartree, "high_hartree"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        if not self.low_hartree <= self.normal_hartree <= self.high_hartree:
            raise ValueError("cutoff hints must be ordered low <= normal <= high")


@dataclass(frozen=True, slots=True, kw_only=True)
class PseudopotentialSourceEntry:
    """Identify one element entry selected from a versioned source-library table.

    Parameters
    ----------
    identity
        Portable immutable entry identity.  It identifies the source selection, not
        equivalence of calculator parsers or resulting finite Hamiltonians.
    family
        Portable library family, such as ``"pseudodojo"``.
    release
        Exact portable library or generator release.
    exchange_correlation
        Exact portable exchange-correlation identifier, such as ``"pbe"``.
    accuracy_tier
        Exact portable source-table tier, such as ``"standard"`` or
        ``"stringent"``.
    element_symbol
        Case-sensitive chemical symbol.
    atomic_number
        Built-in integer in the inclusive range 1 through 118.
    formalism
        Declared electron--ion formalism.
    relativistic_treatment
        Declared relativistic branch.
    valence_electrons
        Positive built-in integer valence-electron count represented by the entry.
    cutoff_hints
        Optional source-library hints in Hartree.  ``None`` means that the catalog
        has no represented hint, not that zero cutoff is appropriate.
    """

    identity: str
    family: str
    release: str
    exchange_correlation: str
    accuracy_tier: str
    element_symbol: str
    atomic_number: int
    formalism: PseudopotentialFormalism
    relativistic_treatment: PseudopotentialRelativity
    valence_electrons: int
    cutoff_hints: PseudopotentialCutoffHints | None

    def __post_init__(self) -> None:
        """Validate the complete intrinsic source-entry declaration."""
        for value, name in (
            (self.identity, "identity"),
            (self.family, "family"),
            (self.exchange_correlation, "exchange_correlation"),
            (self.accuracy_tier, "accuracy_tier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} must be a portable identifier")
        if type(self.release) is not str:
            raise TypeError("release must be a built-in str")
        if _VERSION_PATTERN.fullmatch(self.release) is None:
            raise ValueError("release must be portable lexical version text")
        if type(self.element_symbol) is not str:
            raise TypeError("element_symbol must be a built-in str")
        if _ELEMENT_PATTERN.fullmatch(self.element_symbol) is None:
            raise ValueError("element_symbol must be a chemical symbol")
        if type(self.atomic_number) is not int:
            raise TypeError("atomic_number must be a built-in int")
        if not 1 <= self.atomic_number <= 118:
            raise ValueError("atomic_number must be in the inclusive range 1..118")
        if type(self.formalism) is not PseudopotentialFormalism:
            raise TypeError("formalism must be a PseudopotentialFormalism")
        if type(self.relativistic_treatment) is not PseudopotentialRelativity:
            raise TypeError(
                "relativistic_treatment must be a PseudopotentialRelativity"
            )
        if type(self.valence_electrons) is not int:
            raise TypeError("valence_electrons must be a built-in int")
        if not 1 <= self.valence_electrons <= 118:
            raise ValueError("valence_electrons must be in the inclusive range 1..118")
        if (
            self.cutoff_hints is not None
            and type(self.cutoff_hints) is not PseudopotentialCutoffHints
        ):
            raise TypeError("cutoff_hints must be PseudopotentialCutoffHints or None")


@dataclass(frozen=True, slots=True, kw_only=True)
class PseudopotentialArtifact:
    """Describe one exact native-format representation of a source entry.

    Parameters
    ----------
    source_entry_identity
        Exact :class:`PseudopotentialSourceEntry` identity represented by the file.
    content_identity
        Complete SHA-256 of the uncompressed native-format file.
    format
        Native file format.
    filename
        Portable basename retained beneath the content-addressed directory.
    byte_size
        Positive built-in integer size of the uncompressed file.
    source_url
        Absolute HTTPS acquisition URL without credentials or fragment.

    Notes
    -----
    A shared ``source_entry_identity`` relates native representations to one selected
    library entry.  It does not assert that different formats are byte-identical or
    that calculator parsers construct numerically identical operators.
    """

    source_entry_identity: str
    content_identity: PseudopotentialSha256
    format: PseudopotentialArtifactFormat
    filename: str
    byte_size: int
    source_url: str

    def __post_init__(self) -> None:
        """Validate artifact metadata without opening or acquiring the file."""
        if type(self.source_entry_identity) is not str:
            raise TypeError("source_entry_identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.source_entry_identity) is None:
            raise ValueError("source_entry_identity must be a portable identifier")
        if type(self.content_identity) is not PseudopotentialSha256:
            raise TypeError("content_identity must be a PseudopotentialSha256")
        if type(self.format) is not PseudopotentialArtifactFormat:
            raise TypeError("format must be a PseudopotentialArtifactFormat")
        if type(self.filename) is not str:
            raise TypeError("filename must be a built-in str")
        if _FILENAME_PATTERN.fullmatch(self.filename) is None:
            raise ValueError("filename must be a portable basename")
        if type(self.byte_size) is not int:
            raise TypeError("byte_size must be a built-in int")
        if not 0 < self.byte_size <= _MAX_U64:
            raise ValueError("byte_size must be in the positive u64 range")
        if type(self.source_url) is not str:
            raise TypeError("source_url must be a built-in str")
        parsed_url = urlsplit(self.source_url)
        if (
            parsed_url.scheme != "https"
            or not parsed_url.netloc
            or parsed_url.username is not None
            or parsed_url.password is not None
            or bool(parsed_url.fragment)
        ):
            raise ValueError(
                "source_url must be absolute HTTPS without credentials or fragment"
            )


@dataclass(frozen=True, slots=True)
class PseudopotentialLibraryLayout:
    """Represent deterministic roots for one external pseudopotential library.

    Parameters
    ----------
    root
        Explicit absolute root without parent traversal or control delimiters.  No
        ambient home-directory expansion is performed.

    Notes
    -----
    Public properties expose the authoritative artifact root, set-manifest root,
    schema-v1 catalog path, non-authoritative view root, and mutable incoming root.
    """

    root: Path

    def __post_init__(self) -> None:
        """Validate the explicit, non-anchor library root."""
        if not isinstance(self.root, Path):
            raise TypeError("root must be pathlib.Path")
        if not self.root.is_absolute() or ".." in self.root.parts:
            raise ValueError("root must be absolute without parent traversal")
        if self.root == Path(self.root.anchor):
            raise ValueError("root must not be a filesystem anchor")
        if any(character in self.root.as_posix() for character in "\x00\t\r\n"):
            raise ValueError("root must not contain control delimiters")

    @property
    def artifacts_root(self) -> Path:
        """Return the content-addressed artifact root without filesystem access."""
        return self.root / "artifacts" / "sha256"

    @property
    def manifests_root(self) -> Path:
        """Return the compact versioned set-manifest root."""
        return self.root / "manifests" / "sets"

    @property
    def catalog_root(self) -> Path:
        """Return the SQLite catalog directory."""
        return self.root / "catalog"

    @property
    def catalog_path(self) -> Path:
        """Return the schema-v1 SQLite catalog path."""
        return self.catalog_root / "pseudopotentials-v1.sqlite3"

    @property
    def views_root(self) -> Path:
        """Return the non-authoritative calculator-view root."""
        return self.root / "views"

    @property
    def incoming_root(self) -> Path:
        """Return the mutable staging root reserved for acquisition tooling."""
        return self.root / "incoming"


@dataclass(frozen=True, slots=True)
class PseudopotentialCatalogEntry:
    """Represent one cataloged artifact and its deterministic local location.

    Parameters
    ----------
    source_entry
        Complete source-library selection metadata.
    artifact
        Exact native-format content identity and acquisition metadata.
    local_path
        Absolute content-addressed path beneath the library artifact root.
    """

    source_entry: PseudopotentialSourceEntry
    artifact: PseudopotentialArtifact
    local_path: Path

    def __post_init__(self) -> None:
        """Validate source linkage and exact absolute path representation."""
        if type(self.source_entry) is not PseudopotentialSourceEntry:
            raise TypeError("source_entry must be a PseudopotentialSourceEntry")
        if type(self.artifact) is not PseudopotentialArtifact:
            raise TypeError("artifact must be a PseudopotentialArtifact")
        if self.source_entry.identity != self.artifact.source_entry_identity:
            raise ValueError("artifact must reference source_entry identity")
        if not isinstance(self.local_path, Path):
            raise TypeError("local_path must be pathlib.Path")
        if not self.local_path.is_absolute() or ".." in self.local_path.parts:
            raise ValueError("local_path must be absolute without parent traversal")


@dataclass(frozen=True, slots=True, kw_only=True)
class PseudopotentialArtifactVerificationResult:
    """Record current local-byte verification without scientific interpretation.

    Parameters
    ----------
    entry
        Catalog entry that supplied the expected location and identity.
    status
        Exact structural verification outcome.
    observed_byte_size
        Current byte count when a regular file was observed, otherwise ``None``.
    observed_sha256
        Current SHA-256 when size matched and hashing completed, otherwise ``None``.
    """

    entry: PseudopotentialCatalogEntry
    status: PseudopotentialVerificationStatus
    observed_byte_size: int | None
    observed_sha256: PseudopotentialSha256 | None

    def __post_init__(self) -> None:
        """Validate the status-dependent observation shape."""
        if type(self.entry) is not PseudopotentialCatalogEntry:
            raise TypeError("entry must be a PseudopotentialCatalogEntry")
        if type(self.status) is not PseudopotentialVerificationStatus:
            raise TypeError("status must be a PseudopotentialVerificationStatus")
        if self.observed_byte_size is not None:
            if type(self.observed_byte_size) is not int:
                raise TypeError("observed_byte_size must be a built-in int or None")
            if not 0 <= self.observed_byte_size <= _MAX_U64:
                raise ValueError("observed_byte_size must be in the u64 range")
        if (
            self.observed_sha256 is not None
            and type(self.observed_sha256) is not PseudopotentialSha256
        ):
            raise TypeError("observed_sha256 must be PseudopotentialSha256 or None")
        if self.status in {
            PseudopotentialVerificationStatus.MISSING,
            PseudopotentialVerificationStatus.NOT_REGULAR_FILE,
        } and (self.observed_byte_size is not None or self.observed_sha256 is not None):
            raise ValueError("unreadable statuses cannot carry byte observations")
        if self.status is PseudopotentialVerificationStatus.SIZE_MISMATCH:
            if self.observed_byte_size is None or self.observed_sha256 is not None:
                raise ValueError("size mismatch requires size and forbids a digest")
            if self.observed_byte_size == self.entry.artifact.byte_size:
                raise ValueError("size mismatch must differ from the expected size")
        if self.status in {
            PseudopotentialVerificationStatus.MATCH,
            PseudopotentialVerificationStatus.SHA256_MISMATCH,
        }:
            if self.observed_byte_size is None or self.observed_sha256 is None:
                raise ValueError("digest outcomes require size and digest observations")
            if self.observed_byte_size != self.entry.artifact.byte_size:
                raise ValueError("digest outcomes require the expected byte size")
            digest_matches = (
                self.observed_sha256 == self.entry.artifact.content_identity
            )
            if (
                self.status is PseudopotentialVerificationStatus.MATCH
                and not digest_matches
            ):
                raise ValueError("match status requires the expected SHA-256")
            if (
                self.status is PseudopotentialVerificationStatus.SHA256_MISMATCH
                and digest_matches
            ):
                raise ValueError(
                    "SHA-256 mismatch must differ from the expected digest"
                )


@dataclass(frozen=True, slots=True)
class PseudopotentialArtifactPathResolver:
    """Resolve deterministic content-addressed artifact paths without I/O."""

    def execute(
        self,
        layout: PseudopotentialLibraryLayout,
        artifact: PseudopotentialArtifact,
    ) -> Path:
        """Return ``artifacts/sha256/HH/DIGEST/FILENAME`` beneath ``layout``.

        Parameters
        ----------
        layout
            Explicit external library layout.
        artifact
            Artifact whose complete digest and filename define the path.

        Returns
        -------
        pathlib.Path
            Absolute deterministic content-addressed path.

        Raises
        ------
        TypeError
            If either argument is not its exact public contract type.
        """
        if type(layout) is not PseudopotentialLibraryLayout:
            raise TypeError("layout must be a PseudopotentialLibraryLayout")
        if type(artifact) is not PseudopotentialArtifact:
            raise TypeError("artifact must be a PseudopotentialArtifact")
        digest = artifact.content_identity.digest
        return layout.artifacts_root / digest[:2] / digest / artifact.filename


@dataclass(frozen=True, slots=True)
class PseudopotentialCatalogInitializer:
    """Create a non-destructive schema-v1 external layout and SQLite catalog.

    Notes
    -----
    Initialization creates directories and schema objects only.  It performs no
    acquisition, payload installation, format conversion, scientific selection, or
    calculator execution.  Existing schema-v1 state is retained; another represented
    schema version is rejected rather than migrated or overwritten.
    """

    SCHEMA_VERSION = 1

    def execute(
        self, layout: PseudopotentialLibraryLayout
    ) -> PseudopotentialLibraryLayout:
        """Create missing layout directories and the schema-v1 catalog.

        Parameters
        ----------
        layout
            Explicit external root and its deterministic child paths.

        Returns
        -------
        PseudopotentialLibraryLayout
            The exact supplied layout after successful initialization.

        Raises
        ------
        TypeError
            If ``layout`` is not the exact public layout type.
        ValueError
            If an existing catalog declares a different schema version.
        sqlite3.Error
            If SQLite cannot create or inspect the catalog.
        OSError
            If required directories cannot be created.
        """
        if type(layout) is not PseudopotentialLibraryLayout:
            raise TypeError("layout must be a PseudopotentialLibraryLayout")
        for directory in (
            layout.artifacts_root,
            layout.manifests_root,
            layout.catalog_root,
            layout.views_root / "quantumespresso",
            layout.views_root / "abinit",
            layout.incoming_root,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(layout.catalog_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(self._schema_sql())
            row = connection.execute(
                "SELECT value FROM catalog_metadata WHERE key = 'schema_version'"
            ).fetchone()
            if row is None or len(row) != 1 or row[0] != str(self.SCHEMA_VERSION):
                raise ValueError("catalog schema version does not equal 1")
        return layout

    @staticmethod
    def _schema_sql() -> str:
        """Return the idempotent schema-v1 SQL owned by this initializer."""
        return """
CREATE TABLE IF NOT EXISTS catalog_metadata (
    key TEXT PRIMARY KEY CHECK (length(key) > 0),
    value TEXT NOT NULL
) STRICT;

INSERT OR IGNORE INTO catalog_metadata (key, value)
VALUES ('schema_version', '1');

CREATE TABLE IF NOT EXISTS source_entries (
    identity TEXT PRIMARY KEY,
    family TEXT NOT NULL,
    release TEXT NOT NULL,
    exchange_correlation TEXT NOT NULL,
    accuracy_tier TEXT NOT NULL,
    element_symbol TEXT NOT NULL,
    atomic_number INTEGER NOT NULL CHECK (atomic_number BETWEEN 1 AND 118),
    formalism TEXT NOT NULL CHECK (
        formalism IN ('norm_conserving', 'ultrasoft', 'paw')
    ),
    relativistic_treatment TEXT NOT NULL CHECK (
        relativistic_treatment IN (
            'nonrelativistic', 'scalar_relativistic', 'fully_relativistic'
        )
    ),
    valence_electrons INTEGER NOT NULL CHECK (valence_electrons BETWEEN 1 AND 118),
    cutoff_low_hartree REAL,
    cutoff_normal_hartree REAL,
    cutoff_high_hartree REAL,
    CHECK (
        (cutoff_low_hartree IS NULL AND cutoff_normal_hartree IS NULL
            AND cutoff_high_hartree IS NULL)
        OR
        (cutoff_low_hartree > 0.0
            AND cutoff_low_hartree <= cutoff_normal_hartree
            AND cutoff_normal_hartree <= cutoff_high_hartree)
    )
) STRICT;

CREATE TABLE IF NOT EXISTS artifacts (
    sha256 TEXT PRIMARY KEY CHECK (length(sha256) = 64),
    source_entry_identity TEXT NOT NULL REFERENCES source_entries(identity),
    format TEXT NOT NULL CHECK (
        format IN ('upf2', 'psp8', 'psml', 'abinit_paw_xml')
    ),
    filename TEXT NOT NULL,
    byte_size INTEGER NOT NULL CHECK (byte_size > 0),
    source_url TEXT NOT NULL,
    relative_path TEXT NOT NULL UNIQUE,
    UNIQUE (source_entry_identity, format)
) STRICT;
"""


@dataclass(frozen=True, slots=True)
class PseudopotentialCatalogRecorder:
    """Verify and insert one already-installed artifact into the SQLite catalog.

    Parameters
    ----------
    path_resolver
        Deterministic resolver for the authoritative content-addressed location.

    Notes
    -----
    The operation is insert-only and idempotent for exact repeated metadata.  A source
    identity, artifact digest, or source-entry/format pair that already carries
    different metadata is rejected.  The operation does not copy or download bytes.
    """

    path_resolver: PseudopotentialArtifactPathResolver

    def __post_init__(self) -> None:
        """Validate the explicit location-policy dependency."""
        if type(self.path_resolver) is not PseudopotentialArtifactPathResolver:
            raise TypeError(
                "path_resolver must be a PseudopotentialArtifactPathResolver"
            )

    def execute(
        self,
        layout: PseudopotentialLibraryLayout,
        source_entry: PseudopotentialSourceEntry,
        artifact: PseudopotentialArtifact,
    ) -> PseudopotentialCatalogEntry:
        """Verify local bytes and transactionally record exact metadata.

        Parameters
        ----------
        layout
            Initialized external library layout.
        source_entry
            Source-library entry represented by ``artifact``.
        artifact
            Exact file metadata and expected content identity.

        Returns
        -------
        PseudopotentialCatalogEntry
            Recorded metadata and authoritative content-addressed location.

        Raises
        ------
        TypeError
            If an argument is not its exact public contract type.
        ValueError
            If linkage, local bytes, schema state, or an existing record conflicts.
        FileNotFoundError
            If the catalog or expected artifact file does not exist.
        sqlite3.Error
            If SQLite cannot complete the transaction.
        OSError
            If the artifact cannot be inspected or read.
        """
        if type(layout) is not PseudopotentialLibraryLayout:
            raise TypeError("layout must be a PseudopotentialLibraryLayout")
        if type(source_entry) is not PseudopotentialSourceEntry:
            raise TypeError("source_entry must be a PseudopotentialSourceEntry")
        if type(artifact) is not PseudopotentialArtifact:
            raise TypeError("artifact must be a PseudopotentialArtifact")
        if source_entry.identity != artifact.source_entry_identity:
            raise ValueError("artifact must reference source_entry identity")
        if not layout.catalog_path.is_file():
            raise FileNotFoundError("catalog must be initialized before recording")
        local_path = self.path_resolver.execute(layout, artifact)
        self._verify_expected_bytes(local_path, artifact)
        relative_path = local_path.relative_to(layout.root).as_posix()
        source_values = self._source_values(source_entry)
        artifact_values = (
            artifact.content_identity.digest,
            artifact.source_entry_identity,
            artifact.format.value,
            artifact.filename,
            artifact.byte_size,
            artifact.source_url,
            relative_path,
        )
        with sqlite3.connect(layout.catalog_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("BEGIN IMMEDIATE")
            self._require_schema(connection)
            existing_source = connection.execute(
                """SELECT identity, family, release, exchange_correlation,
                          accuracy_tier, element_symbol, atomic_number, formalism,
                          relativistic_treatment, valence_electrons,
                          cutoff_low_hartree, cutoff_normal_hartree,
                          cutoff_high_hartree
                   FROM source_entries WHERE identity = ?""",
                (source_entry.identity,),
            ).fetchone()
            if existing_source is None:
                connection.execute(
                    """INSERT INTO source_entries (
                           identity, family, release, exchange_correlation,
                           accuracy_tier, element_symbol, atomic_number, formalism,
                           relativistic_treatment, valence_electrons,
                           cutoff_low_hartree, cutoff_normal_hartree,
                           cutoff_high_hartree
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    source_values,
                )
            elif tuple(existing_source) != source_values:
                raise ValueError(
                    "source entry identity conflicts with catalog metadata"
                )
            existing_artifact = connection.execute(
                """SELECT sha256, source_entry_identity, format, filename, byte_size,
                          source_url, relative_path
                   FROM artifacts WHERE sha256 = ?""",
                (artifact.content_identity.digest,),
            ).fetchone()
            if existing_artifact is None:
                try:
                    connection.execute(
                        """INSERT INTO artifacts (
                               sha256, source_entry_identity, format, filename,
                               byte_size, source_url, relative_path
                           ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        artifact_values,
                    )
                except sqlite3.IntegrityError as error:
                    raise ValueError(
                        "source-entry and format pair conflicts with catalog artifact"
                    ) from error
            elif tuple(existing_artifact) != artifact_values:
                raise ValueError("artifact digest conflicts with catalog metadata")
        return PseudopotentialCatalogEntry(source_entry, artifact, local_path)

    @staticmethod
    def _source_values(
        source_entry: PseudopotentialSourceEntry,
    ) -> tuple[str | int | float | None, ...]:
        """Render the exact schema-v1 source row for equality and insertion."""
        if source_entry.cutoff_hints is None:
            low: float | None = None
            normal: float | None = None
            high: float | None = None
        else:
            low = source_entry.cutoff_hints.low_hartree
            normal = source_entry.cutoff_hints.normal_hartree
            high = source_entry.cutoff_hints.high_hartree
        return (
            source_entry.identity,
            source_entry.family,
            source_entry.release,
            source_entry.exchange_correlation,
            source_entry.accuracy_tier,
            source_entry.element_symbol,
            source_entry.atomic_number,
            source_entry.formalism.value,
            source_entry.relativistic_treatment.value,
            source_entry.valence_electrons,
            low,
            normal,
            high,
        )

    @staticmethod
    def _verify_expected_bytes(
        local_path: Path, artifact: PseudopotentialArtifact
    ) -> None:
        """Require regular non-symlink bytes matching size and complete SHA-256."""
        if not local_path.exists():
            raise FileNotFoundError(f"artifact is absent at {local_path}")
        if local_path.is_symlink() or not local_path.is_file():
            raise ValueError("artifact location must be a regular non-symlink file")
        observed_size = local_path.stat().st_size
        if observed_size != artifact.byte_size:
            raise ValueError("artifact byte size does not match declared metadata")
        hasher = hashlib.sha256()
        with local_path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(block)
        if hasher.hexdigest() != artifact.content_identity.digest:
            raise ValueError("artifact SHA-256 does not match declared metadata")

    @staticmethod
    def _require_schema(connection: sqlite3.Connection) -> None:
        """Require exact schema version 1 before catalog mutation."""
        try:
            row = connection.execute(
                "SELECT value FROM catalog_metadata WHERE key = 'schema_version'"
            ).fetchone()
        except sqlite3.OperationalError as error:
            raise ValueError("catalog schema is not initialized") from error
        if row is None or len(row) != 1 or row[0] != "1":
            raise ValueError("catalog schema version does not equal 1")


@dataclass(frozen=True, slots=True)
class PseudopotentialCatalogResolver:
    """Resolve exact catalog metadata by complete artifact SHA-256."""

    path_resolver: PseudopotentialArtifactPathResolver

    def __post_init__(self) -> None:
        """Validate the explicit location-policy dependency."""
        if type(self.path_resolver) is not PseudopotentialArtifactPathResolver:
            raise TypeError(
                "path_resolver must be a PseudopotentialArtifactPathResolver"
            )

    def execute(
        self,
        layout: PseudopotentialLibraryLayout,
        content_identity: PseudopotentialSha256,
    ) -> PseudopotentialCatalogEntry | None:
        """Return recorded metadata for ``content_identity`` or ``None``.

        Resolution performs no current-byte verification.  Use
        :class:`PseudopotentialArtifactVerifier` before staging an artifact into a
        scientific run.

        Parameters
        ----------
        layout
            Initialized external library layout.
        content_identity
            Complete artifact digest to resolve.

        Returns
        -------
        PseudopotentialCatalogEntry or None
            Decoded catalog entry, or ``None`` when no digest is recorded.

        Raises
        ------
        TypeError
            If an argument is not its exact public contract type.
        FileNotFoundError
            If the catalog does not exist.
        ValueError
            If schema or stored metadata violates the public contract.
        sqlite3.Error
            If SQLite cannot read the catalog.
        """
        if type(layout) is not PseudopotentialLibraryLayout:
            raise TypeError("layout must be a PseudopotentialLibraryLayout")
        if type(content_identity) is not PseudopotentialSha256:
            raise TypeError("content_identity must be a PseudopotentialSha256")
        if not layout.catalog_path.is_file():
            raise FileNotFoundError("catalog must be initialized before resolution")
        with sqlite3.connect(layout.catalog_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            self._require_schema(connection)
            row = connection.execute(
                """SELECT
                       s.identity, s.family, s.release, s.exchange_correlation,
                       s.accuracy_tier, s.element_symbol, s.atomic_number,
                       s.formalism, s.relativistic_treatment, s.valence_electrons,
                       s.cutoff_low_hartree, s.cutoff_normal_hartree,
                       s.cutoff_high_hartree,
                       a.sha256, a.format, a.filename, a.byte_size, a.source_url,
                       a.relative_path
                   FROM artifacts AS a
                   JOIN source_entries AS s
                     ON s.identity = a.source_entry_identity
                   WHERE a.sha256 = ?""",
                (content_identity.digest,),
            ).fetchone()
        if row is None:
            return None
        if len(row) != 19:
            raise ValueError("catalog row does not have schema-v1 width")
        low = self._optional_float(row[10], "cutoff_low_hartree")
        normal = self._optional_float(row[11], "cutoff_normal_hartree")
        high = self._optional_float(row[12], "cutoff_high_hartree")
        if low is None and normal is None and high is None:
            cutoff_hints: PseudopotentialCutoffHints | None = None
        elif low is not None and normal is not None and high is not None:
            cutoff_hints = PseudopotentialCutoffHints(
                low_hartree=low,
                normal_hartree=normal,
                high_hartree=high,
            )
        else:
            raise ValueError("catalog cutoff hint columns must be all null or all set")
        source_entry = PseudopotentialSourceEntry(
            identity=self._string(row[0], "identity"),
            family=self._string(row[1], "family"),
            release=self._string(row[2], "release"),
            exchange_correlation=self._string(row[3], "exchange_correlation"),
            accuracy_tier=self._string(row[4], "accuracy_tier"),
            element_symbol=self._string(row[5], "element_symbol"),
            atomic_number=self._integer(row[6], "atomic_number"),
            formalism=PseudopotentialFormalism(self._string(row[7], "formalism")),
            relativistic_treatment=PseudopotentialRelativity(
                self._string(row[8], "relativistic_treatment")
            ),
            valence_electrons=self._integer(row[9], "valence_electrons"),
            cutoff_hints=cutoff_hints,
        )
        artifact = PseudopotentialArtifact(
            source_entry_identity=source_entry.identity,
            content_identity=PseudopotentialSha256(self._string(row[13], "sha256")),
            format=PseudopotentialArtifactFormat(self._string(row[14], "format")),
            filename=self._string(row[15], "filename"),
            byte_size=self._integer(row[16], "byte_size"),
            source_url=self._string(row[17], "source_url"),
        )
        recorded_relative_path = self._string(row[18], "relative_path")
        expected_path = self.path_resolver.execute(layout, artifact)
        if recorded_relative_path != expected_path.relative_to(layout.root).as_posix():
            raise ValueError("catalog relative path is not content-address canonical")
        return PseudopotentialCatalogEntry(source_entry, artifact, expected_path)

    @staticmethod
    def _require_schema(connection: sqlite3.Connection) -> None:
        """Require exact schema version 1 before catalog resolution."""
        try:
            row = connection.execute(
                "SELECT value FROM catalog_metadata WHERE key = 'schema_version'"
            ).fetchone()
        except sqlite3.OperationalError as error:
            raise ValueError("catalog schema is not initialized") from error
        if row is None or len(row) != 1 or row[0] != "1":
            raise ValueError("catalog schema version does not equal 1")

    @staticmethod
    def _string(value: SqliteScalar, name: str) -> str:
        """Decode one required built-in string from the SQLite boundary."""
        if type(value) is not str:
            raise ValueError(f"catalog {name} must be a built-in str")
        return value

    @staticmethod
    def _integer(value: SqliteScalar, name: str) -> int:
        """Decode one required built-in integer from the SQLite boundary."""
        if type(value) is not int:
            raise ValueError(f"catalog {name} must be a built-in int")
        return value

    @staticmethod
    def _optional_float(value: SqliteScalar, name: str) -> float | None:
        """Decode one nullable REAL value without accepting booleans or text."""
        if value is None:
            return None
        if type(value) is not float:
            raise ValueError(f"catalog {name} must be a built-in float or null")
        return value


@dataclass(frozen=True, slots=True)
class PseudopotentialArtifactVerifier:
    """Compare a catalog entry with current local bytes without mutation."""

    def execute(
        self, entry: PseudopotentialCatalogEntry
    ) -> PseudopotentialArtifactVerificationResult:
        """Return exact presence, size, and SHA-256 verification status.

        Parameters
        ----------
        entry
            Catalog entry containing the expected location and identity.

        Returns
        -------
        PseudopotentialArtifactVerificationResult
            Structured current-byte observation.  ``MATCH`` establishes content
            identity only, not format semantics, calculator compatibility, numerical
            verification, or scientific validity.

        Raises
        ------
        TypeError
            If ``entry`` is not the exact public catalog-entry type.
        OSError
            If a present regular file cannot be inspected or read.
        """
        if type(entry) is not PseudopotentialCatalogEntry:
            raise TypeError("entry must be a PseudopotentialCatalogEntry")
        path = entry.local_path
        if not path.exists():
            return PseudopotentialArtifactVerificationResult(
                entry=entry,
                status=PseudopotentialVerificationStatus.MISSING,
                observed_byte_size=None,
                observed_sha256=None,
            )
        if path.is_symlink() or not path.is_file():
            return PseudopotentialArtifactVerificationResult(
                entry=entry,
                status=PseudopotentialVerificationStatus.NOT_REGULAR_FILE,
                observed_byte_size=None,
                observed_sha256=None,
            )
        observed_size = path.stat().st_size
        if observed_size != entry.artifact.byte_size:
            return PseudopotentialArtifactVerificationResult(
                entry=entry,
                status=PseudopotentialVerificationStatus.SIZE_MISMATCH,
                observed_byte_size=observed_size,
                observed_sha256=None,
            )
        hasher = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(block)
        observed_identity = PseudopotentialSha256(hasher.hexdigest())
        status = (
            PseudopotentialVerificationStatus.MATCH
            if observed_identity == entry.artifact.content_identity
            else PseudopotentialVerificationStatus.SHA256_MISMATCH
        )
        return PseudopotentialArtifactVerificationResult(
            entry=entry,
            status=status,
            observed_byte_size=observed_size,
            observed_sha256=observed_identity,
        )
