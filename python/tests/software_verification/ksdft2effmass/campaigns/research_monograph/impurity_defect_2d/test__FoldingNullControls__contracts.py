r"""Software verification of maintained folding and null-alignment controls.

Evidence profile: routine

These tests exercise authored dimensionless scalar hopping data only. They do not read
accepted-parent evidence, restore historical calculation runners, authorize protected
execution, or establish material validation, convergence, or uncertainty estimates.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
from projectkoios.physkit.units import Unitless

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FoldingNullAlignmentAttack,
    FoldingNullCalculationWorkflow,
    FoldingNullCase,
    FoldingNullCaseResult,
    FoldingNullIndependentVerificationWorkflow,
    FoldingNullIndependentVerifier,
    FoldingNullResult,
    FoldingNullResultJsonSerializer,
    FoldingNullStudyDefinition,
    FoldingNullTolerances,
)
from ksdft2effmass.solidstate import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeDimension,
    LatticeDisplacement,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestFoldingNullControls:
    """Own software verification of typed folding/null-control synthetic behavior."""

    def test__FoldingNullControls__method__workflow__retains_adopted_null_and_folding_inventory(  # noqa: E501
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-FOLD-001.

        Requirement: The control suite retains two shapes, four twists, finite
        folding diagnostics, and known-map null-extraction diagnostics.

        Acceptance: Eight cases pass prospective criteria and independent Kronecker
        reconstruction within the declared verification tolerance.
        """
        calculation = FoldingNullCalculationWorkflow().execute(self.definition())
        verification = FoldingNullIndependentVerificationWorkflow().execute(
            calculation.serialized_result,
            verification_relative_tolerance=1.0e-10,
            verification_absolute_tolerance=5.0e-13,
        )

        assert len(calculation.result.cases) == 8
        assert calculation.result.passes
        assert verification.verification.passes
        assert verification.verification.maximum_metric_absolute_difference < 5.0e-13
        assert b'"calculation_status": "calculated_synthetic_result"' in (
            calculation.serialized_result
        )

    def test__FoldingNullControls__artifact__serialization__is_canonical_and_rejects_wire_mutation(  # noqa: E501
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-FOLD-002.

        Requirement: Folding/null result bytes preserve exact typed definition and
        result identity while rejecting unsupported wire identities.

        Acceptance: Canonical round-trip is byte-exact and a record-type mutation is
        rejected before numerical interpretation.
        """
        calculation = FoldingNullCalculationWorkflow().execute(
            self.compact_definition()
        )
        serializer = FoldingNullResultJsonSerializer()

        assert (
            serializer.serialize(serializer.deserialize(calculation.serialized_result))
            == calculation.serialized_result
        )
        mutated = calculation.serialized_result.replace(
            b'"record_type": "periodic2d_rank_defect_folding_null_result"',
            b'"record_type": "unsupported_folding_null_result"',
            1,
        )
        with pytest.raises(ValueError, match="record_type"):
            serializer.deserialize(mutated)

    def test__FoldingNullControls__method__independent_verifier__detects_metric_substitution(  # noqa: E501
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-FOLD-003.

        Requirement: Independent verification detects retained metric substitution
        even when the substituted value remains below the campaign criterion.

        Acceptance: Criterion correlation remains unchanged while arithmetic
        reconstruction fails.
        """
        definition = replace(
            self.compact_definition(),
            tolerances=FoldingNullTolerances(1.0e-3, 1.0e-3),
        )
        retained = FoldingNullCalculationWorkflow().execute(definition).result
        first = retained.cases[0]
        substituted = FoldingNullCaseResult(
            first.case,
            replace(
                first.folding,
                off_diagonal_maximum_absolute=(
                    first.folding.off_diagonal_maximum_absolute + 1.0e-6
                ),
            ),
            first.null_extraction,
        )
        mutated = FoldingNullResult(
            retained.definition,
            (substituted, *retained.cases[1:]),
            (),
        )

        verification = FoldingNullIndependentVerifier().execute(
            mutated,
            relative_tolerance=1.0e-10,
            absolute_tolerance=5.0e-13,
        )

        assert verification.criteria_match
        assert not verification.reconstruction_passed
        assert not verification.passes

    def test__FoldingNullControls__method__criterion_evaluation__retains_reconstructed_failure(  # noqa: E501
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-FOLD-004.

        Requirement: A reproduced criterion failure remains a retained numerical
        outcome and is not converted into verifier failure.

        Acceptance: Zero algebraic tolerances yield named failures while independent
        reconstruction and exact failure correlation still pass.
        """
        definition = replace(
            self.compact_definition(),
            tolerances=FoldingNullTolerances(0.0, 0.0),
        )
        calculation = FoldingNullCalculationWorkflow().execute(definition)
        verification = FoldingNullIndependentVerificationWorkflow().execute(
            calculation.serialized_result,
            verification_relative_tolerance=1.0e-10,
            verification_absolute_tolerance=5.0e-13,
        )

        assert not calculation.result.passes
        assert calculation.result.failed_criteria
        assert verification.verification.reconstruction_passed
        assert verification.verification.criteria_match
        assert verification.verification.passes

    def test__FoldingNullControls__contract__definition__rejects_nonhermitian_parent(
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-FOLD-005.

        Requirement: Finite folding admits only explicitly Hermitian scalar hopping
        inventories.

        Acceptance: Removing one reverse hopping term is rejected at definition
        construction rather than producing complex primitive energies later.
        """
        definition = self.compact_definition()
        parent = replace(
            definition.parent,
            terms=definition.parent.terms[:-1],
        )

        with pytest.raises(ValueError, match="Hermitian"):
            replace(definition, parent=parent)

    @classmethod
    def definition(cls) -> FoldingNullStudyDefinition:
        """Return the adopted eight-case authored folding/null-control definition."""
        cases = tuple(
            FoldingNullCase(
                identifier=f"shape-{extent}.twist-{twist_index}",
                shape=FiniteLatticeShape(LatticeDimension.TWO, (extent, extent)),
                twist=BoundaryTwistLift(LatticeDimension.TWO, twist),
            )
            for extent in (6, 8)
            for twist_index, twist in enumerate(
                ((0.0, 0.0), (0.37, -0.23), (0.5, 0.0), (0.0, 0.5))
            )
        )
        return cls._definition(cases)

    @classmethod
    def compact_definition(cls) -> FoldingNullStudyDefinition:
        """Return one compact folding/null definition for mutation tests."""
        return cls._definition(
            (
                FoldingNullCase(
                    identifier="compact-3x4",
                    shape=FiniteLatticeShape(LatticeDimension.TWO, (3, 4)),
                    twist=BoundaryTwistLift(LatticeDimension.TWO, (0.37, -0.23)),
                ),
            )
        )

    @staticmethod
    def _definition(
        cases: tuple[FoldingNullCase, ...],
    ) -> FoldingNullStudyDefinition:
        """Construct one dimensionless authored definition with frozen controls."""
        terms = tuple(
            ScalarHoppingTerm(
                LatticeDisplacement(LatticeDimension.TWO, displacement),
                real,
                0.0,
            )
            for displacement, real in (
                ((-1, 0), -0.10),
                ((0, -1), -0.08),
                ((0, 0), 0.20),
                ((0, 1), -0.08),
                ((1, 0), -0.10),
            )
        )
        parent = ScalarHoppingModel(
            identifier="authored-folding-null-parent",
            dimension=LatticeDimension.TWO,
            terms=terms,
            energy_unit=Unitless(),
            energy_reference="authored-folding-null-zero",
            basis_identifier="scalar-cell-basis",
        )
        return FoldingNullStudyDefinition(
            identifier="periodic2d-rank-defect.folding-null-controls.v1",
            parent=parent,
            cases=cases,
            null_attack=FoldingNullAlignmentAttack(
                translation_cells=(1, 1),
                site_phase_steps_radians=(0.137, -0.191),
                energy_reference_shift=0.137,
            ),
            tolerances=FoldingNullTolerances(1.0e-11, 1.0e-11),
        )
