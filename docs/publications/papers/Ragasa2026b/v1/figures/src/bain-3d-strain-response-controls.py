"""Generate the Paper 2 Bain strain-response controls."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/run_response_controls.py",
        generated_figure="calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/analysis/replaceable/response/m1-m2-strain-response.pdf",
    )
