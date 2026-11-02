"""Periodic-3D arbitrary-rank aggregate request and case-expansion contracts."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.periodic.lattice import (
    BravaisLattice,
    DirectLattice3D,
    DirectLatticeMetric,
)

from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.case_expansion import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.model import (
    Periodic3DRankNAnalyticCase,
    Periodic3DRankNGaugeNormalizationEnum,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.verification import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerification,
    Periodic3DRankNBandEquivalenceHoppingLocalityVerification,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNBandEquivalenceHoppingLocalityRequest:
    """Freeze exact three-dimensional controls before aggregate analysis exists."""

    @staticmethod
    def _simple_metric(scale: float = 1.0) -> DirectLatticeMetric:
        return DirectLatticeMetric(
            DirectLattice3D(
                a1=np.array((scale, 0.0, 0.0), dtype=np.float64),
                a2=np.array((0.0, scale, 0.0), dtype=np.float64),
                a3=np.array((0.0, 0.0, scale), dtype=np.float64),
            )
        )

    def _request(
        self,
        family: Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
        simple_bonds = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        cases: tuple[Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition, ...]
        if family is Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL:
            cases = (
                Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="simple-cubic-axis-control",
                    positive_bonds=simple_bonds,
                    gauge_normalization=(
                        Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
                    ),
                    direct_metric=self._simple_metric(),
                    shell_metric_scale=1.0,
                ),
            )
            attacks = (0.0, math.pi / 8.0, math.pi / 4.0)
            shell_cap = 9
        else:
            fcc_bonds = (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (-1, 1, 0),
                (-1, 0, 1),
                (0, -1, 1),
            )
            fcc_metric = DirectLatticeMetric(
                BravaisLattice.cubic_face_centered().direct_lattice
            )
            cases = (
                Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="matched-simple-cubic-bravais-control",
                    positive_bonds=simple_bonds,
                    gauge_normalization=(
                        Periodic3DRankNGaugeNormalizationEnum.BOND_RMS
                    ),
                    direct_metric=self._simple_metric(math.sqrt(0.5)),
                    shell_metric_scale=2.0,
                ),
                Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="fcc-bravais-control",
                    positive_bonds=fcc_bonds,
                    gauge_normalization=(
                        Periodic3DRankNGaugeNormalizationEnum.BOND_RMS
                    ),
                    direct_metric=fcc_metric,
                    shell_metric_scale=2.0,
                ),
                Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="fcc-two-basis-metric-control",
                    positive_bonds=fcc_bonds,
                    gauge_normalization=(
                        Periodic3DRankNGaugeNormalizationEnum.BOND_RMS
                    ),
                    direct_metric=fcc_metric,
                    shell_metric_scale=2.0,
                    basis_offsets=((0.0, 0.0, 0.0), (0.25, 0.25, 0.25)),
                ),
            )
            attacks = (
                0.0,
                math.pi / (8.0 * math.sqrt(12.0)),
                math.pi / (4.0 * math.sqrt(12.0)),
            )
            shell_cap = 7
        return Periodic3DRankNBandEquivalenceHoppingLocalityRequest(
            family=family,
            cases=cases,
            retained_ranks=(3, 4, 8),
            circuit_depths=(1, 2, 4),
            construction_size=8,
            evaluation_size=17,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            attack_coefficients=attacks,
            band_tolerances=(1.0e-3, 1.0e-5),
            gauge_alignments=(
                Periodic3DRankNGaugeAlignment.IDENTITY,
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
                Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            ),
            shell_cap=shell_cap,
            procrustes_rank_cutoff_rule=(
                ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM
            ),
            procrustes_rank_absolute=1.0e-12,
            procrustes_rank_relative=1.0e-10,
            procrustes_validation_absolute=1.0e-12,
            procrustes_validation_relative=1.0e-10,
            transport_rank_absolute=1.0e-10,
            transport_rank_relative=1.0e-12,
            norm_energy_scale=1.0,
        )

    @pytest.mark.parametrize(
        "family, expected_count",
        (
            (Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL, 54),
            (
                Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.NONORTHOGONAL,
                162,
            ),  # noqa: E501
        ),
    )
    def test_round_trips_and_expands_the_complete_inventory(
        self,
        family: Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum,
        expected_count: int,
    ) -> None:
        request = self._request(family)
        encoded = request.to_json()

        decoded = Periodic3DRankNBandEquivalenceHoppingLocalityRequest.from_json(
            encoded
        )  # noqa: E501
        expanded = Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=decoded
        ).execute()

        assert decoded.to_json() == encoded
        assert decoded.case_count == expected_count
        assert decoded.band_subspace_ranks == decoded.retained_ranks
        assert len(expanded) == expected_count
        assert all(type(case) is Periodic3DRankNAnalyticCase for case in expanded)
        assert len({case.model_identity for case in expanded}) == expected_count
        assert {case.retained_rank for case in expanded} == {3, 4, 8}
        assert {case.circuit_depth for case in expanded} == {1, 2, 4}
        assert decoded.procrustes_tolerance.rank_cutoff_rule is (
            ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM
        )
        assert decoded.procrustes_tolerance.rank_absolute == 1.0e-12
        assert decoded.procrustes_tolerance.rank_relative == 1.0e-10
        assert decoded.procrustes_tolerance.validation_absolute == 1.0e-12
        assert decoded.procrustes_tolerance.validation_relative == 1.0e-10
        assert decoded.gauge_alignments == (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )

    def test_wire_identities_name_both_aggregate_operands(self) -> None:
        identities = (
            *(
                family.to_wire()
                for family in Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum
            ),
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis.WIRE_IDENTITY,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerification.WIRE_IDENTITY,
            Periodic3DRankNBandEquivalenceHoppingLocalityVerification.WIRE_IDENTITY,
        )

        assert all("band-equivalence-hopping-locality" in value for value in identities)
        assert all("band-equivalence-locality" not in value for value in identities)

    def test_rejects_an_unselected_gauge_alignment_inventory(self) -> None:
        request = self._request(
            Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL
        )

        with pytest.raises(ValueError, match="gauge_alignments"):
            replace(
                request,
                gauge_alignments=request.gauge_alignments[:-1],
            )

    def test_rejects_an_unselected_procrustes_policy(self) -> None:
        request = self._request(
            Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL
        )

        with pytest.raises(ValueError, match="procrustes_rank_cutoff_rule"):
            replace(
                request,
                procrustes_rank_cutoff_rule=(
                    ComplexUnitaryProcrustesRankCutoffRule.ADDITIVE
                ),
            )
        with pytest.raises(ValueError, match="procrustes_rank_absolute"):
            replace(request, procrustes_rank_absolute=1.0e-10)

    def test_rejects_a_rank_two_or_mismatched_geometry_inventory(self) -> None:
        request = self._request(
            Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL
        )
        with pytest.raises(ValueError, match="retained_ranks"):
            Periodic3DRankNBandEquivalenceHoppingLocalityRequest(
                family=request.family,
                cases=request.cases,
                retained_ranks=(2, 3, 4),
                circuit_depths=request.circuit_depths,
                construction_size=request.construction_size,
                evaluation_size=request.evaluation_size,
                evaluation_shift=request.evaluation_shift,
                parent_scales=request.parent_scales,
                attack_coefficients=request.attack_coefficients,
                band_tolerances=request.band_tolerances,
                gauge_alignments=request.gauge_alignments,
                shell_cap=request.shell_cap,
                procrustes_rank_cutoff_rule=request.procrustes_rank_cutoff_rule,
                procrustes_rank_absolute=request.procrustes_rank_absolute,
                procrustes_rank_relative=request.procrustes_rank_relative,
                procrustes_validation_absolute=(request.procrustes_validation_absolute),
                procrustes_validation_relative=(request.procrustes_validation_relative),
                transport_rank_absolute=request.transport_rank_absolute,
                transport_rank_relative=request.transport_rank_relative,
                norm_energy_scale=request.norm_energy_scale,
            )
        with pytest.raises(ValueError, match="geometry inventory"):
            Periodic3DRankNBandEquivalenceHoppingLocalityRequest(
                family=(
                    Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.NONORTHOGONAL
                ),
                cases=request.cases,
                retained_ranks=request.retained_ranks,
                circuit_depths=request.circuit_depths,
                construction_size=request.construction_size,
                evaluation_size=request.evaluation_size,
                evaluation_shift=request.evaluation_shift,
                parent_scales=request.parent_scales,
                attack_coefficients=(
                    0.0,
                    math.pi / (8.0 * math.sqrt(12.0)),
                    math.pi / (4.0 * math.sqrt(12.0)),
                ),
                band_tolerances=request.band_tolerances,
                gauge_alignments=request.gauge_alignments,
                shell_cap=7,
                procrustes_rank_cutoff_rule=request.procrustes_rank_cutoff_rule,
                procrustes_rank_absolute=request.procrustes_rank_absolute,
                procrustes_rank_relative=request.procrustes_rank_relative,
                procrustes_validation_absolute=(request.procrustes_validation_absolute),
                procrustes_validation_relative=(request.procrustes_validation_relative),
                transport_rank_absolute=request.transport_rank_absolute,
                transport_rank_relative=request.transport_rank_relative,
                norm_energy_scale=request.norm_energy_scale,
            )
