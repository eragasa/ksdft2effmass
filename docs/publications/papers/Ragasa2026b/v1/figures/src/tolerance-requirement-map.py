"""Generate the Paper 2 tolerance-requirement map."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/band-equivalence-dimensional-comparison/plot_development.py",
        generated_figure="calculations/band-equivalence-dimensional-comparison/analysis/development/generated/tolerance-requirement-map.pdf",
    )
