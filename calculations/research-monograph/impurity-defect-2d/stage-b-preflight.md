# Superseded Stage B scalar-onsite and D4 preflight

## Historical authority

The human response ``continue`` accepted this single-route design for
execution-free implementation only. Implementation-time toy behavior exposed
the incompatible twist-gauge requirements documented in
`stage-b-implementation-blocker.md`. The resolved HC04 decision adopted
`stage-b-multiroute-preflight.md`. This document remains historical negative
evidence and does not authorize calculation execution. Stage A remains
immutable; Stages C--E remain unimplemented and unauthorized.

## Proposed bounded implementation and execution envelope

| Item | Proposed bound |
|---|---|
| Environment | existing local repository Python environment |
| New dependencies | none |
| External executables | none |
| Network or remote execution | none |
| Parent | accepted isotropic scalar periodic-2D $(\lambda_x,\lambda_y,\lambda_{xy})=(0.5,0.5,0)$ record |
| Prerequisite | human-accepted Stage A result by exact SHA-256 |
| Represented space | one spinless scalar $8\times8$ supercell |
| Maximum matrix dimension | 64 |
| Known-map cases | 18 |
| Blind cases | 2 |
| Maximum blind candidates per case | 512 |
| Adverse numerical cases | 3, plus one software information-boundary check |
| Future runtime limit | 180 seconds |
| Future peak-memory limit | 2 GiB |
| Future retained-output limit | 10 MiB |

These are planning bounds, not measurements or execution authority.

## Design gates and discovered blocker

1. `stage-b-design.json` parses as closed JSON and retains exact parent,
   accepted-design, and Stage A identities.
2. The eight $D_4$ matrices, composition convention, operation order, orbit
   sites, coordinate reduction, and twist reduction are explicit.
3. The known-map attack defines whether phases are evaluated on source or target
   sites and fixes the complete operation order.
4. Defect-only covariance and full-Hamiltonian twist covariance are separate.
5. The fixed-twist adverse control has a predeclared discrimination floor and
   cannot be tuned after execution.
6. The blind route is specified as a non-identifiability test with exact 512 and
   64 candidate inventories, no favorable tie-breaking, and no extracted
   operator after the site-map stop.
7. The blind energy-shift diagnostic uses a median, not a trace mean biased by
   the onsite plant.
8. Known-map, covariance, blind-stop, adverse-control, reconstruction, and
   criterion statuses remain distinct.
9. Stage C model classes, Stage D convergence, Stage E composite structure,
   spin, materials, and production calculations are absent.
10. An adversarial review reports no unresolved `MUST_FIX` finding.
11. Subsequent toy behavior shows that the frozen generic twist, $[0,1)$
    reduction, and bare-permutation full-Hamiltonian covariance cannot all hold
    in one undeclared finite-matrix gauge. The pending checkpoint must select a
    revised convention before this gate can pass.

## Required execution-free behavioral evidence before execution authorization

A future implementation must use authored toy coefficients rather than the
accepted scientific parent and cover:

- malformed, stale, traversing, and wrong-stage authorization records;
- output overwrite refusal and canonical provenance;
- reordered or substituted nominal cases;
- every $D_4$ operation and exact orbit ordering;
- integer action before periodic wrapping;
- source-versus-target site-phase convention;
- known-map inverse composition order;
- correct generic-twist transformation;
- mutation of the fixed-twist adverse control;
- median-versus-mean shift behavior;
- exact Gamma and generic blind ambiguity sets;
- rejection of planted fields at the blind boundary;
- stop precedence and null residual after unresolved site mapping;
- mutation of retained maps, supports, amplitudes, covariance values, and
  criterion disposition; and
- independently reproduced criterion failure as verified negative evidence.

Static lint and type checks alone are insufficient.

## Stop conditions

Do not implement if the design review retains a `MUST_FIX` finding or if a
parent, Stage A, operation, orbit, twist, phase, information-boundary, or
criterion convention is unresolved. Do not execute without a later durable
human decision and a machine record bound to the final design, runner, parent,
Stage A result, repository root, output path, resource envelope, and checkpoint.

If future blind alignment returns a unique map, if the expected ambiguity count
changes, or if the fixed-twist control is nondiscriminating, retain the outcome
as a failed frozen criterion. Do not inspect the plant to repair it and do not
change the design after execution.
