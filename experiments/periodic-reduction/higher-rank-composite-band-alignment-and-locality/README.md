# Higher-rank composite-band alignment and locality

## Purpose

This publication-independent family supplies the common analytic model for the Paper 3
higher-rank study. It separates retained rank, noncommuting Givens-circuit depth,
admissible alignment family, and spatial dimension across orthogonal periodic one-, two-,
and three-dimensional controls.

The first bounded 1-D P0/G0 specialization is now a complete pre-execution protocol
candidate with reserved identity
`ksdft2effmass.campaign.periodic-reduction.periodic1d.higher-rank-composite-band-alignment-and-locality.v1`.
Its parent, exact analytic certificates, real Givens-angle law, rank/depth ladder,
A0--A3 channels, exact Procrustes orientation and application rules, fail-closed
alignment dispositions, meshes, tolerances, supports, convergence and claim-resolution
rules, complete diagnostic ledger, strict input/result/verification/provenance field
inventory, verifier method, resource gate, and evidence policy are selected. Reusable,
rank-generic diagnostic primitives are now under software verification at
`python/src/ksdft2effmass/analysis/matrix_field/diagnostics/`; the experiment calculator,
independent verifier, serializer, and retained composition remain unimplemented.
Reviewed local Optimization owner tranches now provide the required maximum-rule
Procrustes cutoff (`4c69ffa73ada6fd55576b0f9dee0350259813673`) and odd-parity
finite-periodic operations (`d38e00ceef7f0fb1c137d5c3450d210c1ae4c99f`). Both are
published on the owner branch `origin/migration/ksdft2effmass`. PhysKit commit
`7157dcedd0d220673d443c1c025e35a6fd1ffa7a` on its `origin/main` supplies the reviewed
unit-aware physical boundary around those operations. These are capability-review
references, not the KSD dependency binding, and no binding changes without explicit
authorization. The protocol
has no reviewed immutable version, retained run, or evidence package. The 2-D, 3-D, P1,
G1, and A4 branches remain prospective. Empty dimensional implementation packages are
intentionally not created.

## Current scientific boundary

The proposed parent has an isolated rank-$r$ subspace embedded in dimension $2r$, an
analytic global periodic frame, optional retained--exterior projector motion, and a
layered adjacent-pair gauge in either $SO(r)$ or $U(r)$. It supports any declared finite
$r\geq3$ and finite circuit depth, but every calculation remains bounded to a frozen
finite rank/depth ladder. The canonical protocol now states the property-by-construction
grammar explicitly: retained rank, projector, represented spectrum, periodicity under the
declared input constraints, and exterior isolation are analytic guarantees, whereas
restricted alignment residuals, hopping tails, truncation errors, refinement behavior,
and finite rank/depth trends remain measured outcomes. The Paper 1 v3 supplementary
workflow is used only as a diagnostic-completeness checklist: applicable gap, frame,
sewing, Fourier, Parseval, error-decomposition, perturbation-bound, evaluation,
refinement, serialization, and verification channels are retained, while rank-two-only
admissible-set, Nyquist, amplitude-optimization, and first-passing-range channels are
explicitly inapplicable.

The global analytic frame makes the initial family topologically trivial. Closure,
Wilson-loop, and plaquette quantities are sewing and transport diagnostics, not
three-dimensional topological claims. A topologically obstructed model requires a
separate patchwise-frame protocol. Paper 5 owns later pristine/defect common-space
admission, and Paper 6 owns full obstruction studies; neither result is implied here.
Wannier90 initialization, convergence, and optimizer-basin reproducibility likewise
belong to a separate experiment family; historical results may be discussed by Paper 3
but are not executions of this analytic protocol.

## Documents

- [`experimental-protocol.tex`](experimental-protocol.tex) is the canonical protocol
  manuscript. It defines the common family and the complete unexecuted D1 v1 candidate;
  later-dimensional numerical controls remain prospective.
- [`python/src/ksdft2effmass/analysis/matrix_field/diagnostics/`](../../../python/src/ksdft2effmass/analysis/matrix_field/diagnostics/)
  provides reusable typed structural, error-channel, perturbation-bound, decomposition,
  block-norm, tail, monotonicity, and scalar-refinement diagnostics. These primitives do
  not constitute the D1 experiment calculator or evidence.
- [`verify_d1_p0_g0_controls.py`](verify_d1_p0_g0_controls.py) reproduces the finite-grid
  D1 isolation-energy and attack-angle sanity check. Its output is replaceable
  development diagnostics, not an analytic proof or retained evidence.
- [Ragasa2026c/v1](../../../docs/publications/papers/Ragasa2026c/v1/README.md)
  is the publication-side consumer and does not own the experiment identity.
- The retained rank-two
  [`periodic1d/composite-band-alignment-and-locality`](../composite-band-alignment-and-locality/periodic1d/)
  experiment is a predecessor control, not an interchangeable implementation.

Render the protocol without placing build products in the source tree:

```console
mkdir -p /tmp/hr-cbal-protocol-build
latexmk -pdf -interaction=nonstopmode -halt-on-error \\
  -outdir=/tmp/hr-cbal-protocol-build experimental-protocol.tex
```

No calculation, retained evidence, publication, or protected execution is authorized by
these documents. Implementation and schema review must precede any execution request.
