"""Software verification for source-bound finite strain-scan artifacts."""

import json
import math
from dataclasses import dataclass
from pathlib import Path

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPath,
    SyntheticStrainResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    StrainWitnessControl,
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
    calculate_strain_witness_scan,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (  # noqa: E501
    SyntheticStrainScanAssessor,
    SyntheticStrainScanRequest,
    SyntheticStrainScanSummary,
    SyntheticStrainTransitionRefinementResult,
    SyntheticStrainTransitionRefiner,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.serialization import (  # noqa: E501
    CanonicalJsonDocument,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_scan_schemas import (  # noqa: E501
    SyntheticStrainScanSchema,
    SyntheticStrainScanSchemaKind,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_scan_serialization import (  # noqa: E501
    SCAN_REQUEST_SCHEMA_ID,
    SCAN_RESULT_SCHEMA_ID,
    SCAN_VERIFICATION_SCHEMA_ID,
    SyntheticStrainScanArtifactPaths,
    SyntheticStrainScanArtifactVerifier,
    SyntheticStrainScanArtifactWriter,
    SyntheticStrainScanEnvironment,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_serialization import (  # noqa: E501
    SyntheticStrainResponseResultSerializer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


@dataclass(frozen=True, slots=True)
class _CalculatedScan:
    request: SyntheticStrainScanRequest
    summary: SyntheticStrainScanSummary
    transitions: SyntheticStrainTransitionRefinementResult
    geometry: SyntheticStrainResult
    witnesses: tuple[SyntheticStrainWitnessScanResult, ...]
    frozen: SyntheticStrainResponseResult
    radial: SyntheticStrainResponseResult


def _calculate_scan(
    fractions: tuple[float, ...] = (0.0, 0.5, 1.0),
) -> _CalculatedScan:
    request = SyntheticStrainScanRequest(
        path=SyntheticStrainPath.RHOMBIC_2D,
        strain_fractions=fractions,
        geometry_construction_size=4,
        witness_construction_size=4,
        response_construction_size=4,
        response_evaluation_size=5,
        response_evaluation_shift=1.0 / 3.0,
        maximum_rotation_amplitude=math.pi / 8.0,
        radial_decay_beta=1.0,
        tail_tolerances=(1.0e-3,),
        maximum_transition_refinement_depth=2,
    )
    witnesses = tuple(
        calculate_strain_witness_scan(
            request.path,
            control,
            request.witness_construction_size,
            request.strain_fractions,
            request.maximum_rotation_amplitude,
        )
        for control in StrainWitnessControl
    )
    geometry = SyntheticStrainCalculator().execute(
        request.path,
        request.geometry_construction_size,
        request.strain_fractions,
        request.maximum_rotation_amplitude,
        request.tail_tolerances,
    )
    frozen = calculate_synthetic_strain_response(
        request.path,
        StrainResponseModel.M1_FROZEN,
        request.response_construction_size,
        request.response_evaluation_size,
        request.response_evaluation_shift,
        request.strain_fractions,
        request.maximum_rotation_amplitude,
        0.0,
        request.tail_tolerances,
    )
    radial = calculate_synthetic_strain_response(
        request.path,
        StrainResponseModel.M2_RADIAL,
        request.response_construction_size,
        request.response_evaluation_size,
        request.response_evaluation_shift,
        request.strain_fractions,
        request.maximum_rotation_amplitude,
        request.radial_decay_beta,
        request.tail_tolerances,
    )
    return _CalculatedScan(
        request=request,
        summary=SyntheticStrainScanAssessor().execute(
            geometry, witnesses, frozen, radial
        ),
        transitions=SyntheticStrainTransitionRefiner().execute(
            geometry, request.maximum_transition_refinement_depth
        ),
        geometry=geometry,
        witnesses=witnesses,
        frozen=frozen,
        radial=radial,
    )


def _environment() -> SyntheticStrainScanEnvironment:
    return SyntheticStrainScanEnvironment(
        python="test-python",
        platform="test-platform",
        numpy="test-numpy",
        ksdft2effmass="test-ksdft2effmass",
        projectkoios_optimization="test-optimization",
        projectkoios_physkit="test-physkit",
    )


def _write(scan: _CalculatedScan, directory: Path) -> SyntheticStrainScanArtifactPaths:
    return (
        SyntheticStrainScanArtifactWriter()
        .execute(
            scan.request,
            scan.summary,
            scan.transitions,
            scan.geometry,
            scan.witnesses,
            scan.frozen,
            scan.radial,
            directory,
            _environment(),
        )
        .paths
    )


class TestSyntheticStrainScanArtifacts:
    """Establish canonical identity binding and semantic reconstruction."""

    def test_writer__complete_scan__binds_sources_and_reconstructs_summary(
        self, tmp_path: Path
    ) -> None:
        paths = _write(_calculate_scan(), tmp_path)
        request = json.loads(paths.request_path.read_bytes())
        result = json.loads(paths.result_path.read_bytes())
        verification = json.loads(paths.verification_path.read_bytes())

        assert request["schema"] == SCAN_REQUEST_SCHEMA_ID
        assert result["schema"] == SCAN_RESULT_SCHEMA_ID
        assert verification["schema"] == SCAN_VERIFICATION_SCHEMA_ID
        assert verification["passes"] is True
        assert (
            result["scan_request_sha256"]
            == CanonicalJsonDocument(paths.request_path.read_bytes()).content_sha256()
        )
        assert (
            verification["scan_result_sha256"]
            == CanonicalJsonDocument(paths.result_path.read_bytes()).content_sha256()
        )
        assert result["summary"]["base_sample_count"] == 3
        assert len(paths.witness_paths) == len(StrainWitnessControl)
        assert all(path.is_file() for path in paths.witness_paths)

    def test_verifier__changed_derived_extremum__fails_closed(
        self, tmp_path: Path
    ) -> None:
        paths = _write(_calculate_scan(), tmp_path)
        result = json.loads(paths.result_path.read_bytes())
        result["summary"]["maximum_volume_defect"] += 1.0
        paths.result_path.write_bytes(
            (
                json.dumps(
                    result,
                    allow_nan=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
        )

        with pytest.raises(ValueError, match="source-bound semantic read-back"):
            SyntheticStrainScanArtifactVerifier().execute(paths)

    def test_verifier__mixed_grid_response_source__fails_closed(
        self, tmp_path: Path
    ) -> None:
        paths = _write(_calculate_scan(), tmp_path / "primary")
        mixed = _calculate_scan((0.0, 1.0))
        SyntheticStrainResponseResultSerializer().execute(mixed.radial).write_to(
            paths.radial_response_path
        )

        with pytest.raises(ValueError, match="response source does not match"):
            SyntheticStrainScanArtifactVerifier().execute(paths)

    def test_schemas__are_canonical_strict_and_writable(self, tmp_path: Path) -> None:
        for kind in SyntheticStrainScanSchemaKind:
            schema = SyntheticStrainScanSchema(kind)
            content = schema.canonical_bytes()
            decoded = json.loads(content)

            assert decoded["$id"] == schema.identity
            assert content == (
                json.dumps(
                    decoded,
                    allow_nan=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
            assert schema.write_to(tmp_path / kind.value).read_bytes() == content
