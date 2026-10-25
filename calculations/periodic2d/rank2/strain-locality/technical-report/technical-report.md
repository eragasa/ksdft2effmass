# Two-dimensional synthetic-strain locality: technical report

## Scope

This report covers the area-preserving rhombic triangular-to-square controlled path and its rank-two locality diagnostics. It separates geometry-only M0, frozen-response M1, radial-response M2, and combined scan outputs.

## Method

The development scripts evaluate sampled strain fractions, geometry and support changes, restricted alignment residuals, hopping-tail decisions, response defects, qualification records, and transition records. Result serialization and schema validation are performed by maintained `ksdft2effmass` owners.

## Evidence status

JSON and plots under `analysis/development/` are replaceable development artifacts. They are not a retained run, convergence certificate, or external validation package.

## Interpretation boundary

The path is a synthetic geometry control. It is not an elastic model, graphene calculation, stress--strain prediction, or phase-stability analysis.

## Provenance

The experiment root retains the specification. This calculation root owns the development composition and output locations; reusable implementations remain in `python/src/ksdft2effmass/`.
