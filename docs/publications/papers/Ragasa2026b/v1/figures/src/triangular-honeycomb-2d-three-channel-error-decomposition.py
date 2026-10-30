"""Generate the Paper 2 triangular/honeycomb three-channel decomposition."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/plot_development.py",
        generated_figure="calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/analysis/development/figures/three-channel-error-decomposition.pdf",
    )
