r"""Software verification for ``Periodic1DBasisScramblingConstructor``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns reusable finite-periodic site, orbital, phase, and spin basis maps for
controlled periodic-1D toy systems.

Intrinsic and cross-object scope
--------------------------------
The tests are isolated unit tests with hand-authored identity and nontrivial unitary
oracles. They exercise only reusable model construction, not campaign provenance or
acceptance.

VVUQ and scientific exclusions
------------------------------
A pass establishes the represented software contract. It does not identify a physical
basis map, validate silicon or Wannier functions, or perform uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic_1d.model import toy_defects

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]
SUT = toy_defects.Periodic1DBasisScramblingConstructor


class TestPeriodic1DBasisScramblingConstructor:
    """Own reusable periodic-1D basis-scrambling construction evidence."""

    @staticmethod
    def identity_model() -> toy_defects.Periodic1DBasisScramblingModel:
        """Return controls whose site, orbital, phase, and spin actions are neutral."""
        return toy_defects.Periodic1DBasisScramblingModel(
            translation_cells=0,
            orbital_permutation=(0, 1),
            orbital_rotation_radians=0.0,
            orbital_phases_radians=(0.0, 0.0),
            site_phase_step_radians=0.0,
            spin_rotation_axis=(0.0, 0.0, 1.0),
            spin_rotation_radians=0.0,
        )

    def test_method__execute__constructs_identity_for_zero_scrambling(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-015.

        Requirement: Zero translation, rotations, and phases with identity orbital
        permutation must produce identity maps for both supported spin factors.

        Method: Construct spinless and spin-half maps on a three-cell periodic domain.

        Oracle: Exact identity matrices of dimensions six and twelve.

        Acceptance: Both directions agree exactly with their identity oracle.

        Interpretation: A pass establishes the neutral element of the scrambling
        model.

        Limitations: This case does not exercise a boundary-crossing phase.
        """
        constructor = SUT()

        spinless = constructor.execute(
            toy_defects.Periodic1DBasisScramblingRequest(
                self.identity_model(), 3, 0.125, 1
            )
        )
        spinor = constructor.execute(
            toy_defects.Periodic1DBasisScramblingRequest(
                self.identity_model(), 3, 0.125, 2
            )
        )

        np.testing.assert_array_equal(spinless.reference_to_candidate, np.eye(6))
        np.testing.assert_array_equal(spinless.candidate_to_reference, np.eye(6))
        np.testing.assert_array_equal(spinor.reference_to_candidate, np.eye(12))
        np.testing.assert_array_equal(spinor.candidate_to_reference, np.eye(12))

    def test_method__execute__returns_inverse_unitary_directions(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-016.

        Requirement: Nontrivial translation, orbital, site-phase, boundary-phase, and
        spin actions must compose into a unitary map with an explicit inverse direction.

        Method: Construct a spin-half map with all control families nontrivial.

        Oracle: Exact conjugate-transpose direction relation and mathematical unitary
        identities.

        Acceptance: Direction relation is exact after construction and both unitary
        products agree with identity within absolute tolerance ``1e-12``.

        Interpretation: A pass establishes map orientation and finite-periodic
        unitarity.

        Limitations: Unitarity does not establish that this authored map is physically
        appropriate for another represented system.
        """
        model = toy_defects.Periodic1DBasisScramblingModel(
            translation_cells=2,
            orbital_permutation=(1, 0),
            orbital_rotation_radians=0.41,
            orbital_phases_radians=(0.11, -0.23),
            site_phase_step_radians=0.173,
            spin_rotation_axis=(1.0, -2.0, 0.5),
            spin_rotation_radians=0.63,
        )

        result = SUT().execute(
            toy_defects.Periodic1DBasisScramblingRequest(model, 5, 0.017, 2)
        )

        np.testing.assert_array_equal(
            result.candidate_to_reference,
            result.reference_to_candidate.conj().T,
        )
        np.testing.assert_allclose(
            result.reference_to_candidate @ result.candidate_to_reference,
            np.eye(20),
            rtol=0.0,
            atol=1e-12,
        )
        np.testing.assert_allclose(
            result.candidate_to_reference @ result.reference_to_candidate,
            np.eye(20),
            rtol=0.0,
            atol=1e-12,
        )
        assert not result.reference_to_candidate.flags.writeable
        assert not result.candidate_to_reference.flags.writeable
