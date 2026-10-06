# `Periodic1DIsolatedBandParentDiscretization`

## Purpose and status

This implemented row-023 numerical-evidence DataObject keeps the cutoff-11 finite
plane-wave parent and its historical comparison against a separately identified
cutoff-15 finite basis distinct from the untruncated Fourier parent.

## Contract

The record binds the exact finite parent representation, higher-cutoff reference basis,
nonempty comparison momenta, positive compared-band count, matching cutoff observation,
and explicit provenance identity. Both bases use the same reciprocal vector; the
reference cutoff exceeds the represented cutoff.

## Error and claim boundary

The retained observation compares the first three represented bands at five declared
momenta. Its recorded maximum difference is evidence between two finite Galerkin
representations. The sequence is nonmonotone at approximately binary64 scale, so the
value is not a rigorous bound against the untruncated parent, a convergence proof,
physical uncertainty, validation result, or acceptance criterion.

The hierarchy test checks the cutoff, dimension, mesh, reference, momentum set, band
count, and exact retained observation.
