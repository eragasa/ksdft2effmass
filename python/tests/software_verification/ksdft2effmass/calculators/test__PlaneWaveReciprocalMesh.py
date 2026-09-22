r"""Software verification of ``PlaneWaveReciprocalMesh``.

Evidence profile: routine

Bounded artifact scope: exact dimensionless regular-mesh count and half-shift state.

Facet and represented meaning

The module verifies immutable three-axis positive counts and Boolean half-step shifts.

Intrinsic and cross-object scope

``PlaneWaveReciprocalMesh`` is the sole system under test. Reciprocal bases, symmetry,
weights, native rendering, backend equivalence, and parameter selection are excluded.

VVUQ and scientific exclusions

This is software verification using illustrative dimensionless values. It establishes
no mesh convergence, numerical verification, scientific validation, or accepted mesh.
"""

import pytest

from ksdft2effmass.calculators.dft.pw import PlaneWaveReciprocalMesh

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveReciprocalMesh


class TestPlaneWaveReciprocalMesh:
    """Own software evidence for exact portable reciprocal-mesh state."""

    def test_constructor__valid_mesh__retains_exact_axis_order_and_shifts(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-MESH-001

        Requirement: A mesh retains exactly three ordered counts and corresponding
        half-step shift flags without native rendering or symmetry inference.

        Acceptance: Construction preserves both supplied tuples exactly.
        """
        mesh = SUT((4, 6, 8), (False, True, False))

        assert mesh.axis_counts == (4, 6, 8)
        assert mesh.half_step_shifts == (False, True, False)

    @pytest.mark.parametrize(
        "axis_counts",
        [
            pytest.param((1, 2), id="insufficient_axis_count_arity"),
            pytest.param((1, 2, 3, 4), id="excess_axis_count_arity"),
        ],
    )
    def test_constructor__axis_count_arity__rejects_non_three_axis_tuple(
        self, axis_counts: tuple[int, ...]
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-MESH-002

        Requirement: Axis counts contain exactly three values.

        Acceptance: Any other tuple length raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="exactly three"):
            SUT(axis_counts, (False, False, False))  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "axis_counts",
        [
            pytest.param((True, 2, 3), id="boolean_count_representation"),
            pytest.param(("1", 2, 3), id="numeric_text_count_representation"),
        ],
    )
    def test_constructor__axis_count_type__rejects_non_integer_elements(
        self, axis_counts: tuple[bool | int | str, int, int]
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-MESH-003

        Requirement: Counts are exact built-in integers excluding booleans and
        numeric strings.

        Acceptance: Either invalid representation raises ``TypeError``.
        """
        with pytest.raises(TypeError, match="built-in integers"):
            SUT(
                axis_counts,  # type: ignore[arg-type]
                (False, False, False),
            )

    @pytest.mark.parametrize(
        "invalid_count",
        [
            pytest.param(0, id="zero_count_boundary"),
            pytest.param(-1, id="negative_count_partition"),
            pytest.param(2**63, id="signed_i64_count_overflow"),
        ],
    )
    def test_constructor__axis_count_value__rejects_out_of_contract_integer(
        self, invalid_count: int
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-MESH-004

        Requirement: Counts are positive signed-64-bit integers.

        Acceptance: Zero, negative, and above-range counts raise ``ValueError``.
        """
        with pytest.raises(ValueError, match="positive|signed 64-bit"):
            SUT((invalid_count, 2, 3), (False, False, False))

    @pytest.mark.parametrize(
        "half_step_shifts",
        [
            pytest.param((False, True), id="insufficient_shift_arity"),
            pytest.param((False, True, False, True), id="excess_shift_arity"),
        ],
    )
    def test_constructor__shift_arity__rejects_non_three_axis_tuple(
        self, half_step_shifts: tuple[bool, ...]
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-MESH-005

        Requirement: Half-step shift state contains exactly three values.

        Acceptance: Any other tuple length raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="exactly three"):
            SUT((1, 2, 3), half_step_shifts)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "half_step_shifts",
        [
            pytest.param((False, 1, False), id="integer_shift_representation"),
            pytest.param((False, "true", False), id="text_shift_representation"),
        ],
    )
    def test_constructor__shift_type__rejects_non_boolean_elements(
        self, half_step_shifts: tuple[bool, int | str, bool]
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-MESH-006

        Requirement: Shift flags are exact built-in Booleans.

        Acceptance: Integer and string substitutes raise ``TypeError``.
        """
        with pytest.raises(TypeError, match="Booleans"):
            SUT(
                (1, 2, 3),
                half_step_shifts,  # type: ignore[arg-type]
            )
