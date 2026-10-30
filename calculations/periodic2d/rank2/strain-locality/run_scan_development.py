"""Run the bounded 201-point 2-D strain witness and locality scan."""

from __future__ import annotations

import math
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPathEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (
    StrainResponseModelEnum,
    StrainWitnessControlEnum,
    calculate_strain_witness_scan,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (
    SyntheticStrainScanAssessor,
    SyntheticStrainScanRequest,
    SyntheticStrainTransitionRefiner,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan_plotting import (
    SyntheticStrainScanPlotRequest,
    SyntheticStrainScanPlotWriter,
)

FRACTIONS = tuple(float(index) / 200.0 for index in range(201))
TOLERANCES = (1.0e-3, 1.0e-5)
PATH = SyntheticStrainPathEnum.RHOMBIC_2D


def main() -> int:
    """Calculate, bind, verify, and plot sampled finite-strain envelopes."""
    request = SyntheticStrainScanRequest(
        path=PATH,
        strain_fractions=FRACTIONS,
        geometry_construction_size=64,
        witness_construction_size=16,
        response_construction_size=16,
        response_evaluation_size=33,
        response_evaluation_shift=1.0 / 3.0,
        maximum_rotation_amplitude=math.pi / 4.0,
        radial_decay_beta=1.0,
        tail_tolerances=TOLERANCES,
        maximum_transition_refinement_depth=5,
    )
    witnesses = tuple(
        calculate_strain_witness_scan(
            request.path,
            control,
            request.witness_construction_size,
            request.strain_fractions,
            request.maximum_rotation_amplitude,
        )
        for control in StrainWitnessControlEnum
    )
    geometry = SyntheticStrainCalculator(
        path=request.path,
        construction_size=request.geometry_construction_size,
        strain_fractions=request.strain_fractions,
        maximum_rotation_amplitude=request.maximum_rotation_amplitude,
        tail_tolerances=request.tail_tolerances,
    ).execute()
    transitions = SyntheticStrainTransitionRefiner(
        base_result=geometry,
        maximum_refinement_depth=request.maximum_transition_refinement_depth,
    ).execute()
    frozen = calculate_synthetic_strain_response(
        request.path,
        StrainResponseModelEnum.M1_FROZEN,
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
        StrainResponseModelEnum.M2_RADIAL,
        request.response_construction_size,
        request.response_evaluation_size,
        request.response_evaluation_shift,
        request.strain_fractions,
        request.maximum_rotation_amplitude,
        request.radial_decay_beta,
        request.tail_tolerances,
    )
    summary = SyntheticStrainScanAssessor(
        geometry_result=geometry,
        witness_results=witnesses,
        frozen_response=frozen,
        radial_response=radial,
    ).execute()
    output = Path(__file__).resolve().parent / "analysis" / "development" / "scan"
    output.mkdir(parents=True, exist_ok=True)
    typed_artifacts = (
        (output / "rhombic-2d-strain-scan-request.json", request),
        (output / "rhombic-2d-geometry-source.json", geometry),
        *(
            (
                output
                / (
                    "rhombic-2d-"
                    f"{witness.control.to_wire().replace('_', '-')}-witness-source.json"
                ),
                witness,
            )
            for witness in witnesses
        ),
        (output / "rhombic-2d-frozen-response-source.json", frozen),
        (output / "rhombic-2d-radial-response-source.json", radial),
        (output / "rhombic-2d-strain-scan-summary.json", summary),
        (output / "rhombic-2d-strain-transition-refinement.json", transitions),
    )
    for artifact_path, artifact in typed_artifacts:
        artifact_path.write_bytes(artifact.to_json())
    result = SyntheticStrainScanPlotWriter(
        request=SyntheticStrainScanPlotRequest(
            witness_results=witnesses,
            geometry_result=geometry,
            frozen_response=frozen,
            radial_response=radial,
            output_directory=output,
            title="2-D rhombic synthetic-strain scan",
        )
    ).execute()
    print(
        f"lifecycle=development path={request.path.to_wire()} "
        f"strain_samples={len(request.strain_fractions)}"
    )
    print(
        f"maximum_volume_defect={summary.maximum_volume_defect:.17g} "
        f"strain_fraction={summary.maximum_volume_defect_strain_fraction:.17g}"
    )
    print(
        f"maximum_direct_band_defect={summary.maximum_direct_band_defect:.17g} "
        f"strain_fraction={summary.maximum_direct_band_defect_strain_fraction:.17g}"
    )
    for witness in summary.witness_requirements:
        print(
            f"witness={witness.control.to_wire()} "
            f"optimized_maximum={witness.optimized_maximum:.17g} "
            f"optimized_strain_fraction={witness.optimized_maximum_strain_fraction:.17g}"
        )
    for locality in summary.locality:
        print(
            f"tail_tolerance={locality.tail_tolerance:.17g} "
            f"maximum_physical_radius={locality.maximum_physical_radius:.17g} "
            f"maximum_retained_blocks={locality.maximum_retained_blocks}"
        )
    for response in summary.responses:
        print(
            f"response={response.control.to_wire()} "
            f"maximum_aligned_hamiltonian_defect="
            f"{response.maximum_aligned_hamiltonian_defect:.17g} "
            f"strain_fraction={response.maximum_strain_fraction:.17g}"
        )
    print(
        f"qualification_records={len(summary.qualifications)} "
        f"approximation_records={len(summary.approximations)} "
        f"mechanism_records={len(summary.mechanisms)} "
        f"shell_transitions={len(transitions.shell_transitions)} "
        f"bond_degeneracy_transitions={len(transitions.bond_degeneracy_transitions)}"
    )
    for artifact_path, _ in typed_artifacts:
        print(f"output={artifact_path}")
    for path in result.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
