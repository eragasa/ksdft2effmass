"""Generate the Paper 2 square-lattice scientific-story figure."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d/rank2/orthogonal/band-equivalence-locality/plot_development.py",
        generated_figure="calculations/periodic2d/rank2/orthogonal/band-equivalence-locality/analysis/development/figures/band-equivalence-locality-scientific-story.pdf",
    )
