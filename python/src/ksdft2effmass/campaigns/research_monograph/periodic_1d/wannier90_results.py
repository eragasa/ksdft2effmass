"""Typed Wilson-loop and center outcomes from retained Appendix G Wannier90 results."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifactIdentity
from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.solid_state import (
    WilsonCenterConvention1D,
    WilsonLoopPhaseSetComparator1D,
    WilsonLoopPhaseSetComparisonResult1D,
    WilsonLoopSpectrum1D,
    WilsonLoopSpectrumCanonicalizer1D,
)

from .result_documents import (
    Periodic1DJsonObject,
    Periodic1DRetainedResultDocument,
    Periodic1DRetainedResultJsonSerializer,
    Periodic1DRetainedResultKind,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90WilsonGroupResult:
    """Retain direct Wilson phases and their comparison with Wannier90 centers.

    The candidate phase spectrum is obtained only from the active first coordinate of
    each retained Wannier90 center.  Inactive coordinates remain retained explicitly;
    they are not silently pooled into the one-dimensional comparison.
    """

    group_id: str
    band_indices: tuple[int, ...]
    direct_spectrum: WilsonLoopSpectrum1D
    direct_centers_over_period: tuple[float, ...]
    wannier90_centers_cell_coordinates: tuple[tuple[float, float, float], ...]
    center_phase_comparison: WilsonLoopPhaseSetComparisonResult1D
    recorded_center_set_circular_maximum_defect: float
    artifact_identities: tuple[Wannier90NativeArtifactIdentity, ...]
    localization_status: str
    convergence_criterion_satisfied: bool

    def __post_init__(self) -> None:
        """Validate ranks, center conventions, comparison correlation, and status."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if (
            not isinstance(self.band_indices, tuple)
            or not self.band_indices
            or any(type(index) is not int or index < 0 for index in self.band_indices)
        ):
            raise ValueError(
                "band_indices must be a nonempty tuple of nonnegative ints"
            )
        if type(self.direct_spectrum) is not WilsonLoopSpectrum1D:
            raise TypeError("direct_spectrum must be WilsonLoopSpectrum1D")
        rank = len(self.band_indices)
        if self.direct_spectrum.rank != rank:
            raise ValueError(
                "direct Wilson spectrum rank must equal retained band count"
            )
        if (
            not isinstance(self.direct_centers_over_period, tuple)
            or len(self.direct_centers_over_period) != rank
            or any(
                type(center) is not float or not np.isfinite(center)
                for center in self.direct_centers_over_period
            )
        ):
            raise ValueError("direct centers must be a finite built-in float tuple")
        expected_direct = self.direct_spectrum.centers_over_period(
            WilsonCenterConvention1D.PHASE_OVER_TWO_PI
        )
        if not np.allclose(
            self.direct_centers_over_period,
            expected_direct,
            rtol=0.0,
            atol=1.0e-15,
        ):
            raise ValueError("direct centers do not agree with the phase convention")
        if (
            not isinstance(self.wannier90_centers_cell_coordinates, tuple)
            or len(self.wannier90_centers_cell_coordinates) != rank
            or any(
                not isinstance(center, tuple)
                or len(center) != 3
                or any(
                    type(value) is not float or not np.isfinite(value)
                    for value in center
                )
                for center in self.wannier90_centers_cell_coordinates
            )
        ):
            raise ValueError("Wannier90 centers must be finite Cartesian triples")
        if (
            type(self.center_phase_comparison)
            is not WilsonLoopPhaseSetComparisonResult1D
        ):
            raise TypeError("center_phase_comparison uses the wrong ResultObject")
        if self.center_phase_comparison.reference != self.direct_spectrum:
            raise ValueError("center comparison reference must be the direct spectrum")
        if (
            type(self.recorded_center_set_circular_maximum_defect) is not float
            or not np.isfinite(self.recorded_center_set_circular_maximum_defect)
            or self.recorded_center_set_circular_maximum_defect < 0.0
        ):
            raise ValueError("recorded center defect must be finite and nonnegative")
        reconstructed_center_defect = (
            self.center_phase_comparison.maximum_absolute_phase_defect / (2.0 * np.pi)
        )
        if not np.isclose(
            reconstructed_center_defect,
            self.recorded_center_set_circular_maximum_defect,
            rtol=0.0,
            atol=1.0e-15,
        ):
            raise ValueError(
                "recorded center defect does not match circular comparison"
            )
        if (
            not isinstance(self.artifact_identities, tuple)
            or not self.artifact_identities
            or any(
                type(identity) is not Wannier90NativeArtifactIdentity
                for identity in self.artifact_identities
            )
        ):
            raise TypeError("artifact_identities must be a nonempty typed tuple")
        artifact_names = tuple(identity.name for identity in self.artifact_identities)
        if len(set(artifact_names)) != len(artifact_names):
            raise ValueError("native artifact names must be unique")
        if type(self.localization_status) is not str or not self.localization_status:
            raise ValueError("localization_status must be a nonempty built-in str")
        if type(self.convergence_criterion_satisfied) is not bool:
            raise TypeError("convergence_criterion_satisfied must be a built-in bool")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90CampaignResult:
    """Retain typed Wilson-center outcomes and one complete Wannier90 document."""

    source_document: Periodic1DRetainedResultDocument
    groups: tuple[Periodic1DWannier90WilsonGroupResult, ...]

    def __post_init__(self) -> None:
        """Validate supported source kind and unique nonempty typed group inventory."""
        if type(self.source_document) is not Periodic1DRetainedResultDocument:
            raise TypeError("source_document must be Periodic1DRetainedResultDocument")
        if self.source_document.kind not in {
            Periodic1DRetainedResultKind.WANNIER90,
            Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("source_document must be a retained Wannier90 result")
        if (
            not isinstance(self.groups, tuple)
            or not self.groups
            or any(
                type(group) is not Periodic1DWannier90WilsonGroupResult
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")
        group_ids = tuple(group.group_id for group in self.groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("Wannier90 group identifiers must be unique")


class Periodic1DWannier90ResultJsonSerializer(
    JsonCodec[Periodic1DWannier90CampaignResult, bytes]
):
    """Adapt one supported retained Wannier90 result format to typed outcomes."""

    __slots__ = ("retained",)

    canonicalizer = WilsonLoopSpectrumCanonicalizer1D()
    comparator = WilsonLoopPhaseSetComparator1D()

    def __init__(self, kind: Periodic1DRetainedResultKind) -> None:
        """Bind the adapter to original or preconditioned retained result bytes."""
        if type(kind) is not Periodic1DRetainedResultKind:
            raise TypeError("kind must be Periodic1DRetainedResultKind")
        if kind not in {
            Periodic1DRetainedResultKind.WANNIER90,
            Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("kind must identify a supported Wannier90 result")
        self.retained = Periodic1DRetainedResultJsonSerializer(kind)

    def deserialize(self, payload: bytes) -> Periodic1DWannier90CampaignResult:
        """Decode the full source and reconstruct every Wilson-center comparison."""
        document = self.retained.deserialize(payload)
        return Periodic1DWannier90CampaignResult(
            document,
            tuple(
                self.decode_group(group)
                for group in self.retained.object_array_field(document.root, "groups")
            ),
        )

    def serialize(self, value: Periodic1DWannier90CampaignResult) -> bytes:
        """Encode the complete correlated source document canonically."""
        if type(value) is not Periodic1DWannier90CampaignResult:
            raise TypeError("value must be Periodic1DWannier90CampaignResult")
        return self.retained.serialize(value.source_document)

    def decode_group(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DWannier90WilsonGroupResult:
        """Extract one direct spectrum, center inventory, and circular comparison."""
        direct_phases = self.retained.real_vector_field(
            value, "direct_wilson_eigenphases"
        )
        direct_spectrum = self.canonicalizer.execute(
            tuple(float(phase) for phase in direct_phases)
        )
        direct_centers = tuple(
            float(center)
            for center in self.retained.real_vector_field(
                value, "direct_wilson_centers_by_phase_convention"
            )
        )
        wannier90_centers = self.decode_center_coordinates(value)
        center_phase_spectrum = self.canonicalizer.execute(
            tuple(center[0] * 2.0 * np.pi for center in wannier90_centers)
        )
        recorded_defect = self.retained.real_field(
            value, "center_set_circular_maximum_defect"
        )
        comparison = self.comparator.execute(
            direct_spectrum,
            center_phase_spectrum,
            recorded_defect * 2.0 * np.pi + 1.0e-14,
        )
        return Periodic1DWannier90WilsonGroupResult(
            self.retained.string_field(value, "id"),
            self.retained.integer_tuple_field(value, "band_indices"),
            direct_spectrum,
            direct_centers,
            wannier90_centers,
            comparison,
            recorded_defect,
            tuple(
                self.decode_artifact_identity(identity)
                for identity in self.retained.object_array_field(
                    value, "artifact_identities"
                )
            ),
            self.retained.string_field(value, "localization_status"),
            self.retained.boolean_field(value, "convergence_criterion_satisfied"),
        )

    def decode_artifact_identity(
        self, value: Periodic1DJsonObject
    ) -> Wannier90NativeArtifactIdentity:
        """Decode one retained native artifact name, byte count, and digest."""
        return Wannier90NativeArtifactIdentity(
            self.retained.string_field(value, "name"),
            self.retained.integer_field(value, "bytes"),
            self.retained.string_field(value, "sha256"),
        )

    def decode_center_coordinates(
        self, value: Periodic1DJsonObject
    ) -> tuple[tuple[float, float, float], ...]:
        """Decode retained Wannier90 center triples in cell coordinates."""
        array = self.retained.array(
            value.field("centers_cell_coordinates"), "centers_cell_coordinates"
        )
        centers: list[tuple[float, float, float]] = []
        for index, item in enumerate(array.values):
            triple = self.retained.array(item, f"centers_cell_coordinates[{index}]")
            if len(triple.values) != 3:
                raise ValueError("each Wannier90 center must contain three coordinates")
            centers.append(
                (
                    self.retained.real(triple.values[0], "center.x"),
                    self.retained.real(triple.values[1], "center.y"),
                    self.retained.real(triple.values[2], "center.z"),
                )
            )
        return tuple(centers)
