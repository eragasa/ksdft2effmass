"""Immutable periodic-3D rank-N aggregate analysis results."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from ksdft2effmass.band_equivalence_hopping_locality.rankN.result import (
    PeriodicRankNBandEquivalenceHoppingLocalityErrorChannels,
    PeriodicRankNBandEquivalenceHoppingLocalityLocalitySummary,
    PeriodicRankNFittedAlignmentEvidence,
    PeriodicRankNPrescribedAlignmentEvidence,
    PeriodicRankNSupportSelected,
    PeriodicRankNSupportUnresolved,
)
from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentGroupIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignmentAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.base import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)
from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StrWireEnum,
)

from .policy import Periodic3DRankNBandEquivalenceHoppingLocalityPolicy
from .request import Periodic3DRankNBandEquivalenceHoppingLocalityRequest


def _nonnegative_float(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels(
    PeriodicRankNBandEquivalenceHoppingLocalityErrorChannels,
):
    """Retain rank-normalized matrix and ordered-spectrum errors."""


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary(
    PeriodicRankNBandEquivalenceHoppingLocalityLocalitySummary,
):
    """Retain normalized total, onsite, and nononsite hopping powers.

    A stored zero non-onsite power is not an exact onsite-only certificate.  The
    current producer derives this scalar by subtraction and zero clipping, which can
    suppress roundoff-scale power under the bounded baseline; see ``TD-BEL-003``.
    """


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis:
    """Retain one complete physical-metric shell consequence."""

    ordinal_shell_index: int
    metric_shell_value: int
    retained_block_count: int
    reference_shell_power: float
    comparison_shell_power: float
    reference_omitted_power: float
    comparison_omitted_power: float
    reference_total_errors: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    comparison_total_errors: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    reference_truncation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    comparison_truncation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )

    def __post_init__(self) -> None:
        for value, name in (
            (self.ordinal_shell_index, "ordinal_shell_index"),
            (self.metric_shell_value, "metric_shell_value"),
            (self.retained_block_count, "retained_block_count"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.retained_block_count == 0:
            raise ValueError("retained_block_count must be positive")
        for name, float_value in (
            ("reference_shell_power", self.reference_shell_power),
            ("comparison_shell_power", self.comparison_shell_power),
            ("reference_omitted_power", self.reference_omitted_power),
            ("comparison_omitted_power", self.comparison_omitted_power),
        ):
            _nonnegative_float(float_value, name)
        error_type = Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
        for error_value, name in (
            (self.reference_total_errors, "reference_total_errors"),
            (self.comparison_total_errors, "comparison_total_errors"),
            (self.reference_truncation_errors, "reference_truncation_errors"),
            (self.comparison_truncation_errors, "comparison_truncation_errors"),
        ):
            if type(error_value) is not error_type:
                raise TypeError(f"{name} must be the exact error-channel type")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNSupportSelected(PeriodicRankNSupportSelected):
    """Retain one minimum tolerance-satisfying metric shell."""


@dataclass(frozen=True, slots=True)
class Periodic3DRankNSupportUnresolved(PeriodicRankNSupportUnresolved):
    """Retain the unresolved support-selection error evidence."""


type Periodic3DRankNSupportSelection = (
    Periodic3DRankNSupportSelected | Periodic3DRankNSupportUnresolved
)


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision:
    """Retain support decisions for both channels and error functionals."""

    tolerance: float
    reference_matrix: Periodic3DRankNSupportSelection
    reference_ordered_spectrum: Periodic3DRankNSupportSelection
    comparison_matrix: Periodic3DRankNSupportSelection
    comparison_ordered_spectrum: Periodic3DRankNSupportSelection

    def __post_init__(self) -> None:
        _nonnegative_float(self.tolerance, "tolerance")
        admitted = (Periodic3DRankNSupportSelected, Periodic3DRankNSupportUnresolved)
        for value, name in (
            (self.reference_matrix, "reference_matrix"),
            (self.reference_ordered_spectrum, "reference_ordered_spectrum"),
            (self.comparison_matrix, "comparison_matrix"),
            (self.comparison_ordered_spectrum, "comparison_ordered_spectrum"),
        ):
            if type(value) not in admitted:
                raise TypeError(f"{name} must be one exact support outcome")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNFittedAlignmentEvidence(
    PeriodicRankNFittedAlignmentEvidence,
):
    """Retain invariant evidence for one fitted unitary alignment."""


@dataclass(frozen=True, slots=True)
class Periodic3DRankNPrescribedAlignmentEvidence(
    PeriodicRankNPrescribedAlignmentEvidence,
):
    """Identify a prescribed identity or construction-oracle alignment."""


type Periodic3DRankNAlignmentEvidence = (
    Periodic3DRankNFittedAlignmentEvidence | Periodic3DRankNPrescribedAlignmentEvidence
)


class Periodic3DRankNAlignmentInapplicabilityEnum(StrWireEnum):
    """Identify why one fitted alignment has no downstream aggregate values."""

    AGGREGATE_RANK_DEFICIENT = "aggregate-rank-deficient"
    POINTWISE_CONSTRUCTION_RANK_DEFICIENT = "pointwise-construction-rank-deficient"
    POINTWISE_EVALUATION_RANK_DEFICIENT = "pointwise-evaluation-rank-deficient"
    TRANSPORT_LINK_RANK_DEFICIENT = "transport-link-rank-deficient"


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis(
    Periodic3DGaugeAlignmentAnalysis,
):
    """Retain complete scalar evidence for one applicable alignment route."""

    identity: GaugeAlignmentAnalysisIdentity
    alignment: Periodic3DRankNGaugeAlignment
    alignment_evidence: Periodic3DRankNAlignmentEvidence
    maximum_aligned_frame_defect: float
    minimum_transport_singular_value: float
    maximum_transport_procrustes_residual: float
    maximum_transport_unitarity_defect: float
    maximum_transport_rank_cutoff: float
    maximum_absolute_closure_phases: tuple[float, ...]
    maximum_plaquette_phase: float
    maximum_direct_matrix_difference: float
    maximum_direct_ordered_spectrum_difference: float
    reference_reconstruction_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    comparison_reconstruction_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    reference_interpolation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    comparison_interpolation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    reference_locality: Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary
    comparison_locality: Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary
    shells: tuple[Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis, ...]
    tolerance_decisions: tuple[
        Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision, ...
    ]

    def __post_init__(self) -> None:
        if type(self.identity) is not GaugeAlignmentAnalysisIdentity:
            raise TypeError("identity must be the exact gauge-analysis identity")
        if type(self.alignment) is not Periodic3DRankNGaugeAlignment:
            raise TypeError("alignment must be the exact periodic-3D enum")
        if type(self.alignment_evidence) not in (
            Periodic3DRankNFittedAlignmentEvidence,
            Periodic3DRankNPrescribedAlignmentEvidence,
        ):
            raise TypeError("alignment_evidence must be one exact evidence type")
        if (
            self.alignment
            in (
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            )
        ) is not (
            type(self.alignment_evidence) is Periodic3DRankNFittedAlignmentEvidence
        ):
            raise ValueError("alignment and evidence type are inconsistent")
        for name, value in (
            ("maximum_aligned_frame_defect", self.maximum_aligned_frame_defect),
            ("minimum_transport_singular_value", self.minimum_transport_singular_value),
            (
                "maximum_transport_procrustes_residual",
                self.maximum_transport_procrustes_residual,
            ),
            (
                "maximum_transport_unitarity_defect",
                self.maximum_transport_unitarity_defect,
            ),
            ("maximum_transport_rank_cutoff", self.maximum_transport_rank_cutoff),
            ("maximum_plaquette_phase", self.maximum_plaquette_phase),
            ("maximum_direct_matrix_difference", self.maximum_direct_matrix_difference),
            (
                "maximum_direct_ordered_spectrum_difference",
                self.maximum_direct_ordered_spectrum_difference,
            ),
        ):
            _nonnegative_float(value, name)
        if type(self.maximum_absolute_closure_phases) is not tuple or any(
            type(value) is not float or not math.isfinite(value) or value < 0.0
            for value in self.maximum_absolute_closure_phases
        ):
            raise TypeError("maximum_absolute_closure_phases must be finite floats")
        if not self.maximum_absolute_closure_phases:
            raise ValueError("maximum_absolute_closure_phases must be nonempty")
        error_type = Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
        for error_value, name in (
            (self.reference_reconstruction_errors, "reference_reconstruction_errors"),
            (self.comparison_reconstruction_errors, "comparison_reconstruction_errors"),
            (self.reference_interpolation_errors, "reference_interpolation_errors"),
            (self.comparison_interpolation_errors, "comparison_interpolation_errors"),
        ):
            if type(error_value) is not error_type:
                raise TypeError(f"{name} must be the exact error type")
        locality_type = Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary
        if type(self.reference_locality) is not locality_type:
            raise TypeError("reference_locality must be the exact locality type")
        if type(self.comparison_locality) is not locality_type:
            raise TypeError("comparison_locality must be the exact locality type")
        if (
            type(self.shells) is not tuple
            or not self.shells
            or any(
                type(value)
                is not Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis
                for value in self.shells
            )
        ):
            raise TypeError("shells must contain exact nonempty shell analyses")
        if tuple(shell.ordinal_shell_index for shell in self.shells) != tuple(
            range(len(self.shells))
        ):
            raise ValueError("shells must follow contiguous ordinal order")
        if type(self.tolerance_decisions) is not tuple or any(
            type(value)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision
            for value in self.tolerance_decisions
        ):
            raise TypeError("tolerance_decisions must contain exact decisions")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the explicit finite-rank gauge-analysis identity."""
        return self.identity


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
    Periodic3DGaugeAlignmentAnalysis,
):
    """Retain typed rank-deficiency evidence without downstream values."""

    identity: GaugeAlignmentAnalysisIdentity
    alignment: Periodic3DRankNGaugeAlignment
    reason: Periodic3DRankNAlignmentInapplicabilityEnum
    deficient_sample_count: int
    minimum_numerical_rank: int | None

    def __post_init__(self) -> None:
        if type(self.identity) is not GaugeAlignmentAnalysisIdentity:
            raise TypeError("identity must be the exact gauge-analysis identity")
        if type(self.alignment) is not Periodic3DRankNGaugeAlignment:
            raise TypeError("alignment must be the exact periodic-3D enum")
        if type(self.reason) is not Periodic3DRankNAlignmentInapplicabilityEnum:
            raise TypeError("reason must be the exact inapplicability enum")
        if type(self.deficient_sample_count) is not int:
            raise TypeError("deficient_sample_count must be a built-in integer")
        if self.deficient_sample_count <= 0:
            raise ValueError("deficient_sample_count must be positive")
        transport_failure = (
            self.reason
            is Periodic3DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
        )
        if transport_failure:
            if self.minimum_numerical_rank is not None:
                raise ValueError(
                    "transport-link failure has no selected alignment rank"
                )
        else:
            if self.alignment not in (
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            ):
                raise ValueError("Procrustes rank deficiency requires a fitted route")
            if type(self.minimum_numerical_rank) is not int:
                raise TypeError("minimum_numerical_rank must be a built-in integer")
            if self.minimum_numerical_rank < 0:
                raise ValueError("minimum_numerical_rank must be nonnegative")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the explicit finite-rank gauge-analysis identity."""
        return self.identity


type Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis = (
    Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
    | Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
)


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalysis(
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue
):
    """Retain generic analysis results for one pair of represented field channels."""

    policy: Periodic3DRankNBandEquivalenceHoppingLocalityPolicy
    geometry_identifier: str
    retained_rank: int
    operator_identifier: str
    energy_reference: str
    energy_unit: str
    basis_identifier: str
    alignments: tuple[
        Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis, ...
    ]

    @property
    def band_subspace_rank(self) -> int:
        """Return the represented field rank."""
        return self.retained_rank

    def __post_init__(self) -> None:
        if type(self.policy) is not Periodic3DRankNBandEquivalenceHoppingLocalityPolicy:
            raise TypeError("policy must be the exact periodic-3D rank-N policy")
        if type(self.geometry_identifier) is not str:
            raise TypeError("geometry_identifier must be a built-in string")
        if not self.geometry_identifier:
            raise ValueError("geometry_identifier must be nonempty")
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        for value, name in (
            (self.operator_identifier, "operator_identifier"),
            (self.energy_reference, "energy_reference"),
            (self.energy_unit, "energy_unit"),
            (self.basis_identifier, "basis_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.alignments) is not tuple or not self.alignments:
            raise TypeError("alignments must be a nonempty tuple")
        if any(
            type(value)
            not in (
                Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
                Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
            )
            for value in self.alignments
        ):
            raise TypeError("alignments must contain exact alignment analyses")
        if any(value.retained_rank != self.retained_rank for value in self.alignments):
            raise ValueError("alignment identities must match the field retained rank")
        alignment_inventory = tuple(value.alignment for value in self.alignments)
        if len(set(alignment_inventory)) != len(alignment_inventory):
            raise ValueError("alignment routes must be unique")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis(
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue
):
    """Retain all alignment routes in the synthetic v1 case envelope."""

    @property
    def band_subspace_rank(self) -> int:
        """Return the exact case's represented band-subspace rank."""
        return self.retained_rank

    model_identity: str
    case_identifier: str
    retained_rank: int
    circuit_depth: int
    parent_scale: float
    transformation_coefficient: float
    minimum_sampled_external_gap: float
    alignments: tuple[
        Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis, ...
    ]

    def __post_init__(self) -> None:
        for string_value, name in (
            (self.model_identity, "model_identity"),
            (self.case_identifier, "case_identifier"),
        ):
            if type(string_value) is not str or not string_value:
                raise TypeError(f"{name} must be a nonempty built-in string")
        for integer_value, name in (
            (self.retained_rank, "retained_rank"),
            (self.circuit_depth, "circuit_depth"),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if integer_value <= 0:
                raise ValueError(f"{name} must be positive")
        _nonnegative_float(self.parent_scale, "parent_scale")
        _nonnegative_float(
            self.transformation_coefficient, "transformation_coefficient"
        )
        _nonnegative_float(
            self.minimum_sampled_external_gap, "minimum_sampled_external_gap"
        )
        if type(self.alignments) is not tuple or any(
            type(value)
            not in (
                Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
                Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
            )
            for value in self.alignments
        ):
            raise TypeError("alignments must contain exact alignment analyses")
        if any(value.retained_rank != self.retained_rank for value in self.alignments):
            raise ValueError("alignment identities must match the case retained rank")
        if tuple(value.alignment for value in self.alignments) != (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        ):
            raise ValueError("alignments must follow the selected four-route inventory")


class Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum(StrWireEnum):
    """Identify the claim boundary of one aggregate software analysis."""

    SOFTWARE_QUALIFICATION_NOT_SCIENTIFIC_EVIDENCE = (
        "software-qualification-not-scientific-evidence"
    )


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis(
    BaseTypedRecord,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole[
        Periodic3DRankNBandEquivalenceHoppingLocalityRequest
    ],
):
    """Retain one complete periodic-3D rank-N aggregate software analysis."""

    WIRE_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic3d-rankN-band-equivalence-hopping-locality-analysis.v1"
    )

    request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest
    status: Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum
    cases: tuple[Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis, ...]

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the analyzed band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError("request must be the exact periodic-3D rank-N request")
        if (
            type(self.status)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum
        ):
            raise TypeError("status must be the exact periodic-3D analysis-status enum")
        if type(self.cases) is not tuple or any(
            type(value) is not Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis
            for value in self.cases
        ):
            raise TypeError("cases must contain exact periodic-3D case analyses")
        if len(self.cases) != self.request.case_count:
            raise ValueError("cases must match the expanded request count")
        identities = tuple(case.model_identity for case in self.cases)
        if len(set(identities)) != len(identities):
            raise ValueError("case model identities must be unique")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "wire_identity": self.WIRE_IDENTITY,
            "request": self.request,
            "status": self.status.to_wire(),
            "cases": tuple(_case_mapping(case) for case in self.cases),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"wire_identity", "request", "status", "cases"}:
            raise ValueError("periodic-3D rank-N analysis fields do not match")
        wire_identity = values["wire_identity"]
        request = values["request"]
        status = values["status"]
        cases = values["cases"]
        if wire_identity != cls.WIRE_IDENTITY:
            raise ValueError("wire_identity must match the periodic-3D rank-N analysis")
        if not isinstance(request, Mapping):
            raise TypeError("request must decode to a mapping")
        if type(status) is not str:
            raise TypeError("status must decode to a built-in string")
        if type(cases) is not tuple or any(
            not isinstance(case, Mapping) for case in cases
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        return cls(
            request=Periodic3DRankNBandEquivalenceHoppingLocalityRequest.from_dict(
                request
            ),
            status=Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum.from_wire(
                status
            ),
            cases=tuple(_case_from_mapping(case) for case in cases),
        )


def _error_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
) -> Mapping[str, SerializableValue]:
    return {
        "maximum_matrix_frobenius": value.maximum_matrix_frobenius,
        "root_mean_square_matrix_frobenius": value.root_mean_square_matrix_frobenius,
        "maximum_ordered_spectrum": value.maximum_ordered_spectrum,
        "root_mean_square_ordered_spectrum": value.root_mean_square_ordered_spectrum,
    }


