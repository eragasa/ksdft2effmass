"""Generate the Paper 2 simple-cubic scientific-story figure."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic3d_rank2_simple_cubic/band_equivalence_hopping_locality/render_nominal_analysis.py",
        generated_figure="calculations/periodic3d_rank2_simple_cubic/band_equivalence_hopping_locality/analysis/replaceable/figures/band-equivalence-locality-scientific-story.pdf",
    )
