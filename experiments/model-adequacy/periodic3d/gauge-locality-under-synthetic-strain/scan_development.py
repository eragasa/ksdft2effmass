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
    SyntheticStrainTransitionRefiner,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_scan_plotting import (  # noqa: E501
    SyntheticStrainScanPlotRequest,
    SyntheticStrainScanPlotWriter,
)

FRACTIONS = tuple(float(index) / 200.0 for index in range(201))
TOLERANCES = (1.0e-3, 1.0e-5)
PATH = SyntheticStrainPath.BAIN_3D


def main() -> None:
    """Calculate and plot replaceable sampled development envelopes."""
    witnesses = tuple(
        calculate_strain_witness_scan(PATH, control, 8, FRACTIONS, math.pi / 4.0)
        for control in StrainWitnessControl
    )
    geometry = SyntheticStrainCalculator().execute(
        PATH,
        24,
        FRACTIONS,
        math.pi / 4.0,
        TOLERANCES,
    )
    transitions = SyntheticStrainTransitionRefiner().execute(geometry, 5)
    frozen = calculate_synthetic_strain_response(
        PATH,
        StrainResponseModel.M1_FROZEN,
        8,
        17,
        1.0 / 3.0,
        FRACTIONS,
        math.pi / 4.0,
        0.0,
        TOLERANCES,
    )
    radial = calculate_synthetic_strain_response(
        PATH,
        StrainResponseModel.M2_RADIAL,
        8,
        17,
        1.0 / 3.0,
        FRACTIONS,
        math.pi / 4.0,
        1.0,
        TOLERANCES,
    )
    summary = SyntheticStrainScanAssessor().execute(
        geometry,
        witnesses,
        frozen,
        radial,
    )
    output = Path(__file__).resolve().parent / "analysis" / "scan-development"
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
    for path in result.paths:
        print(path)


if __name__ == "__main__":
    main()