def _error_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels:
    required = {
        "maximum_matrix_frobenius",
        "root_mean_square_matrix_frobenius",
        "maximum_ordered_spectrum",
        "root_mean_square_ordered_spectrum",
    }
    if set(values) != required:
        raise TypeError("error-channel fields must be exact built-in floats")
    maximum_matrix_frobenius = values["maximum_matrix_frobenius"]
    root_mean_square_matrix_frobenius = values["root_mean_square_matrix_frobenius"]
    maximum_ordered_spectrum = values["maximum_ordered_spectrum"]
    root_mean_square_ordered_spectrum = values["root_mean_square_ordered_spectrum"]
    if (
        type(maximum_matrix_frobenius) is not float
        or type(root_mean_square_matrix_frobenius) is not float
        or type(maximum_ordered_spectrum) is not float
        or type(root_mean_square_ordered_spectrum) is not float
    ):
        raise TypeError("error-channel fields must be exact built-in floats")
    return Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels(
        maximum_matrix_frobenius=maximum_matrix_frobenius,
        root_mean_square_matrix_frobenius=root_mean_square_matrix_frobenius,
        maximum_ordered_spectrum=maximum_ordered_spectrum,
        root_mean_square_ordered_spectrum=root_mean_square_ordered_spectrum,
    )


