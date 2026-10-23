# Square-lattice rank-two band-equivalence and locality: technical report

## Scope

This report covers the synthetic periodic two-dimensional orthogonal square-lattice family and its rank-two retained operator. It supports Paper B but is calculation-owned and publication-independent.

## Method

The development entrypoints construct typed requests at the declared base mesh and two bounded refinements, calculate spectral and operator diagnostics, and invoke the independent in-repository result verifier. The plotting entrypoint recomputes the typed diagnostics and renders scientific-story, refinement, error-channel, shell-profile, and first-passing-shell views.

## Evidence status

The scripts and schemas are maintained code. Generated JSON and figures are replaceable development output. No immutable retained run, checksum manifest, or production evidence package is asserted.

## Interpretation boundary

The calculation compares band agreement, represented-operator agreement, and hopping locality for a controlled square-lattice family. It does not establish convergence beyond the sampled ladder, material applicability, or experimental validity.

## Provenance

The scientific protocol remains in the corresponding experiment root. Reusable mathematics, schemas, verification, and plotting implementations remain under `python/src/ksdft2effmass/`; this calculation root owns only composition and replaceable outputs.
