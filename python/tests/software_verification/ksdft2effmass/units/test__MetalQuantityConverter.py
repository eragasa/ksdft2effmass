r"""Software verification of ``MetalQuantityConverter``.

Evidence profile: routine

Bounded artifact scope: explicit scalar conversion and represented result provenance.

Facet and represented meaning

The module verifies supported conversion, immutable source correlation, binary64
rounding, and closed unsupported/overflow behavior.

Intrinsic and cross-object scope

``MetalQuantityConverter`` is the sole system under test. Native aggregate adapters,
wire serialization, external execution, and scientific interpretation are excluded.

VVUQ and scientific exclusions

This is software verification using authority-derived factors and illustrative scalar
inputs. It retains but does not propagate factor uncertainty and establishes no
scientific validation.
"""

import sys

import pytest

from ksdft2effmass.units import (
    ContentIdentity,
    MetalQuantityConverter,
    MetalUnitConversionFailure,
    MetalUnitConversionFailureCode,
    MetalUnitConversionLimitation,
    MetalUnitConversionOutcome,
    MetalUnitConversionRequest,
    MetalUnitConversionSourceCorrelation,
    MetalUnitConversionSuccess,
    UnitIdentity,
    UnitScalar,
)

pytestmark = pytest.mark.software_verification
SUT = MetalQuantityConverter


class TestMetalQuantityConverter:
    """Own software evidence for explicit native-to-metal scalar conversion."""

    @pytest.mark.parametrize(
        ("source", "target_unit", "expected"),
        [
            pytest.param(
                UnitScalar(1.0, UnitIdentity.HARTREE),
                UnitIdentity.ELECTRON_VOLT,
                27.211386245981,
                id="hartree_energy_conversion",
            ),
            pytest.param(
                UnitScalar(2.0, UnitIdentity.RYDBERG),
                UnitIdentity.ELECTRON_VOLT,
                27.211386245981,
                id="rydberg_energy_conversion",
            ),
            pytest.param(
                UnitScalar(1.0, UnitIdentity.BOHR),
                UnitIdentity.ANGSTROM,
                0.529177210544,
                id="bohr_length_conversion",
            ),
            pytest.param(
                UnitScalar(1.0, UnitIdentity.UNIFIED_ATOMIC_MASS_UNIT),
                UnitIdentity.GRAM_PER_MOLE,
                1.00000000105,
                id="atomic_to_molar_mass_conversion",
            ),
        ],
    )
    def test_method__convert__uses_exact_retained_decimal_scale(
        self, source: UnitScalar, target_unit: UnitIdentity, expected: float
    ) -> None:
        """Evidence ID: SV-UNITS-METAL-CONVERTER-001

        Requirement: Each demonstrated pair follows its retained decimal scale and
        produces one finite target-unit binary64 value.

        Acceptance: Unit source values convert to the expected rounded binary64
        values without changing the source objects.
        """
        request = MetalUnitConversionRequest(source, target_unit)

        result = SUT().convert(request)

        assert type(result) is MetalUnitConversionSuccess
        assert result.outcome is MetalUnitConversionOutcome.CONVERTED
        assert result.request is request
        assert result.request.source is source
        assert result.output == UnitScalar(expected, target_unit)
        assert result.definition.source_unit is source.unit
        assert result.definition.target_unit is target_unit

    def test_method__convert__retains_exact_source_correlation(self) -> None:
        """Evidence ID: SV-UNITS-METAL-CONVERTER-002

        Requirement: Conversion retains available source artifact, result,
        provenance, and content identities rather than reconstructing native history.

        Acceptance: The success retains the exact immutable request correlation and
        the exact definition/catalog content identities.
        """
        correlation = MetalUnitConversionSourceCorrelation(
            artifact_identity="artifact.native-qe-record",
            result_identity="result.imported-retained-fixture",
            provenance_identity="provenance.qe-example",
            content_identity=ContentIdentity(
                "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ),
        )
        request = MetalUnitConversionRequest(
            UnitScalar(1.0, UnitIdentity.HARTREE),
            UnitIdentity.ELECTRON_VOLT,
            correlation,
        )

        result = SUT().convert(request)

        assert type(result) is MetalUnitConversionSuccess
        assert result.request.source_correlation is correlation
        assert result.definition.content_identity.value.startswith("sha256:")
        assert result.catalog_content_identity.value == (
            "sha256:f8555a74b689f05a2f9267030b627c690839c26c4ad6d582e236d366f113fe7e"
        )
        assert result.limitations == (
            MetalUnitConversionLimitation.BINARY64_OUTPUT_ROUNDED,
            MetalUnitConversionLimitation.FACTOR_UNCERTAINTY_NOT_PROPAGATED,
        )

    def test_method__convert__returns_closed_unsupported_pair_failure(self) -> None:
        """Evidence ID: SV-UNITS-METAL-CONVERTER-003

        Requirement: Unimplemented inverse, identity, or cross-dimension requests
        fail closed without unit inference or fabricated output.

        Acceptance: Angstrom-to-bohr returns the exact unsupported failure and no
        conversion definition.
        """
        request = MetalUnitConversionRequest(
            UnitScalar(1.0, UnitIdentity.ANGSTROM), UnitIdentity.BOHR
        )

        result = SUT().convert(request)

        assert type(result) is MetalUnitConversionFailure
        assert result.outcome is MetalUnitConversionOutcome.UNSUPPORTED
        assert result.code is MetalUnitConversionFailureCode.UNSUPPORTED_UNIT_PAIR
        assert result.definition is None
        assert result.request is request
        assert result.limitations == ()

    def test_method__convert__returns_closed_binary64_overflow(self) -> None:
        """Evidence ID: SV-UNITS-METAL-CONVERTER-004

        Requirement: A finite exact decimal product outside binary64 range must not
        become a successful infinity.

        Acceptance: Maximum binary64 Hartree converts to a represented overflow that
        retains the selected definition and its limitations.
        """
        request = MetalUnitConversionRequest(
            UnitScalar(sys.float_info.max, UnitIdentity.HARTREE),
            UnitIdentity.ELECTRON_VOLT,
        )

        result = SUT().convert(request)

        assert type(result) is MetalUnitConversionFailure
        assert result.outcome is MetalUnitConversionOutcome.OVERFLOW
        assert result.code is MetalUnitConversionFailureCode.BINARY64_OVERFLOW
        assert result.definition is not None
        assert result.definition.identity == "hartree-to-electron-volt"
        assert result.limitations == (
            MetalUnitConversionLimitation.BINARY64_OUTPUT_ROUNDED,
            MetalUnitConversionLimitation.FACTOR_UNCERTAINTY_NOT_PROPAGATED,
        )