def _locality_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary,
) -> Mapping[str, SerializableValue]:
    return {
        "total_power": value.total_power,
        "onsite_power": value.onsite_power,
        "nononsite_power": value.nononsite_power,
    }


def _locality_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary:
    required = {"total_power", "onsite_power", "nononsite_power"}
    if set(values) != required:
        raise TypeError("locality fields must be exact built-in floats")
    total_power = values["total_power"]
    onsite_power = values["onsite_power"]
    nononsite_power = values["nononsite_power"]
    if (
        type(total_power) is not float
        or type(onsite_power) is not float
        or type(nononsite_power) is not float
    ):
        raise TypeError("locality fields must be exact built-in floats")
    return Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary(
        total_power=total_power,
        onsite_power=onsite_power,
        nononsite_power=nononsite_power,
    )


def _support_mapping(
    value: Periodic3DRankNSupportSelection,
) -> Mapping[str, SerializableValue]:
    if isinstance(value, Periodic3DRankNSupportSelected):
        if type(value) is not Periodic3DRankNSupportSelected:
            raise TypeError("selected support subclasses are not admitted")
        return {
            "disposition": "selected",
            "ordinal_shell_index": value.ordinal_shell_index,
            "metric_shell_value": value.metric_shell_value,
            "satisfying_error": value.satisfying_error,
            "preceding_error": value.preceding_error,
        }
    if isinstance(value, Periodic3DRankNSupportUnresolved):
        if type(value) is not Periodic3DRankNSupportUnresolved:
            raise TypeError("unresolved support subclasses are not admitted")
        return {
            "disposition": "unresolved",
            "comparison_count": value.comparison_count,
            "minimum_observed_error": value.minimum_observed_error,
            "largest_support_error": value.largest_support_error,
        }
    raise TypeError("support selection type is not admitted")


