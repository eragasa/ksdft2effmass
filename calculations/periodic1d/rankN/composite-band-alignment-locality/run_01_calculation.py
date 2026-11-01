"""Run the direct higher-rank periodic-1D development calculation."""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path

from analysis.development.cache import (
    HigherRankDevelopmentCacheWriter,
    HigherRankDevelopmentCacheWriteRequest,
)
from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DAlignmentStudyFactory,
    Periodic1DRankNAlignmentStudyAnalyzer,
    Periodic1DRankNAlignmentStudySpecification,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationControls,
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation_result import (
    Periodic1DRankNAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite.calculation import (
    Periodic1DRankNAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.serialization import TypedJsonValueCodec
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.solidstate.electronic import (
    ClosedLoopPolarFrameTransporter,
)
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def _configuration() -> Periodic1DRankNAlignmentConfiguration:
    """Return the complete frozen version-one configuration."""
    return Periodic1DRankNAlignmentConfiguration.frozen()


def _request(
    configuration: Periodic1DRankNAlignmentConfiguration,
    retained_rank: int,
    circuit_depth: int,
) -> Periodic1DRankNAlignmentCalculationRequest:
    """Return one complete immutable calculation request."""
    return Periodic1DRankNAlignmentCalculationRequest(
        configuration=configuration,
        controls=Periodic1DRankNAlignmentCalculationControls.frozen(),
        retained_rank=retained_rank,
        circuit_depth=circuit_depth,
        ambient_basis_identifier="analytic-parent-ordered-retained-exterior-basis",
        retained_frame_identifier="analytic-retained-coordinate-frame",
        endpoint_sewing_identifier="analytic-periodic-identity-sewing",
        represented_basis_identifier="aligned-retained-orbital-basis",
        energy_reference_identifier="analytic-dimensionless-zero",
    )


def _calculate(
    request: Periodic1DRankNAlignmentCalculationRequest,
    lattice_geometry: Periodic1DLatticeGeometry,
) -> Periodic1DRankNAlignmentCalculationResult:
    """Execute one rank-first case with explicit reviewed collaborators."""
    study = Periodic1DAlignmentStudyFactory(
        Periodic1DRankNAlignmentStudySpecification(
            lattice_geometry=lattice_geometry,
            request=request,
            procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            transporter=ClosedLoopPolarFrameTransporter(),
            scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
        )
    ).create()
    return study.execute()


def _case_summary(
    result: Periodic1DRankNAlignmentCalculationResult,
) -> dict[str, JsonValue]:
    """Return a bounded development summary without claiming retained evidence."""
    final_gauge_alignments: list[JsonValue] = []
    for alignment in result.meshes[-1].gauge_alignment_results:
        summary: dict[str, JsonValue] = {
            "gauge_alignment": alignment.status.gauge_alignment.to_wire(),
            "alignment_status": alignment.status.status.to_wire(),
            "downstream_applicability": (
                None
                if alignment.status.global_unitary_downstream_applicability is None
                else alignment.status.global_unitary_downstream_applicability.to_wire()
            ),
            "support_count": len(alignment.supports),
        }
        if len(alignment.supports) > 2:
            support_two = alignment.supports[2]
            summary["support_two_normalized_tail_l2"] = (
                support_two.normalized_omitted_frobenius_l2_norm
            )
            summary["support_two_normalized_total_operator_error"] = (
                support_two.total.errors.normalized_matrix_frobenius_maximum
            )
            summary["support_two_normalized_total_spectrum_error"] = (
                support_two.total.errors.normalized_ordered_spectrum_maximum
            )
        final_gauge_alignments.append(summary)
    return {
        "case_identity": result.request.case_identity,
        "retained_rank": result.request.retained_rank,
        "circuit_depth": result.request.circuit_depth,
        "construction_mesh_count": len(result.meshes),
        "block_refinement_record_count": len(result.block_refinements),
        "scalar_refinement_record_count": len(result.scalar_refinements),
        "final_mesh_gauge_alignments": final_gauge_alignments,
    }


def _calculation_results(
    configuration: Periodic1DRankNAlignmentConfiguration,
    lattice_geometry: Periodic1DLatticeGeometry,
) -> tuple[Periodic1DRankNAlignmentCalculationResult, ...]:
    """Calculate every frozen case for explicitly unverified development use."""
    return tuple(
        _calculate(
            _request(configuration, retained_rank, circuit_depth),
            lattice_geometry,
        )
        for retained_rank in configuration.retained_ranks
        for circuit_depth in configuration.circuit_depths
    )


def _summary(
    results: tuple[Periodic1DRankNAlignmentCalculationResult, ...],
    lattice_geometry: Periodic1DLatticeGeometry,
) -> dict[str, JsonValue]:
    """Return a development-only shape summary for complete calculated results."""
    configuration = results[0].request.configuration
    cases: list[JsonValue] = [_case_summary(result) for result in results]
    return {
        "artifact_role": "replaceable-direct-development-summary",
        "scientific_evidence": False,
        "family_identity": configuration.family_identity,
        "version_identity": configuration.version_identity,
        "lattice_geometry": {
            "lattice_period": lattice_geometry.lattice_period,
            "lattice_unit": lattice_geometry.lattice_unit.expression,
        },
        "case_count": len(cases),
        "cases": cases,
    }


def main() -> int:
    """Calculate once and write canonical reusable calculation-cache bytes."""
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "direct-development-summary.json"
    cache_directory = output / "development-cache"
    configuration = _configuration()
    lattice_geometry = configuration.reduced_lattice_geometry
    source_types = (
        Periodic1DAlignmentStudyFactory,
        Periodic1DRankNAlignmentStudyAnalyzer,
        Periodic1DRankNAlignmentAnalyzer,
        Periodic1DRankNAlignmentConfiguration,
        Periodic1DRankNAlignmentCalculationResult,
        ScalarRefinementAnalyzer,
        NumpyBatchedComplexUnitaryProcrustesSolver,
        ClosedLoopPolarFrameTransporter,
        FinitePeriodicMatrixFourierTransformer,
        FinitePeriodicMatrixFourierTensorEvaluator,
    )
    source_inventory = (
        ("calculation-configuration.json", configuration.to_json()),
        (
            "lattice-geometry.json",
            TypedJsonValueCodec().serialize_bytes(
                {
                    "lattice_period": lattice_geometry.lattice_period,
                    "lattice_unit": lattice_geometry.lattice_unit,
                }
            ),
        ),
    ) + tuple(
        (
            f"{source_type.__module__}.{source_type.__qualname__}",
            Path(inspect.getfile(source_type)).read_bytes(),
        )
        for source_type in source_types
    )
    infrastructure_digest = hashlib.sha256(
        b"ksdft2effmass.calculation-infrastructure.v1\x00"
    )
    for source_name, source_bytes in sorted(source_inventory):
        encoded_name = source_name.encode("utf-8")
        infrastructure_digest.update(len(encoded_name).to_bytes(8, "big"))
        infrastructure_digest.update(encoded_name)
        infrastructure_digest.update(len(source_bytes).to_bytes(8, "big"))
        infrastructure_digest.update(source_bytes)
    infrastructure_sha256 = infrastructure_digest.hexdigest()
    results = _calculation_results(configuration, lattice_geometry)
    payload = _summary(results, lattice_geometry)
    destination.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest = HigherRankDevelopmentCacheWriter(
        HigherRankDevelopmentCacheWriteRequest(
            calculation_results=results,
            lattice_geometry=lattice_geometry,
            cache_directory=cache_directory,
            calculation_infrastructure_sha256=infrastructure_sha256,
        )
    ).execute()
    print(
        "lifecycle=replaceable-direct-development-cache "
        f"scientific_evidence=false case_count={payload['case_count']} "
        f"calculation_infrastructure_sha256={infrastructure_sha256} "
        f"cache_entry_count={len(manifest.entries)} output={destination}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
