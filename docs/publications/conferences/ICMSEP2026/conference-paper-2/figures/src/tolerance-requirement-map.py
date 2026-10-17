"""Generate the Paper 2 tolerance-requirement map."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/band-equivalence-dimensional-comparison/plot_development.py",
        generated_figure="experiments/model-adequacy/band-equivalence-dimensional-comparison/analysis/development/tolerance-requirement-map.pdf",
    )
