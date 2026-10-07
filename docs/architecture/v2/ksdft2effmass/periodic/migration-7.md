# Migration phase 7: periodic2d scientific adoption

## Status

**In implementation on the work branch.** The cosine-potential toy parent and
scalar-hopping finite-extent defect now have nominal scientific-model membership, and
the general plane-wave representation definition remains explicitly separate.
Retained-space/operator adoption and campaign decomposition remain incomplete.

## Purpose

Apply the general hierarchy and scientific-retention contracts to periodic2d while
finishing capability parity with applicable periodic1d coverage.

## Included crosswalk entries

Phase 7 primarily implements:

- `PERIODIC-XWALK-010` and `PERIODIC-XWALK-012`;
- the two-dimensional portions of `PERIODIC-XWALK-016`,
  `PERIODIC-XWALK-019`, and `PERIODIC-XWALK-028` through
  `PERIODIC-XWALK-036`; and
- campaign families `PERIODIC-XWALK-067` through `PERIODIC-XWALK-072`.

## Scientific-model progress

- [x] `PERIODIC-XWALK-010`: adopt `Periodic2DCosinePotentialToyModel` into nominal
  `Periodic2DModel` membership with a stable family identity and exact toy role while
  preserving the dimensionless period-$2\pi$ equation and separate represented
  operators.
- [x] `PERIODIC-XWALK-012`: rename the colliding concrete defect record to
  `Periodic2DScalarHoppingDefectModel`, adopt nominal `Periodic2DDefectModel`
  membership, retain its configured and pristine-parent identities, and assign the
  exact controlled-toy role without permitting a material-reference relabeling.
- [x] `PERIODIC-XWALK-016`: retain `PlaneWaveBlochHamiltonian2DModel` as the
  established numerical name for a finite representation definition, not a nominal
  scientific model; its result remains the represented operator.

These changes establish model identity and parentage only. They do not register a toy
catalog, construct retained spaces/operators, alter campaign payloads, or establish
scientific validation.

## Represented-operator progress

- [x] `PERIODIC-XWALK-033`: keep the general 2D continuum plane-wave result as
  reusable represented-space output with its complete request, explicit identities,
  PhysKit lattice geometry, matrix unit, basis order, and duality evidence.
- [x] `PERIODIC-XWALK-034`: retain the cosine-model result as a campaign adapter whose
  constructor delegates the actual matrix assembly to the general 2D plane-wave
  constructor while preserving exact campaign correlation.
- [x] `PERIODIC-XWALK-035`: the cosine finite-difference route is an adapter over the
  reusable `FiniteDifferenceBlochHamiltonian2DConstructor`; the general contract owns
  explicit state-space, Euclidean ordered-basis, energy-reference, unit, source/operator,
  and provenance metadata while preserving grid order and Bloch-seam direction.
- [x] `PERIODIC-XWALK-036`: keep the common-space object as a threshold-free comparison
  result with an explicit directional transport, signed difference, and intrinsically
  correlated norms; it is neither a represented operator nor acceptance policy. The
  implementation disposition is complete, but its numerical-evidence gate is reopened
  pending qualification of the three candidate analytic oracles.

These dispositions complete the demonstrated plane-wave adapter and common-space
comparison boundaries without claiming overall Phase 7 completion. Missing metadata
for row 035 are not inferred from the toy-model implementation.

## `PERIODIC-XWALK-036` implementation dossier and reopened evidence gate

| Field | Reconciled row-036 content |
|---|---|
| Crosswalk identity | `PERIODIC-XWALK-036`; source owner `ksdft2effmass.periodic2d.compare.common_space.Periodic2DCommonSpaceComparisonResult` |
| Scientific category | Campaign-specific finite represented-operator comparison Result; neither represented operator nor effective model |
| Target ownership | Defining `periodic2d.compare.common_space` Request/Result/Comparator with deliberate `periodic2d.compare` and `periodic2d` exports |
| Preserved meaning | Period-`2*pi` normalized sampling map, `p_outer_q_inner` columns, `x_outer_y_inner` rows, grid-to-plane-wave transport, signed `H_fd_tilde - H_pw` difference, and threshold-free Frobenius/max diagnostics |
| Changed meaning | Result construction now rejects a transported matrix that is not `T^dagger H_fd T`; no name, sign, unit, ordering, public route, or acceptance policy changed |
| Representation contract | Source space `C**(N**2)` in Euclidean coordinate-site order; target/common space `C**((2*M+1)**2)` in plane-wave order; fixed cosine parent, Bloch fiber, period-`2*pi` geometry, scalar spin, dimensionless energy and model zero; immutable complex128 matrices |
| Construction route | Exact normalized sampling, directional congruence transport, then signed subtraction; no projection, band selection, disentanglement, fitting, downfolding, or acceptance threshold |
| Error boundaries | Diagnostic disagreement may contain finite-difference and plane-wave representation effects; parent-model, retention, reduction, interpolation, convergence, UQ, and scientific errors remain separate |
| Source documentation | Complete module/class/method NumPy docstrings, short delegated Result/Request checks, basis-order and alignment comments, explicit range/resource failures |
| Public documentation | `specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`; `doc/sphinx/api/ksdft2effmass/periodic2d/common_space.rst`; `doc/sphinx/concepts/periodic2d-controlled-reduction.rst`; canonical `docs/architecture/v2/ksdft2effmass/periodic2d/compare/` pages |
| Verification | Software Request, Result, and Comparator evidence remains accepted. Numerical consumer tests exercise two-sided square-map unitarity at `M=2,N=5` and centered-difference relations with entrywise absolute tolerances `4e-15` and `6e-15`, but these results remain provisional until the separately documented DFT-orthogonality, centered-difference-dispersion, and resolved-cosine-transfer candidates receive versioned records, independent qualification tests, reviewed-revision dispositions, and ordered candidate/acceptance gates. |
| Retained evidence | Not applicable: no retained calculation artifact is created or consumed; fixtures are synthetic software evidence and provisional numerical evidence |
| Unavailable information | No material identity, continuum-limit result, external execution provenance, physical uncertainty, or scientific acceptance is supplied or inferred |
| Claim boundary | Software verification is supported. Numerical verification is not yet evaluated under the new oracle-qualification gate; scientific validation, UQ, and human acceptance are not established. |

