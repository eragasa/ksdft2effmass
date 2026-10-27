# Physical Review B manuscript, version 3

This directory contains the working Physical Review B and arXiv revision that grew from
Conference Paper 1. Version 3 recenters the paper on the publication-independent
experiment *Band Equivalence versus Hopping Locality*. The historical directory path
does not define the manuscript's target venue or the experiment's identity.

## Scientific relationship to version 2

Version 2 presented a broad model-class-expressivity framework supported by scalar,
rank-two, two-dimensional, Wannier90, and tutorial-scale silicon examples. Version 3
uses the same broad scientific question but replaces the former M2/M3 centerpiece with:

- exact continuous global \(SO(2)\) alignment rather than a finite angle inventory;
- common-curvature rank-two admissible-set geometry;
- the smooth family \(U_a(q)=R(a\sin 2\pi q)\);
- the flat-parent \(J_0(2a)\) threshold law;
- the exact residual--nonlocal-hopping identity;
- a bounded flat-to-dispersive parent homotopy;
- fixed-sampled-accuracy hopping-range inflation; and
- separate cyclic-conversion, interpolation, truncation, and total-error channels.

The earlier M2 and nine-angle M3 calculations remain historical supporting records.
They do not define the active alignment or numerical controls of version 3. Version 2
is preserved unchanged as a historical manuscript draft.

## Authoritative calculation source

The publication consumes the maintained calculation at:

```text
calculations/periodic1d/rank2/
  band-equivalence-versus-hopping-locality/
```

The calculation-family identity is independent of this publication version. The
manuscript references calculation-owned figures and tabulated development analysis
directly rather than copying them into a second evidence tree. The program-wide
[allocation ledger](../../experiment-to-paper-allocation.md) also assigns the retained
single-band Fourier reduction to this paper as a separate scalar precursor.

Prospective dimensional successors have independent calculation owners under the
orthogonal and nonorthogonal rank-two families at:

```text
calculations/periodic2d/rank2/{orthogonal,nonorthogonal}/band-equivalence-locality/
calculations/periodic3d/rank2/{orthogonal,nonorthogonal}/band-equivalence-locality/
```

They own independent square, triangular/graphene-inspired, simple-cubic, and
FCC/silicon-inspired bounded development calculations. Those smoke and first-refinement
records are not versions of the 1-D experiment, are not Paper 1 v3 evidence, and do not
upgrade the manuscript's numerical evidence status.

## Evidence boundary

The analytic rank-two geometry, Bessel threshold law, and flat-parent locality identity
are mathematical results. The current dispersive homotopy and truncation figures are
development calculations on declared sample inventories. They are not a retained
production run or evidence package. Supplemental Section S7 now records the separate
retained `single-band-fourier-reduction.v1` run as a verified scalar precursor; its
retained status is not transferred to the active rank-two experiment. The range-inflation
map now reports the first passing cutoff over every integer
$R_c=0,\ldots,16$ on the sampled $(\rho,a)$ grid. The cap remains a development control,
not a frozen universal range.

The dense inventory, threshold-adjacent refinement through $N=512$, strict truncation
serialization, and independent reconstruction of every first-passing decision are
implemented for development. Before arXiv submission, the numerical headline still
requires reviewed and frozen production controls, authorized retained execution and
package verification, and a public archival record.

Five PDFs referenced by the current main manuscript and supplement were absent from
every Git ref and were found only in a separate dirty worktree. After operator
authorization, the complete producing source/data graph and predecessor figure bytes
were recovered into the calculation owner. The
[recovery audit and disposition](../../../../../calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/publication-input-recovery-audit.md)
records the exact identities, adaptations, and bounded reproduction checks. The
manuscript and supplement now read those PDFs from the calculation owner, so this
missing-input build blocker is resolved. Scratch `latexmk` builds completed for both
21-page PDFs. The main source still reports undefined `Ragasa2026b`--`d` citations and
the supplement reports two undefined Marzari citations; those pre-existing bibliography
issues remain separate submission gates. The recovered figures remain development
publication inputs, not retained evidence.

