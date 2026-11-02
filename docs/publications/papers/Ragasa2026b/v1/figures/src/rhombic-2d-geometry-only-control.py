"""Generate the Paper 2 rhombic geometry-only strain control."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d_rank2_rhombic_path/band_equivalence_hopping_locality/run_geometry_control.py",
        generated_figure="calculations/periodic2d_rank2_rhombic_path/band_equivalence_hopping_locality/analysis/replaceable/results/gauge-locality-under-synthetic-strain.pdf",
    )
