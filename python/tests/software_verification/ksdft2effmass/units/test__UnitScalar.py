r"""Software verification of ``UnitScalar``.

Evidence profile: routine

Bounded artifact scope: exact scalar and unit invariants of the public unit value.

Facet and represented meaning

The module verifies finite built-in binary64 values with explicit closed unit identity.

Intrinsic and cross-object scope

``UnitScalar`` is the sole system under test. Conversion arithmetic, native records,
serialization, and scientific interpretation are excluded.

VVUQ and scientific exclusions

This is software verification using illustrative scalar values. It establishes no
physical result, conversion accuracy beyond the constructor contract, validation, or
uncertainty result.
"""

import pytest

from ksdft2effmass.units import PhysicalDimension, UnitIdentity, UnitScalar

pytestmark = pytest.mark.software_verification
SUT = UnitScalar


class TestUnitScalar:
    """Own software evidence for exact scalar and unit invariants."""

    @pytest.mark.parametrize(
        "invalid_value",
        [
            pytest.param(True, id="boolean_representation"),
            pytest.param(1, id="integer_representation"),
            pytest.param("1.0", id="numeric_text_representation"),
        ],
    )
    def test_constructor__non_float_value__rejects_erased_numeric_inputs(
        self, invalid_value: bool | int | str
    ) -> None:
        """Evidence ID: SV-UNITS-UNIT-SCALAR-001

        Requirement: Public unit scalars accept only an exact built-in ``float``.

        Acceptance: Boolean, integer, and numeric-string values raise ``TypeError``.
        """
        with pytest.raises(TypeError, match="built-in float"):
            SUT(
                invalid_value,  # type: ignore[arg-type]
                UnitIdentity.ELECTRON_VOLT,
            )

    @pytest.mark.parametrize(
        "invalid_value",
        [
            pytest.param(float("nan"), id="not_a_number_representation"),
            pytest.param(float("inf"), id="positive_nonfinite_representation"),
            pytest.param(float("-inf"), id="negative_nonfinite_representation"),
        ],
    )
    def test_constructor__nonfinite_value__rejects_nonfinite_binary64(
        self, invalid_value: float
    ) -> None:
        """Evidence ID: SV-UNITS-UNIT-SCALAR-002

        Requirement: A represented unit scalar is finite.

        Acceptance: NaN and either infinity raise ``ValueError`` naming finiteness.
        """
        with pytest.raises(ValueError, match="finite"):
            SUT(invalid_value, UnitIdentity.ELECTRON_VOLT)

    def test_property__dimension__returns_declared_unit_dimension(self) -> None:
        """Evidence ID: SV-UNITS-UNIT-SCALAR-003

        Requirement: Unit identity determines one closed represented dimension.

        Acceptance: A bohr-valued scalar reports length without conversion.
        """
        scalar = SUT(-2.0, UnitIdentity.BOHR)

        assert scalar.dimension is PhysicalDimension.LENGTH
        assert scalar.value == -2.0
        assert scalar.unit is UnitIdentity.BOHR
