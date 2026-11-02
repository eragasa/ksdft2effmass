"""Generate the Paper 2 rhombic strain-response controls."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d_rank2_rhombic_path/band_equivalence_hopping_locality/run_response_controls.py",
        generated_figure="calculations/periodic2d_rank2_rhombic_path/band_equivalence_hopping_locality/analysis/replaceable/response/m1-m2-strain-response.pdf",
    )
