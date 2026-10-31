"""Byte-bound consistency assessment for maintained five-scale artifacts.

This is a non-entrypoint assessment module consumed by verification tests and by
``run_15_five_scale_evidence_assessment.py``. It reads
existing development CSV bytes and the immutable direct-v2 calculation. It does not run
a scientific analyzer, alter an artifact, promote the development tables to retained
evidence, or claim numerical parity. Its conclusions are limited to source integrity,
table reproduction, cutoff-decision consistency, retained evidence coverage, and the
explicit momentum-disposition difference.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

from development_diagnostics import (
    DiagnosticBundle,
    DiagnosticTable,
    DiagnosticTableData,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2 import (
    Periodic1DRank2CalculationRecord,
    Periodic1DRank2MomentumRefinementUnresolved,
    Periodic1DRank2TruncationCompleted,
)
from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
    OrderedEigenvalueErrors,
    RankNormalizedMatrixFrobeniusErrors,
    RealSpaceSupportTruncationComparison,
    RealSpaceSupportTruncationErrors,
    RealSpaceSupportTruncationToleranceSelectionRequest,
    RealSpaceSupportTruncationToleranceSelector,
    SymmetricRangeSupport1D,
)

_EXPECTED_SOURCE_DIGESTS = (
    (
        "parent-family-continuum.csv",
        "1ab9a26544f70f2f53ad798f6ab61aa9f72b7f065f5dc3fa67ff84f8b5557597",
    ),
    (
        "parent-family-summary.csv",
        "aa249ec7b19b8126e906f10ee657e79998c81980e6531440d2da2c0359c1aeb9",
    ),
    (
        "truncation-consequences.csv",
        "84c1769c98d737f2e65e53c1ea105cca9c01e7f36c39713112c6649a2f92c40c",
    ),
    (
        "truncation-refinement.csv",
        "bf3b3c80cc7b9ee37da00ad02735368a9b1b5b281d5af56098f77a2cc0d09b20",
    ),
    (
        "truncation-summary.csv",
        "5c18c4d8506f0a4e54b921cb7d508862c9ed8067bf879a1fe5e403a8a15a7575",
    ),
)
_EXPECTED_DIRECT_V2_SHA256 = (
    "29c1a2bdd7ec85b721cb9c9248ba0961cd1472278cf79a33f641eaa9e657dd01"
)
# These prefixes are fixed historical CSV column names, not shared scientific terms.
_LEGACY_DECISION_CHANNELS = (
    ("reference_band", "reference_maximum_band_error"),
    ("comparison_band", "comparison_maximum_total_band_error"),
    (
        "reference_hamiltonian",
        "reference_maximum_truncation_hamiltonian_error",
    ),
    ("comparison_hamiltonian", "comparison_maximum_total_hamiltonian_error"),
)


@dataclass(frozen=True, slots=True)
class DevelopmentSourceDigest:
    """Bind one maintained development source to its SHA-256 identity."""

    filename: str
    sha256: str


@dataclass(frozen=True, slots=True)
class FiveScaleSourceArtifactIntegrity:
    """Bind the exact admitted development and direct-v2 source bytes."""

    development_sources: tuple[DevelopmentSourceDigest, ...]
    direct_v2_sha256: str


@dataclass(frozen=True, slots=True)
class FiveScaleSourceIntegrityAssessment:
    """Compose source identity with the canonical admitted direct-v2 record."""

    source_integrity: FiveScaleSourceArtifactIntegrity
    direct_v2_record: Periodic1DRank2CalculationRecord


@dataclass(frozen=True, slots=True)
class FiveScaleTableReproductionConsistency:
    """Retain complete-grid inventories and exact table reproductions."""

    parent_hopping_scales: tuple[float, ...]
    amplitudes: tuple[float, ...]
    maximum_ranges: tuple[int, ...]
    construction_mesh_sizes: tuple[int, ...]
    parent_family_surface_rows: int
    parent_family_summary_rows: int
    truncation_consequence_rows: int
    truncation_summary_rows: int
    truncation_refinement_rows: int
    parent_endpoint_value_comparisons: int
    parent_endpoint_maximum_defect: float
    truncation_summary_value_comparisons: int
    truncation_summary_maximum_defect: float


@dataclass(frozen=True, slots=True)
class FiveScaleCutoffDecisionConsistency:
    """Retain exact threshold values and adjacent-mesh decision stability."""

    threshold_decision_comparisons: int
    threshold_value_comparisons: int
    threshold_value_maximum_defect: float
    decision_changes_128_to_256: int
    decision_changes_256_to_512: int


@dataclass(frozen=True, slots=True)
class FiveScaleEvidenceCoverage:
    """Retain the direct-v2 coverage and the explicit unmatched development scope."""

    development_truncation_rows: int
    direct_v2_truncation_rows: int
    unmatched_development_truncation_rows: int

    def __post_init__(self) -> None:
        if type(self.development_truncation_rows) is not int:
            raise TypeError("development_truncation_rows must be a built-in integer")
        if type(self.direct_v2_truncation_rows) is not int:
            raise TypeError("direct_v2_truncation_rows must be a built-in integer")
        if type(self.unmatched_development_truncation_rows) is not int:
            raise TypeError(
                "unmatched_development_truncation_rows must be a built-in integer"
            )
        if self.development_truncation_rows < 0:
            raise ValueError("development_truncation_rows must be nonnegative")
        if self.direct_v2_truncation_rows < 0:
            raise ValueError("direct_v2_truncation_rows must be nonnegative")
        if self.unmatched_development_truncation_rows < 0:
            raise ValueError(
                "unmatched_development_truncation_rows must be nonnegative"
            )
        if (
            self.direct_v2_truncation_rows + self.unmatched_development_truncation_rows
            != self.development_truncation_rows
        ):
            raise ValueError(
                "direct and unmatched rows must partition development rows"
            )

    @property
    def complete_retained_coverage(self) -> bool:
        """Return whether direct v2 covers every maintained truncation row."""
        return self.unmatched_development_truncation_rows == 0


@dataclass(frozen=True, slots=True)
class FiveScaleMomentumDisposition:
    """Keep historical donor and installed momentum outcomes explicitly distinct."""

    donor_dispositions: tuple[str, ...]
    installed_direct_v2_disposition: str

    @property
    def semantic_equivalence_established(self) -> bool:
        """Return false because this assessment does not equate the diagnostics."""
        return False


@dataclass(frozen=True, slots=True)
class FiveScaleConsistencyAssessment:
    """Compose bounded five-scale consistency conclusions without a parity claim."""

    source_integrity: FiveScaleSourceArtifactIntegrity
    table_reproduction: FiveScaleTableReproductionConsistency
    cutoff_decisions: FiveScaleCutoffDecisionConsistency
    evidence_coverage: FiveScaleEvidenceCoverage
    momentum_disposition: FiveScaleMomentumDisposition


class FiveScaleSourceIntegrityAssessor:
    """Admit the exact development bytes and canonical direct-v2 record."""

    __slots__ = ()

    def assess(
        self,
        *,
        results_directory: Path,
        direct_v2_calculation: Path,
    ) -> FiveScaleSourceIntegrityAssessment:
        """Return source identities and the canonical admitted direct-v2 record."""
        if not isinstance(results_directory, Path):
            raise TypeError("results_directory must be a pathlib.Path")
        if not isinstance(direct_v2_calculation, Path):
            raise TypeError("direct_v2_calculation must be a pathlib.Path")

        digests: list[DevelopmentSourceDigest] = []
        for filename, expected in _EXPECTED_SOURCE_DIGESTS:
            path = results_directory / filename
            observed = hashlib.sha256(path.read_bytes()).hexdigest()
            if observed != expected:
                raise ValueError(f"{filename} does not match its audited digest")
            digests.append(DevelopmentSourceDigest(filename, observed))

        payload = direct_v2_calculation.read_bytes()
        direct_v2_sha256 = hashlib.sha256(payload).hexdigest()
        if direct_v2_sha256 != _EXPECTED_DIRECT_V2_SHA256:
            raise ValueError("direct-v2 calculation does not match its audited digest")
        direct_v2_record = Periodic1DRank2CalculationRecord.from_json(payload)
        if direct_v2_record.to_json() != payload:
            raise ValueError("direct-v2 calculation is not canonical typed JSON")
        return FiveScaleSourceIntegrityAssessment(
            source_integrity=FiveScaleSourceArtifactIntegrity(
                development_sources=tuple(digests),
                direct_v2_sha256=direct_v2_sha256,
            ),
            direct_v2_record=direct_v2_record,
        )


class FiveScaleTableConsistencyAssessor:
    """Assess complete inventories and reproduction of derived summary tables."""

    __slots__ = ()

    def assess(
        self,
        *,
        continuum: DiagnosticTableData,
        parent_summary: DiagnosticTableData,
        truncation: DiagnosticTableData,
        truncation_summary: DiagnosticTableData,
        refinement: DiagnosticTableData,
    ) -> FiveScaleTableReproductionConsistency:
        """Return exact inventory and table-reproduction consistency values."""
        scales = parent_summary.unique_numbers("parent_hopping_scale")
        amplitudes = continuum.unique_numbers("amplitude")
        maximum_ranges = tuple(
            int(value) for value in truncation.unique_numbers("maximum_range")
        )
        meshes = tuple(
            int(value) for value in refinement.unique_numbers("construction_mesh_size")
        )
        if scales != (0.0, 0.25, 0.5, 0.75, 1.0):
            raise ValueError("maintained parent-scale inventory changed")
        expected_amplitudes = tuple(float(index * math.pi / 128) for index in range(33))
        if amplitudes != expected_amplitudes:
            raise ValueError("maintained amplitude inventory changed")
        if maximum_ranges != tuple(range(17)):
            raise ValueError("maintained dense cutoff inventory changed")
        if meshes != (128, 256, 512):
            raise ValueError("maintained refinement mesh inventory changed")

        parent_defects: list[float] = []
        parent_fields = (
            (
                "endpoint_minimum_threshold_over_sqrt_kappa",
                "minimum_operator_threshold_over_sqrt_kappa",
            ),
            (
                "endpoint_excess_nonzero_hopping_weight",
                "excess_nonzero_hopping_weight",
            ),
        )
        for scale, summary_row in zip(scales, parent_summary.rows, strict=True):
            rows = continuum.selected(parent_hopping_scale=scale)
            endpoint_row = max(rows, key=lambda row: continuum.number(row, "amplitude"))
            parent_defects.extend(
                abs(
                    parent_summary.number(summary_row, destination)
                    - continuum.number(endpoint_row, source)
                )
                for destination, source in parent_fields
            )
        if not parent_defects:
            raise ValueError("parent endpoint consistency requires comparisons")

        summary_defects: list[float] = []
        maximum_fields = (
            ("maximum_direct_band_defect", "maximum_direct_band_defect"),
            (
                "maximum_interpolation_hamiltonian_error",
                "comparison_maximum_interpolation_hamiltonian_error",
            ),
            (
                "maximum_interpolation_band_error",
                "comparison_maximum_interpolation_band_error",
            ),
        )
        endpoint_fields = (
            (
                "total_hamiltonian_error",
                "comparison_maximum_total_hamiltonian_error",
            ),
            ("total_band_error", "comparison_maximum_total_band_error"),
        )
        for scale, summary_row in zip(scales, truncation_summary.rows, strict=True):
            rows = truncation.selected(parent_hopping_scale=scale)
            for destination, source in maximum_fields:
                expected = max(truncation.number(row, source) for row in rows)
                summary_defects.append(
                    abs(truncation_summary.number(summary_row, destination) - expected)
                )
            maximum_amplitude = max(truncation.number(row, "amplitude") for row in rows)
            endpoint_rows = truncation.selected(
                parent_hopping_scale=scale,
                amplitude=maximum_amplitude,
            )
            for maximum_range in (0, 8, 16):
                range_row = next(
                    row
                    for row in endpoint_rows
                    if truncation.integer(row, "maximum_range") == maximum_range
                )
                for suffix, source in endpoint_fields:
                    destination = f"endpoint_range_{maximum_range}_{suffix}"
                    summary_defects.append(
                        abs(
                            truncation_summary.number(summary_row, destination)
                            - truncation.number(range_row, source)
                        )
                    )
        if not summary_defects:
            raise ValueError("truncation summary consistency requires comparisons")

        return FiveScaleTableReproductionConsistency(
            parent_hopping_scales=scales,
            amplitudes=amplitudes,
            maximum_ranges=maximum_ranges,
            construction_mesh_sizes=meshes,
            parent_family_surface_rows=len(continuum.rows),
            parent_family_summary_rows=len(parent_summary.rows),
            truncation_consequence_rows=len(truncation.rows),
            truncation_summary_rows=len(truncation_summary.rows),
            truncation_refinement_rows=len(refinement.rows),
            parent_endpoint_value_comparisons=len(parent_defects),
            parent_endpoint_maximum_defect=max(parent_defects),
            truncation_summary_value_comparisons=len(summary_defects),
            truncation_summary_maximum_defect=max(summary_defects),
        )


class FiveScaleEvidenceCoverageAssessor:
    """Assess direct-v2 truncation coverage of the five-scale table scope."""

    __slots__ = ()

    def assess(
        self,
        *,
        direct_v2_record: Periodic1DRank2CalculationRecord,
        parent_hopping_scales: tuple[float, ...],
        development_truncation_rows: int,
    ) -> FiveScaleEvidenceCoverage:
        """Return the exact retained and unmatched truncation row counts."""
        direct_parent_scales = tuple(
            member.request.parent_hopping_scale
            for member in direct_v2_record.parent_family.members
        )
        if direct_parent_scales != parent_hopping_scales:
            raise ValueError("direct-v2 parent family does not cover the five scales")
        direct_truncation = direct_v2_record.truncation
        if type(direct_truncation) is not (Periodic1DRank2TruncationCompleted):
            raise ValueError("direct v2 no longer contains completed truncation")
        if direct_truncation.request.template_request.parent_hopping_scale != 1.0:
            raise ValueError("direct-v2 truncation is not the scale-one slice")
        direct_truncation_rows = sum(
            len(point.ranges) for point in direct_truncation.points
        )
        if direct_truncation_rows > development_truncation_rows:
            raise ValueError(
                "direct-v2 truncation exceeds maintained development scope"
            )
        return FiveScaleEvidenceCoverage(
            development_truncation_rows=development_truncation_rows,
            direct_v2_truncation_rows=direct_truncation_rows,
            unmatched_development_truncation_rows=(
                development_truncation_rows - direct_truncation_rows
            ),
        )


class FiveScaleMomentumDispositionAssessor:
    """Keep donor and installed momentum diagnostic outcomes distinct."""

    __slots__ = ()

    def assess(
        self,
        *,
        parent_summary: DiagnosticTableData,
        direct_v2_record: Periodic1DRank2CalculationRecord,
        parent_hopping_scales: tuple[float, ...],
    ) -> FiveScaleMomentumDisposition:
        """Return exact donor and installed dispositions without equating them."""
        donor_dispositions = tuple(
            parent_summary.text(row, "momentum_disposition")
            for row in parent_summary.rows
        )
        if donor_dispositions != ("converged",) * len(parent_hopping_scales):
            raise ValueError("historical donor momentum dispositions changed")
        momentum = direct_v2_record.momentum_refinement
        if type(momentum) is not (Periodic1DRank2MomentumRefinementUnresolved):
            raise ValueError("direct v2 no longer exposes the unresolved outcome")
        return FiveScaleMomentumDisposition(
            donor_dispositions=donor_dispositions,
            installed_direct_v2_disposition=type(momentum).__name__,
        )


class FiveScaleCutoffConsistencyAssessor:
    """Assess stored minimum-support decisions and adjacent-mesh stability."""

    __slots__ = ()

    def assess(
        self,
        *,
        truncation: DiagnosticTableData,
        refinement: DiagnosticTableData,
    ) -> FiveScaleCutoffDecisionConsistency:
        """Return threshold-value reproduction and adjacent-mesh decision changes."""
        consequence_rows = {
            (
                truncation.text(row, "parent_hopping_scale"),
                truncation.text(row, "amplitude"),
            ): truncation.selected(
                parent_hopping_scale=truncation.number(row, "parent_hopping_scale"),
                amplitude=truncation.number(row, "amplitude"),
            )
            for row in truncation.rows
        }
        decision_comparisons = 0
        value_defects: list[float] = []
        for row in refinement.rows:
            tolerance = refinement.number(row, "decision_tolerance")
            if refinement.integer(row, "evaluation_mesh_size") != (
                4 * refinement.integer(row, "construction_mesh_size") + 1
            ):
                raise ValueError("refinement evaluation mesh is not disjoint")
            for prefix, _ in _LEGACY_DECISION_CHANNELS:
                maximum_range = refinement.integer(
                    row,
                    f"{prefix}_first_passing_range",
                )
                passing = refinement.number(row, f"{prefix}_passing_error")
                if passing > tolerance:
                    raise ValueError("stored first-passing error exceeds tolerance")
                preceding = refinement.text(row, f"{prefix}_preceding_error")
                if maximum_range == 0:
                    if preceding != "not-applicable":
                        raise ValueError("range-zero decision has a predecessor")
                elif float(preceding) <= tolerance:
                    raise ValueError("stored preceding error already passes")

            if refinement.integer(row, "construction_mesh_size") != 256:
                continue
            identity = (
                refinement.text(row, "parent_hopping_scale"),
                refinement.text(row, "amplitude"),
            )
            rows = tuple(
                sorted(
                    consequence_rows[identity],
                    key=lambda item: truncation.integer(item, "maximum_range"),
                )
            )
            selection = RealSpaceSupportTruncationToleranceSelector().execute(
                RealSpaceSupportTruncationToleranceSelectionRequest(
                    comparisons=tuple(
                        RealSpaceSupportTruncationComparison(
                            support=SymmetricRangeSupport1D(
                                truncation.integer(item, "maximum_range")
                            ).support,
                            reference_model_errors=RealSpaceSupportTruncationErrors(
                                matrix_frobenius=RankNormalizedMatrixFrobeniusErrors(
                                    maximum_error=truncation.number(
                                        item,
                                        "reference_maximum_truncation_"
                                        "hamiltonian_error",
                                    ),
                                    root_mean_square_error=truncation.number(
                                        item,
                                        "reference_rms_truncation_hamiltonian_error",
                                    ),
                                ),
                                ordered_eigenvalues=OrderedEigenvalueErrors(
                                    maximum_absolute_error=truncation.number(
                                        item,
                                        "reference_maximum_band_error",
                                    ),
                                    root_mean_square_error=truncation.number(
                                        item,
                                        "reference_rms_band_error",
                                    ),
                                ),
                            ),
                            comparison_model_errors=RealSpaceSupportTruncationErrors(
                                matrix_frobenius=RankNormalizedMatrixFrobeniusErrors(
                                    maximum_error=truncation.number(
                                        item,
                                        "comparison_maximum_total_hamiltonian_error",
                                    ),
                                    root_mean_square_error=truncation.number(
                                        item,
                                        "comparison_rms_total_hamiltonian_error",
                                    ),
                                ),
                                ordered_eigenvalues=OrderedEigenvalueErrors(
                                    maximum_absolute_error=truncation.number(
                                        item,
                                        "comparison_maximum_total_band_error",
                                    ),
                                    root_mean_square_error=truncation.number(
                                        item,
                                        "comparison_rms_total_band_error",
                                    ),
                                ),
                            ),
                        )
                        for item in rows
                    ),
                    tolerance=tolerance,
                )
            )
            outcomes = {
                "reference_band": (
                    selection.reference_model.ordered_eigenvalue_maximum_absolute_error
                ),
                "comparison_band": (
                    selection.comparison_model.ordered_eigenvalue_maximum_absolute_error
                ),
                "reference_hamiltonian": (
                    selection.reference_model.matrix_frobenius_maximum_error
                ),
                "comparison_hamiltonian": (
                    selection.comparison_model.matrix_frobenius_maximum_error
                ),
            }
            for prefix, _ in _LEGACY_DECISION_CHANNELS:
                outcome = outcomes[prefix]
                if type(outcome) is not MinimumToleranceSatisfyingSupport:
                    raise ValueError("stored N=256 support selection is unresolved")
                maximum_range = truncation.integer(
                    rows[outcome.comparison_index], "maximum_range"
                )
                if maximum_range != refinement.integer(
                    row,
                    f"{prefix}_first_passing_range",
                ):
                    raise ValueError("stored N=256 support selection changed")
                decision_comparisons += 1
                value_defects.append(
                    abs(
                        outcome.satisfying_error
                        - refinement.number(row, f"{prefix}_passing_error")
                    )
                )
                if outcome.preceding_error is not None:
                    value_defects.append(
                        abs(
                            outcome.preceding_error
                            - float(
                                refinement.text(
                                    row,
                                    f"{prefix}_preceding_error",
                                )
                            )
                        )
                    )
        if not value_defects:
            raise ValueError("threshold consistency requires N=256 comparisons")

        channels = tuple(
            f"{prefix}_first_passing_range" for prefix, _ in _LEGACY_DECISION_CHANNELS
        )
        refinement_rows = {
            (
                refinement.number(row, "parent_hopping_scale"),
                refinement.number(row, "amplitude"),
                refinement.integer(row, "construction_mesh_size"),
            ): row
            for row in refinement.rows
        }
        changes_128_to_256 = 0
        changes_256_to_512 = 0
        for scale in refinement.unique_numbers("parent_hopping_scale"):
            for amplitude in refinement.unique_numbers("amplitude"):
                row_128 = refinement_rows[(scale, amplitude, 128)]
                row_256 = refinement_rows[(scale, amplitude, 256)]
                row_512 = refinement_rows[(scale, amplitude, 512)]
                changes_128_to_256 += sum(
                    refinement.text(row_128, channel)
                    != refinement.text(row_256, channel)
                    for channel in channels
                )
                changes_256_to_512 += sum(
                    refinement.text(row_256, channel)
                    != refinement.text(row_512, channel)
                    for channel in channels
                )
        if changes_128_to_256 != 0 or changes_256_to_512 != 0:
            raise ValueError("stored threshold-adjacent decisions are not stable")

        return FiveScaleCutoffDecisionConsistency(
            threshold_decision_comparisons=decision_comparisons,
            threshold_value_comparisons=len(value_defects),
            threshold_value_maximum_defect=max(value_defects),
            decision_changes_128_to_256=changes_128_to_256,
            decision_changes_256_to_512=changes_256_to_512,
        )


class FiveScaleConsistencyAssessor:
    """Compose bounded consistency values without executing scientific owners."""

    __slots__ = ()

    def assess(
        self,
        *,
        results_directory: Path,
        direct_v2_calculation: Path,
    ) -> FiveScaleConsistencyAssessment:
        """Compose the five independently named consistency components."""
        source_assessment = FiveScaleSourceIntegrityAssessor().assess(
            results_directory=results_directory,
            direct_v2_calculation=direct_v2_calculation,
        )
        bundle = DiagnosticBundle.load(results_directory)
        continuum = bundle.table(DiagnosticTable.PARENT_FAMILY_CONTINUUM)
        parent_summary = bundle.table(DiagnosticTable.PARENT_FAMILY_SUMMARY)
        truncation = bundle.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
        truncation_summary = bundle.table(DiagnosticTable.TRUNCATION_SUMMARY)
        refinement = bundle.table(DiagnosticTable.TRUNCATION_REFINEMENT)
        table_reproduction = FiveScaleTableConsistencyAssessor().assess(
            continuum=continuum,
            parent_summary=parent_summary,
            truncation=truncation,
            truncation_summary=truncation_summary,
            refinement=refinement,
        )
        return FiveScaleConsistencyAssessment(
            source_integrity=source_assessment.source_integrity,
            table_reproduction=table_reproduction,
            cutoff_decisions=FiveScaleCutoffConsistencyAssessor().assess(
                truncation=truncation,
                refinement=refinement,
            ),
            evidence_coverage=FiveScaleEvidenceCoverageAssessor().assess(
                direct_v2_record=source_assessment.direct_v2_record,
                parent_hopping_scales=table_reproduction.parent_hopping_scales,
                development_truncation_rows=(
                    table_reproduction.truncation_consequence_rows
                ),
            ),
            momentum_disposition=FiveScaleMomentumDispositionAssessor().assess(
                parent_summary=parent_summary,
                direct_v2_record=source_assessment.direct_v2_record,
                parent_hopping_scales=table_reproduction.parent_hopping_scales,
            ),
        )


__all__ = [
    "DevelopmentSourceDigest",
    "FiveScaleConsistencyAssessment",
    "FiveScaleConsistencyAssessor",
    "FiveScaleCutoffConsistencyAssessor",
    "FiveScaleCutoffDecisionConsistency",
    "FiveScaleEvidenceCoverage",
    "FiveScaleEvidenceCoverageAssessor",
    "FiveScaleMomentumDisposition",
    "FiveScaleMomentumDispositionAssessor",
    "FiveScaleSourceArtifactIntegrity",
    "FiveScaleSourceIntegrityAssessment",
    "FiveScaleSourceIntegrityAssessor",
    "FiveScaleTableConsistencyAssessor",
    "FiveScaleTableReproductionConsistency",
]
