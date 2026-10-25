# Rank-one single-band Fourier-locality protocol

**Lifecycle:** pre-execution design.

## Question

What Fourier interpolation and hopping-support truncation behavior does a scalar periodic retained Hamiltonian exhibit when evaluated under conventions compatible with the rank-two and higher-rank controlled families?

## Required compatibility

Before implementation, review must select and freeze:

- the scalar dispersion as an explicit rank-one specialization of the controlled parent family;
- the periodic momentum domain and endpoint convention;
- the positive energy reference;
- construction, independent evaluation, and refinement meshes;
- Fourier-transform normalization and displacement convention;
- hopping supports and ordering;
- interpolation, truncation, and total scalar/spectral error definitions;
- external-isolation qualification, when an ambient parent is retained;
- binary64 tolerance and fail-closed rules;
- strict input, result, verification, analysis, and provenance records; and
- the relationship between analytic statements and sampled numerical checks.

No coefficients or tolerances are selected by this document.

## Rank-one alignment boundary

Only the no-alignment scalar channel is scientifically distinct. The following higher-rank alignment controls are inapplicable as separate represented-operator calculations:

- one global phase alignment;
- pointwise phase alignment;
- known-inverse phase control; and
- restricted internal rotation circuits.

They must be encoded as inapplicable, not emitted as duplicate numerical channels.

## Intended five-stage contract

1. calculate the scalar experiment from a frozen input;
2. independently verify experiment identities and scalar reconstruction;
3. analyze only the verified experiment output;
4. independently verify the derived analysis; and
5. render plots from verified analysis.

No stage is added until its input/output contract exists.

## Evidence boundary

A future passing run may establish only the declared finite-mesh scalar results. It will not establish higher-rank gauge behavior, continuum convergence, material applicability, or validation of Mathieu1D. Evidence promotion requires a separately authorized immutable version and retained run.
