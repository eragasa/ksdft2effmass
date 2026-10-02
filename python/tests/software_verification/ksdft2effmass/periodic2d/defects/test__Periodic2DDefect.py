r"""Software verification of ``Periodic2DDefect``.

Evidence profile: claim_bearing

Bounded artifact scope: sparse representation of a periodic scalar parent modified by
one finite-support perturbation.

VVUQ and scientific exclusions

A pass establishes represented operator composition. It does not establish material
validity, continuum convergence, scientific validation, or uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic2DDefect,
    Periodic2DDefectLocalityResult,
    Periodic2DDefectModel,
    Periodic2DDefectRepresentationResult,
)
from ksdft2effmass.operators import PhysicalUnit, ScalarQuantity
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DDefect


class TestPeriodic2DDefect:
    """Own finite-extent periodic-2D defect representation evidence."""

    @staticmethod
    def _bulk() -> ScalarHoppingModel:
        return ScalarHoppingModel(
            "bulk",
            LatticeDimension.TWO,
            (
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.TWO, (0, 0)), 1.0, 0.0
                ),
            ),
            PhysicalUnit("electron_volt"),
            "bulk_zero",
            "scalar_cell_basis",
        )

    @classmethod
    def _onsite_defect(cls) -> Periodic2DDefect:
        perturbation = LocalizedPerturbation(
            "one_site_potential",
            LatticeDimension.TWO,
            (
                LocalizedOnsiteTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (0, 0)), 0.5, 0.0
                ),
            ),
            PhysicalUnit("electron_volt"),
            "bulk_zero",
            "scalar_cell_basis",
        )
        return SUT(Periodic2DDefectModel("finite_extent", cls._bulk(), perturbation))

    def test_method__represent__adds_finite_onsite_potential_to_bulk(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-001

        Requirement: An onsite finite-support perturbation remains separate from the
        periodic bulk while their compatible represented sum is retained.

        Method: Add a one-site ``0.5 eV`` perturbation to a ``3 x 3`` unit onsite
        parent at a nonzero boundary twist.

        Oracle: Explicit diagonal bulk, perturbation, and defect matrices.

        Acceptance: The perturbation changes exactly one represented diagonal entry and
        the defect operator equals the sparse bulk-plus-perturbation sum.

        Interpretation: A pass establishes finite represented support and composition.

        Limitations: The synthetic onsite model is not a material potential.
        """
        defect = self._onsite_defect()

        result = defect.represent(
            shape=FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
            twist=BoundaryTwistLift(LatticeDimension.TWO, (0.25, -0.125)),
        )

        assert type(result) is Periodic2DDefectRepresentationResult
        assert defect.model.represents_onsite_potential
        np.testing.assert_array_equal(
            result.bulk_operator.matrix.to_csr().toarray(), np.eye(9)
        )
        expected_perturbation = np.zeros((9, 9), dtype=np.complex128)
        expected_perturbation[0, 0] = 0.5
        np.testing.assert_array_equal(
            result.perturbation_operator.matrix.to_csr().toarray(),
            expected_perturbation,
        )
        np.testing.assert_array_equal(
            result.defect_operator.matrix.to_csr().toarray(),
            np.eye(9) + expected_perturbation,
        )
        assert result.compatibility.compatible

    def test_method__extract__recovers_finite_perturbation_from_defect(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-003

        Requirement: A compatible modified operator and bulk operator determine the
        represented perturbation by direct subtraction.

        Method: Represent the one-site synthetic defect, then extract the perturbation
        from the retained bulk and defect operators.

        Oracle: Independently retained planted perturbation representation.

        Acceptance: Extracted and planted sparse matrices agree exactly.

        Interpretation: A pass establishes the bounded represented extraction route.

        Limitations: Inputs are already aligned; no basis or energy-zero inference is
        performed.
        """
        defect = self._onsite_defect()
        represented = defect.represent(
            shape=FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
            twist=BoundaryTwistLift(LatticeDimension.TWO, (0.25, -0.125)),
        )

        extracted = defect.extract(
            bulk_operator=represented.bulk_operator,
            defect_operator=represented.defect_operator,
        )

        assert extracted.compatibility.compatible
        np.testing.assert_array_equal(
            extracted.perturbation_operator.matrix.to_csr().toarray(),
            represented.perturbation_operator.matrix.to_csr().toarray(),
        )

    def test_method__analyze_locality__confirms_one_site_extent(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-004

        Requirement: Finite extent is an explicit partition-resolved finding rather
        than an inference from the model label.

        Method: Analyze the one-site perturbation about its exact origin with a
        zero-radius core and zero exterior tolerances.

        Oracle: The represented difference has no exterior or core-exterior entries.

        Acceptance: Both excluded-region norms are exactly zero and disposition passes.

        Interpretation: A pass establishes bounded finite-extent analysis.

        Limitations: The selected core and tolerances are authored synthetic controls.
        """
        defect = self._onsite_defect()
        represented = defect.represent(
            shape=FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
            twist=BoundaryTwistLift(LatticeDimension.TWO, (0.25, -0.125)),
        )
        zero_energy = ScalarQuantity(0.0, PhysicalUnit("electron_volt"))

        result = defect.analyze_locality(
            bulk_operator=represented.bulk_operator,
            defect_operator=represented.defect_operator,
            origin=LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
            core_radius=0,
            exterior_frobenius_tolerance=zero_energy,
            core_exterior_frobenius_tolerance=zero_energy,
        )

        assert type(result) is Periodic2DDefectLocalityResult
        assert result.residual.core_frobenius_residual == 0.5
        assert result.residual.exterior_frobenius_residual == 0.0
        assert result.residual.core_exterior_frobenius_residual == 0.0
        assert result.passes

    def test_method__analyze_locality__rejects_core_crossing_bond(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-005

        Requirement: A perturbation crossing the declared core boundary must not pass
        the finite-extent criterion for that core.

        Method: Represent a Hermitian nearest-neighbor bond change and analyze it using
        a zero-radius core with zero excluded-region tolerances.

        Oracle: The bond and its reverse couple the core to one exterior site.

        Acceptance: The core--exterior norm is positive and disposition is false.

        Interpretation: A pass establishes that locality is measured, not assumed.

        Limitations: This synthetic bond change is not a fitted material defect.
        """
        perturbation = LocalizedPerturbation(
            "hermitian_bond_change",
            LatticeDimension.TWO,
            (
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
                    LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
                    0.1,
                    0.0,
                ),
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (1, 0)),
                    LatticeDisplacement(LatticeDimension.TWO, (-1, 0)),
                    0.1,
                    0.0,
                ),
            ),
            PhysicalUnit("electron_volt"),
            "bulk_zero",
            "scalar_cell_basis",
        )
        defect = SUT(Periodic2DDefectModel("bond_defect", self._bulk(), perturbation))
        represented = defect.represent(
            shape=FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
            twist=BoundaryTwistLift(LatticeDimension.TWO, (0.0, 0.0)),
        )
        zero_energy = ScalarQuantity(0.0, PhysicalUnit("electron_volt"))

        result = defect.analyze_locality(
            bulk_operator=represented.bulk_operator,
            defect_operator=represented.defect_operator,
            origin=LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
            core_radius=0,
            exterior_frobenius_tolerance=zero_energy,
            core_exterior_frobenius_tolerance=zero_energy,
        )

        assert result.residual.core_exterior_frobenius_residual > 0.0
        assert not result.passes

    def test_property__represents_onsite_potential__distinguishes_bond_change(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-002

        Requirement: The model must not call an off-diagonal bond perturbation a scalar
        potential.

        Method: Encapsulate one directed finite-support nearest-neighbor bond change.

        Oracle: Exact localized-term semantic type.

        Acceptance: ``represents_onsite_potential`` is false.

        Interpretation: A pass preserves the potential/operator distinction.

        Limitations: Hermiticity requires a separately declared reverse bond.
        """
        perturbation = LocalizedPerturbation(
            "directed_bond_change",
            LatticeDimension.TWO,
            (
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
                    LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
                    0.1,
                    0.0,
                ),
            ),
            PhysicalUnit("electron_volt"),
            "bulk_zero",
            "scalar_cell_basis",
        )

        model = Periodic2DDefectModel("bond_defect", self._bulk(), perturbation)

        assert not model.represents_onsite_potential