def _support_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNSupportSelection:
    disposition = values.get("disposition")
    if disposition == "selected":
        required = {
            "disposition",
            "ordinal_shell_index",
            "metric_shell_value",
            "satisfying_error",
            "preceding_error",
        }
        if set(values) != required:
            raise ValueError("selected support fields do not match")
        ordinal = values["ordinal_shell_index"]
        metric = values["metric_shell_value"]
        error = values["satisfying_error"]
        preceding = values["preceding_error"]
        if (
            type(ordinal) is not int
            or type(metric) is not int
            or type(error) is not float
        ):
            raise TypeError("selected support fields have invalid types")
        if preceding is not None and type(preceding) is not float:
            raise TypeError("preceding_error must decode to float or None")
        return Periodic3DRankNSupportSelected(ordinal, metric, error, preceding)
    if disposition == "unresolved":
        required = {
            "disposition",
            "comparison_count",
            "minimum_observed_error",
            "largest_support_error",
        }
        if set(values) != required:
            raise ValueError("unresolved support fields do not match")
        count = values["comparison_count"]
        minimum = values["minimum_observed_error"]
        largest = values["largest_support_error"]
        if (
            type(count) is not int
            or type(minimum) is not float
            or type(largest) is not float
        ):
            raise TypeError("unresolved support fields have invalid types")
        return Periodic3DRankNSupportUnresolved(count, minimum, largest)
    raise ValueError("support disposition is not recognized")


