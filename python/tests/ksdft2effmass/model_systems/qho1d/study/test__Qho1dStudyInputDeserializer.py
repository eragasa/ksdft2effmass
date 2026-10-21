r"""Software verification of ``Qho1dStudyInputDeserializer``.

Evidence profile: routine

Bounded artifact scope: version-one harmonic-oscillator monograph study input.

Facet and represented meaning

The class under test converts the retained Appendix E version-one JSON input into the
public immutable harmonic-oscillator study definition.

Intrinsic and cross-object scope

The supported public import, exact maintained controls, closed field set, version, and
scalar conversion are included. Study evaluation and result serialization are
excluded.

VVUQ and scientific exclusions

This is software verification of a wire adapter. It establishes no numerical
verification, convergence, scientific validation, uncertainty quantification, or
human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns import research_monograph
from ksdft2effmass.model_systems import ScalarQuantity, Unitless
from ksdft2effmass.model_systems.qho1d import (
    Qho1dStudyDefinition,
    Qho1dStudyInputDeserializer,
)
from ksdft2effmass.model_systems.study import (
    ModelId,
    ModelSystemStudyIdentity,
    ModelSystemStudySchemaId,
)

pytestmark = pytest.mark.software_verification
SUT = Qho1dStudyInputDeserializer


class TestQho1dStudyInputDeserializer:
    """Own software evidence for ``Qho1dStudyInputDeserializer``."""

    @staticmethod
    def input_path() -> Path:
        """Return the maintained QHO1D input path."""
        return (
            Path(__file__).resolve().parents[6]
            / "calculations"
            / "qho1d"
            / "input.json"
        )

    def test_method__execute__maps_maintained_version_one_input(self) -> None:
        """Evidence ID: SV-MONOGRAPH-HO-001

        Requirement: The public deserializer maps the maintained closed version-one
        input to its exact identifier, evidence status, dimensionless parameters,
        ordered control sweeps, representation, and comparison-map declarations.

        Acceptance: The package import resolves to the documented class and every
        resulting field equals the maintained wire value.
        """
        assert (
            research_monograph.HarmonicOscillatorStudyInputDeserializer
            is Qho1dStudyInputDeserializer
        )

        definition = Qho1dStudyInputDeserializer().execute(
            self.input_path().read_bytes()
        )

        assert isinstance(definition, Qho1dStudyDefinition)
        assert definition.experiment_id == "qho1d.development.v1"
        assert definition.evidence_status == "illustrative numerical experiment"
        assert definition.study_identity() == ModelSystemStudyIdentity(
            model_id=ModelId.qho1d,
            schema_id=ModelSystemStudySchemaId.qho1d_v1,
        )
        assert definition.parameters.hbar == ScalarQuantity(1.0, Unitless())
        assert definition.parameters.mass == ScalarQuantity(1.0, Unitless())
        assert definition.parameters.omega == ScalarQuantity(1.0, Unitless())
        assert definition.parameters.oscillator_length == ScalarQuantity(
            1.0, Unitless()
        )
        assert definition.box_half_widths == (4.0, 6.0, 8.0)
        assert definition.grid_spacings == (0.2, 0.1, 0.05)
        assert definition.retained_dimensions == (2, 4, 6)
        assert definition.spatial_representation == (
            "second-order centered finite differences on a uniform interior "
            "Dirichlet grid"
        )
        assert definition.comparison_map == (
            "quadrature-scaled real-line oscillator states followed by symmetric "
            "Gram orthonormalization"
        )

    def test_method__execute__preserves_historical_calculation_identity(self) -> None:
        """The retained monograph input remains a supported immutable payload."""
        historical_input = (
            Path(__file__).resolve().parents[6]
            / "calculations"
            / "research-monograph"
            / "harmonic-oscillator"
            / "input.json"
        )

        definition = Qho1dStudyInputDeserializer().execute(
            historical_input.read_bytes()
        )

        assert definition.experiment_id == (
            "research-monograph.harmonic-oscillator.v1"
        )
        assert definition.evidence_status == "illustrative numerical experiment"
        assert definition.study_identity() == ModelSystemStudyIdentity(
            model_id=ModelId.qho1d,
            schema_id=ModelSystemStudySchemaId.qho1d_v1,
        )
