"""Typed controls for the periodic-1D higher-rank alignment family."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import ClassVar, Self

from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
    EndpointSewingAction,
    FrameRotationAction,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.protocol import (
    CIRCUIT_DEPTHS as PROTOCOL_CIRCUIT_DEPTHS,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.protocol import (
    CONSTRUCTION_MESH_SIZES as PROTOCOL_CONSTRUCTION_MESH_SIZES,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.protocol import (
    RETAINED_RANKS as PROTOCOL_RETAINED_RANKS,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ...geometry import Periodic1DReducedCoordinateConvention


def _decoded_integer_tuple(
    value: SerializableValue,
    name: str,
) -> tuple[int, ...]:
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must decode to a tuple")
    decoded: list[int] = []
    for entry in value:
        if type(entry) is not int:
            raise TypeError(f"{name} must decode to built-in integers")
        decoded.append(entry)
    return tuple(decoded)


@dataclass(frozen=True, slots=True)
class Periodic1DRankNAlignmentConfiguration(
    BaseTypedRecord,
    Periodic1DReducedCoordinateConvention,
):
    """Store the fixed numerical design of the higher-rank alignment study.

    Parameters
    ----------
    family_identity, version_identity
        Nonempty built-in strings fixed by the version-one protocol.
    retained_ranks
        Exact tuple ``(3, 4, 8, 16)`` of unitless retained-subspace dimensions.
    circuit_depths
        Exact tuple ``(1, 2, 4, 8)`` of unitless synthetic-gauge depths.
    construction_mesh_sizes
        Exact tuple ``(513, 1025, 2049)`` of point counts on the unshifted periodic
        construction meshes.
    final_construction_mesh_size
        Built-in integer point count ``2049`` for the final construction mesh.
    global_unitary_selection_mesh_size
        Built-in integer point count ``2049`` on which the one global right-unitary is
        selected. Selection is not repeated on the evaluation mesh.
    evaluation_mesh_size
        Built-in integer point count ``8191`` for shifted direct evaluation.
    evaluation_shift_numerator, evaluation_shift_denominator
        Built-in integers ``1`` and ``2`` defining the half-step evaluation shift.
    gauge_alignments
        Exact ordered tuple of the four prescribed gauge alignments.
    frame_rotation_action
        Right action on retained-frame columns.
    endpoint_sewing_action
        Left action on the ordered ambient basis.
    principal_phase_branch
        Principal phase interval ``(-pi, pi]``.
    rank_cutoff_rule
        Maximum-rule singular-value cutoff.
    rank_absolute_tolerance, rank_relative_tolerance
        Unitless built-in binary64 controls ``1e-12`` and ``1e-10``.
    backend_validation_absolute_tolerance, backend_validation_relative_tolerance
        Unitless built-in binary64 controls ``1e-12`` and ``1e-10`` used for backend
        matrix-identity checks.
    endpoint_and_primitive_closure_tolerance
        Unitless normalized-Frobenius threshold ``1e-11``.
    maximum_closure_phase_tolerance
        Built-in binary64 angular threshold ``1e-10`` radians.

    Notes
    -----
    Python integers do not overflow. Numeric fields reject booleans, numeric strings,
    nonfinite floats, and values outside the frozen inventories. Binary64 tolerances are
    serialized exactly as supplied and must equal the declared constants.
    """

    family_identity: str
    version_identity: str
    retained_ranks: tuple[int, ...]
    circuit_depths: tuple[int, ...]
    construction_mesh_sizes: tuple[int, ...]
    final_construction_mesh_size: int
    global_unitary_selection_mesh_size: int
    evaluation_mesh_size: int
    evaluation_shift_numerator: int
    evaluation_shift_denominator: int
    gauge_alignments: tuple[Periodic1DRankNGaugeAlignment, ...]
    frame_rotation_action: FrameRotationAction
    endpoint_sewing_action: EndpointSewingAction
    principal_phase_branch: ClosedLoopPolarFrameTransportPrincipalPhaseBranch
    rank_cutoff_rule: ComplexUnitaryProcrustesRankCutoffRule
    rank_absolute_tolerance: float
    rank_relative_tolerance: float
    backend_validation_absolute_tolerance: float
    backend_validation_relative_tolerance: float
    endpoint_and_primitive_closure_tolerance: float
    maximum_closure_phase_tolerance: float

    FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.campaign.periodic-reduction.periodic1d."
        "higher-rank-composite-band-alignment-and-locality"
    )
    VERSION_IDENTITY: ClassVar[str] = f"{FAMILY_IDENTITY}.v1"
    RETAINED_RANKS: ClassVar[tuple[int, ...]] = PROTOCOL_RETAINED_RANKS
    CIRCUIT_DEPTHS: ClassVar[tuple[int, ...]] = PROTOCOL_CIRCUIT_DEPTHS
    CONSTRUCTION_MESH_SIZES: ClassVar[tuple[int, ...]] = (
        PROTOCOL_CONSTRUCTION_MESH_SIZES
    )
    FINAL_CONSTRUCTION_MESH_SIZE: ClassVar[int] = 2049
    GLOBAL_UNITARY_SELECTION_MESH_SIZE: ClassVar[int] = 2049
    EVALUATION_MESH_SIZE: ClassVar[int] = 8191
    EVALUATION_SHIFT_NUMERATOR: ClassVar[int] = 1
    EVALUATION_SHIFT_DENOMINATOR: ClassVar[int] = 2
    GAUGE_ALIGNMENTS: ClassVar[tuple[Periodic1DRankNGaugeAlignment, ...]] = (
        Periodic1DRankNGaugeAlignment.IDENTITY,
        Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
        Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
        Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
    )
    RANK_CUTOFF_RULE: ClassVar[ComplexUnitaryProcrustesRankCutoffRule] = (
        ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM
    )
    RANK_ABSOLUTE_TOLERANCE: ClassVar[float] = 1.0e-12
    RANK_RELATIVE_TOLERANCE: ClassVar[float] = 1.0e-10
    BACKEND_VALIDATION_ABSOLUTE_TOLERANCE: ClassVar[float] = 1.0e-12
    BACKEND_VALIDATION_RELATIVE_TOLERANCE: ClassVar[float] = 1.0e-10
    ENDPOINT_AND_PRIMITIVE_CLOSURE_TOLERANCE: ClassVar[float] = 1.0e-11
    MAXIMUM_CLOSURE_PHASE_TOLERANCE: ClassVar[float] = 1.0e-10

    def __post_init__(self) -> None:
        """Reject alternate protocol identities, inventories, and conventions."""
        if type(self.family_identity) is not str:
            raise TypeError("family_identity must be a built-in string")
        if type(self.version_identity) is not str:
            raise TypeError("version_identity must be a built-in string")
        if self.family_identity != self.FAMILY_IDENTITY:
            raise ValueError("family_identity must match the frozen higher-rank family")
        if self.version_identity != self.VERSION_IDENTITY:
            raise ValueError(
                "version_identity must match the frozen version-one family"
            )

        for values, name in (
            (self.retained_ranks, "retained_ranks"),
            (self.circuit_depths, "circuit_depths"),
            (self.construction_mesh_sizes, "construction_mesh_sizes"),
        ):
            if type(values) is not tuple or any(
                type(value) is not int for value in values
            ):
                raise TypeError(f"{name} must be an exact tuple of built-in integers")
        if self.retained_ranks != self.RETAINED_RANKS:
            raise ValueError("retained_ranks must match the frozen rank inventory")
        if self.circuit_depths != self.CIRCUIT_DEPTHS:
            raise ValueError("circuit_depths must match the frozen depth inventory")
        if self.construction_mesh_sizes != self.CONSTRUCTION_MESH_SIZES:
            raise ValueError(
                "construction_mesh_sizes must match the frozen refinement inventory"
            )
        if any(size <= 0 or size % 2 != 1 for size in self.construction_mesh_sizes):
            raise ValueError("every construction mesh size must be positive and odd")

        for value, name in (
            (self.final_construction_mesh_size, "final_construction_mesh_size"),
            (
                self.global_unitary_selection_mesh_size,
                "global_unitary_selection_mesh_size",
            ),
            (self.evaluation_mesh_size, "evaluation_mesh_size"),
            (self.evaluation_shift_numerator, "evaluation_shift_numerator"),
            (self.evaluation_shift_denominator, "evaluation_shift_denominator"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
        if self.final_construction_mesh_size != self.FINAL_CONSTRUCTION_MESH_SIZE:
            raise ValueError("final construction mesh size must equal 2049")
        if self.final_construction_mesh_size != self.construction_mesh_sizes[-1]:
            raise ValueError("final construction mesh must be the last refinement mesh")
        if (
            self.global_unitary_selection_mesh_size
            != self.GLOBAL_UNITARY_SELECTION_MESH_SIZE
        ):
            raise ValueError("global-unitary selection mesh size must equal 2049")
        if self.global_unitary_selection_mesh_size != self.final_construction_mesh_size:
            raise ValueError(
                "global-unitary selection mesh must be the final construction mesh"
            )
        if self.evaluation_mesh_size != self.EVALUATION_MESH_SIZE:
            raise ValueError("evaluation mesh size must equal 8191")
        if self.evaluation_mesh_size % 2 != 1:
            raise ValueError("evaluation mesh size must be odd")
        if (
            self.evaluation_shift_numerator != self.EVALUATION_SHIFT_NUMERATOR
            or self.evaluation_shift_denominator != self.EVALUATION_SHIFT_DENOMINATOR
        ):
            raise ValueError("evaluation shift must equal the frozen half step")

        if type(self.gauge_alignments) is not tuple or any(
            type(gauge_alignment) is not Periodic1DRankNGaugeAlignment
            for gauge_alignment in self.gauge_alignments
        ):
            raise TypeError("gauge_alignments must contain exact gauge-alignment enums")
        if self.gauge_alignments != self.GAUGE_ALIGNMENTS:
            raise ValueError("gauge_alignments must match the frozen scientific order")
        if type(self.frame_rotation_action) is not FrameRotationAction:
            raise TypeError("frame_rotation_action must be FrameRotationAction")
        if self.frame_rotation_action is not FrameRotationAction.RIGHT:
            raise ValueError("higher-rank frame rotations must act on the right")
        if type(self.endpoint_sewing_action) is not EndpointSewingAction:
            raise TypeError("endpoint_sewing_action must be EndpointSewingAction")
        if self.endpoint_sewing_action is not EndpointSewingAction.LEFT_AMBIENT:
            raise ValueError("endpoint sewing must act on the left ambient space")
        if type(self.principal_phase_branch) is not (
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch
        ):
            raise TypeError(
                "principal_phase_branch must be the PhysKit transport branch enum"
            )
        if self.principal_phase_branch is not (
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
        ):
            raise ValueError("higher-rank closure phases must use the (-pi, pi] branch")
        if type(self.rank_cutoff_rule) is not ComplexUnitaryProcrustesRankCutoffRule:
            raise TypeError("rank_cutoff_rule must be the exact Optimization enum")
        if self.rank_cutoff_rule is not self.RANK_CUTOFF_RULE:
            raise ValueError("higher-rank numerical rank must use the maximum rule")

        for tolerance_value, name in (
            (self.rank_absolute_tolerance, "rank_absolute_tolerance"),
            (self.rank_relative_tolerance, "rank_relative_tolerance"),
            (
                self.backend_validation_absolute_tolerance,
                "backend_validation_absolute_tolerance",
            ),
            (
                self.backend_validation_relative_tolerance,
                "backend_validation_relative_tolerance",
            ),
            (
                self.endpoint_and_primitive_closure_tolerance,
                "endpoint_and_primitive_closure_tolerance",
            ),
            (
                self.maximum_closure_phase_tolerance,
                "maximum_closure_phase_tolerance",
            ),
        ):
            if type(tolerance_value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not isfinite(tolerance_value) or tolerance_value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        expected_tolerances = (
            self.RANK_ABSOLUTE_TOLERANCE,
            self.RANK_RELATIVE_TOLERANCE,
            self.BACKEND_VALIDATION_ABSOLUTE_TOLERANCE,
            self.BACKEND_VALIDATION_RELATIVE_TOLERANCE,
            self.ENDPOINT_AND_PRIMITIVE_CLOSURE_TOLERANCE,
            self.MAXIMUM_CLOSURE_PHASE_TOLERANCE,
        )
        actual_tolerances = (
            self.rank_absolute_tolerance,
            self.rank_relative_tolerance,
            self.backend_validation_absolute_tolerance,
            self.backend_validation_relative_tolerance,
            self.endpoint_and_primitive_closure_tolerance,
            self.maximum_closure_phase_tolerance,
        )
        if actual_tolerances != expected_tolerances:
            raise ValueError("alignment tolerances must match the frozen protocol")

    @property
    def case_order(self) -> tuple[str, ...]:
        """Return the frozen rank-major, depth-minor case inventory."""
        return tuple(
            f"r{rank:02d}-L{depth:02d}"
            for rank in self.retained_ranks
            for depth in self.circuit_depths
        )

    def ambient_dimension(self, retained_rank: int) -> int:
        """Return the protocol ambient dimension for one selected retained rank."""
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank not in self.retained_ranks:
            raise ValueError("retained_rank is not in the frozen inventory")
        return 2 * retained_rank

    def owner_transport_tolerance(self) -> ComplexUnitaryProcrustesTolerance:
        """Construct the exact unit-free Optimization transport tolerance."""
        return ComplexUnitaryProcrustesTolerance(
            rank_absolute=self.rank_absolute_tolerance,
            rank_relative=self.rank_relative_tolerance,
            validation_absolute=self.backend_validation_absolute_tolerance,
            validation_relative=self.backend_validation_relative_tolerance,
            rank_cutoff_rule=self.rank_cutoff_rule,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "family_identity": self.family_identity,
            "version_identity": self.version_identity,
            "retained_ranks": self.retained_ranks,
            "circuit_depths": self.circuit_depths,
            "construction_mesh_sizes": self.construction_mesh_sizes,
            "final_construction_mesh_size": self.final_construction_mesh_size,
            "global_unitary_selection_mesh_size": (
                self.global_unitary_selection_mesh_size
            ),
            "evaluation_mesh_size": self.evaluation_mesh_size,
            "evaluation_shift_numerator": self.evaluation_shift_numerator,
            "evaluation_shift_denominator": self.evaluation_shift_denominator,
            "gauge_alignments": tuple(
                gauge_alignment.to_wire()
                for gauge_alignment in self.gauge_alignments
            ),
            "frame_rotation_action": self.frame_rotation_action.value,
            "endpoint_sewing_action": self.endpoint_sewing_action.value,
            "principal_phase_branch": self.principal_phase_branch.value,
            "rank_cutoff_rule": self.rank_cutoff_rule.value,
            "rank_absolute_tolerance": self.rank_absolute_tolerance,
            "rank_relative_tolerance": self.rank_relative_tolerance,
            "backend_validation_absolute_tolerance": (
                self.backend_validation_absolute_tolerance
            ),
            "backend_validation_relative_tolerance": (
                self.backend_validation_relative_tolerance
            ),
            "endpoint_and_primitive_closure_tolerance": (
                self.endpoint_and_primitive_closure_tolerance
            ),
            "maximum_closure_phase_tolerance": (self.maximum_closure_phase_tolerance),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "family_identity",
            "version_identity",
            "retained_ranks",
            "circuit_depths",
            "construction_mesh_sizes",
            "final_construction_mesh_size",
            "global_unitary_selection_mesh_size",
            "evaluation_mesh_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
            "gauge_alignments",
            "frame_rotation_action",
            "endpoint_sewing_action",
            "principal_phase_branch",
            "rank_cutoff_rule",
            "rank_absolute_tolerance",
            "rank_relative_tolerance",
            "backend_validation_absolute_tolerance",
            "backend_validation_relative_tolerance",
            "endpoint_and_primitive_closure_tolerance",
            "maximum_closure_phase_tolerance",
        }
        if set(values) != required:
            raise ValueError("higher-rank alignment configuration fields do not match")

        family_identity = values["family_identity"]
        version_identity = values["version_identity"]
        if type(family_identity) is not str or type(version_identity) is not str:
            raise TypeError("family and version identities must decode to strings")

        retained_ranks = _decoded_integer_tuple(
            values["retained_ranks"], "retained_ranks"
        )
        circuit_depths = _decoded_integer_tuple(
            values["circuit_depths"], "circuit_depths"
        )
        construction_mesh_sizes = _decoded_integer_tuple(
            values["construction_mesh_sizes"], "construction_mesh_sizes"
        )
        gauge_alignment_values = values["gauge_alignments"]
        if not isinstance(gauge_alignment_values, tuple):
            raise TypeError("gauge_alignments must decode to a tuple")
        gauge_alignments: list[Periodic1DRankNGaugeAlignment] = []
        for gauge_alignment_value in gauge_alignment_values:
            if type(gauge_alignment_value) is not str:
                raise TypeError("gauge alignments must decode to strings")
            gauge_alignments.append(
                Periodic1DRankNGaugeAlignment.from_wire(gauge_alignment_value)
            )

        integer_names = (
            "final_construction_mesh_size",
            "global_unitary_selection_mesh_size",
            "evaluation_mesh_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
        )
        integers: dict[str, int] = {}
        for name in integer_names:
            value = values[name]
            if type(value) is not int:
                raise TypeError(f"{name} must decode to a built-in integer")
            integers[name] = value

        float_names = (
            "rank_absolute_tolerance",
            "rank_relative_tolerance",
            "backend_validation_absolute_tolerance",
            "backend_validation_relative_tolerance",
            "endpoint_and_primitive_closure_tolerance",
            "maximum_closure_phase_tolerance",
        )
        floats: dict[str, float] = {}
        for name in float_names:
            value = values[name]
            if type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float")
            floats[name] = value

        frame_rotation_action = values["frame_rotation_action"]
        endpoint_sewing_action = values["endpoint_sewing_action"]
        principal_phase_branch = values["principal_phase_branch"]
        rank_cutoff_rule = values["rank_cutoff_rule"]
        if (
            type(frame_rotation_action) is not str
            or type(endpoint_sewing_action) is not str
            or type(principal_phase_branch) is not str
            or type(rank_cutoff_rule) is not str
        ):
            raise TypeError(
                "owner action, branch, and cutoff-rule values must decode to strings"
            )
        return cls(
            family_identity=family_identity,
            version_identity=version_identity,
            retained_ranks=retained_ranks,
            circuit_depths=circuit_depths,
            construction_mesh_sizes=construction_mesh_sizes,
            final_construction_mesh_size=integers["final_construction_mesh_size"],
            global_unitary_selection_mesh_size=integers[
                "global_unitary_selection_mesh_size"
            ],
            evaluation_mesh_size=integers["evaluation_mesh_size"],
            evaluation_shift_numerator=integers["evaluation_shift_numerator"],
            evaluation_shift_denominator=integers["evaluation_shift_denominator"],
            gauge_alignments=tuple(gauge_alignments),
            frame_rotation_action=FrameRotationAction(frame_rotation_action),
            endpoint_sewing_action=EndpointSewingAction(endpoint_sewing_action),
            principal_phase_branch=(
                ClosedLoopPolarFrameTransportPrincipalPhaseBranch(
                    principal_phase_branch
                )
            ),
            rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule(rank_cutoff_rule),
            rank_absolute_tolerance=floats["rank_absolute_tolerance"],
            rank_relative_tolerance=floats["rank_relative_tolerance"],
            backend_validation_absolute_tolerance=floats[
                "backend_validation_absolute_tolerance"
            ],
            backend_validation_relative_tolerance=floats[
                "backend_validation_relative_tolerance"
            ],
            endpoint_and_primitive_closure_tolerance=floats[
                "endpoint_and_primitive_closure_tolerance"
            ],
            maximum_closure_phase_tolerance=floats["maximum_closure_phase_tolerance"],
        )


__all__ = ["Periodic1DRankNAlignmentConfiguration"]
