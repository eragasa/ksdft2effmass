"""Exact collection of declared native ``pw.x`` output candidates."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import PurePosixPath

from ksdft2effmass.serialization import StrWireEnum
from ksdft2effmass.workflows import (
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
)

from ..contracts import (
    QeArtifactDestination,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeFileArtifactContent,
    QePreparationIdentity,
    QeProgram,
    QeTreeArtifactContent,
)
from .workspace import (
    QeWorkspaceEntryType,
    QeWorkspaceSnapshot,
    QeWorkspaceSnapshotEntry,
    QeWorkspaceSnapshotPhase,
)


class QeNativeOutputRole(StrWireEnum):
    """Closed roles represented by the initial native-output candidate manifest."""

    STDOUT = "stdout"
    STDERR = "stderr"
    NATIVE_STATE = "native_state"
    NATIVE_RESULT = "native_result"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeNativeOutputCandidateSpecification:
    """Declare one exact workspace candidate for operation/version extraction.

    Attributes
    ----------
    artifact_identity
        Exact nominal identity retained for cross-record correlation.
    role
        Closed integration-owned artifact role.
    relative_path
        Parent-free portable POSIX path relative to the workspace.
    entry_type
        Closed supported regular-file or directory kind.
    required
        Whether absence of this candidate fails native-output collection.
    """

    artifact_identity: ArtifactIdentity
    role: QeNativeOutputRole
    relative_path: QeArtifactDestination
    entry_type: QeWorkspaceEntryType
    required: bool

    def __post_init__(self) -> None:
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if type(self.role) is not QeNativeOutputRole:
            raise TypeError("role must be QeNativeOutputRole")
        if type(self.relative_path) is not QeArtifactDestination:
            raise TypeError("relative_path must be QeArtifactDestination")
        if type(self.entry_type) is not QeWorkspaceEntryType:
            raise TypeError("entry_type must be QeWorkspaceEntryType")
        if type(self.required) is not bool:
            raise TypeError("required must be a built-in bool")
        if self.role in (
            QeNativeOutputRole.STDOUT,
            QeNativeOutputRole.STDERR,
        ) and (
            not self.required
            or self.entry_type is not QeWorkspaceEntryType.REGULAR_FILE
        ):
            raise ValueError("stream candidates must be required regular files")


@dataclass(frozen=True, slots=True, kw_only=True)
class QeNativeOutputExtractionSpecification:
    """Bind explicit output candidates to one program and executable version.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    executable_configuration_identity
        Exact nominal identity retained for cross-record correlation.
    program
        Closed Quantum ESPRESSO program role.
    executable_kind
        Closed real-executable or deterministic-fixture namespace.
    program_version
        Exact admitted executable program version string.
    candidates
        Canonical immutable native-output candidate specifications.
    """

    identity: str
    executable_configuration_identity: QeExecutableConfigurationIdentity
    program: QeProgram
    executable_kind: QeExecutableKind
    program_version: str
    candidates: tuple[QeNativeOutputCandidateSpecification, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if not self.identity:
            raise ValueError("identity must not be empty")
        if (
            type(self.executable_configuration_identity)
            is not QeExecutableConfigurationIdentity
        ):
            raise TypeError(
                "executable_configuration_identity must be "
                "QeExecutableConfigurationIdentity"
            )
        if type(self.program) is not QeProgram:
            raise TypeError("program must be QeProgram")
        if type(self.executable_kind) is not QeExecutableKind:
            raise TypeError("executable_kind must be QeExecutableKind")
        if type(self.program_version) is not str:
            raise TypeError("program_version must be a built-in str")
        if not self.program_version:
            raise ValueError("program_version must not be empty")
        values = self.candidates
        if type(values) is not tuple or any(
            type(value) is not QeNativeOutputCandidateSpecification for value in values
        ):
            raise TypeError(
                "candidates must contain QeNativeOutputCandidateSpecification values"
            )
        if (
            values
            != tuple(sorted(values, key=lambda value: value.artifact_identity.value))
            or len({value.artifact_identity for value in values}) != len(values)
            or len({value.relative_path for value in values}) != len(values)
        ):
            raise ValueError(
                "candidates must be unique and sorted by artifact identity"
            )
        roles = tuple(value.role for value in values)
        if (
            roles.count(QeNativeOutputRole.STDOUT) != 1
            or roles.count(QeNativeOutputRole.STDERR) != 1
        ):
            raise ValueError(
                "specification requires exactly one stdout and stderr candidate"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class QeNativeOutputManifestEntry:
    """Represent one verified stream or native workspace candidate.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    artifact_identity
        Exact nominal identity retained for cross-record correlation.
    role
        Closed integration-owned artifact role.
    relative_path
        Parent-free portable POSIX path relative to the workspace.
    entry_type
        Closed supported regular-file or directory kind.
    content
        Closed exact file or deterministic tree content contract.
    symlink_observed
        Always false in a successful closed manifest entry.
    """

    identity: ArtifactManifestEntryIdentity
    artifact_identity: ArtifactIdentity
    role: QeNativeOutputRole
    relative_path: QeArtifactDestination
    entry_type: QeWorkspaceEntryType
    content: QeFileArtifactContent | QeTreeArtifactContent
    symlink_observed: bool

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactManifestEntryIdentity:
            raise TypeError("identity must be ArtifactManifestEntryIdentity")
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if type(self.role) is not QeNativeOutputRole:
            raise TypeError("role must be QeNativeOutputRole")
        if type(self.relative_path) is not QeArtifactDestination:
            raise TypeError("relative_path must be QeArtifactDestination")
        if type(self.entry_type) is not QeWorkspaceEntryType:
            raise TypeError("entry_type must be QeWorkspaceEntryType")
        if type(self.symlink_observed) is not bool:
            raise TypeError("symlink_observed must be a built-in bool")
        if self.symlink_observed:
            raise ValueError("verified manifest entries cannot be symlinks")
        expected_content_type = (
            QeFileArtifactContent
            if self.entry_type is QeWorkspaceEntryType.REGULAR_FILE
            else QeTreeArtifactContent
        )
        if type(self.content) is not expected_content_type:
            raise TypeError("content variant must agree with entry_type")


@dataclass(frozen=True, slots=True, kw_only=True)
class QeNativeOutputManifest:
    """Represent verified output candidates without asserting semantic availability.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    preparation_identity
        Exact nominal identity retained for cross-record correlation.
    after_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    extraction_specification_identity
        Exact nominal identity retained for cross-record correlation.
    entries
        Canonical immutable manifest-entry tuple.
    """

    identity: ArtifactManifestIdentity
    preparation_identity: QePreparationIdentity
    after_snapshot_identity: ArtifactManifestIdentity
    extraction_specification_identity: str
    entries: tuple[QeNativeOutputManifestEntry, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactManifestIdentity:
            raise TypeError("identity must be ArtifactManifestIdentity")
        if type(self.preparation_identity) is not QePreparationIdentity:
            raise TypeError("preparation_identity must be QePreparationIdentity")
        if type(self.after_snapshot_identity) is not ArtifactManifestIdentity:
            raise TypeError("after_snapshot_identity must be ArtifactManifestIdentity")
        if type(self.extraction_specification_identity) is not str:
            raise TypeError("extraction_specification_identity must be a built-in str")
        if not self.extraction_specification_identity:
            raise ValueError("extraction_specification_identity must not be empty")
        if type(self.entries) is not tuple or any(
            type(value) is not QeNativeOutputManifestEntry for value in self.entries
        ):
            raise TypeError("entries must contain QeNativeOutputManifestEntry values")
        if self.entries != tuple(
            sorted(self.entries, key=lambda value: value.artifact_identity.value)
        ) or len({value.artifact_identity for value in self.entries}) != len(
            self.entries
        ):
            raise ValueError("entries must be unique and sorted by artifact identity")
        roles = tuple(value.role for value in self.entries)
        if (
            roles.count(QeNativeOutputRole.STDOUT) != 1
            or roles.count(QeNativeOutputRole.STDERR) != 1
        ):
            raise ValueError("manifest requires exactly one stdout and stderr entry")


class QeNativeOutputCollectionFailureCode(StrWireEnum):
    """Closed native-output candidate collection failure codes."""

    NOT_AFTER_SNAPSHOT = "not_after_snapshot"
    BINDING_MISMATCH = "binding_mismatch"
    REQUIRED_CANDIDATE_MISSING = "required_candidate_missing"
    CANDIDATE_TYPE_MISMATCH = "candidate_type_mismatch"
    EMPTY_TREE = "empty_tree"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeNativeOutputCollectionFailure:
    """Represent failure to construct a verified candidate manifest.

    Attributes
    ----------
    code
        Closed failure code for this result.
    after_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    extraction_specification_identity
        Exact nominal identity retained for cross-record correlation.
    related_identity
        Exact nominal identity retained for cross-record correlation.
    """

    code: QeNativeOutputCollectionFailureCode
    after_snapshot_identity: ArtifactManifestIdentity
    extraction_specification_identity: str
    related_identity: str

    def __post_init__(self) -> None:
        if type(self.code) is not QeNativeOutputCollectionFailureCode:
            raise TypeError("code must be QeNativeOutputCollectionFailureCode")
        if type(self.after_snapshot_identity) is not ArtifactManifestIdentity:
            raise TypeError("after_snapshot_identity must be ArtifactManifestIdentity")
        for value, name in (
            (
                self.extraction_specification_identity,
                "extraction_specification_identity",
            ),
            (self.related_identity, "related_identity"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")


type QeNativeOutputCollectionResult = (
    QeNativeOutputManifest | QeNativeOutputCollectionFailure
)


@dataclass(frozen=True, slots=True)
class QeNativeOutputCollector:
    """Collect explicit operation/version candidates from a closed after-snapshot.

    Attributes
    ----------
    implementation_version
        Nonempty identity of the owning deterministic implementation.
    """

    implementation_version: str

    def __post_init__(self) -> None:
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")

    def execute(
        self,
        snapshot: QeWorkspaceSnapshot,
        specification: QeNativeOutputExtractionSpecification,
    ) -> QeNativeOutputCollectionResult:
        """Return a verified candidate manifest or a typed collection failure."""
        if type(snapshot) is not QeWorkspaceSnapshot:
            raise TypeError("snapshot must be QeWorkspaceSnapshot")
        if type(specification) is not QeNativeOutputExtractionSpecification:
            raise TypeError(
                "specification must be QeNativeOutputExtractionSpecification"
            )
        if snapshot.phase is not QeWorkspaceSnapshotPhase.AFTER:
            return self._failure(
                snapshot,
                specification,
                QeNativeOutputCollectionFailureCode.NOT_AFTER_SNAPSHOT,
                snapshot.identity.value,
            )
        if (
            snapshot.executable_configuration_identity
            != specification.executable_configuration_identity
            or snapshot.program is not specification.program
            or snapshot.executable_kind is not specification.executable_kind
            or snapshot.program_version != specification.program_version
        ):
            return self._failure(
                snapshot,
                specification,
                QeNativeOutputCollectionFailureCode.BINDING_MISMATCH,
                specification.identity,
            )
        by_path = {value.relative_path: value for value in snapshot.entries}
        entries: list[QeNativeOutputManifestEntry] = []
        for candidate in specification.candidates:
            observed = by_path.get(candidate.relative_path)
            if observed is None:
                if candidate.required:
                    return self._failure(
                        snapshot,
                        specification,
                        QeNativeOutputCollectionFailureCode.REQUIRED_CANDIDATE_MISSING,
                        candidate.artifact_identity.value,
                    )
                continue
            if observed.entry_type is not candidate.entry_type:
                return self._failure(
                    snapshot,
                    specification,
                    QeNativeOutputCollectionFailureCode.CANDIDATE_TYPE_MISMATCH,
                    candidate.artifact_identity.value,
                )
            if observed.entry_type is QeWorkspaceEntryType.REGULAR_FILE:
                content: QeFileArtifactContent | QeTreeArtifactContent = (
                    QeFileArtifactContent(observed.content_identity)
                )
                content_key = (
                    f"{observed.content_identity.algorithm}:"
                    f"{observed.content_identity.digest}:"
                    f"{observed.content_identity.byte_count}"
                )
            else:
                prefix = candidate.relative_path.value + "/"
                descendants = tuple(
                    value
                    for value in snapshot.entries
                    if value.relative_path.value.startswith(prefix)
                )
                if not descendants:
                    return self._failure(
                        snapshot,
                        specification,
                        QeNativeOutputCollectionFailureCode.EMPTY_TREE,
                        candidate.artifact_identity.value,
                    )
                tree_entries = tuple(
                    sorted(
                        (
                            self._tree_entry(candidate.relative_path, value)
                            for value in descendants
                        ),
                        key=lambda value: value.value,
                    )
                )
                tree_manifest = ArtifactManifestIdentity(
                    "qe-native-output-tree-v1:"
                    + self._framed_digest(tuple(value.value for value in tree_entries))
                )
                content = QeTreeArtifactContent(tree_manifest, tree_entries)
                content_key = tree_manifest.value
            entry_identity = ArtifactManifestEntryIdentity(
                "qe-native-output-entry-v1:"
                + self._framed_digest(
                    (
                        candidate.artifact_identity.value,
                        candidate.role.value,
                        candidate.relative_path.value,
                        candidate.entry_type.value,
                        content_key,
                        "symlink:false",
                    )
                )
            )
            entries.append(
                QeNativeOutputManifestEntry(
                    identity=entry_identity,
                    artifact_identity=candidate.artifact_identity,
                    role=candidate.role,
                    relative_path=candidate.relative_path,
                    entry_type=candidate.entry_type,
                    content=content,
                    symlink_observed=False,
                )
            )
        canonical = tuple(
            sorted(entries, key=lambda value: value.artifact_identity.value)
        )
        manifest_identity = ArtifactManifestIdentity(
            "qe-native-output-manifest-v1:"
            + self._framed_digest(
                (
                    self.implementation_version,
                    snapshot.identity.value,
                    specification.identity,
                    *(value.identity.value for value in canonical),
                )
            )
        )
        return QeNativeOutputManifest(
            identity=manifest_identity,
            preparation_identity=snapshot.preparation_identity,
            after_snapshot_identity=snapshot.identity,
            extraction_specification_identity=specification.identity,
            entries=canonical,
        )

    @staticmethod
    def _failure(
        snapshot: QeWorkspaceSnapshot,
        specification: QeNativeOutputExtractionSpecification,
        code: QeNativeOutputCollectionFailureCode,
        related: str,
    ) -> QeNativeOutputCollectionFailure:
        return QeNativeOutputCollectionFailure(
            code=code,
            after_snapshot_identity=snapshot.identity,
            extraction_specification_identity=specification.identity,
            related_identity=related,
        )

    @classmethod
    def _tree_entry(
        cls,
        root: QeArtifactDestination,
        entry: QeWorkspaceSnapshotEntry,
    ) -> ArtifactManifestEntryIdentity:
        relative = (
            PurePosixPath(entry.relative_path.value)
            .relative_to(PurePosixPath(root.value))
            .as_posix()
        )
        return ArtifactManifestEntryIdentity(
            "qe-native-output-tree-entry-v1:"
            + cls._framed_digest(
                (
                    entry.entry_type.value,
                    relative,
                    entry.content_identity.algorithm,
                    entry.content_identity.digest,
                    str(entry.content_identity.byte_count),
                )
            )
        )

    @staticmethod
    def _framed_digest(values: tuple[str, ...]) -> str:
        digest = hashlib.sha256()
        for value in values:
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
        return digest.hexdigest()
