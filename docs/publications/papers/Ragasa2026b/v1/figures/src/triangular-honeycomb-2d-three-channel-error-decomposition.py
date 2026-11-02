"""Generate the Paper 2 triangular/honeycomb three-channel decomposition."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d_rank2_hexagonal/band_equivalence_hopping_locality/render_nominal_analysis.py",
        generated_figure="calculations/periodic2d_rank2_hexagonal/band_equivalence_hopping_locality/analysis/replaceable/figures/three-channel-error-decomposition.pdf",
    )
