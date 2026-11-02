"""Generate the Paper 2 2-D strain qualification and response scan."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d_rank2_rhombic_path/band_equivalence_hopping_locality/run_path_scan.py",
        generated_figure="calculations/periodic2d_rank2_rhombic_path/band_equivalence_hopping_locality/analysis/replaceable/scan/strain-qualification-response-scan.pdf",
    )
