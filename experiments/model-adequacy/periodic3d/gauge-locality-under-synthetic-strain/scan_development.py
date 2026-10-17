"""Run the bounded 201-point 3-D Bain witness and locality scan."""

from __future__ import annotations

import math
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPath,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    StrainWitnessControl,
    calculate_strain_witness_scan,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (  # noqa: E501
    SyntheticStrainScanAssessor,
    SyntheticStrainScanRequest,
    SyntheticStrainTransitionRefiner,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_scan_plotting import (  # noqa: E501
    SyntheticStrainScanPlotRequest,
    SyntheticStrainScanPlotWriter,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_scan_serialization import (  # noqa: E501
    SyntheticStrainScanArtifactWriter,
    SyntheticStrainScanEnvironment,
)

FRACTIONS = tuple(float(index) / 200.0 for index in range(201))
TOLERANCES = (1.0e-3, 1.0e-5)
PATH = SyntheticStrainPath.BAIN_3D


def main() -> None:
    """Calculate, bind, verify, and plot sampled finite-strain envelopes."""
    request = SyntheticStrainScanRequest(
        path=PATH,
        strain_fractions=FRACTIONS,
        geometry_construction_size=24,
        witness_construction_size=8,
        response_construction_size=8,
        response_evaluation_size=17,
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
        for control in StrainWitnessControl
    )
    geometry = SyntheticStrainCalculator().execute(
        request.path,
        request.geometry_construction_size,
        request.strain_fractions,
        request.maximum_rotation_amplitude,
        request.tail_tolerances,
    )
    transitions = SyntheticStrainTransitionRefiner().execute(
        geometry, request.maximum_transition_refinement_depth
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
    summary = SyntheticStrainScanAssessor().execute(
        geometry,
        witnesses,
        frozen,
        radial,
    )
    output = Path(__file__).resolve().parent / "analysis" / "scan-development"
    artifacts = SyntheticStrainScanArtifactWriter().execute(
        request,
        summary,
        transitions,
        geometry,
        witnesses,
        frozen,
        radial,
        output,
        SyntheticStrainScanEnvironment.capture(),
    )
    result = SyntheticStrainScanPlotWriter().execute(
        SyntheticStrainScanPlotRequest(
            witness_results=witnesses,
            geometry_result=geometry,
            frozen_response=frozen,
            radial_response=radial,
            output_directory=output,
            title="3-D Bain synthetic-strain scan",
        )
    )
    print(
        "maximum-volume-defect",
        summary.maximum_volume_defect,
        summary.maximum_volume_defect_strain_fraction,
    )
    print(
        "maximum-direct-band-defect",
        summary.maximum_direct_band_defect,
        summary.maximum_direct_band_defect_strain_fraction,
    )
    for witness in summary.witness_requirements:
        print(
            witness.control.value,
            witness.optimized_maximum,
            witness.optimized_maximum_strain_fraction,
            witness.fixed_candidate_maximum,
            witness.fixed_candidate_maximum_strain_fraction,
        )
    for locality in summary.locality:
        print(
            "locality-envelope",
            locality.tail_tolerance,
            locality.maximum_physical_radius,
            locality.maximum_physical_radius_strain_fraction,
            locality.maximum_retained_blocks,
            locality.maximum_retained_blocks_strain_fraction,
        )
    for response in summary.responses:
        print(
            "response-envelope",
            response.control.value,
            response.maximum_aligned_hamiltonian_defect,
            response.maximum_strain_fraction,
        )
    for qualification in summary.qualifications:
        print("qualification-envelope", qualification)
    for approximation in summary.approximations:
        print("approximation-envelope", approximation)
    for mechanism in summary.mechanisms:
        print("response-mechanism-envelope", mechanism)
    for shell_transition in transitions.shell_transitions:
        print(
            "shell-transition",
            shell_transition.tail_tolerance,
            shell_transition.left_strain_fraction,
            shell_transition.right_strain_fraction,
            shell_transition.left_retained_blocks,
            shell_transition.right_retained_blocks,
        )
    for bond_transition in transitions.bond_degeneracy_transitions:
        print(
            "bond-degeneracy-transition",
            bond_transition.left_strain_fraction,
            bond_transition.right_strain_fraction,
            bond_transition.left_distinct_bond_lengths,
            bond_transition.right_distinct_bond_lengths,
        )
    for path in (*artifacts.paths.witness_paths, *result.paths):
        print(path)
    print(artifacts.paths.request_path)
    print(artifacts.paths.geometry_path)
    print(artifacts.paths.frozen_response_path)
    print(artifacts.paths.radial_response_path)
    print(artifacts.paths.result_path)
    print(artifacts.paths.verification_path)


if __name__ == "__main__":
    main()