## Submission-oriented structure

The main manuscript is encapsulated in the APS `revtex4-2` class with the `prb` and
two-column `reprint` options. The separate Supplemental Material remains a standalone
one-column LaTeX article so its multipage verification tables remain readable; APS does
not require the Supplemental Material PDF to use RevTeX. This formatting choice does
not constitute submission or venue acceptance.

The working paper is divided into a focused main manuscript and separate Supplemental
Material.

The main manuscript follows:

1. Introduction;
2. Background and related work;
3. Theory;
4. Methods;
5. Results;
6. Discussion, including the controlled validation ladder;
7. Conclusions.

Diagnostics retain three explicit roles: Methods defines the workflow, Results reports
the bounded conclusions, and Discussion interprets what the checks do and do not rule
out. Detailed diagnostic plots, proofs, resolution and verification contracts, the
claim--evidence register, and execution procedures are in the supplement. Moving this
material does not change its scientific or provenance status. Supplemental
Sec.~S1.6 contains the limited attainment and transported-frame covariance result for
the declared cross-model alignment loss. It explicitly distinguishes that result from
the established MLWF spread decomposition: the former is contract-dependent operator
comparison bookkeeping, whereas the latter separates projector- and frame-dependent
parts of a Wannier localization functional.

## Version 2 technical-material disposition

Version 2 remains unchanged as the historical record. Its technical material is handled
as follows in version 3:

- **Gauge-orbit loss and frame excess:** reduced to the limited proposition in
  Supplemental Sec.~S1.6 because version 3 uses a declared global-alignment minimum.
  It is not presented as a novelty or as the MLWF spread decomposition.
- **Spectral projection versus finite support:** not migrated. It addresses projection,
  whereas version 3 isolates representation-induced range under pointwise unitary
  equivalence. The example remains valid historical background and can be developed in
  a projection-focused successor without burdening this manuscript.
- **Generic witness/separation logic and the M3 finite-alignment example:** extracted to
  Conference Paper 3 as a controlled rank-two precursor. Version 3 retains only the
  exact common-curvature geometry needed by its focused continuous-alignment experiment
  and does not absorb either historical admissible-set plot. The direct scalar example
  remains in the version-2 archive.
- **M2 finite attack/Procrustes and M3 nine-angle admissible-set calculations:**
  extracted to Conference Paper 3 as bounded rank-two precursors. The active version-3
  experiment nevertheless uses its own smooth attack, continuous global $SO(2)$
  optimization, resolution, and verification contract. **M1** remains only in the
  historical Paper 1 lineage because the maintained version-3 experiment supersedes its
  role.
- **Two-dimensional, Wannier90, and tutorial-silicon material:** not used as version-3
  evidence. Bounded 2-D precursors are extracted to Papers 2 and 3, while the tutorial
  silicon preview remains bounded to Paper 4.

No version-2 proof or calculation is silently treated as version-3 evidence.

## Files

- `manuscript.tex` — working main manuscript.
- `supplementary.tex` — working supplementary information; imports main-manuscript
  labels through `xr-hyper`.
- `references.bib` — bibliography for the working manuscript.
- `novelty-and-convention-audit.md` — bounded literature-search and v2/v3 Fourier-
  convention audit; not evidence of exhaustive priority.
- `claim-and-commitment-inventory.md` — complete editorial ledger of analytic claims,
  sampled numerical claims, method contracts, nonclaims, roadmap commitments, and
  submission blockers; not a separate scientific authority.
- `manuscript.pdf` and `supplementary.pdf` — generated local builds; not retained
  evidence.

## Build

Build the main manuscript before the supplement so external references resolve:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary.tex
```

No submission, publication, release, retained execution, or public deposit is authorized
by this working directory.