def _shell_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis,
) -> Mapping[str, SerializableValue]:
    return {
        "ordinal_shell_index": value.ordinal_shell_index,
        "metric_shell_value": value.metric_shell_value,
        "retained_block_count": value.retained_block_count,
        "reference_shell_power": value.reference_shell_power,
        "comparison_shell_power": value.comparison_shell_power,
        "reference_omitted_power": value.reference_omitted_power,
        "comparison_omitted_power": value.comparison_omitted_power,
        "reference_total_errors": _error_mapping(value.reference_total_errors),
        "comparison_total_errors": _error_mapping(value.comparison_total_errors),
        "reference_truncation_errors": _error_mapping(
            value.reference_truncation_errors
        ),
        "comparison_truncation_errors": _error_mapping(
            value.comparison_truncation_errors
        ),
    }


def _shell_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis:
    required = {
        "ordinal_shell_index",
        "metric_shell_value",
        "retained_block_count",
        "reference_shell_power",
        "comparison_shell_power",
        "reference_omitted_power",
        "comparison_omitted_power",
        "reference_total_errors",
        "comparison_total_errors",
        "reference_truncation_errors",
        "comparison_truncation_errors",
    }
    if set(values) != required:
        raise ValueError("shell fields do not match")
    ordinal_shell_index = values["ordinal_shell_index"]
    metric_shell_value = values["metric_shell_value"]
    retained_block_count = values["retained_block_count"]
    reference_shell_power = values["reference_shell_power"]
    comparison_shell_power = values["comparison_shell_power"]
    reference_omitted_power = values["reference_omitted_power"]
    comparison_omitted_power = values["comparison_omitted_power"]
    if (
        type(ordinal_shell_index) is not int
        or type(metric_shell_value) is not int
        or type(retained_block_count) is not int
        or type(reference_shell_power) is not float
        or type(comparison_shell_power) is not float
        or type(reference_omitted_power) is not float
        or type(comparison_omitted_power) is not float
    ):
        raise TypeError("shell scalar fields have invalid types")
    reference_total_errors = values["reference_total_errors"]
    comparison_total_errors = values["comparison_total_errors"]
    reference_truncation_errors = values["reference_truncation_errors"]
    comparison_truncation_errors = values["comparison_truncation_errors"]
    if (
        not isinstance(reference_total_errors, Mapping)
        or not isinstance(comparison_total_errors, Mapping)
        or not isinstance(reference_truncation_errors, Mapping)
        or not isinstance(comparison_truncation_errors, Mapping)
    ):
        raise TypeError("shell error fields must decode to mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis(
        ordinal_shell_index=ordinal_shell_index,
        metric_shell_value=metric_shell_value,
        retained_block_count=retained_block_count,
        reference_shell_power=reference_shell_power,
        comparison_shell_power=comparison_shell_power,
        reference_omitted_power=reference_omitted_power,
        comparison_omitted_power=comparison_omitted_power,
        reference_total_errors=_error_from_mapping(reference_total_errors),
        comparison_total_errors=_error_from_mapping(comparison_total_errors),
        reference_truncation_errors=_error_from_mapping(reference_truncation_errors),
        comparison_truncation_errors=_error_from_mapping(comparison_truncation_errors),
    )


def _decision_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision,
) -> Mapping[str, SerializableValue]:
    return {
        "tolerance": value.tolerance,
        "reference_matrix": _support_mapping(value.reference_matrix),
        "reference_ordered_spectrum": _support_mapping(
            value.reference_ordered_spectrum
        ),
        "comparison_matrix": _support_mapping(value.comparison_matrix),
        "comparison_ordered_spectrum": _support_mapping(
            value.comparison_ordered_spectrum
        ),
    }


def _decision_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision:
    required = {
        "tolerance",
        "reference_matrix",
        "reference_ordered_spectrum",
        "comparison_matrix",
        "comparison_ordered_spectrum",
    }
    if set(values) != required:
        raise ValueError("tolerance-decision fields do not match")
    tolerance = values["tolerance"]
    if type(tolerance) is not float:
        raise ValueError("tolerance-decision fields do not match")
    reference_matrix = values["reference_matrix"]
    reference_ordered_spectrum = values["reference_ordered_spectrum"]
    comparison_matrix = values["comparison_matrix"]
    comparison_ordered_spectrum = values["comparison_ordered_spectrum"]
    if (
        not isinstance(reference_matrix, Mapping)
        or not isinstance(reference_ordered_spectrum, Mapping)
        or not isinstance(comparison_matrix, Mapping)
        or not isinstance(comparison_ordered_spectrum, Mapping)
    ):
        raise TypeError("support decisions must decode to mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision(
        tolerance=tolerance,
        reference_matrix=_support_from_mapping(reference_matrix),
        reference_ordered_spectrum=_support_from_mapping(reference_ordered_spectrum),
        comparison_matrix=_support_from_mapping(comparison_matrix),
        comparison_ordered_spectrum=_support_from_mapping(comparison_ordered_spectrum),
    )


