"""Generate the Paper 2 triangular/honeycomb scientific-story figure."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/plot_development.py",
        generated_figure="experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/analysis/band-equivalence-locality-scientific-story.pdf",
    )
