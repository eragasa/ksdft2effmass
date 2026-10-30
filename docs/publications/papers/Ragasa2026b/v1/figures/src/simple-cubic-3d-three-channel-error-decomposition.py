"""Generate the Paper 2 simple-cubic three-channel decomposition."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/plot_development.py",
        generated_figure="calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/analysis/development/figures/three-channel-error-decomposition.pdf",
    )
