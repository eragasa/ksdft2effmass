"""Numerical verification tests for direct QHO1D results."""

import hashlib
from collections.abc import Mapping

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalysisRequest,
    Qho1dAnalyzer,
    Qho1dConfiguration,
    Qho1dVerifier,
)
from ksdft2effmass.serialization import (
    SerializableValue,
    TypedJsonMappingDeserializer,
    TypedJsonMappingSerializer,
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
        result = Qho1dAnalyzer(
            Qho1dAnalysisRequest(
                configuration=configuration,
                calculation_family="qho1d-spatial-truncation",
                execution_id="test-direct",
                evidence_status="illustrative numerical experiment",
                claim_boundary="test fixture; no scientific-validation claim",
            )
        ).execute()
        wire = result.to_json()
        return wire, TypedJsonMappingDeserializer().deserialize(wire)

    def test_method__result__passes_independent_reference_comparisons(self) -> None:
        """Independent formulas pass all sweep, state, and projection checks."""
        wire, _ = self.decoded_result()

        verification_result = Qho1dVerifier(result_wire=wire).result()

        assert verification_result.verification.passed
        assert (
            verification_result.verification.subject_sha256
            == hashlib.sha256(wire).hexdigest()
        )
        assert len(verification_result.verification.checks) == 468
        components = verification_result.verification.to_dict()["components"]
        assert isinstance(components, Mapping)
        assert set(components) == {
            "spatial_representation",
            "sampled_state_alignment",
            "hamiltonian_comparison",
            "residual",
            "state_comparison",
            "visualization_projection",
        }
        assert (
            verification_result.verification.visualization_data_sha256
            == hashlib.sha256(
                verification_result.visualization_data.to_json()
            ).hexdigest()
        )

    def test_method__result__detects_tampered_typed_diagnostic(self) -> None:
        """A locally valid but altered discrepancy fails independent verification."""
        _, decoded = self.decoded_result()
        cases_value = decoded["cases"]
        assert isinstance(cases_value, tuple)
        assert cases_value and isinstance(cases_value[0], Mapping)
        first_case: dict[str, SerializableValue] = dict(cases_value[0])
        hamiltonian_value = first_case["hamiltonian_comparison"]
        assert isinstance(hamiltonian_value, Mapping)
        hamiltonian: dict[str, SerializableValue] = dict(hamiltonian_value)
        hamiltonian["relative_discrepancy"] = ScalarQuantity(0.0, Unitless())
        first_case["hamiltonian_comparison"] = hamiltonian
        tampered: dict[str, SerializableValue] = dict(decoded)
        tampered["cases"] = (first_case, *cases_value[1:])

        tampered_wire = TypedJsonMappingSerializer().serialize(tampered)
        verification = Qho1dVerifier(result_wire=tampered_wire).result().verification

        assert not verification.passed
        assert (
            verification.checks["case_00_relative_discrepancy_maximum_absolute_error"]
            > verification.check_tolerances[
                "case_00_relative_discrepancy_maximum_absolute_error"
            ]
        )
