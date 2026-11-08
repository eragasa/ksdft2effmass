# Certifications

## Status

`ksdft2effmass.certifications` is the implemented owner for scientific certification
contracts. A certification binds one exact proposition to exact inputs, claimed
outward enclosures, independent containment evidence, and a conservative disposition.
It is distinct from:

- software verification, which checks implementation behavior;
- numerical verification, which checks a numerical method against declared mathematics;
- scientific validation, which assesses adequacy for an intended physical use; and
- human acceptance, publication, or release authority.

The first implemented leaf is
[`periodic1d/rank1/first_passing_support`](periodic1d/rank1/first_passing_support/index.md).
It owns the exact wire contract for the finite rank-one first-passing-support
proposition. Its optional `arb` provider leaf owns local lowest-parent-eigenvalue and
transform-mediated maximum-error enclosure actions. The direct objective and independent
containment verifier remain absent, and no checked retained runtime certificate is
claimed.

## Ownership boundary

The certification root owns:

- proposition-specific immutable request and result records;
- exact rational endpoint and conservative disposition semantics;
- domain-owned `_mapping()` and `_from_mapping()` contracts using the shared final
  `to_dict()`, `from_dict()`, `to_json()`, and `from_json()` boundary;
- correlation of proposition, source, result, producer, verifier, and retained artifact
  identities; and
- explicit unresolved outcomes when the intervals do not decide the proposition.

Scientific analyses continue to own the quantities being certified. In particular,
`periodic1d.fourier_locality` owns the finite Fourier and direct-fit calculations, while
the rank-one band-equivalence/hopping-locality calculation owns its retained scientific
composition. Certification consumes those exact identities; it does not become their
analysis or calculation owner.

Provider-specific interval engines belong beneath the applicable certification leaf and
must not be imported by the dependency-free wire contract. The reviewed `certificates`
extra pins `python-flint==0.9.0`; any additional or replacement enclosure engine remains
a separately reviewed dependency decision.

## Package map

- Source: `python/src/ksdft2effmass/certifications/`
- Tests: `python/tests/ksdft2effmass/certifications/`
- [Implementation](implementation.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
