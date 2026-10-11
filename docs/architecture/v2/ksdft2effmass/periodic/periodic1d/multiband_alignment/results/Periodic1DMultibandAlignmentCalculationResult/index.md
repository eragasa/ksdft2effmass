# `Periodic1DMultibandAlignmentCalculationResult`

## Purpose

Immutable aggregate correlation boundary for M2.

## Fields

It binds the exact definition; common training/evaluation target spectra; diagnostics;
reference, attacked, and pointwise-aligned complete Fourier transforms; three matching
Hermiticity results; and the ordered range study.

## Invariants

The aggregate enforces calculation identity, rank, meshes, coordinate units, target
roles, external-gap threshold, frame-transport thresholds, transform tolerances,
representatives, energy units, Hermiticity ownership, and exact range sequence.
Cross-wired records with compatible shapes are rejected.

## Evidence and limitations

M2 execution, construction, serialization, determinism, verifier, and mutation tests
exercise this boundary. It summarizes the frozen synthetic calculation and does not
encode scientific acceptance or a universal gauge claim.
