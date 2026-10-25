# Simple-cubic rank-two band-equivalence and locality: technical report

## Scope

This report covers the synthetic periodic three-dimensional orthogonal simple-cubic family. The retained operator has rank two; dimensionality and retained rank are distinct.

## Method

The bounded development entrypoints evaluate the base mesh and two refinement points, serialize typed diagnostics, and invoke the independent in-repository verifier. The plotting entrypoint renders cross-channel and locality diagnostics from the declared requests.

## Evidence status

All generated artifacts remain replaceable development output. No retained production run, checksum-bound evidence package, or complete convergence claim exists.

## Interpretation boundary

The calculation supports controlled cross-dimensional comparison. It does not model a named material or validate a bulk three-dimensional reduction.

## Provenance

The experiment root owns the protocol. Reusable calculations, records, serializers, verifiers, and plotters remain in `python/src/ksdft2effmass/`; this root owns their calculation-specific composition.
