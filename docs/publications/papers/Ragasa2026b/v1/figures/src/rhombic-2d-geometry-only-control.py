"""Generate the Paper 2 rhombic geometry-only strain control."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/run_development.py",
        generated_figure="experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/analysis/development/gauge-locality-under-synthetic-strain.pdf",
    )