def _evidence_mapping(
    value: Periodic3DRankNAlignmentEvidence,
) -> Mapping[str, SerializableValue]:
    if isinstance(value, Periodic3DRankNFittedAlignmentEvidence):
        if type(value) is not Periodic3DRankNFittedAlignmentEvidence:
            raise TypeError("fitted evidence subclasses are not admitted")
        return {
            "kind": "fitted",
            "sample_count": value.sample_count,
            "minimum_numerical_rank": value.minimum_numerical_rank,
            "minimum_cross_singular_value": value.minimum_cross_singular_value,
            "maximum_optimal_residual_frobenius_norm": (
                value.maximum_optimal_residual_frobenius_norm
            ),
            "maximum_applied_rank_cutoff": value.maximum_applied_rank_cutoff,
        }
    if isinstance(value, Periodic3DRankNPrescribedAlignmentEvidence):
        if type(value) is not Periodic3DRankNPrescribedAlignmentEvidence:
            raise TypeError("prescribed evidence subclasses are not admitted")
        return {"kind": "prescribed", "identifier": value.identifier}
    raise TypeError("alignment evidence type is not admitted")


def _evidence_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNAlignmentEvidence:
    kind = values.get("kind")
    if kind == "prescribed":
        if (
            set(values) != {"kind", "identifier"}
            or type(values["identifier"]) is not str
        ):
            raise TypeError("prescribed evidence fields have invalid types")
        return Periodic3DRankNPrescribedAlignmentEvidence(values["identifier"])
    if kind == "fitted":
        required = {
            "kind",
            "sample_count",
            "minimum_numerical_rank",
            "minimum_cross_singular_value",
            "maximum_optimal_residual_frobenius_norm",
            "maximum_applied_rank_cutoff",
        }
        if set(values) != required:
            raise ValueError("fitted evidence fields do not match")
        sample_count = values["sample_count"]
        minimum_numerical_rank = values["minimum_numerical_rank"]
        if type(sample_count) is not int or type(minimum_numerical_rank) is not int:
            raise TypeError("fitted evidence integer fields have invalid types")
        minimum_cross_singular_value = values["minimum_cross_singular_value"]
        maximum_optimal_residual_frobenius_norm = values[
            "maximum_optimal_residual_frobenius_norm"
        ]
        maximum_applied_rank_cutoff = values["maximum_applied_rank_cutoff"]
        if (
            type(minimum_cross_singular_value) is not float
            or type(maximum_optimal_residual_frobenius_norm) is not float
            or type(maximum_applied_rank_cutoff) is not float
        ):
            raise TypeError("fitted evidence float fields have invalid types")
        return Periodic3DRankNFittedAlignmentEvidence(
            sample_count=sample_count,
            minimum_numerical_rank=minimum_numerical_rank,
            minimum_cross_singular_value=minimum_cross_singular_value,
            maximum_optimal_residual_frobenius_norm=(
                maximum_optimal_residual_frobenius_norm
            ),
            maximum_applied_rank_cutoff=maximum_applied_rank_cutoff,
        )
    raise ValueError("alignment evidence kind is not recognized")


def _identity_mapping(
    value: GaugeAlignmentAnalysisIdentity,
) -> Mapping[str, SerializableValue]:
    return {
        "represented_dimension": value.gauge_group_identity.represented_dimension,
        "alignment_sample_count": value.alignment_sample_count,
        "action_convention": value.action_convention.to_wire(),
        "inner_product_convention": value.inner_product_convention.to_wire(),
    }


def _identity_from_mapping(
    values: Mapping[str, SerializableValue],
) -> GaugeAlignmentAnalysisIdentity:
    required = {
        "represented_dimension",
        "alignment_sample_count",
        "action_convention",
        "inner_product_convention",
    }
    if set(values) != required:
        raise ValueError("gauge-analysis identity fields do not match")
    represented_dimension = values["represented_dimension"]
    sample_count = values["alignment_sample_count"]
    action = values["action_convention"]
    inner_product = values["inner_product_convention"]
    if type(represented_dimension) is not int or type(sample_count) is not int:
        raise TypeError("gauge-analysis dimensions must decode to integers")
    if type(action) is not str or type(inner_product) is not str:
        raise TypeError("gauge-analysis conventions must decode to strings")
    return GaugeAlignmentAnalysisIdentity(
        gauge_group_identity=GaugeAlignmentGroupIdentity.unitary(
            represented_dimension=represented_dimension
        ),
        alignment_sample_count=sample_count,
        action_convention=GaugeAlignmentActionConvention.from_wire(action),
        inner_product_convention=GaugeAlignmentInnerProductConvention.from_wire(
            inner_product
        ),
    )


