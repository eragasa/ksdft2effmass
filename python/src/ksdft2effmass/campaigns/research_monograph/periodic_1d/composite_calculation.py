"""Typed records for execution-local Appendix G composite-band calculations.

These immutable DataObjects and ResultObjects retain explicit calculation controls,
parent operators/eigenframes, per-group frame provenance, and established composite
outcomes. They perform no calculation, filesystem access, external execution,
scientific validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.operators import ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BandFrameAlignmentResult1D,
    BandProjectorPathResult1D,
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    PolarBandFrameTransportResult1D,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorSamples1D,
    WilsonLoopPhaseSetComparisonResult1D,
)

from .composite import (
    Periodic1DCompositeCampaignDefinition,
    Periodic1DRetainedBandGroup,
)
from .composite_results import Periodic1DCompositeBandGroupResult


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandCalculationRequest:
    """Declare one execution-local composite-band calculation.

    Every scalar tolerance is a nonnegative :class:`ScalarQuantity` with
    :class:`Unitless`. ``wilson_phase_absolute_tolerance`` is a finite nonnegative
    built-in ``float`` in radians, matching the public Wilson-spectrum contract.
    Tolerances remain separate because they govern different represented operations.
    """

    definition: Periodic1DCompositeCampaignDefinition
    duality_absolute_tolerance: ScalarQuantity
    frame_orthonormality_absolute_tolerance: ScalarQuantity
    overlap_singular_value_threshold: ScalarQuantity
    coordinate_absolute_tolerance: ScalarQuantity
    transform_reconstruction_absolute_tolerance: ScalarQuantity
    hopping_hermiticity_absolute_tolerance: ScalarQuantity
    wilson_phase_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate exact campaign ownership and explicit nonnegative tolerances."""

        if type(self.definition) is not Periodic1DCompositeCampaignDefinition:
            raise TypeError("definition must be Periodic1DCompositeCampaignDefinition")
        for name, quantity in (
            ("duality_absolute_tolerance", self.duality_absolute_tolerance),
            (
                "frame_orthonormality_absolute_tolerance",
                self.frame_orthonormality_absolute_tolerance,
            ),
            (
                "overlap_singular_value_threshold",
                self.overlap_singular_value_threshold,
            ),
            ("coordinate_absolute_tolerance", self.coordinate_absolute_tolerance),
            (
                "transform_reconstruction_absolute_tolerance",
                self.transform_reconstruction_absolute_tolerance,
            ),
            (
                "hopping_hermiticity_absolute_tolerance",
                self.hopping_hermiticity_absolute_tolerance,
            ),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(quantity.unit, Unitless):
                raise ValueError(f"{name} must be unitless")
            if quantity.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.wilson_phase_absolute_tolerance) is not float:
            raise TypeError("wilson_phase_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.wilson_phase_absolute_tolerance)
            or self.wilson_phase_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "wilson_phase_absolute_tolerance must be finite and nonnegative"
            )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeParentCalculationResult:
    """Retain training parent operators, eigenspaces, and withheld band samples."""

    mesh: CenteredUniformReciprocalMesh1D
    basis: PlaneWaveBasis1D
    parent_operators: ReciprocalOperatorSamples1D
    training_spectrum: BandSpectrumSamples1D
    parent_eigenframes: ReciprocalBandFramePath1D
    withheld_spectrum: BandSpectrumSamples1D

    def __post_init__(self) -> None:
        """Validate parent dimensions, meshes, and explicit represented correlations."""

        if type(self.mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("mesh must be CenteredUniformReciprocalMesh1D")
        if type(self.basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(self.parent_operators) is not ReciprocalOperatorSamples1D:
            raise TypeError("parent_operators must be ReciprocalOperatorSamples1D")
        if type(self.training_spectrum) is not BandSpectrumSamples1D:
            raise TypeError("training_spectrum must be BandSpectrumSamples1D")
        if type(self.parent_eigenframes) is not ReciprocalBandFramePath1D:
            raise TypeError("parent_eigenframes must be ReciprocalBandFramePath1D")
        if type(self.withheld_spectrum) is not BandSpectrumSamples1D:
            raise TypeError("withheld_spectrum must be BandSpectrumSamples1D")
        if self.parent_operators.matrix_dimension != self.basis.dimension:
            raise ValueError(
                "parent operator dimension must equal plane-wave dimension"
            )
        if self.parent_eigenframes.ambient_dimension != self.basis.dimension:
            raise ValueError(
                "parent frame ambient dimension must equal basis dimension"
            )
        if self.parent_eigenframes.rank != self.training_spectrum.band_count:
            raise ValueError("parent frame rank must equal retained spectrum width")
        if self.parent_eigenframes.mesh != self.mesh:
            raise ValueError("parent frames must use the declared training mesh")
        expected_coordinates = self.mesh.coordinates.magnitude
        for name, coordinates in (
            ("parent_operators", self.parent_operators.coordinates.magnitude),
            ("training_spectrum", self.training_spectrum.coordinates.magnitude),
        ):
            if not np.array_equal(coordinates, expected_coordinates):
                raise ValueError(f"{name} must use the complete training mesh")
        if self.withheld_spectrum.band_count != self.training_spectrum.band_count:
            raise ValueError("training and withheld spectrum widths must agree")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeBandCalculationGroupResult:
    """Retain one calculated composite group and its explicit frame provenance."""

    group: Periodic1DRetainedBandGroup
    outcome: Periodic1DCompositeBandGroupResult
    source_frames: ReciprocalBandFramePath1D
    smooth_transport: PolarBandFrameTransportResult1D
    controlled_source_frames: ReciprocalBandFramePath1D
    controlled_transport: PolarBandFrameTransportResult1D
    controlled_alignment: BandFrameAlignmentResult1D
    source_projectors: BandProjectorPathResult1D
    controlled_source_projectors: BandProjectorPathResult1D
    rough_frames: ReciprocalBandFramePath1D
    wilson_comparison: WilsonLoopPhaseSetComparisonResult1D

    def __post_init__(self) -> None:
        """Validate group identity, ranks, meshes, and transport ownership."""

        if type(self.group) is not Periodic1DRetainedBandGroup:
            raise TypeError("group must be Periodic1DRetainedBandGroup")
        if type(self.outcome) is not Periodic1DCompositeBandGroupResult:
            raise TypeError("outcome must be Periodic1DCompositeBandGroupResult")
        if self.outcome.group_id != self.group.identifier:
            raise ValueError("outcome and calculation group identifiers must agree")
        expected_indices = tuple(
            range(self.group.lower_index, self.group.upper_index + 1)
        )
        if self.outcome.band_indices != expected_indices:
            raise ValueError("outcome band indices must match the calculation group")
        for name, path in (
            ("source_frames", self.source_frames),
            ("controlled_source_frames", self.controlled_source_frames),
            ("rough_frames", self.rough_frames),
        ):
            if type(path) is not ReciprocalBandFramePath1D:
                raise TypeError(f"{name} must be ReciprocalBandFramePath1D")
            if path.rank != self.group.band_count:
                raise ValueError(f"{name} rank must equal retained group size")
        for transport_name, transport_result in (
            ("smooth_transport", self.smooth_transport),
            ("controlled_transport", self.controlled_transport),
        ):
            if type(transport_result) is not PolarBandFrameTransportResult1D:
                raise TypeError(
                    f"{transport_name} must be PolarBandFrameTransportResult1D"
                )
        if type(self.controlled_alignment) is not BandFrameAlignmentResult1D:
            raise TypeError("controlled_alignment must be BandFrameAlignmentResult1D")
        for projector_name, projector_result in (
            ("source_projectors", self.source_projectors),
            (
                "controlled_source_projectors",
                self.controlled_source_projectors,
            ),
        ):
            if type(projector_result) is not BandProjectorPathResult1D:
                raise TypeError(f"{projector_name} must be BandProjectorPathResult1D")
        if type(self.wilson_comparison) is not WilsonLoopPhaseSetComparisonResult1D:
            raise TypeError(
                "wilson_comparison must be WilsonLoopPhaseSetComparisonResult1D"
            )
        mesh = self.source_frames.mesh
        paths = (
            self.smooth_transport.transported,
            self.controlled_source_frames,
            self.controlled_transport.transported,
            self.controlled_alignment.aligned,
            self.rough_frames,
        )
        if any(path.mesh != mesh for path in paths):
            raise ValueError("all group frame paths must use the same mesh")
        if self.smooth_transport.source is not self.source_frames:
            raise ValueError("smooth transport must retain source_frames")
        if self.controlled_transport.source is not self.controlled_source_frames:
            raise ValueError(
                "controlled transport must retain controlled source frames"
            )
        if self.source_projectors.source is not self.source_frames:
            raise ValueError("source projectors must retain source_frames")
        if (
            self.controlled_source_projectors.source
            is not self.controlled_source_frames
        ):
            raise ValueError(
                "controlled source projectors must retain controlled source frames"
            )
        if self.wilson_comparison.reference != self.outcome.wilson.spectrum:
            raise ValueError("Wilson comparison reference must equal outcome spectrum")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeBandCalculationResult:
    """Retain complete execution-local parent and composite-group outcomes."""

    request: Periodic1DCompositeBandCalculationRequest
    parent: Periodic1DCompositeParentCalculationResult
    groups: tuple[Periodic1DCompositeBandCalculationGroupResult, ...]

    def __post_init__(self) -> None:
        """Validate exact request ownership and ordered calculated group coverage."""

        if type(self.request) is not Periodic1DCompositeBandCalculationRequest:
            raise TypeError("request must be Periodic1DCompositeBandCalculationRequest")
        if type(self.parent) is not Periodic1DCompositeParentCalculationResult:
            raise TypeError("parent must be Periodic1DCompositeParentCalculationResult")
        if type(self.groups) is not tuple or not self.groups:
            raise TypeError("groups must be a nonempty built-in tuple")
        if any(
            type(group) is not Periodic1DCompositeBandCalculationGroupResult
            for group in self.groups
        ):
            raise TypeError("every group must be a calculated group result")
        expected = tuple(
            group.identifier for group in self.request.definition.retained_band_groups
        )
        represented = tuple(group.group.identifier for group in self.groups)
        if represented != expected:
            raise ValueError("calculated groups must preserve definition order")
