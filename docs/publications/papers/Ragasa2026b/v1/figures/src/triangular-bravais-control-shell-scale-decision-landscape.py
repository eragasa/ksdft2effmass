"""Generate the triangular-control shell--scale decision landscape."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="experiments/model-adequacy/band-equivalence-dimensional-comparison/plot_shell_scale_decision_landscapes.py",
        generated_figure="experiments/model-adequacy/band-equivalence-dimensional-comparison/analysis/development/triangular-bravais-control-shell-scale-decision-landscape.pdf",
    )
