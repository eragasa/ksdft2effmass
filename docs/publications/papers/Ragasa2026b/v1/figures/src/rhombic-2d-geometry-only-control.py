"""Generate the Paper 2 rhombic geometry-only strain control."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d/rank2/strain-locality/run_development.py",
        generated_figure="calculations/periodic2d/rank2/strain-locality/analysis/development/results/gauge-locality-under-synthetic-strain.pdf",
    )
