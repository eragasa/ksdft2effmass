# Periodic multiband analysis order

**Status: PROGRAM-LEVEL DEPENDENCY AND INTERPRETATION ORDER — NOT EXECUTION AUTHORITY**

This document records the analysis dependency graph for the live periodic calculation
owners indexed by [`README.md`](README.md). It does not merge calculation identities,
transfer parameters or thresholds, authorize execution, or upgrade development output to
evidence. Each calculation's local protocol remains authoritative for its operands,
units, basis, gauge, meshes, tolerances, verification, and claim boundary.

## Program-level order

The principal periodic analysis spine is:

1. **Structural and scalar controls.** Establish analytic identities, scalar Fourier
   reconstruction, withheld interpolation, and support-truncation semantics in
   `periodic1d_rank1/band_equivalence_hopping_locality/`. `mathieu1d/` remains outside this multiband
   authority; do not infer or install its local order from this document.
2. **One-dimensional rank-two controls.** Establish retained-state qualification,
   gauge/frame alignment, band equivalence, matrix-valued Fourier hopping, and distinct
   interpolation/truncation/total consequences in the two periodic-1D rank-two owners.
3. **Orthogonal multidimensional rank-two controls.** Analyze the square and
   simple-cubic families before using nonorthogonal or basis-aware cases to isolate the
   change caused by dimension rather than metric complexity.
4. **Nonorthogonal and basis-aware rank-two controls.** Analyze the hexagonal-metric and
   FCC/two-basis families, always evaluating the matched orthogonal control before the
   nonorthogonal Bravais case and the two-basis case.
5. **Continuous rank-two geometry paths.** Qualify the rhombic or Bain geometry and
   common-state map before the separate M0, M1, and M2 channels, witnesses, sampled path
   scans, and transition summaries.
6. **Cross-family rank-two comparison.** Consume only identified, family-owned,
   independently admitted operands. Never transfer a family's tolerances, shell index,
   support decision, or evidence status into another family.
7. **Higher-rank controls.** Analyze the one-dimensional non-Abelian rank/depth ladder
   before interpreting multidimensional higher-rank controls. In each dimension, the
   fixed-geometry periodic-2D or periodic-3D rank-N baseline precedes its separate
   continuous rank-N strain composition. The 2-D strain protocol is prospective; the
   3-D strain protocol selects a Bain path only partially. Neither contributes a
   numerical result.
8. **Material-facing or external-code work.** Synthetic periodic controls can inform
   method design but cannot validate silicon or another material. Material calculations
   retain separate parent, provenance, execution, and evidence authority.

The hopping-support hierarchy is a separate dependency branch. Its selected order is
isotropic 2-D, isotropic 3-D, anisotropic 2-D, then anisotropic 3-D. It must not be
interleaved with the rank ladder as if the studies had one family identity.

The program order is not a source inheritance order. Reusable rank-two operations refine
finite-rank dimensional capabilities even when rank-two studies are analyzed before
study inventories restricted to ranks greater than two. Calculation-owned admission
inventories, thresholds, and evidence identities remain exact and do not widen through
capability inheritance.

## Fixed-geometry family order

Within a fixed-geometry periodic family, analyze in this order:

1. protocol identity, units, direct lattice, basis offsets, reciprocal convention, and
   common state space;
2. parent operator, retained subspace, isolation/projectability, and energy reference;
3. prescribed gauge and known-inverse construction control;
4. frame transport, link rank, closures, and applicable plaquettes;
5. same-space band-equivalence operands and ordered spectra;
6. complete finite Fourier conversion, Hermitian pairing, Parseval, and withheld
   interpolation before support removal;
7. descriptive hopping locality without changing support;
8. irreversible complete-shell support truncation;
9. separate interpolation, truncation-only, and total operator/spectral consequences;
10. producer-independent verification and typed unresolved/inapplicable dispositions;
11. prospectively frozen refinement, with each refinement retained as a distinct
    calculation and never relabelled as convergence evidence; and
12. authenticated rendering from admitted stored data, followed only then by
    cross-family aggregation.

Alignment must precede subtraction. Descriptive locality must precede support removal.
Withheld interpolation must be measured before truncation. Separately maximized error
channels are not added.

## Continuous-path family order

Within a synthetic geometry path, analyze in this order:

1. path domain, unit-volume/area certificate, orientation, endpoints, direct/reciprocal
   convention, common-cell map, basis offsets, and common state space;
2. M0 geometry-only/frozen-gauge control;
3. M1 or M1N frozen-parent null-response control;
4. M2 prescribed-response control only after its exact operator law is selected;
5. channel-specific same-strain and cross-strain operands;
6. Fourier/locality analysis and any later complete-shell support policy;
7. qualification witnesses and separately named error channels;
8. prospectively frozen path sampling, transition detection, and between-sample claim
   boundary;
9. independent reconstruction and verification; and
10. authenticated response and scan rendering.

A channel with an unselected operator, inventory, mesh, tolerance, or independent route
blocks every dependent numerical stage. An exact zero common-coordinate response does
not imply unchanged physical bond lengths, shells, or support radii.

## Higher-rank admission order

For a prospective multidimensional rank-N family, the documentation and software order
is:

1. parent/common-state-space and dimension/rank vocabulary;
2. lattice geometry and basis-aware metric;
3. gauge group, generators, action side, depth semantics, and oracle boundary;
4. alignment inventory and numerical-rank applicability;
5. reciprocal sampling and frame-transport topology;
6. Fourier convention, locality inventory, and support ladder;
7. exact error operands and normalizations;
8. producer-independent references and typed failure outcomes;
9. numerical gates and bounded resource envelope;
10. visualization and authentication projection;
11. lifecycle and no-overwrite execution identity; and
12. separate execution authorization.

Passing software tests at an earlier stage establishes software behavior only. It does
not close a later scientific gate.

## Evidence and rendering order

For any implemented direct lifecycle, the operational order is

```text
typed calculation -> byte-owning or declared independent verification
                  -> authenticated projection -> rendering
```

A family whose stage-two action checks only integrity must say so and must not call that
check independent scientific verification. Rendering never recalculates science.
Sealing, promotion, publication use, and release remain separate human decisions after
analysis.
