"""Generate the Paper 2 3-D strain qualification and response scan."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/run_path_scan.py",
        generated_figure="calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/analysis/replaceable/scan/strain-qualification-response-scan.pdf",
    )
