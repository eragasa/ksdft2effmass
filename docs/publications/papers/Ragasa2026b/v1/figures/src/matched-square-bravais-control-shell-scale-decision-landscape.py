"""Generate the matched-square shell--scale decision landscape."""

from _publish import publish

if __name__ == "__main__":
    publish(
        generator="calculations/band-equivalence-dimensional-comparison/plot_shell_scale_decision_landscapes.py",
        generated_figure="calculations/band-equivalence-dimensional-comparison/analysis/development/generated/matched-square-bravais-control-shell-scale-decision-landscape.pdf",
    )
