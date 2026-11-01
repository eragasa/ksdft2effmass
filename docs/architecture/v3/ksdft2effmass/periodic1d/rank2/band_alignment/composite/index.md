# `ksdft2effmass.periodic1d.rank2.band_alignment.composite`

## Purpose

This package owns the direct rank-two composite-band alignment and block-locality
vertical slice. It composes an exact four-state parent and lowest-two-state frames with
the rank-first frame-transport, gauge-alignment, hopping-locality, and
support-truncation capabilities. It assembles their represented-Hamiltonian and finite
range evidence into the established aggregate result before independent verification
and authenticated rendering. The composite package does not own those consumed
capabilities.

## Public modules

The package initializer is an inert namespace. Consumers import values and actions
from the authoritative defining modules below rather than from package re-exports.

- [`configuration`](../configuration/index.md) owns genuine frozen scientific inputs.
- [`result`](result/index.md) owns explicit immutable output sections and the root wire.
- [`analysis`](analysis/index.md) owns the pure `execute()` producer.
- [`reference`](reference/index.md) owns request-bound producer-independent numerical
  reconstruction.
- [`verification`](verification/index.md) owns exact-byte admission and aggregate
  authentication.
- [`visualizations`](visualizations/index.md) owns the authenticated projection and
  closed three-PNG inventory.

The package imports no historical campaign, `multiband_alignment`, or calculation-local
workflow code. It is distinct from band-equivalence/locality and from M3 admissible-set
policy. The obsolete unranked `periodic1d.composite_band_alignment` source path is not
retained as a compatibility package.
