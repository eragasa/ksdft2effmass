"""Periodic-2D arbitrary-rank aggregate request and case-expansion contracts."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

from ksdft2effmass.periodic.operators import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisInventory,
    PeriodicBasisInventoryEntry,
)
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.case import (
    Periodic2DRankNParentGaugeCase,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.verification import (  # noqa: E501
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification,
    Periodic2DRankNBandEquivalenceHoppingLocalityVerification,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.definition import (
    Periodic2DRankNGaugeAlignment,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.transformation import (
    Periodic2DRankNGaugeNormalizationEnum,
)
from periodic2d_rankn_analytic_case_support import (
    SyntheticPeriodic2DRankNCaseExpander,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

_TEST_BASIS_INVENTORY = PeriodicBasisInventory(
    entries=tuple(
        PeriodicBasisInventoryEntry(
            retained_rank=rank,
            basis_identity=Periodic2DBasisIdentity(
                display_identifier=f"periodic2d-rankN-test-basis-r{rank}",
                coordinates=tuple(
                    LabeledComponentBasisCoordinate(
                        label=f"test-retained-orbital-{index:02d}"
                    )
                    for index in range(rank)
                ),
            ),
        )
        for rank in (3, 4, 8)
    )
)


class TestPeriodic2DRankNBandEquivalenceHoppingLocalityRequest:
    """Freeze exact dimension-owned controls before aggregate analysis exists."""

    @staticmethod
    def _square_metric() -> DirectLatticeMetric:
        return DirectLatticeMetric(
            DirectLattice2D(
                a1=np.array((1.0, 0.0), dtype=np.float64),
                a2=np.array((0.0, 1.0), dtype=np.float64),
            )
        )

    @staticmethod
    def _triangular_metric() -> DirectLatticeMetric:
        return DirectLatticeMetric(
            DirectLattice2D(
                a1=np.array((1.0, 0.0), dtype=np.float64),
                a2=np.array((0.5, math.sqrt(3.0) / 2.0), dtype=np.float64),
            )
        )

    def _request(
        self,
        family: Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum,
    ) -> Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
        cases: tuple[Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition, ...]
        if family is Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL:
            cases = (
                Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="square-axis-control",
                    positive_bonds=((1, 0), (0, 1)),
                    gauge_normalization=(
                        Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
                    ),
                    direct_metric=self._square_metric(),
                    shell_metric_scale=1.0,
                ),
            )
            transformations = (0.0, math.pi / 8.0, math.pi / 4.0)
            shell_cap = 25
        else:
            triangular_bonds = ((1, 0), (0, 1), (1, -1))
            cases = (
                Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="matched-square-bravais-control",
                    positive_bonds=((1, 0), (0, 1)),
                    gauge_normalization=(
                        Periodic2DRankNGaugeNormalizationEnum.BOND_RMS
                    ),
                    direct_metric=self._square_metric(),
                    shell_metric_scale=1.0,
                ),
                Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="triangular-bravais-control",
                    positive_bonds=triangular_bonds,
                    gauge_normalization=(
                        Periodic2DRankNGaugeNormalizationEnum.BOND_RMS
                    ),
                    direct_metric=self._triangular_metric(),
                    shell_metric_scale=1.0,
                ),
                Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition(
                    identifier="triangular-two-basis-metric-control",
                    positive_bonds=triangular_bonds,
                    gauge_normalization=(
                        Periodic2DRankNGaugeNormalizationEnum.BOND_RMS
                    ),
                    direct_metric=self._triangular_metric(),
                    shell_metric_scale=1.0,
                    basis_offsets=((0.0, 0.0), (1.0 / 3.0, 1.0 / 3.0)),
                ),
            )
            transformations = (
                0.0,
                math.pi / (8.0 * math.sqrt(6.0)),
                math.pi / (4.0 * math.sqrt(6.0)),
            )
            shell_cap = 21
        return Periodic2DRankNBandEquivalenceHoppingLocalityRequest(
            family=family,
            cases=cases,
            retained_ranks=(3, 4, 8),
            circuit_depths=(1, 2, 4),
            construction_size=16,
            evaluation_size=33,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            transformation_coefficients=transformations,
            band_tolerances=(1.0e-3, 1.0e-5),
            gauge_alignments=(
                Periodic2DRankNGaugeAlignment.IDENTITY,
                Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY,
                Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
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
            (Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL, 54),
            (
                Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.NONORTHOGONAL,
                162,
            ),  # noqa: E501
        ),
    )
    def test_round_trips_and_expands_the_complete_inventory(
        self,
        family: Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum,
        expected_count: int,
    ) -> None:
        request = self._request(family)
        encoded = request.to_json()

        decoded = Periodic2DRankNBandEquivalenceHoppingLocalityRequest.from_json(
            encoded
        )  # noqa: E501
        expanded = SyntheticPeriodic2DRankNCaseExpander(
            request=decoded,
            basis_inventory=_TEST_BASIS_INVENTORY,
        ).execute()

        assert decoded.to_json() == encoded
        assert decoded.case_count == expected_count
        assert decoded.band_subspace_ranks == decoded.retained_ranks
        assert len(expanded) == expected_count
        assert all(type(case) is Periodic2DRankNParentGaugeCase for case in expanded)
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
            Periodic2DRankNGaugeAlignment.IDENTITY,
            Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )

    def test_wire_identities_name_both_aggregate_operands(self) -> None:
        identities = (
            *(
                family.to_wire()
                for family in Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum
            ),
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis.WIRE_IDENTITY,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification.WIRE_IDENTITY,
            Periodic2DRankNBandEquivalenceHoppingLocalityVerification.WIRE_IDENTITY,
        )

        assert all("band-equivalence-hopping-locality" in value for value in identities)
        assert all("band-equivalence-locality" not in value for value in identities)

    def test_rejects_an_unselected_gauge_alignment_inventory(self) -> None:
        request = self._request(
            Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL
        )

        with pytest.raises(ValueError, match="gauge_alignments"):
            replace(
                request,
                gauge_alignments=request.gauge_alignments[:-1],
            )

    def test_rejects_an_unselected_procrustes_policy(self) -> None:
        request = self._request(
            Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL
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
            Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL
        )
        with pytest.raises(ValueError, match="retained_ranks"):
            Periodic2DRankNBandEquivalenceHoppingLocalityRequest(
                family=request.family,
                cases=request.cases,
                retained_ranks=(2, 3, 4),
                circuit_depths=request.circuit_depths,
                construction_size=request.construction_size,
                evaluation_size=request.evaluation_size,
                evaluation_shift=request.evaluation_shift,
                parent_scales=request.parent_scales,
                transformation_coefficients=request.transformation_coefficients,
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
            Periodic2DRankNBandEquivalenceHoppingLocalityRequest(
                family=(
                    Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.NONORTHOGONAL
                ),
                cases=request.cases,
                retained_ranks=request.retained_ranks,
                circuit_depths=request.circuit_depths,
                construction_size=request.construction_size,
                evaluation_size=request.evaluation_size,
                evaluation_shift=request.evaluation_shift,
                parent_scales=request.parent_scales,
                transformation_coefficients=(
                    0.0,
                    math.pi / (8.0 * math.sqrt(6.0)),
                    math.pi / (4.0 * math.sqrt(6.0)),
                ),
                band_tolerances=request.band_tolerances,
                gauge_alignments=request.gauge_alignments,
                shell_cap=21,
                procrustes_rank_cutoff_rule=request.procrustes_rank_cutoff_rule,
                procrustes_rank_absolute=request.procrustes_rank_absolute,
                procrustes_rank_relative=request.procrustes_rank_relative,
                procrustes_validation_absolute=(request.procrustes_validation_absolute),
                procrustes_validation_relative=(request.procrustes_validation_relative),
                transport_rank_absolute=request.transport_rank_absolute,
                transport_rank_relative=request.transport_rank_relative,
                norm_energy_scale=request.norm_energy_scale,
            )
