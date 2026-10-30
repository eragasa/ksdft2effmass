"""Generate the Paper 2 rhombic strain-response controls."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/periodic2d/rank2/strain-locality/run_response_development.py",
        generated_figure="calculations/periodic2d/rank2/strain-locality/analysis/development/response/m1-m2-strain-response.pdf",
    )
