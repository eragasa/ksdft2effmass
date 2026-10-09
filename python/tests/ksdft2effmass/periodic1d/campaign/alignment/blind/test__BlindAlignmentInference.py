# ruff: noqa: E501
r"""Software verification for ``BlindAlignmentInference``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns the public Action that infers a candidate-to-reference partial
isometry, scalar energy shift, and identified-sector perturbation from explicit finite
matrix observations.

Intrinsic and cross-object scope
--------------------------------
The tests use hand-constructed finite operators and unitary or partial-isometry maps as
independent exact oracles. They cover full, square-partial, rectangular-partial, and
structured-stop behavior without using a retained runner implementation.

VVUQ and scientific exclusions
------------------------------
This is software verification with bounded analytical numerical checks. It does not
validate silicon, a dopant model, an electronic-structure alignment method,
transferability, uncertainty quantification, or a unique map on an unidentified
complement.
"""

from typing import Literal

import numpy as np
import pytest

from ksdft2effmass.periodic1d.campaign.alignment.blind.inference import (
    BlindAlignmentInference,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.records import (
    BlindAlignmentInferencePolicy,
    BlindAlignmentInferenceRequest,
    BlindAlignmentObservation,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.supercell_metadata import (
    BlindAlignmentSupercellMetadataAuthor,
)
from ksdft2effmass.periodic1d.campaign.extraction import matched as matched_extraction

RepresentedOperator = matched_extraction.RepresentedOperator
SupercellBasis = matched_extraction.SupercellBasis

type StopCase = Literal[
    "anchor_rank_zero",
    "ill_conditioned",
    "rank_deficient",
    "principal_angle",
    "spin_mismatch",
    "energy_anchor",
]

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]
SUT = BlindAlignmentInference


class TestBlindAlignmentInference:
    """Own observation-only blind-alignment inference evidence."""

    @staticmethod
    def make_basis(
        identifier: str,
        dimension: int,
        *,
        spin_count: int = 1,
        energy_reference: str = "reference-zero",
    ) -> SupercellBasis:
        """Construct comparison metadata for one small represented oracle."""
        if dimension % spin_count != 0:
            raise ValueError("test dimension must be divisible by spin count")
        return SupercellBasis(
            state_space_id=identifier,
            cell_count=dimension // spin_count,
            orbital_count=1,
            spin_count=spin_count,
            reduced_momentum=0.125,
            site_ordering="site-major",
            orbital_ordering="single-orbital",
            spin_ordering="spin-fastest",
            coordinate_frame=identifier,
            energy_unit="dimensionless-energy",
            energy_reference=energy_reference,
            geometry_id="blind-alignment-test-geometry",
            subspace_id="blind-alignment-test-subspace",
            operator_metadata=BlindAlignmentSupercellMetadataAuthor().execute(
                state_space_id=identifier,
                cell_count=dimension // spin_count,
                orbital_count=1,
                spin_count=spin_count,
                site_ordering="site-major",
                orbital_ordering="single-orbital",
                spin_ordering="spin-fastest",
                coordinate_frame=identifier,
                energy_reference=energy_reference,
                geometry_id="blind-alignment-test-geometry",
            ),
        )

    def make_operator(
        self,
        identifier: str,
        matrix: np.ndarray[tuple[int, int], np.dtype[np.complex128]],
        *,
        spin_count: int = 1,
        energy_reference: str = "reference-zero",
    ) -> RepresentedOperator:
        """Construct one represented operator with explicit comparison metadata."""
        return RepresentedOperator(
            identifier,
            self.make_basis(
                identifier,
                matrix.shape[0],
                spin_count=spin_count,
                energy_reference=energy_reference,
            ),
            matrix,
        )

    @staticmethod
    def make_policy() -> BlindAlignmentInferencePolicy:
        """Return the bounded analytical test policy."""
        return BlindAlignmentInferencePolicy(
            anchor_rank_tolerance=1.0e-10,
            maximum_anchor_condition_number=1.0e6,
            maximum_principal_angle_radians=0.35,
            minimum_energy_anchor_rank=2,
        )

    def make_full_request(
        self,
    ) -> tuple[BlindAlignmentInferenceRequest, np.ndarray, np.ndarray]:
        """Construct a full-rank observation and its exact perturbation oracle."""
        reference = np.diag(np.asarray((0.0, 1.0, 2.0, 3.0), dtype=np.complex128))
        perturbation = np.diag(np.asarray((0.2, 0.0, 0.0, 0.0), dtype=np.complex128))
        alignment = np.asarray(
            (
                (0.0, 1.0, 0.0, 0.0),
                (1.0j, 0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
                (0.0, 0.0, 1.0, 0.0),
            ),
            dtype=np.complex128,
        )
        shift = 0.4
        candidate = alignment.conj().T @ (
            reference + perturbation
        ) @ alignment + shift * np.eye(4, dtype=np.complex128)
        anchor = np.diag(np.asarray((1.0, 0.9, 0.8, 0.7))) @ alignment
        exterior = np.diag(np.asarray((0.0, 1.0, 1.0, 1.0)))
        request = BlindAlignmentInferenceRequest(
            BlindAlignmentObservation(
                identifier="full-rank",
                reference_operator=self.make_operator("reference", reference),
                candidate_operator=self.make_operator(
                    "candidate",
                    candidate,
                    energy_reference="candidate-shifted",
                ),
                anchor_cross_covariance=anchor,
                retained_subspace_overlap=np.eye(4, dtype=np.complex128),
                exterior_energy_anchor=exterior,
                allow_partial_alignment=False,
            ),
            self.make_policy(),
        )
        return request, perturbation, alignment

    def make_stop_request(self, case: StopCase) -> BlindAlignmentInferenceRequest:
        """Construct one observation adjacent to a structured stop boundary."""
        request, _, _ = self.make_full_request()
        observation = request.observation
        anchor = observation.anchor_cross_covariance.copy()
        overlap = observation.retained_subspace_overlap.copy()
        energy_anchor = observation.exterior_energy_anchor.copy()
        candidate = observation.candidate_operator
        allow_partial = False
        if case == "anchor_rank_zero":
            anchor[:] = 0.0
        elif case == "ill_conditioned":
            anchor = np.diag(np.asarray((1.0, 1.0, 1.0, 1.0e-8)))
        elif case == "rank_deficient":
            anchor = np.diag(np.asarray((1.0, 1.0, 1.0, 0.0)))
        elif case == "principal_angle":
            overlap[-1, -1] = np.cos(0.5)
        elif case == "spin_mismatch":
            candidate = self.make_operator(
                "spinor-candidate",
                candidate.matrix,
                spin_count=2,
                energy_reference="candidate-shifted",
            )
        elif case == "energy_anchor":
            energy_anchor[:] = 0.0
        return BlindAlignmentInferenceRequest(
            BlindAlignmentObservation(
                identifier=case,
                reference_operator=observation.reference_operator,
                candidate_operator=candidate,
                anchor_cross_covariance=anchor,
                retained_subspace_overlap=overlap,
                exterior_energy_anchor=energy_anchor,
                allow_partial_alignment=allow_partial,
            ),
            request.policy,
        )

    def test_method__execute__recovers_full_rank_map_shift_and_perturbation(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-004.

        Requirement: Full-rank inference must recover the polar alignment, exterior
        scalar shift, and represented perturbation without receiving hidden oracles.

        Method: Apply the Action to a four-dimensional candidate generated by a
        hand-authored unitary, one onsite perturbation, and a scalar shift.

        Oracle: Direct unitary conjugation and exact diagonal perturbation arithmetic.

        Acceptance: Status and rank agree exactly; map, projector, shift, and
        perturbation agree within absolute tolerance ``1e-12``.

        Interpretation: A pass establishes bounded full-rank inference behavior.

        Limitations: The authored cross-covariance is synthetic and exactly
        well-conditioned.
        """
        request, perturbation, alignment = self.make_full_request()

        result = SUT().execute(request)

        assert result.status == "aligned_full"
        assert result.anchor_rank == 4
        assert result.alignment_map is not None
        assert result.reference_projector is not None
        assert result.extracted_operator is not None
        np.testing.assert_allclose(result.alignment_map, alignment, atol=1e-12)
        np.testing.assert_allclose(result.reference_projector, np.eye(4), atol=1e-12)
        assert result.inferred_energy_shift == pytest.approx(0.4, abs=1e-12)
        np.testing.assert_allclose(result.extracted_operator, perturbation, atol=1e-12)

    def test_method__execute__limits_rank_deficient_result_to_identified_sector(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-005.

        Requirement: An explicitly admitted rank-deficient square anchor must return
        only the identified reference-sector extraction.

        Method: Use a diagonal rank-two anchor and an exterior anchor contained in its
        identified sector.

        Oracle: The hand-authored projector ``diag(1, 1, 0, 0)`` and direct compressed
        subtraction.

        Acceptance: Partial status, projector, shift, and compressed perturbation
        agree within absolute tolerance ``1e-12``.

        Interpretation: A pass establishes identified-sector semantics without
        assigning a map on the complement.

        Limitations: No uniqueness claim is made outside the two-dimensional sector.
        """
        reference = np.diag(np.asarray((0.0, 1.0, 2.0, 3.0), dtype=np.complex128))
        perturbation = np.diag(np.asarray((0.2, 0.0, 0.0, 0.0), dtype=np.complex128))
        shift = 0.3
        request = BlindAlignmentInferenceRequest(
            BlindAlignmentObservation(
                "square-partial",
                self.make_operator("reference", reference),
                self.make_operator(
                    "candidate",
                    reference + perturbation + shift * np.eye(4),
                    energy_reference="candidate-shifted",
                ),
                np.diag(np.asarray((1.0, 0.8, 0.0, 0.0))),
                np.eye(4, dtype=np.complex128),
                np.diag(np.asarray((0.0, 1.0, 0.0, 0.0))),
                True,
            ),
            BlindAlignmentInferencePolicy(1e-10, 1e6, 0.35, 1),
        )

        result = SUT().execute(request)

        assert result.status == "aligned_partial"
        assert result.reference_projector is not None
        assert result.extracted_operator is not None
        projector = np.diag(np.asarray((1.0, 1.0, 0.0, 0.0)))
        np.testing.assert_allclose(result.reference_projector, projector, atol=1e-12)
        assert result.inferred_energy_shift == pytest.approx(shift, abs=1e-12)
        np.testing.assert_allclose(
            result.extracted_operator,
            projector @ perturbation @ projector,
            atol=1e-12,
        )

    def test_method__execute_reconciled_partial__supports_rectangular_isometry(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-006.

        Requirement: Rectangular reconciliation must require its explicit route and
        recover a declared lower-dimensional common sector.

        Method: Embed a three-dimensional candidate into a four-dimensional reference
        through the first three coordinate vectors.

        Oracle: The exact embedding isometry and its diagonal rank-three projector.

        Acceptance: The direct route stops with ``RANK_MISMATCH``; the reconciled
        route returns the exact partial isometry, projector, scalar shift, and zero
        perturbation within ``1e-12``.

        Interpretation: A pass establishes explicit unequal-rank reconciliation.

        Limitations: The dropped direction and its operator action are unidentified.
        """
        reference = np.diag(np.asarray((0.0, 1.0, 2.0, 3.0), dtype=np.complex128))
        isometry = np.eye(4, 3, dtype=np.complex128)
        shift = 0.25
        candidate = isometry.conj().T @ reference @ isometry + shift * np.eye(
            3, dtype=np.complex128
        )
        request = BlindAlignmentInferenceRequest(
            BlindAlignmentObservation(
                "rectangular-partial",
                self.make_operator("reference", reference),
                self.make_operator(
                    "candidate", candidate, energy_reference="candidate-shifted"
                ),
                isometry @ np.diag(np.asarray((1.0, 0.9, 0.8))),
                isometry,
                np.diag(np.asarray((1.0, 1.0, 1.0, 0.0))),
                True,
            ),
            self.make_policy(),
        )
        actionizer = SUT()

        direct = actionizer.execute(request)
        result = actionizer.execute_reconciled_partial(request)

        assert direct.issue_codes == ("BLIND_ALIGNMENT.RANK_MISMATCH",)
        assert result.status == "aligned_partial"
        assert result.alignment_map is not None
        assert result.reference_projector is not None
        assert result.extracted_operator is not None
        np.testing.assert_allclose(result.alignment_map, isometry, atol=1e-12)
        np.testing.assert_allclose(
            result.reference_projector,
            np.diag(np.asarray((1.0, 1.0, 1.0, 0.0))),
            atol=1e-12,
        )
        assert result.inferred_energy_shift == pytest.approx(shift, abs=1e-12)
        np.testing.assert_allclose(result.extracted_operator, 0.0, atol=1e-12)

    @pytest.mark.parametrize(
        ("case", "issue_code"),
        (
            pytest.param(
                "anchor_rank_zero",
                "BLIND_ALIGNMENT.ANCHOR_RANK_ZERO",
                id="zero_anchor_rank",
            ),
            pytest.param(
                "ill_conditioned",
                "BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED",
                id="ill_conditioned_anchor",
            ),
            pytest.param(
                "rank_deficient",
                "BLIND_ALIGNMENT.ANCHOR_RANK_DEFICIENT",
                id="undeclared_rank_deficiency",
            ),
            pytest.param(
                "principal_angle",
                "BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED",
                id="retained_subspace_angle",
            ),
            pytest.param(
                "spin_mismatch",
                "BLIND_ALIGNMENT.SPIN_MISMATCH",
                id="spin_space_mismatch",
            ),
            pytest.param(
                "energy_anchor",
                "BLIND_ALIGNMENT.ENERGY_ANCHOR_INSUFFICIENT",
                id="insufficient_energy_anchor",
            ),
        ),
    )
    def test_method__execute__returns_structured_stop_without_aligned_outputs(
        self, case: StopCase, issue_code: str
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-007.

        Requirement: Unidentifiable, unstable, or incompatible observations must stop
        with the applicable structured code and no represented outputs.

        Method: Exercise six explicit semantic partitions adjacent to policy and
        represented-space boundaries.

        Oracle: The documented issue-code precedence and threshold rules.

        Acceptance: Each partition returns ``stopped``, its exact single issue code,
        and ``None`` for map, projector, extraction, and shift.

        Interpretation: A pass establishes active structured stopping behavior.

        Limitations: The partitions do not exhaust malformed matrix inputs.
        """
        result = SUT().execute(self.make_stop_request(case))

        assert result.status == "stopped"
        assert result.issue_codes == (issue_code,)
        assert result.alignment_map is None
        assert result.reference_projector is None
        assert result.extracted_operator is None
        assert result.inferred_energy_shift is None
