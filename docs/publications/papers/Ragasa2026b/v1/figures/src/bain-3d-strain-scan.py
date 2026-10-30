"""Generate the Paper 2 sampled 3-D Bain strain scan."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic3d/rank2/strain-locality/run_scan_development.py",
        generated_figure="calculations/periodic3d/rank2/strain-locality/analysis/development/scan/strain-witness-locality-scan.pdf",
    )
