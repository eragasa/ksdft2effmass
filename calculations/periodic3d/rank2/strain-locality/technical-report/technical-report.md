# Three-dimensional Bain-path synthetic-strain locality: technical report

## Scope

This report covers the volume-preserving FCC-to-BCC Bain controlled path and its rank-two locality diagnostics. It separates geometry-only M0, frozen-response M1, radial-response M2, and combined scan outputs.

## Method

The development scripts evaluate sampled strain fractions, geometry and support transitions, alignment residuals, hopping-tail decisions, response defects, qualification records, and transition records. Maintained serializers and schemas validate the generated development documents.

## Evidence status

JSON and plots under `analysis/development/` are replaceable development artifacts. No retained production run, convergence certificate, or first-principles evidence package exists here.

## Interpretation boundary

The Bain path is a synthetic control. It does not predict phase stability, model material silicon, or establish thermodynamic or experimental validity.

## Provenance

The experiment root retains the specification. This root owns the calculation composition and output locations; reusable implementations remain in `python/src/ksdft2effmass/`.
