# Periodic-3D rank-two Bain-path synthetic-strain locality

## Scope

This report covers the unit-primitive-volume FCC-to-BCC Bain controlled path and its
rank-two locality diagnostics. It separates:

- M0 geometry/frozen-gauge locality;
- M1 four-state frozen response;
- M2 prescribed radial response;
- common-cell, endpoint, and path qualification witnesses; and
- the bounded base-grid and transition-refinement scan.

The governing calculation-owned protocol is [`../protocol.md`](../protocol.md).

## Method and action ownership

- [`../run_geometry_control.py`](../run_geometry_control.py) evaluates M0 geometry,
  alignment, Parseval, shell, and hopping-tail diagnostics.
- [`../run_response_controls.py`](../run_response_controls.py) evaluates separately
  labeled M1 and M2 matrix, band, and hopping-response channels.
- [`../run_path_scan.py`](../run_path_scan.py) evaluates the 201-point base grid,
  qualification records, operator-requirement envelopes, and declared transition
  refinement.

The actions write only to `analysis/replaceable/`. Maintained serializers and schemas
validate those generated documents. The actions do not own retained-execution,
visualization-lifecycle, or publication authority.

## Evidence status

No JSON or plot is retained in this calculation root. Generated products under
`analysis/replaceable/` are replaceable development artifacts. No production run,
continuum or convergence certificate, first-principles evidence package, accepted
operator tolerance, or retained common path witness exists here.

Previously reported finite-sample M0, M1, and M2 observations remain development values;
they are not rerun or independently validated by this migration. The pointwise optimized
operator requirement is not one common path witness. A constant reference candidate is
not scientific evidence until frozen limits establish feasibility at every required
fraction and between-sample bounds establish the claimed path scope.

## Interpretation boundary

The Bain path is a synthetic geometry and response control. It does not predict elastic
energy, stress, phase stability, a martensitic transition, silicon behavior, or any other
thermodynamic, experimental, or material result. Geometry-driven physical-radius changes,
frozen-parent behavior, and the prescribed radial response remain distinct claims.

## Provenance

This calculation root owns the context, scientific protocol, executable composition,
replaceable output paths, and technical report. The legacy experiment path is a forward
pointer only. Reusable maintained software remains under
`python/src/ksdft2effmass/`; this migration neither changes it nor executes a scientific
calculation.
