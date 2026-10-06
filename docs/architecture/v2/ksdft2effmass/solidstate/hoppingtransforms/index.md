# `solid_state.hopping_transforms`

## Purpose and status

This implemented numerical module owns role-neutral reciprocal matrix samples,
band-frame projection, complete reciprocal/hopping transforms, hopping truncation, and
related represented mechanics. Scientific parent, retained, or effective-model meaning
is attached only by explicit composing objects.

## Row-026 owner

[`ReciprocalOperatorSamples1D`](ReciprocalOperatorSamples1D/index.md) stores ordered
coordinates, reciprocal period, and homogeneous square matrix values. Its class does not
infer whether those matrices are parent, projected, retained, or reconstructed.

## Code and evidence

Source: `python/src/ksdft2effmass/solid_state/hopping_transforms.py`.
Tests: `python/tests/software_verification/ksdft2effmass/solid_state/test__ReciprocalOperatorSamples1D.py`, projection tests, and Fourier-transform tests.
Sphinx: `doc/sphinx/api/solid-state.rst` and the represented-operator API page.

These are finite represented numerical operations. Passing does not establish a
scientific retained operator, convergence, physical adequacy, validation, UQ, or
acceptance.
