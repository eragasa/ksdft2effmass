"""Generate the Paper 2 sampled 2-D rhombic strain scan."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/scan_development.py",
        generated_figure="experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/analysis/scan-development/strain-witness-locality-scan.pdf",
    )
