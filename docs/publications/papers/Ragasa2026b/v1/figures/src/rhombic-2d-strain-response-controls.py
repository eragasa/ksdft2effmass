"""Generate the Paper 2 rhombic strain-response controls."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/run_response_development.py",
        generated_figure="experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/analysis/response-development/m1-m2-strain-response.pdf",
    )
