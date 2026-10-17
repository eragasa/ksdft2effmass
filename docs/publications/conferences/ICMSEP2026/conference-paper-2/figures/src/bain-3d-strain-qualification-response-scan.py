"""Generate the Paper 2 3-D strain qualification and response scan."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/scan_development.py",
        generated_figure="experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/analysis/scan-development/strain-qualification-response-scan.pdf",
    )
