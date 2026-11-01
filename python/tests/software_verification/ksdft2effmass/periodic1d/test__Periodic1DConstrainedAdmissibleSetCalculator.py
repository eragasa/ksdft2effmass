"""Software verification for authenticated constrained admissible sets."""

from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.periodic1d.admissible_sets.calculate import (
    Periodic1DConstrainedAdmissibleSetAnalyzer,
)
from ksdft2effmass.periodic1d.admissible_sets.definition import (
    Periodic1DAdmissibleSetThresholds,
    Periodic1DConstrainedAdmissibleSetAnalysisRequest,
    Periodic1DConstrainedAdmissibleSetConfiguration,
)
from ksdft2effmass.periodic1d.admissible_sets.results import (
    Periodic1DAdmissibleSetDisposition,
    Periodic1DConstrainedAdmissibleSetCalculationResult,
)
from ksdft2effmass.periodic1d.admissible_sets.verify import (
    Periodic1DConstrainedAdmissibleSetVerifier,
)
from ksdft2effmass.periodic1d.admissible_sets.visualizations.data import (
    Periodic1DConstrainedAdmissibleSetVisualizationData,
)
from ksdft2effmass.periodic1d.admissible_sets.visualizations.inventory import (
    Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum,
)
from ksdft2effmass.periodic1d.admissible_sets.visualizations.visualizer import (
    Periodic1DConstrainedAdmissibleSetVisualizer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.analysis import (
    Periodic1DCompositeBandAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.verification import (
    Periodic1DCompositeBandAlignmentVerifier,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


@pytest.fixture(scope="module")
def composite_wire() -> bytes:
    """Return one canonical direct rank-two composite result wire."""
    configuration_type = Periodic1DCompositeBandAlignmentConfiguration
    configuration = configuration_type(
        parent_identity=configuration_type.PARENT_IDENTITY,
        onsite_numerators=configuration_type.PARENT_ONSITE_NUMERATORS,
        positive_hopping_numerators=(
            configuration_type.PARENT_POSITIVE_HOPPING_NUMERATORS
        ),
        coefficient_denominator=configuration_type.PARENT_COEFFICIENT_DENOMINATOR,
        retained_rank=2,
        construction_size=64,
        evaluation_size=257,
        evaluation_shift_numerator=1,
        evaluation_shift_denominator=65,
        hopping_ranges=configuration_type.HOPPING_RANGES,
        attack_constant_angle=0.30,
        attack_sine_coefficients=(0.65, 0.30),
        sampled_gap_threshold=0.5,
        overlap_singular_value_threshold=0.8,
        procrustes_rank_absolute_tolerance=1.0e-14,
        procrustes_rank_relative_tolerance=1.0e-12,
        energy_absolute_tolerance=1.0e-11,
        dimensionless_absolute_tolerance=1.0e-12,
    )
    return (
        Periodic1DCompositeBandAlignmentAnalyzer(
            configuration,
            NumpyBatchedComplexUnitaryProcrustesSolver(),
        )
        .execute()
        .to_json()
    )


@pytest.fixture(scope="module")
def admissible_configuration(
    composite_wire: bytes,
) -> Periodic1DConstrainedAdmissibleSetConfiguration:
    """Return the compact frozen M3 controls bound to the composite wire."""
    return Periodic1DConstrainedAdmissibleSetConfiguration(
        calculation_id="m3-authenticated-test",
        upstream_result_sha256=hashlib.sha256(composite_wire).hexdigest(),
        energy_shift_ratio_bounds=(-0.25, 0.25),
        splitting_scale_bounds=(0.4, 1.2),
        alignment_angles=(-1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2),
        loss_energy_scale=ScalarQuantity(1.0, Unitless()),
        compatible_thresholds=Periodic1DAdmissibleSetThresholds(
            "compatible", 0.03, 0.33
        ),
        separated_thresholds=Periodic1DAdmissibleSetThresholds("separated", 0.03, 0.31),
        compatible_witness=(0.0, 1.0),
        locality_ranges=(0, 1, 2, 3, 4, 6, 8),
        separation_resolution=0.05,
        quadratic_absolute_tolerance=1.0e-12,
        verification_absolute_tolerance=1.0e-11,
    )


@pytest.fixture(scope="module")
def admissible_result(
    composite_wire: bytes,
    admissible_configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
) -> Periodic1DConstrainedAdmissibleSetCalculationResult:
    """Analyze the authenticated composite result once for this module."""
    request = Periodic1DConstrainedAdmissibleSetAnalysisRequest(
        admissible_configuration,
        composite_wire,
    )
    upstream_verifier = Periodic1DCompositeBandAlignmentVerifier(
        result_wire=composite_wire
    )
    analyzer = Periodic1DConstrainedAdmissibleSetAnalyzer(request, upstream_verifier)
    assert analyzer.request is request
    assert analyzer.upstream_verifier is upstream_verifier
    return analyzer.execute()


class TestPeriodic1DConstrainedAdmissibleSetAnalyzer:
    """Establish exact-byte composition, certificates, and verification."""

    def test__request__binds_canonical_upstream_bytes(
        self,
        composite_wire: bytes,
        admissible_configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
    ) -> None:
        request = Periodic1DConstrainedAdmissibleSetAnalysisRequest(
            admissible_configuration,
            composite_wire,
        )

        assert request.upstream_result.to_json() == composite_wire
        assert (
            Periodic1DConstrainedAdmissibleSetConfiguration.from_json(
                admissible_configuration.to_json()
            )
            == admissible_configuration
        )
        with pytest.raises(ValueError, match="canonical"):
            Periodic1DConstrainedAdmissibleSetAnalysisRequest(
                admissible_configuration,
                composite_wire + b" ",
            )

    def test__execute__retains_witness_certificate_and_separate_locality_channels(
        self,
        admissible_result: Periodic1DConstrainedAdmissibleSetCalculationResult,
    ) -> None:
        compatible, separated = admissible_result.cases

        assert compatible.disposition is (
            Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS
        )
        assert compatible.common_witness is not None
        assert compatible.common_witness.parameter == (0.0, 1.0)
        assert compatible.common_witness.selected_alignment_angle != 0.0
        assert separated.disposition is (
            Periodic1DAdmissibleSetDisposition.CERTIFIED_SEPARATED
        )
        assert separated.separation_lower_bound > separated.separation_resolution
        locality = separated.operator_certificate_point.locality[-1]
        assert locality.attacked_cyclic_conversion_power >= 0.0
        assert locality.attacked_ordinary_omitted_block_l2_norm >= 0.0

    def test__result__round_trips_canonical_typed_json(
        self,
        admissible_result: Periodic1DConstrainedAdmissibleSetCalculationResult,
    ) -> None:
        wire = admissible_result.to_json()

        decoded = Periodic1DConstrainedAdmissibleSetCalculationResult.from_json(wire)

        assert decoded.to_json() == wire
        assert decoded.composite_baseline.to_json() == (
            admissible_result.composite_baseline.to_json()
        )

    def test__verifier__authenticates_upstream_result_and_projection(
        self,
        admissible_result: Periodic1DConstrainedAdmissibleSetCalculationResult,
    ) -> None:
        wire = admissible_result.to_json()

        verified = Periodic1DConstrainedAdmissibleSetVerifier(result_wire=wire).result()

        assert verified.verification.passed
        assert verified.verification.subject_sha256 == hashlib.sha256(wire).hexdigest()
        assert (
            Periodic1DConstrainedAdmissibleSetVisualizationData.from_json(
                verified.visualization_data.to_json()
            ).to_json()
            == verified.visualization_data.to_json()
        )
        assert verified.verification.authenticated_visualization_data_sha256() == (
            hashlib.sha256(verified.visualization_data.to_json()).hexdigest()
        )

    def test__verifier__uses_one_closed_component_observation_inventory(
        self,
        admissible_result: Periodic1DConstrainedAdmissibleSetCalculationResult,
    ) -> None:
        verifier = Periodic1DConstrainedAdmissibleSetVerifier(
            result_wire=admissible_result.to_json()
        )

        verified = verifier.result()

        assert tuple(
            type(component) for component in verified.verification.components
        ) == tuple(
            component_type for component_type, _ in verifier.verification_inventory
        )
        assert tuple(
            frozenset(component.observations)
            for component in verified.verification.components
        ) == tuple(
            observation_names
            for _, observation_names in verifier.verification_inventory
        )

    def test__visualizer__renders_only_authenticated_projection_values(
        self,
        admissible_result: Periodic1DConstrainedAdmissibleSetCalculationResult,
    ) -> None:
        verified = Periodic1DConstrainedAdmissibleSetVerifier(
            result_wire=admissible_result.to_json()
        ).result()

        visualizations = Periodic1DConstrainedAdmissibleSetVisualizer(
            data=verified.visualization_data,
            verification=verified.verification,
            dpi=80,
        ).visualize()

        assert {item.plot for item in visualizations} == set(
            Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum
        )
        assert all(item.png.startswith(b"\x89PNG\r\n\x1a\n") for item in visualizations)

    def test__verifier__detects_tampered_evaluation_diagnostic(
        self,
        admissible_result: Periodic1DConstrainedAdmissibleSetCalculationResult,
    ) -> None:
        compatible = admissible_result.cases[0]
        assert compatible.common_witness is not None
        changed = replace(
            compatible.common_witness,
            evaluation_operator_rms_loss=(
                compatible.common_witness.evaluation_operator_rms_loss + 1.0e-3
            ),
        )
        changed_case = replace(
            compatible,
            common_witness=changed,
            spectral_certificate_point=changed,
            operator_certificate_point=changed,
        )
        tampered = replace(
            admissible_result,
            cases=(changed_case, admissible_result.cases[1]),
        )

        verified = Periodic1DConstrainedAdmissibleSetVerifier(
            result_wire=tampered.to_json()
        ).result()

        assert not verified.verification.passed

    def test__source__does_not_import_or_execute_legacy_multiband_alignment(
        self,
    ) -> None:
        package = (
            Path(__file__).resolve().parents[4]
            / "src/ksdft2effmass/periodic1d/admissible_sets"
        )
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(package.rglob("*.py"))
        )

        assert "periodic1d.multiband_alignment" not in source
        assert "Periodic1DMultibandAlignment" not in source
        assert "ConstrainedAdmissibleSetCalculator" not in source
        assert "ResultJsonSerializer" not in source
        assert "_compare_values" not in source
        assert '.startswith("result.")' not in source
        assert '.startswith("visualization.")' not in source
        assert "@staticmethod" not in source
