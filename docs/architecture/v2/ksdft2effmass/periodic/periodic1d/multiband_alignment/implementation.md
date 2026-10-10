# M2 implementation

## Algorithm

`Periodic1DMultibandAlignmentCalculator.execute()`:

1. interpolates the exact finite-hopping parent on the training mesh;
2. diagonalizes the parent and selects the lowest rank-two group;
3. transports raw frames by polar overlap factors, including closure;
4. applies the frozen periodic gauge attack;
5. computes independent pointwise and one-global-unitary alignments;
6. projects the parent into reference, attacked, pointwise-aligned, and constrained
   frames;
7. transforms reference, attacked, and pointwise-aligned operators to hopping blocks;
8. verifies block Hermiticity;
9. truncates declared ranges and evaluates training/evaluation spectra; and
10. constructs one immutable correlated result.

## Correlation enforcement

Result construction checks exact definition type, rank, mesh extents, coordinate units,
frame/transform mesh identity, transform tolerances, external-gap lower bound,
Hermiticity ownership, range order, and common training/evaluation targets. Compatible
arrays with unrelated provenance are rejected.

## Serialization

The serializer emits
`ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1`. It records the
attack family, staggered-mesh rule, pointwise and global channels, complete transforms,
range summaries, and explicit negative scope claims. Complex matrices use ordered
`[real, imaginary]` pairs.

## Independent reconstruction

The library verifier independently rebuilds parent interpolation, eigensystems, polar
transport, gauge attacks, pointwise and global alignment, projections, Fourier blocks,
Hermiticity, and range errors. The retained standalone verifier strictly decodes the
wire document and rejects control or evidence tampering without importing producer
modules.

## Code mapping

| Stage | Source owner |
|---|---|
| Controls | `periodic1d/multiband_alignment/definition.py` |
| Producer | `periodic1d/multiband_alignment/calculate.py` |
| Results | `periodic1d/multiband_alignment/results.py` |
| Encoding | `periodic1d/multiband_alignment/serialization.py` |
| Reconstruction | `periodic1d/multiband_alignment/verify.py` |
| Retained package | `calculations/ICMSEP2026/conference/paper_1/multiband-alignment/` |

## External boundary

M2 is in-process synthetic work. It does not call Wannier90; the separately retained
Wannier90 bridge is different evidence and must not be attributed to M2.
