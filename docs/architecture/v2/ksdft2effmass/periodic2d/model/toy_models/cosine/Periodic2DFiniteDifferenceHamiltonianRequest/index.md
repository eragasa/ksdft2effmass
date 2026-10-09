# `Periodic2DFiniteDifferenceHamiltonianRequest`

## Purpose and status

This implemented row-035 campaign-adapter request binds the exact cosine scientific
parent, reduced momentum, and odd square-grid extent.

Its derived grid retains the period-`2*pi` half-open points, `x_outer_y_inner` order,
spacing, represented dimension, and directed Bloch seam phases. The request does not
itself infer reusable metadata: its constructor adapter supplies the authorized
Euclidean basis, dimensionless energy, model-zero, source/operator/state-space, and
provenance contract when composing the reusable request.

No convergence tolerance or scientific acceptance policy is present.
