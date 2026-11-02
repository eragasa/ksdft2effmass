# Two-dimensional synthetic-strain locality: technical report

## Scope

This report covers the area-preserving rhombic triangular-to-square controlled path and its rank-two locality diagnostics. It separates geometry-only M0, frozen-response M1, radial-response M2, and combined scan outputs.

## Method

The development scripts evaluate sampled strain fractions, geometry and support changes, restricted alignment residuals, hopping-tail decisions, response defects, qualification records, and transition records. Result serialization and schema validation are performed by maintained `ksdft2effmass` owners.

## Current replaceable development summary

The bounded M0 action preserves the normalized restricted residual at `0.3418465443`
and Parseval to `1.2e-16`. From the triangular to square-metric endpoint, the first
radius at tail tolerance `1e-5` changes from about `3.7224` to `4.2426`, while the
retained block count changes from `43` to `61`. This is a sampled frozen-gauge geometry
result, not a material-strain result.

In the separately labeled M1/M2 smoke action, M1's aligned path difference remains at
roundoff. With the prospectively fixed synthetic M2 law and `beta=1`, the square-metric
endpoint has hopping responses from about `0.81758` to `1.27146` and a maximum aligned
retained-space perturbation of about `0.063575 E_ref`. This action is unconverged and has
no retained-evidence status.

## Evidence status

JSON and plots under `analysis/replaceable/` are replaceable unsealed artifacts. They are not a retained run, convergence certificate, or external validation package.

## Interpretation boundary

The path is a synthetic geometry control. It is not an elastic model, graphene calculation, stress--strain prediction, or phase-stability analysis.

## Provenance

The authoritative research specification is [`../protocol.md`](../protocol.md). This
calculation root owns the protocol, development composition, output locations, and
technical report; reusable implementations remain in `python/src/ksdft2effmass/`. The
former experiment-tree location is a legacy forward pointer only.
