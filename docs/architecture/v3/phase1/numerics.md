# Phase 1 numerical scope

Phase 1 validates finite metadata and immutable matrix storage. It does not execute frame
compression, gauge conjugation, alignment, Fourier conversion, support truncation, or
reconstruction.

The representation side composes Numerics-owned mesh geometry and stores exact finite
`complex128` matrix fields correlated with an ordered domain. Dimensions are derived from
complete owners and array shape rather than repeated as independent inputs.

The transformation side validates edge metadata and provides non-generic nominal
request, result, and request-bound transformation ABCs. Shared helpers check exact enum
kinds. Exact request/result types and helper invocation belong to every future final
concrete triple and require direct concrete tests. Kind agreement is structural software
behavior, not numerical evidence.

Detailed numerical contracts:

- [representation numerics](../src/ksdft2effmass/operators/representations/numerics.md);
- [transformation numerics](../src/ksdft2effmass/operators/transformations/numerics.md).
