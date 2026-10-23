"""Software verification for canonical shell--scale artifacts."""

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from band_equivalence_workflow.decision_landscape_schemas import (
    DecisionLandscapeSchema,
    DecisionLandscapeSchemaKind,
)
from band_equivalence_workflow.decision_landscape_serialization import (
    DECISION_RESULT_SCHEMA_ID,
    DecisionLandscapeEnvironment,
    ShellScaleDecisionLandscapeArtifactWriter,
)
from jsonschema import ValidationError  # type: ignore[import-untyped]
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape import (
    ShellScaleCaseDecisionLandscape,
    ShellScaleDecisionLandscapeCalculator,
    ShellScaleDecisionLandscapeRequest,
    ShellScaleDecisionLandscapeResult,
    ShellScaleDecisionPoint,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamily,
    BandEquivalenceLocalityRequest,
    GaugeNormalization,
    ParentKind,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestShellScaleDecisionLandscapeArtifacts:
    """Establish schema, source binding, and exact read-back behavior."""

    @staticmethod
    def request() -> ShellScaleDecisionLandscapeRequest:
        """Return one bounded source request."""
        locality = BandEquivalenceLocalityRequest(
            family=BandEquivalenceLocalityFamily.SQUARE,
            cases=(
                BandEquivalenceLocalityCase(
                    name="square-directed-parent",
                    dimension=2,
                    parent_kind=ParentKind.DIRECTED_AXIS,
                    gauge_normalization=GaugeNormalization.AXIS_MAXIMUM,
                    positive_bonds=((1, 0), (0, 1)),
                    direct_metric=DirectLatticeMetric(
                        DirectLattice2D(
                            a1=np.asarray((1.0, 0.0), dtype=np.float64),
                            a2=np.asarray((0.0, 1.0), dtype=np.float64),
                        )
                    ),
                    shell_metric_scale=1.0,
                ),
            ),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(0.5,),
            band_tolerances=(1.0e-3,),
            shell_cap=1,
        )
        return ShellScaleDecisionLandscapeRequest(locality, 2)

    @staticmethod
    def result() -> ShellScaleDecisionLandscapeResult:
        """Return one exact serialization fixture."""
        case = ShellScaleCaseDecisionLandscape(
            name="square-directed-parent",
            parent_scale=1.0,
            gauge_amplitude=0.5,
            optimized_comparison_scale=0.8,
            shell_indices=(0, 1),
            retained_block_counts=(1, 5),
            scale_path_coordinates=(0.0, 1.0),
            comparison_scales=(0.8, 1.0),
            points=(
                ShellScaleDecisionPoint(0, 1, 0.0, 0.8, 0.4, 0.3, True),
                ShellScaleDecisionPoint(1, 5, 0.0, 0.8, 0.2, 0.15, True),
                ShellScaleDecisionPoint(0, 1, 1.0, 1.0, 0.5, 0.2, True),
                ShellScaleDecisionPoint(1, 5, 1.0, 1.0, 0.3, 0.05, True),
            ),
        )
        return ShellScaleDecisionLandscapeResult(
            family=BandEquivalenceLocalityFamily.SQUARE,
            construction_size=4,
            evaluation_size=5,
            scale_sample_count=2,
            cases=(case,),
        )

    def test_execute__canonical_files__binds_and_verifies_read_back(
        self, tmp_path: Path
    ) -> None:
        environment = DecisionLandscapeEnvironment(
            python="test-python",
            platform="test-platform",
            numpy="test-numpy",
            matplotlib="test-matplotlib",
            ksdft2effmass="test-ksd",
            projectkoios_optimization="test-optimization",
            projectkoios_physkit="test-physkit",
        )

        request = self.request()
        artifact = ShellScaleDecisionLandscapeArtifactWriter().execute(
            request,
            ShellScaleDecisionLandscapeCalculator().execute(request),
            tmp_path,
            environment,
        )

        assert all(
            path.is_file()
            for path in (
                artifact.source_request_path,
                artifact.decision_request_path,
                artifact.decision_result_path,
                artifact.verification_path,
            )
        )
        request_wire = json.loads(artifact.decision_request_path.read_bytes())
        result_wire = json.loads(artifact.decision_result_path.read_bytes())
        verification_wire = json.loads(artifact.verification_path.read_bytes())
        assert (
            request_wire["source_analysis_request_sha256"]
            == artifact.source_analysis_request_sha256
        )
        assert (
            result_wire["decision_request_sha256"] == artifact.decision_request_sha256
        )
        assert verification_wire["passes"] is True
        assert (
            verification_wire["decision_result_sha256"]
            == artifact.decision_result_sha256
        )

    def test_execute__request_inconsistent_result__fails_closed(
        self, tmp_path: Path
    ) -> None:
        environment = DecisionLandscapeEnvironment(
            python="test-python",
            platform="test-platform",
            numpy="test-numpy",
            matplotlib="test-matplotlib",
            ksdft2effmass="test-ksd",
            projectkoios_optimization="test-optimization",
            projectkoios_physkit="test-physkit",
        )

        with pytest.raises(
            ValueError,
            match="result does not replay from the source request",
        ):
            ShellScaleDecisionLandscapeArtifactWriter().execute(
                self.request(),
                self.result(),
                tmp_path,
                environment,
            )

    def test_execute__changed_numerical_point__fails_closed(
        self, tmp_path: Path
    ) -> None:
        request = self.request()
        calculated = ShellScaleDecisionLandscapeCalculator().execute(request)
        case = calculated.cases[0]
        changed_point = replace(
            case.points[0],
            maximum_hamiltonian_error=(
                case.points[0].maximum_hamiltonian_error + 1.0e-12
            ),
        )
        changed_case = replace(
            case,
            points=(changed_point, *case.points[1:]),
        )
        changed_result = replace(calculated, cases=(changed_case,))
        environment = DecisionLandscapeEnvironment(
            python="test-python",
            platform="test-platform",
            numpy="test-numpy",
            matplotlib="test-matplotlib",
            ksdft2effmass="test-ksd",
            projectkoios_optimization="test-optimization",
            projectkoios_physkit="test-physkit",
        )

        with pytest.raises(
            ValueError,
            match="result does not replay from the source request",
        ):
            ShellScaleDecisionLandscapeArtifactWriter().execute(
                request,
                changed_result,
                tmp_path,
                environment,
            )

    def test_result_schema__unknown_property__fails_closed(self) -> None:
        invalid = {
            "schema": DECISION_RESULT_SCHEMA_ID,
            "unexpected": True,
        }
        with pytest.raises(ValidationError):
            DecisionLandscapeSchema(DecisionLandscapeSchemaKind.RESULT).validate(
                (json.dumps(invalid) + "\n").encode("utf-8")
            )
