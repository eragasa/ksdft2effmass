"""Software verification for focused parent-qualification comparison."""

from __future__ import annotations

from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2 import (
    parent_scale,
)

pytestmark = pytest.mark.software_verification
QualificationVerificationAssessor = (
    parent_scale.Periodic1DRank2QualificationVerificationAssessor
)
ExternalGapFailure = parent_scale.Periodic1DRank2ExternalGapFailure
QualifiedParent = parent_scale.Periodic1DRank2QualifiedParent


class TestPeriodic1DRank2QualificationVerificationAssessor:
    """Compare closed qualification variants without caller-owned mutation."""

    def test_assess__qualified_parents__compares_all_scalar_channels(self) -> None:
        reference = QualifiedParent(
            minimum_external_gap=1.0,
            minimum_transport_singular_value=0.9,
            maximum_transport_rank_cutoff=1.0e-14,
            maximum_transport_unitarity_defect=2.0e-14,
            maximum_primitive_link_frobenius_residual=3.0e-14,
            closure_holonomy_phases=(-0.2, 0.3),
            closure_alignment_residual=4.0e-14,
            closure_alignment_unitarity_defect=5.0e-14,
            maximum_frame_orthonormality_defect=6.0e-14,
            maximum_reference_hermiticity_defect=7.0e-14,
        )
        observed = replace(
            reference,
            minimum_external_gap=1.0 + 5.0e-12,
            maximum_transport_unitarity_defect=2.0e-12,
            closure_holonomy_phases=(-0.2, 0.3 + 4.0e-12),
        )

        verification = QualificationVerificationAssessor(
            observed=observed,
            reference=reference,
            tolerance=1.0e-10,
        ).assess()

        assert set(verification.observations) == {
            "qualification_variant_defect",
            "minimum_external_gap_absolute_defect",
            "qualification_scalar_maximum_absolute_defect",
            "closure_phase_maximum_absolute_defect",
        }
        assert verification.passed

    def test_assess__different_variants__reports_variant_defect(self) -> None:
        observed = ExternalGapFailure(minimum_external_gap=1.0)
        reference = QualifiedParent(
            minimum_external_gap=1.0,
            minimum_transport_singular_value=0.9,
            maximum_transport_rank_cutoff=0.0,
            maximum_transport_unitarity_defect=0.0,
            maximum_primitive_link_frobenius_residual=0.0,
            closure_holonomy_phases=(-0.2, 0.3),
            closure_alignment_residual=0.0,
            closure_alignment_unitarity_defect=0.0,
            maximum_frame_orthonormality_defect=0.0,
            maximum_reference_hermiticity_defect=0.0,
        )

        verification = QualificationVerificationAssessor(
            observed=observed,
            reference=reference,
            tolerance=1.0e-10,
        ).assess()

        assert set(verification.observations) == {
            "qualification_variant_defect",
            "minimum_external_gap_absolute_defect",
        }
        assert not verification.passed

    @pytest.mark.parametrize("tolerance", (True, 1, "1.0"))
    def test_init__rejects_non_float_tolerance(
        self,
        tolerance: bool | int | str,
    ) -> None:
        outcome = ExternalGapFailure(minimum_external_gap=1.0)

        with pytest.raises(TypeError, match="tolerance must be a built-in float"):
            QualificationVerificationAssessor(
                observed=outcome,
                reference=outcome,
                tolerance=tolerance,  # type: ignore[arg-type]
            )