## Retention-definition progress

- [x] `PERIODIC-XWALK-019`: retain `ContiguousBandSelection` as reusable interval data
  and compose it with `PeriodicRetentionDefinition` through
  `Periodic2DSelectedBandRetentionDefinition`. The dimensional specialization requires
  an exact 2D parent, `SELECTED_BANDS` construction kind, and equality between selected
  count and retained rank.
- [ ] Retained-subspace and retained-operator adoption remains blocked. The preserved
  isolated-band result contains energies, topology diagnostics, and hopping
  coefficients but no authenticated frame or projector coordinates. The preserved
  composite result contains represented-space metadata, energies, hopping blocks, and
  diagnostics but likewise no retained smooth/rough frame or projector bytes. Equal
  rank, spectra, or route names cannot fill that gap.
- [x] The
  [band-frame ownership decision](band-frame-ownership-decision.md) removes the generic
  projector/frame union from the target retained-space owner, assigns available frame
  content to typed frame bindings, leaves digest-only projector evidence with its
  campaign result until coordinates exist, and assigns the unit-carrying 1D and
  reduced-coordinate 2D half-open meshes to a lower-level solid-state owner before 2D
  frame implementation.
- [x] The reciprocal-mesh move is implemented in `solid_state.reciprocal_meshes`
  without old-module compatibility aliases or coordinate, unit, ordering, and
  validation changes.
- [x] The generic retained-space correction and both 1D adoption migrations are
  implemented: the isolated typed frame binding owns its authenticated frame digest,
  while composite projector-digest evidence remains only with the exact source result.
- [ ] The 2D frame contract and authenticated 2D artifact remain unimplemented.

The completed definition declares what is selected; it does not claim that an exact
retained mathematical space or operator has been reconstructed. No payload replay,
sidecar creation, or campaign-row migration is part of this slice.

## Required migration

1. Migrate `Periodic2DCosinePotentialToyModel` into nominal `Periodic2DModel`
   membership with stable identity and unchanged equation and coefficient conventions.
2. Rename the concrete scalar-hopping `Periodic2DDefectModel` to eliminate collision
   with the nominal defect base, then adopt nominal defect membership with explicit
   parent identity.
3. Connect selected-band and composite-subspace studies to phase-4 retained spaces and
   operators.
4. Preserve distinctions among plane-wave continuum construction, finite-difference
   representation, reciprocal-mesh topology, finite-cutoff sewing, finite-periodic
   hopping, and transported common-space comparison.
5. Decompose isolated, composite, topology, effective-mass, and Wannier90 outputs into
   typed results without changing preserved campaign documents.
6. Complete stress controls, gauge/alignment, hopping transforms, route reconciliation,
   serializers, verification, tests, API documentation, and concept documentation as
   required by the
   [periodic2d capability-parity gate](../periodic2d-capability-parity.md).

## PhysKit boundary

Continue to use PhysKit direct/reciprocal lattice and applicable finite-periodic
operator constructors. Do not substitute finite-periodic scalar hopping construction
for continuum plane-wave construction. Any later migration of the temporary 2D
continuum builder to PhysKit requires a separate accepted dependency contract.

## Defect gate

No new periodic2d defect campaign proceeds until parent-model, retained-space,
represented-operator, alignment, energy-reference, compatibility, and comparison
prerequisites pass. Existing defect evidence remains unchanged.

## Excluded work

Phase 7 does not define graphene material-reference physics without a specification,
access native archives, execute Wannier90 or electronic-structure software, or claim
scientific validation from parity checks.

## Completion gate

- Concrete 2D models have correct nominal membership and stable identities.
- Retained spaces/operators and represented results identify parents, bases, gauges,
  units, geometry, and energy references.
- Periodic2d parity requirements have terminal implemented or explicitly unavailable
  dispositions.
- Encoded documents, digests, provenance, and historical experiment identifiers remain
  unchanged.
- Relevant tests, verifier CLIs, typing, Ruff, formatting, Sphinx, links, and diff
  checks pass.
