# Seven-paper research-program roadmap

## Status

This roadmap records publication scope and dependency boundaries. It does not assign
submission venues, authorize calculations, freeze numerical protocols, create evidence,
or assert that every prospective paper will reach publication. Each paper requires its
own reviewed protocol, authenticated evidence, and publication decision.

## Sequence

| Working paper | Citekey | Central question | Selected boundary |
|---|---|---|---|
| 1 | [`Ragasa2026a`](../../papers/Ragasa2026a/) | Can exactly band-equivalent rank-two representations have different operator residuals and hopping locality? | Controlled periodic one-dimensional synthetic models |
| 2 | [`Ragasa2026b`](../../papers/Ragasa2026b/) | How does the rank-two mechanism change with spatial dimension, lattice geometry, finite support, and synthetic strain? | Controlled one-, two-, and three-dimensional synthetic families; no material claim |
| 3 | [`Ragasa2026c`](../../papers/Ragasa2026c/) | How do retained rank and noncommuting multiband gauge structure affect alignment, sewing, and matrix-valued locality? | Arbitrary finite rank in topologically trivial synthetic 1-D, 2-D, and 3-D controls |
| 4 | [`Ragasa2026d`](../../papers/Ragasa2026d/) | Are spectral and operator reductions compatible for a qualified pristine bulk-silicon parent? | Scalar-relativistic, non-spin-polarized, non-SOC bulk Si; ten-spatial-orbital $sp^3s^*$ hierarchy |
| 5 | [`Ragasa2026e`](../../papers/Ragasa2026e/) | When is a pristine/defect impurity-operator subtraction defined on a common retained space? | Matched pristine and doped supercells, bundle-compatibility screening, energy/orbital alignment, and P:Si/B:Si specialization contracts; no production dopant result |
| 6 | [`Ragasa2026f`](../../papers/Ragasa2026f/) | When do topological or symmetry obstructions prevent a global periodic multiband alignment? | Patchwise frames, transition functions, complex/real/time-reversal-compatible obstruction diagnostics, and controlled models |
| 7 | [`Ragasa2026g`](../../papers/Ragasa2026g/) | What impurity operators and reduced descriptions follow for substitutional P and B in silicon under a common SOC program? | Separate matched pristine-Si/SOC, Si:P/SOC, and Si:B/SOC production branches; no use of the non-SOC bulk operator as the direct SOC subtraction reference |

## Dependency and non-transfer rules

Paper 4 is a non-SOC bulk baseline. Its ten-component spatial-orbital operator is not the
common-space parent for later SOC defect subtraction. Paper 7 must construct and qualify
its own fully relativistic pristine-Si SOC reference on the same supercell, spinor,
energy-reference, and Wannier conventions used by each doped branch.

Paper 5 owns the fail-closed state-space decision required before any impurity subtraction:

- equal retained rank or an explicit projection/embedding;
- compatible supercell and Brillouin-zone folding;
- qualified cross-projector principal angles and overlap singular values;
- compatible reciprocal-face sewing and global alignment;
- common orbital semantics and scalar energy reference; and
- separate treatment of additional localized defect states.

Paper 6 owns full obstruction theory and classification. Paper 5 may use a minimal
obstruction screen, but it does not make Chern, $\mathbb Z_2$, crystalline-topology, or
real-bundle claims. Paper 6 becomes a hard dependency for a Paper 7 branch only if the
required global or symmetry-compatible alignment cannot otherwise be constructively
qualified, or if a topological claim is added.

Paper 7 keeps P:Si and B:Si as separate physical branches. Shared spinor dimensions do
not by themselves establish compatible retained spaces. Electron count, magnetic state,
SOC response, pseudopotentials, projections, windows, defect-localized states, and
surviving symmetries remain branch-specific.

The complete maintained-experiment assignment is recorded in the
[experiment-to-paper allocation](../../papers/experiment-to-paper-allocation.md).

## Wannier90 evidence allocation

Historical Wannier90 records are assigned by scientific role rather than by their legacy
conference path:

| Retained calculation | Publication role |
|---|---|
| `calculations/research-monograph/periodic-1d/wannier90-*` | Paper 3 rank-two algorithm-selected precursor and future `periodic1d` child of a separate Wannier90 localization-reproducibility experiment; not part of the Paper 3 analytic D1 P0/G0 protocol |
| `calculations/research-monograph/periodic-2d/wannier90-balanced-*` | Paper 3 rank-three algorithm-selected frame/locality bridge |
| `calculations/research-monograph/periodic-2d/wannier90-study-*` | Paper 3 finite sensitivity evidence; not a convergence sequence |
| `calculations/research-monograph/periodic-2d-optimizer-basin/` | Paper 3 optimizer-reproducibility result and future `periodic2d` child of the separate reproducibility experiment |
| `calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/` | Paper 4 tutorial-scale silicon appendix only; not production silicon evidence |

The reproducibility family and the analytic higher-rank family remain distinct experiment
identities. Paper 3 may compare their bounded conclusions without pooling their error
channels or treating one protocol as execution evidence for the other.

## Current evidence boundary

Papers 1--3 contain controlled synthetic or extracted precursor work with their stated
finite scopes. Paper 4 remains pre-results for the production bulk-Si path. Papers 5--7
are prospective scopes only. The proposed SOC P:Si branch differs from the current
physical-specification v1 primary P:Si branch and requires an explicitly reviewed
specification amendment or successor before production execution.

No Quantum ESPRESSO or Wannier90 execution, retained-evidence creation, submission,
publication, release, or promotion is authorized by this roadmap.
