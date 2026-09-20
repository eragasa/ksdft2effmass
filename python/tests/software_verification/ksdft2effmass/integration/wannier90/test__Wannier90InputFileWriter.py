r"""Software verification of ``Wannier90InputFileWriter``.

Evidence profile: claim_bearing

Bounded artifact scope: deterministic writing of the demonstrated ``.win`` subset.

Facet and represented meaning

The ActionObject serializes explicit settings, cell vectors, atoms, projections,
reciprocal mesh, and fractional reciprocal points.

Intrinsic and cross-object scope

Text ordering and spelling are included; scientific default selection and Wannier90
execution are excluded.

VVUQ and scientific exclusions

This is software verification of an interface representation, not localization
validation, scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.integration.wannier90 import (
    Wannier90InputData,
    Wannier90InputFileWriter,
)

pytestmark = pytest.mark.software_verification
SUT = Wannier90InputFileWriter


class TestWannier90InputFileWriter:
    """Own deterministic ``.win`` writer evidence."""

    @staticmethod
    def input_data(convergence_tolerance: float) -> Wannier90InputData:
        """Return the complete authored input with one selected tolerance."""

        return Wannier90InputData(
            num_bands=2,
            num_wann=2,
            num_iter=5000,
            convergence_tolerance=convergence_tolerance,
            convergence_window=5,
            precondition=True,
            search_shells=130,
            write_hr=True,
            write_u_matrices=True,
            translate_home_cell=True,
            unit_cell_cart_angstrom=(
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            atoms_fractional=(("H", 0.0, 0.0, 0.0),),
            projections=("random",),
            mp_grid=(2, 1, 1),
            kpoints_fractional=((0.0, 0.0, 0.0), (0.5, 0.0, 0.0)),
        )

    def test_method__execute__writes_complete_deterministic_input_subset(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-016

        Requirement: The supported input subset has one deterministic text form.

        Method: Serialize an authored two-point one-dimensional embedding.

        Oracle: The expected text is written independently as the declared native
        field and block order.

        Acceptance: Output agrees exactly and ends with one newline.

        Interpretation: A pass verifies deterministic ``.win`` representation.

        Limitations: The fixture does not establish parameter adequacy or execution.
        """

        input_data = self.input_data(1.0e-12)
        expected = """num_bands = 2
num_wann = 2
num_iter = 5000
conv_tol = 1.0d-12
conv_window = 5
precond = true
search_shells = 130
write_hr = true
write_u_matrices = true
translate_home_cell = true

begin unit_cell_cart
ang
1.0 0.0 0.0
0.0 1.0 0.0
0.0 0.0 1.0
end unit_cell_cart

begin atoms_frac
H 0.0 0.0 0.0
end atoms_frac

begin projections
random
end projections

mp_grid = 2 1 1

begin kpoints
0.0000000000000000 0.0 0.0
0.5000000000000000 0.0 0.0
end kpoints
"""

        assert SUT().execute(input_data) == expected

    def test_method__execute__retains_fixed_tolerance_notation(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-026

        Requirement: Tolerance text uses shortest round-trip notation, rewriting only
        an exponent that is present in that representation.

        Method: Serialize an authored tolerance whose shortest form is fixed-point.

        Oracle: Python represents ``0.1`` without an exponent, and Wannier90 accepts
        that native fixed-point form.

        Acceptance: The output contains exactly ``conv_tol = 0.1``.

        Interpretation: A pass verifies the documented fixed/exponential contract.

        Limitations: This does not select or validate a localization tolerance.
        """

        text = SUT().execute(self.input_data(0.1))

        assert "\nconv_tol = 0.1\n" in text
