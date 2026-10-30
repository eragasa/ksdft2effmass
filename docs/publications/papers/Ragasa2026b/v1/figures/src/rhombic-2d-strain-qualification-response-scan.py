"""Generate the Paper 2 2-D strain qualification and response scan."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d/rank2/strain-locality/run_scan_development.py",
        generated_figure="calculations/periodic2d/rank2/strain-locality/analysis/development/scan/strain-qualification-response-scan.pdf",
    )