def _alignment_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis,
) -> Mapping[str, SerializableValue]:
    if isinstance(
        value,
        Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
    ):
        if (
            type(value)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis  # noqa: E501
        ):
            raise TypeError("inapplicable alignment subclasses are not admitted")
        return {
            "disposition": "inapplicable",
            "analysis_identity": _identity_mapping(value.identity),
            "alignment": value.alignment.to_wire(),
            "reason": value.reason.to_wire(),
            "deficient_sample_count": value.deficient_sample_count,
            "minimum_numerical_rank": value.minimum_numerical_rank,
        }
    if not isinstance(
        value,
        Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    ):
        raise TypeError("alignment-analysis type is not admitted")
    if (
        type(value)
        is not Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
    ):
        raise TypeError("qualified alignment subclasses are not admitted")
    return {
        "disposition": "qualified",
        "analysis_identity": _identity_mapping(value.identity),
        "alignment": value.alignment.to_wire(),
        "alignment_evidence": _evidence_mapping(value.alignment_evidence),
        "maximum_aligned_frame_defect": value.maximum_aligned_frame_defect,
        "minimum_transport_singular_value": value.minimum_transport_singular_value,
        "maximum_transport_procrustes_residual": (
            value.maximum_transport_procrustes_residual
        ),
        "maximum_transport_unitarity_defect": value.maximum_transport_unitarity_defect,
        "maximum_transport_rank_cutoff": value.maximum_transport_rank_cutoff,
        "maximum_absolute_closure_phases": value.maximum_absolute_closure_phases,
        "maximum_plaquette_phase": value.maximum_plaquette_phase,
        "maximum_direct_matrix_difference": value.maximum_direct_matrix_difference,
        "maximum_direct_ordered_spectrum_difference": (
            value.maximum_direct_ordered_spectrum_difference
        ),
        "reference_reconstruction_errors": _error_mapping(
            value.reference_reconstruction_errors
        ),
        "comparison_reconstruction_errors": _error_mapping(
            value.comparison_reconstruction_errors
        ),
        "reference_interpolation_errors": _error_mapping(
            value.reference_interpolation_errors
        ),
        "comparison_interpolation_errors": _error_mapping(
            value.comparison_interpolation_errors
        ),
        "reference_locality": _locality_mapping(value.reference_locality),
        "comparison_locality": _locality_mapping(value.comparison_locality),
        "shells": tuple(_shell_mapping(shell) for shell in value.shells),
        "tolerance_decisions": tuple(
            _decision_mapping(decision) for decision in value.tolerance_decisions
        ),
    }


def _alignment_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis:
    disposition = values.get("disposition")
    alignment_wire = values.get("alignment")
    identity_value = values.get("analysis_identity")
    if type(alignment_wire) is not str:
        raise TypeError("alignment must decode to a built-in string")
    if not isinstance(identity_value, Mapping):
        raise TypeError("analysis_identity must decode to a mapping")
    alignment = Periodic3DRankNGaugeAlignment.from_wire(alignment_wire)
    analysis_identity = _identity_from_mapping(identity_value)
    if disposition == "inapplicable":
        required = {
            "disposition",
            "analysis_identity",
            "alignment",
            "reason",
            "deficient_sample_count",
            "minimum_numerical_rank",
        }
        if set(values) != required or type(values["reason"]) is not str:
            raise ValueError("inapplicable alignment fields do not match")
        count = values["deficient_sample_count"]
        rank = values["minimum_numerical_rank"]
        if type(count) is not int:
            raise TypeError("deficient_sample_count must be a built-in integer")
        if rank is not None and type(rank) is not int:
            raise TypeError("minimum_numerical_rank must decode to integer or None")
        return (
            Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                identity=analysis_identity,
                alignment=alignment,
                reason=Periodic3DRankNAlignmentInapplicabilityEnum.from_wire(
                    values["reason"]
                ),
                deficient_sample_count=count,
                minimum_numerical_rank=rank,
            )
        )
    if disposition != "qualified":
        raise ValueError("alignment disposition is not recognized")
    required = {
        "disposition",
        "analysis_identity",
        "alignment",
        "alignment_evidence",
        "maximum_aligned_frame_defect",
        "minimum_transport_singular_value",
        "maximum_transport_procrustes_residual",
        "maximum_transport_unitarity_defect",
        "maximum_transport_rank_cutoff",
        "maximum_absolute_closure_phases",
        "maximum_plaquette_phase",
        "maximum_direct_matrix_difference",
        "maximum_direct_ordered_spectrum_difference",
        "reference_reconstruction_errors",
        "comparison_reconstruction_errors",
        "reference_interpolation_errors",
        "comparison_interpolation_errors",
        "reference_locality",
        "comparison_locality",
        "shells",
        "tolerance_decisions",
    }
    if set(values) != required:
        raise ValueError("qualified alignment fields do not match")
    alignment_evidence = values["alignment_evidence"]
    reference_reconstruction_errors = values["reference_reconstruction_errors"]
    comparison_reconstruction_errors = values["comparison_reconstruction_errors"]
    reference_interpolation_errors = values["reference_interpolation_errors"]
    comparison_interpolation_errors = values["comparison_interpolation_errors"]
    reference_locality = values["reference_locality"]
    comparison_locality = values["comparison_locality"]
    if (
        not isinstance(alignment_evidence, Mapping)
        or not isinstance(reference_reconstruction_errors, Mapping)
        or not isinstance(comparison_reconstruction_errors, Mapping)
        or not isinstance(reference_interpolation_errors, Mapping)
        or not isinstance(comparison_interpolation_errors, Mapping)
        or not isinstance(reference_locality, Mapping)
        or not isinstance(comparison_locality, Mapping)
    ):
        raise TypeError("qualified alignment nested fields must decode to mappings")
    maximum_aligned_frame_defect = values["maximum_aligned_frame_defect"]
    minimum_transport_singular_value = values["minimum_transport_singular_value"]
    maximum_transport_procrustes_residual = values[
        "maximum_transport_procrustes_residual"
    ]
    maximum_transport_unitarity_defect = values["maximum_transport_unitarity_defect"]
    maximum_transport_rank_cutoff = values["maximum_transport_rank_cutoff"]
    maximum_plaquette_phase = values["maximum_plaquette_phase"]
    maximum_direct_matrix_difference = values["maximum_direct_matrix_difference"]
    maximum_direct_ordered_spectrum_difference = values[
        "maximum_direct_ordered_spectrum_difference"
    ]
    if (
        type(maximum_aligned_frame_defect) is not float
        or type(minimum_transport_singular_value) is not float
        or type(maximum_transport_procrustes_residual) is not float
        or type(maximum_transport_unitarity_defect) is not float
        or type(maximum_transport_rank_cutoff) is not float
        or type(maximum_plaquette_phase) is not float
        or type(maximum_direct_matrix_difference) is not float
        or type(maximum_direct_ordered_spectrum_difference) is not float
    ):
        raise TypeError("qualified alignment scalar diagnostics must be floats")
    phases = values["maximum_absolute_closure_phases"]
    shells = values["shells"]
    decisions = values["tolerance_decisions"]
    if type(phases) is not tuple or any(type(value) is not float for value in phases):
        raise TypeError("closure phases must decode to built-in floats")
    if type(shells) is not tuple or any(
        not isinstance(value, Mapping) for value in shells
    ):
        raise TypeError("shells must decode to mappings")
    if type(decisions) is not tuple or any(
        not isinstance(value, Mapping) for value in decisions
    ):
        raise TypeError("tolerance decisions must decode to mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis(
        identity=analysis_identity,
        alignment=alignment,
        alignment_evidence=_evidence_from_mapping(alignment_evidence),
        maximum_aligned_frame_defect=maximum_aligned_frame_defect,
        minimum_transport_singular_value=minimum_transport_singular_value,
        maximum_transport_procrustes_residual=(maximum_transport_procrustes_residual),
        maximum_transport_unitarity_defect=maximum_transport_unitarity_defect,
        maximum_transport_rank_cutoff=maximum_transport_rank_cutoff,
        maximum_absolute_closure_phases=phases,
        maximum_plaquette_phase=maximum_plaquette_phase,
        maximum_direct_matrix_difference=maximum_direct_matrix_difference,
        maximum_direct_ordered_spectrum_difference=(
            maximum_direct_ordered_spectrum_difference
        ),
        reference_reconstruction_errors=_error_from_mapping(
            reference_reconstruction_errors
        ),
        comparison_reconstruction_errors=_error_from_mapping(
            comparison_reconstruction_errors
        ),
        reference_interpolation_errors=_error_from_mapping(
            reference_interpolation_errors
        ),
        comparison_interpolation_errors=_error_from_mapping(
            comparison_interpolation_errors
        ),
        reference_locality=_locality_from_mapping(reference_locality),
        comparison_locality=_locality_from_mapping(comparison_locality),
        shells=tuple(_shell_from_mapping(value) for value in shells),
        tolerance_decisions=tuple(_decision_from_mapping(value) for value in decisions),
    )


