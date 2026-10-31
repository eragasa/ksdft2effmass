"""Read-only parity audit for the historical rank-two workflow donors."""

from __future__ import annotations

import csv
import hashlib
import math
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.periodic1d import (
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2CalculationRecord,
    Periodic1DRank2MomentumRefinementUnresolved,
    Periodic1DRank2TruncationCompleted,
)


def _calculation_root() -> Path:
    repository = next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "calculations").is_dir()
    )
    return (
        repository
        / "calculations"
        / "periodic1d"
        / "rank2"
        / "band-equivalence-versus-hopping-locality"
    )


def _rows(name: str) -> list[dict[str, str]]:
    path = _calculation_root() / "simulations" / "development" / "results" / name
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _record() -> Periodic1DRank2CalculationRecord:
    path = (
        _calculation_root()
        / "executions"
        / "direct-embedded-rank2-controlled-v2"
        / "results"
        / "calculation.json"
    )
    return Periodic1DRank2CalculationRecord.from_json(path.read_bytes())


def _defects(row: Mapping[str, str], values: Mapping[str, float | int]) -> list[float]:
    return [abs(float(row[name]) - float(value)) for name, value in values.items()]


class TestPeriodic1DRank2DonorParity:
    """Compare immutable donor tables with the immutable direct-v2 calculation."""

    def test_audit_inputs_have_bound_digests(self) -> None:
        expected = {
            "parent-family-continuum.csv": (
                "1ab9a26544f70f2f53ad798f6ab61aa9f72b7f065f5dc3fa67ff84f8b5557597"
            ),
            "nonflat-momentum-refinement.csv": (
                "cd513a6fea1d4f28984e857f64c2995cf7fab493e9775ddef64ec1b4dc8c28d3"
            ),
            "nonflat-amplitude-resolution.csv": (
                "72873cbaa911a20145700148b77b4deb885617c7f37c08c9e468aaadb2ef8d18"
            ),
            "nonflat-continuum.csv": (
                "d59c34e829025a66037fa97f7be6408ef6a40fc393f66c9a6da99e17034f38f9"
            ),
            "nonflat-hopping-power-map.csv": (
                "f48ddc94f6559853c1c9124cddae29d890f06f747bddfd36e72c3460817601a0"
            ),
            "nonflat-selected-hopping-tails.csv": (
                "98c9c46430e4840ad7497a1a6f0a61591ef87e1acf68353bcb6d5054c8515857"
            ),
            "truncation-consequences.csv": (
                "84c1769c98d737f2e65e53c1ea105cca9c01e7f36c39713112c6649a2f92c40c"
            ),
        }
        result_directory = (
            _calculation_root() / "simulations" / "development" / "results"
        )
        for name, digest in expected.items():
            observed_digest = hashlib.sha256(
                (result_directory / name).read_bytes()
            ).hexdigest()
            assert observed_digest == digest

        calculation = (
            _calculation_root()
            / "executions"
            / "direct-embedded-rank2-controlled-v2"
            / "results"
            / "calculation.json"
        )
        assert hashlib.sha256(calculation.read_bytes()).hexdigest() == (
            "29c1a2bdd7ec85b721cb9c9248ba0961cd1472278cf79a33f641eaa9e657dd01"
        )

    def test_parent_family_and_nonflat_surfaces_agree(self) -> None:
        record = _record()
        defects: list[float] = []
        rows = _rows("parent-family-continuum.csv")
        members = [
            member for member in record.parent_family.members for _ in member.points
        ]
        points = [
            point for member in record.parent_family.members for point in member.points
        ]
        assert len(rows) == len(points) == 165
        for row, member, point in zip(rows, members, points, strict=True):
            root_scale = math.sqrt(point.splitting_scale)
            excess = (
                point.comparison_nonzero_hopping_weight
                - point.reference_nonzero_hopping_weight
            )
            normalized_threshold = point.minimum_operator_threshold / root_scale
            normalized_excess = excess / point.splitting_scale
            defects.extend(
                _defects(
                    row,
                    {
                        "parent_hopping_scale": member.request.parent_hopping_scale,
                        "amplitude": point.amplitude,
                        "maximum_correlation": point.discrete_maximum_correlation,
                        "splitting_scale": point.splitting_scale,
                        "minimum_operator_threshold_over_sqrt_kappa": (
                            normalized_threshold
                        ),
                        "joint_threshold_over_sqrt_kappa": (
                            point.exact_spectrum_joint_operator_threshold / root_scale
                        ),
                        "reference_nonzero_hopping_weight": (
                            point.reference_nonzero_hopping_weight
                        ),
                        "comparison_nonzero_hopping_weight": (
                            point.comparison_nonzero_hopping_weight
                        ),
                        "excess_nonzero_hopping_weight": excess,
                        "normalized_squared_operator_residual": (
                            normalized_threshold**2
                        ),
                        "normalized_excess_nonzero_hopping_weight": normalized_excess,
                        "flat_identity_departure": (
                            normalized_excess - normalized_threshold**2
                        ),
                        "maximum_band_defect": point.maximum_band_defect,
                    },
                )
            )

        final = record.momentum_refinement.mesh_analyses[-1]
        continuum_rows = _rows("nonflat-continuum.csv")
        assert len(continuum_rows) == len(final.points) == 65
        for row, point in zip(continuum_rows, final.points, strict=True):
            defects.extend(
                _defects(
                    row,
                    {
                        "amplitude": point.amplitude,
                        "maximum_band_defect": point.maximum_band_defect,
                        "maximum_correlation": point.discrete_maximum_correlation,
                        "minimum_operator_threshold": (
                            point.minimum_operator_threshold
                        ),
                        "exact_spectrum_joint_operator_threshold": (
                            point.exact_spectrum_joint_operator_threshold
                        ),
                        "reference_nonzero_hopping_weight": (
                            point.reference_nonzero_hopping_weight
                        ),
                        "comparison_nonzero_hopping_weight": (
                            point.comparison_nonzero_hopping_weight
                        ),
                    },
                )
            )

        power_rows = _rows("nonflat-hopping-power-map.csv")
        assert len(power_rows) == 845
        for row in power_rows:
            point = min(
                final.points,
                key=lambda value: abs(value.amplitude - float(row["amplitude"])),
            )
            assert abs(point.amplitude - float(row["amplitude"])) < 1.0e-15
            displacement = int(row["absolute_displacement"])
            reference = math.fsum(
                power.reference_normalized_squared_frobenius_norm
                for power in point.hopping_powers
                if abs(power.displacement) == displacement
            )
            comparison = math.fsum(
                power.comparison_normalized_squared_frobenius_norm
                for power in point.hopping_powers
                if abs(power.displacement) == displacement
            )
            defects.extend(
                _defects(
                    row,
                    {
                        "reference_normalized_hopping_weight": reference,
                        "comparison_normalized_hopping_weight": comparison,
                    },
                )
            )

        tail_rows = _rows("nonflat-selected-hopping-tails.csv")
        assert len(tail_rows) == 21
        for row in tail_rows:
            point = min(
                final.points,
                key=lambda value: abs(value.amplitude - float(row["amplitude"])),
            )
            maximum_range = int(row["maximum_range"])
            defects.extend(
                _defects(
                    row,
                    {
                        "amplitude": point.amplitude,
                        "reference_normalized_tail_weight": math.fsum(
                            power.reference_normalized_squared_frobenius_norm
                            for power in point.hopping_powers
                            if abs(power.displacement) > maximum_range
                        ),
                        "comparison_normalized_tail_weight": math.fsum(
                            power.comparison_normalized_squared_frobenius_norm
                            for power in point.hopping_powers
                            if abs(power.displacement) > maximum_range
                        ),
                        "maximum_correlation": point.discrete_maximum_correlation,
                        "minimum_operator_threshold": (
                            point.minimum_operator_threshold
                        ),
                        "exact_spectrum_joint_operator_threshold": (
                            point.exact_spectrum_joint_operator_threshold
                        ),
                    },
                )
            )

        assert len(defects) == 4_416
        assert max(defects) < 1.0e-13

    def test_momentum_parity_exposes_expanded_parent_diagnostic(self) -> None:
        record = _record()
        momentum_refinement = record.momentum_refinement
        assert type(momentum_refinement) is Periodic1DRank2MomentumRefinementUnresolved
        rows = _rows("nonflat-momentum-refinement.csv")
        refinements = momentum_refinement.refinements
        assert len(rows) == len(refinements) == 4
        defects: list[float] = []
        donor_parent_changes: list[float] = []
        installed_parent_changes: list[float] = []
        for row, refinement in zip(rows, refinements, strict=True):
            defects.extend(
                _defects(
                    row,
                    {
                        "coarse_mesh_size": refinement.coarse_mesh_size,
                        "fine_mesh_size": refinement.fine_mesh_size,
                        "maximum_shared_parent_eigenvalue_defect": (
                            refinement.maximum_shared_parent_eigenvalue_defect
                        ),
                        "maximum_shared_projector_defect": (
                            refinement.maximum_shared_parent_projector_defect
                        ),
                        "maximum_correlation_change": (
                            refinement.maximum_correlation_change
                        ),
                        "maximum_threshold_change": (
                            refinement.maximum_threshold_change
                        ),
                        "maximum_hopping_weight_change": (
                            refinement.maximum_hopping_weight_change
                        ),
                        "maximum_hopping_block_power_change": (
                            refinement.maximum_hopping_power_change
                        ),
                        "maximum_angle_change": refinement.maximum_angle_change,
                        "maximum_band_defect": refinement.maximum_band_defect,
                        "maximum_reconstruction_defect": (
                            refinement.maximum_reconstruction_defect
                        ),
                        "maximum_parseval_defect": (refinement.maximum_parseval_defect),
                    },
                )
            )
            assert row["within_draft_tolerances"] == "true"
            assert not refinement.within_tolerances
            donor_parent_changes.append(float(row["maximum_parent_diagnostic_change"]))
            installed_parent_changes.append(refinement.maximum_parent_diagnostic_change)

        assert max(defects) < 2.0e-15
        assert max(donor_parent_changes) < 1.0e-12
        assert min(installed_parent_changes) > 9.0e-4
        assert all(
            fine < coarse
            for coarse, fine in zip(
                installed_parent_changes,
                installed_parent_changes[1:],
                strict=False,
            )
        )
        assert not momentum_refinement.converged

    def test_adaptive_and_scale_one_truncation_channels_agree(self) -> None:
        record = _record()
        defects: list[float] = []
        adaptive_amplitude = record.adaptive_amplitude
        assert (
            type(adaptive_amplitude) is Periodic1DRank2AdaptiveAmplitudeLevelsExhausted
        )
        amplitude_rows = _rows("nonflat-amplitude-resolution.csv")
        assert len(amplitude_rows) == len(adaptive_amplitude.levels) == 4
        for row, level in zip(
            amplitude_rows,
            adaptive_amplitude.levels,
            strict=True,
        ):
            defects.extend(
                _defects(
                    row,
                    {
                        "amplitude_intervals": len(level.interpolation_nodes) - 1,
                        "maximum_correlation_midpoint_defect": (
                            level.maximum_correlation_defect
                        ),
                        "maximum_operator_threshold_midpoint_defect": (
                            level.maximum_operator_threshold_defect
                        ),
                        "maximum_joint_threshold_midpoint_defect": (
                            level.maximum_joint_threshold_defect
                        ),
                        "maximum_nonzero_hopping_weight_midpoint_defect": (
                            level.maximum_hopping_weight_defect
                        ),
                        "maximum_hopping_block_power_midpoint_defect": (
                            level.maximum_hopping_power_defect
                        ),
                    },
                )
            )
            assert row["passes_draft_tolerance"] == "false"
            assert not level.within_tolerances
        assert not adaptive_amplitude.converged

        truncation = record.truncation
        assert type(truncation) is Periodic1DRank2TruncationCompleted
        all_truncation_rows = _rows("truncation-consequences.csv")
        donor_scales = {
            float(row["parent_hopping_scale"]) for row in all_truncation_rows
        }
        assert donor_scales == {0.0, 0.25, 0.5, 0.75, 1.0}
        truncation_rows = [
            row
            for row in all_truncation_rows
            if float(row["parent_hopping_scale"]) == 1.0
        ]
        points = [point for point in truncation.points for _ in point.ranges]
        ranges = [
            range_result for point in truncation.points for range_result in point.ranges
        ]
        assert len(truncation_rows) == len(points) == len(ranges) == 561
        for row, point, range_result in zip(
            truncation_rows,
            points,
            ranges,
            strict=True,
        ):
            defects.extend(
                _defects(
                    row,
                    {
                        "amplitude": point.amplitude,
                        "maximum_range": range_result.maximum_range,
                        "reference_nyquist_power": point.reference_nyquist_power,
                        "comparison_nyquist_power": point.comparison_nyquist_power,
                        "maximum_direct_band_defect": (
                            point.direct_spectral_maximum_defect
                        ),
                        "comparison_maximum_interpolation_hamiltonian_error": (
                            point.comparison_interpolation_hamiltonian_maximum_error
                        ),
                        "comparison_rms_interpolation_hamiltonian_error": (
                            point.comparison_interpolation_hamiltonian_rms_error
                        ),
                        "comparison_maximum_interpolation_band_error": (
                            point.comparison_interpolation_spectral_maximum_error
                        ),
                        "comparison_rms_interpolation_band_error": (
                            point.comparison_interpolation_spectral_rms_error
                        ),
                        "reference_ordinary_omitted_power": (
                            range_result.reference_ordinary_omitted_power
                        ),
                        "comparison_ordinary_omitted_power": (
                            range_result.comparison_ordinary_omitted_power
                        ),
                        "reference_total_omitted_power": (
                            range_result.reference_total_omitted_power
                        ),
                        "comparison_total_omitted_power": (
                            range_result.comparison_total_omitted_power
                        ),
                        "reference_maximum_truncation_hamiltonian_error": (
                            range_result.reference_truncation_hamiltonian_maximum_error
                        ),
                        "reference_rms_truncation_hamiltonian_error": (
                            range_result.reference_truncation_hamiltonian_rms_error
                        ),
                        "reference_maximum_band_error": (
                            range_result.reference_truncation_spectral_maximum_error
                        ),
                        "reference_rms_band_error": (
                            range_result.reference_truncation_spectral_rms_error
                        ),
                        "comparison_maximum_truncation_hamiltonian_error": (
                            range_result.comparison_truncation_hamiltonian_maximum_error
                        ),
                        "comparison_rms_truncation_hamiltonian_error": (
                            range_result.comparison_truncation_hamiltonian_rms_error
                        ),
                        "comparison_maximum_truncation_band_error": (
                            range_result.comparison_truncation_spectral_maximum_error
                        ),
                        "comparison_rms_truncation_band_error": (
                            range_result.comparison_truncation_spectral_rms_error
                        ),
                        "comparison_maximum_total_hamiltonian_error": (
                            range_result.comparison_total_hamiltonian_maximum_error
                        ),
                        "comparison_rms_total_hamiltonian_error": (
                            range_result.comparison_total_hamiltonian_rms_error
                        ),
                        "comparison_maximum_total_band_error": (
                            range_result.comparison_total_spectral_maximum_error
                        ),
                        "comparison_rms_total_band_error": (
                            range_result.comparison_total_spectral_rms_error
                        ),
                    },
                )
            )

        assert len(defects) == 14_049
        assert max(defects) < 1.0e-13
