"""Numerical verification tests for direct QHO1D results."""

import hashlib
from collections.abc import Mapping

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalyzer,
    Qho1dConfiguration,
    Qho1dVerifier,
)
from ksdft2effmass.serialization import (
    SerializableValue,
    TypedJsonMappingDeserializer,
)


class TestQho1dVerifier:
    """Verify independent reconstruction and tamper detection."""

    @staticmethod
    def decoded_result() -> tuple[bytes, Mapping[str, SerializableValue]]:
        """Return exact result bytes and their shared-codec mapping."""
        configuration = Qho1dConfiguration(
            hbar=1.0,
            mass=1.0,
            omega=1.0,
            box_half_widths=(4.0, 6.0, 8.0),
            grid_spacings=(0.2, 0.1, 0.05),
            retained_dimensions=(2, 4, 6),
            selected_box_half_width=8.0,
            selected_grid_spacing=0.05,
            selected_retained_dimension=6,
            displayed_states=4,
        )
        result = Qho1dAnalyzer().execute(
            configuration,
            calculation_family="qho1d-spatial-truncation",
            execution_id="test-direct",
            evidence_status="illustrative numerical experiment",
            claim_boundary="test fixture; no scientific-validation claim",
        )
        wire = result.to_json()
        return wire, TypedJsonMappingDeserializer().deserialize(wire)

    def test_method__result__passes_independent_reference_comparisons(self) -> None:
        """Independent formulas pass all sweep, state, and projection checks."""
        wire, decoded = self.decoded_result()

        verification_result = Qho1dVerifier(
            result=decoded,
            subject_sha256=hashlib.sha256(wire).hexdigest(),
        ).result()

        assert verification_result.verification.passed
        assert len(verification_result.verification.checks) == 468
        assert (
            verification_result.verification.visualization_data_sha256
            == hashlib.sha256(
                verification_result.visualization_data.to_json()
            ).hexdigest()
        )

    def test_method__result__detects_tampered_typed_diagnostic(self) -> None:
        """A locally valid but altered discrepancy fails independent verification."""
        wire, decoded = self.decoded_result()
        cases_value = decoded["cases"]
        assert isinstance(cases_value, tuple)
        assert cases_value and isinstance(cases_value[0], Mapping)
        first_case: dict[str, SerializableValue] = dict(cases_value[0])
        first_case["relative_discrepancy"] = ScalarQuantity(0.0, Unitless())
        tampered: dict[str, SerializableValue] = dict(decoded)
        tampered["cases"] = (first_case, *cases_value[1:])

        verification = (
            Qho1dVerifier(
                result=tampered,
                subject_sha256=hashlib.sha256(wire).hexdigest(),
            )
            .result()
            .verification
        )

        assert not verification.passed
        assert (
            verification.checks["case_00_relative_discrepancy_maximum_absolute_error"]
            > verification.check_tolerances[
                "case_00_relative_discrepancy_maximum_absolute_error"
            ]
        )
