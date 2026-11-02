"""Generate the Paper 2 Bain geometry-only strain control."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/run_geometry_control.py",
        generated_figure="calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/analysis/replaceable/results/gauge-locality-under-synthetic-strain.pdf",
    )
