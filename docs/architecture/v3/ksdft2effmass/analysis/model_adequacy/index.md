# `ksdft2effmass.analysis.model_adequacy`

## Purpose

`model_adequacy` owns reusable analyses that compare a declared represented model with a
declared finite approximation or support restriction. It does not decide experiment
identity, retained-evidence status, sealing, publication acceptance, or execution
policy.

## Implemented child

- [`band_equivalence_locality`](band_equivalence_locality/index.md) owns the typed
  multidimensional rank-two band-equivalence and hopping-locality calculation,
  exact-byte verification, and authenticated visualization projection.

## Boundary

A model-adequacy result states its finite spaces, basis and gauge relation, sampling
meshes, support inventory, error channels, and applicable thresholds. It does not turn
sampled agreement into continuum convergence, uncertainty quantification, or material
validation.
