"""Generate the Paper 2 square-lattice three-channel decomposition."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/plot_development.py",
        generated_figure="experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/analysis/three-channel-error-decomposition.pdf",
    )
