"""Immutable state for one retained periodic-1D Wannier90 integration."""

from dataclasses import dataclass

from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact

from ...result_documents import Periodic1DRetainedResultKind


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactGroup:
    """Store one retained group identity and explicit native artifact bytes.

    Parameters
    ----------
    group_id
        Nonempty retained Wannier90 band-group identifier.
    artifacts
        Immutable inventory of uniquely named native Wannier90 artifacts.
    """

    group_id: str
    artifacts: tuple[Wannier90NativeArtifact, ...]

    def __post_init__(self) -> None:
        """Require a stable group identity and unique typed artifacts."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if (
            not isinstance(self.artifacts, tuple)
            or not self.artifacts
            or any(type(item) is not Wannier90NativeArtifact for item in self.artifacts)
        ):
            raise TypeError("artifacts must be a nonempty typed tuple")
        names = tuple(artifact.name for artifact in self.artifacts)
        if len(set(names)) != len(names):
            raise ValueError("native artifact names must be unique")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationModel:
    """Encapsulate retained controls, results, and explicit native artifacts.

    Parameters
    ----------
    composite_input_payload
        Nonempty immutable version-one composite campaign input bytes.
    result_payload
        Nonempty immutable retained Wannier90 result bytes.
    result_kind
        Exact retained-result variant represented by ``result_payload``.
    artifact_groups
        Explicit native artifact inventories ordered by retained band group. An empty
        tuple represents unavailable native artifacts and remains usable for retained
        campaign correlation; native verification requires a nonempty inventory.

    Notes
    -----
    The model owns immutable integration state only. Correlation, artifact parsing,
    numerical tolerances, and verification belong to separate Actionizers.
    """

    composite_input_payload: bytes
    result_payload: bytes
    result_kind: Periodic1DRetainedResultKind
    artifact_groups: tuple[Periodic1DWannier90NativeArtifactGroup, ...] = ()

    def __post_init__(self) -> None:
        """Require exact retained representations and unique artifact groups."""
        if (
            type(self.composite_input_payload) is not bytes
            or not self.composite_input_payload
        ):
            raise ValueError("composite_input_payload must be nonempty built-in bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")
        if type(self.result_kind) is not Periodic1DRetainedResultKind:
            raise TypeError("result_kind must be Periodic1DRetainedResultKind")
        if self.result_kind not in {
            Periodic1DRetainedResultKind.WANNIER90,
            Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("result_kind must identify a supported Wannier90 result")
        if not isinstance(self.artifact_groups, tuple) or any(
            type(group) is not Periodic1DWannier90NativeArtifactGroup
            for group in self.artifact_groups
        ):
            raise TypeError("artifact_groups must be a typed tuple")
        group_ids = tuple(group.group_id for group in self.artifact_groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("native artifact group identifiers must be unique")