def _case_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
) -> Mapping[str, SerializableValue]:
    return {
        "model_identity": value.model_identity,
        "case_identifier": value.case_identifier,
        "retained_rank": value.retained_rank,
        "circuit_depth": value.circuit_depth,
        "parent_scale": value.parent_scale,
        "transformation_coefficient": value.transformation_coefficient,
        "minimum_sampled_external_gap": value.minimum_sampled_external_gap,
        "alignments": tuple(_alignment_mapping(item) for item in value.alignments),
    }


def _case_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis:
    required = {
        "model_identity",
        "case_identifier",
        "retained_rank",
        "circuit_depth",
        "parent_scale",
        "transformation_coefficient",
        "minimum_sampled_external_gap",
        "alignments",
    }
    if set(values) != required:
        raise ValueError("case-analysis fields do not match")
    if (
        type(values["model_identity"]) is not str
        or type(values["case_identifier"]) is not str
    ):
        raise TypeError("case identities must decode to built-in strings")
    if (
        type(values["retained_rank"]) is not int
        or type(values["circuit_depth"]) is not int
    ):
        raise TypeError("case rank and depth must decode to built-in integers")
    parent_scale = values["parent_scale"]
    transformation_coefficient = values["transformation_coefficient"]
    minimum_sampled_external_gap = values["minimum_sampled_external_gap"]
    if type(parent_scale) is not float:
        raise TypeError("parent_scale must decode to a built-in float")
    if type(transformation_coefficient) is not float:
        raise TypeError("transformation_coefficient must decode to a built-in float")
    if type(minimum_sampled_external_gap) is not float:
        raise TypeError("minimum_sampled_external_gap must decode to a built-in float")
    alignments = values["alignments"]
    if type(alignments) is not tuple or any(
        not isinstance(value, Mapping) for value in alignments
    ):
        raise TypeError("alignments must decode to a tuple of mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis(
        model_identity=values["model_identity"],
        case_identifier=values["case_identifier"],
        retained_rank=values["retained_rank"],
        circuit_depth=values["circuit_depth"],
        parent_scale=parent_scale,
        transformation_coefficient=transformation_coefficient,
        minimum_sampled_external_gap=minimum_sampled_external_gap,
        alignments=tuple(_alignment_from_mapping(value) for value in alignments),
    )


__all__ = [
    "Periodic3DRankNAlignmentInapplicabilityEnum",
    "Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels",
    "Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary",
    "Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision",
    "Periodic3DRankNFittedAlignmentEvidence",
    "Periodic3DRankNPrescribedAlignmentEvidence",
    "Periodic3DRankNSupportSelected",
    "Periodic3DRankNSupportUnresolved",
]
