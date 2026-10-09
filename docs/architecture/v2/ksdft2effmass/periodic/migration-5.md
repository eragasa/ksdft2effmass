# Migration phase 5: periodic1d scientific adoption

## Status

**Implemented on the work branch.** Existing Appendix G calculations and typed
results remain evidence. Row 023 used one separately authorized deterministic local
replay solely to retain previously omitted compact frame/projector and effective-model
artifacts; historical files remain unchanged. This status does not mean merged,
reviewed, released, or scientifically validated.

## Purpose

Migrate the best-defined one-dimensional scientific models first and connect their
existing represented evidence to the phase-4 retention contracts.

## Included crosswalk entries

Phase 5 primarily implements:

- model candidates `PERIODIC-XWALK-011` and `PERIODIC-XWALK-013` through
  `PERIODIC-XWALK-018`;
- retention and operator mappings `PERIODIC-XWALK-019` through
  `PERIODIC-XWALK-033` where one-dimensional; and
- campaign families `PERIODIC-XWALK-058` through `PERIODIC-XWALK-066`.

## Implementation progress

- [x] `PERIODIC-XWALK-011`: move `Periodic1DFiniteHoppingToyModel` and its
  intrinsic hopping-block data to canonical `periodic1d` ownership, add stable
  configured-model identity and nominal `Periodic1DModel` membership, and retain
  the ordered blocks, energy unit, absolute Hermiticity tolerance, and existing
  primitive/supercell numerical constructors without a campaign-owned model alias.
- [x] `PERIODIC-XWALK-013`: replace the scientifically overbroad Gaussian defect-model
  family with `Periodic1DGaussianOnsitePerturbationDefinition` and typed
  Request/Result/Constructor owners. The definition remains parent-free perturbation
  data; matched extraction supplies its separate parent and compatibility contracts.
  Former defect names are absent without aliases, and exact minimum-image construction
  numerics are unchanged.
- [x] `PERIODIC-XWALK-014`: keep `BlockHoppingModel1D` as reusable coefficient
  data; classify complete centered-mesh Fourier transforms as representations of
  exact retained operators; and construct separately identified truncation- and
  fit-derived effective models through distinct result types without changing
  coefficients, representatives, units, or numerical route results.
- [x] `PERIODIC-XWALK-015`: retain `ScalarHoppingModel` as dimensioned reusable
  finite-periodic representation data independent of nominal model/campaign classes.
  A scientific effective model remains unavailable because no demonstrated artifact
  supplies the complete parentage, geometry, reduction route, gauge, energy reference,
  and provenance needed for that claim; none is inferred from coefficient shape.
- [x] `PERIODIC-XWALK-017`: keep `PeriodicFourierPotential1D` as reusable
  potential data and compose it into the complete
  `Periodic1DFourierHamiltonianToyModel`, whose stable model, Bloch state-space,
  primitive reciprocal-domain, potential, positive recoil-energy scale, nominal
  one-dimensional membership, and exact toy role identify the untruncated parent
  separately from any finite matrix representation.
- [x] `PERIODIC-XWALK-018`: rename `Periodic1DBasisScramblingModel` to
  `Periodic1DBasisScramblingDefinition`, make the numerical request refer to the
  definition explicitly, and retain the site, orbital, phase, spin, map-direction,
  and unitary construction conventions without a compatibility alias.
- [x] `PERIODIC-XWALK-019`: keep `ContiguousBandSelection` as reusable numerical
  selection data and compose it into the parent-qualified
  `Periodic1DSelectedBandRetentionDefinition` under canonical `periodic1d`
  ownership. The aggregate requires a one-dimensional parent, selected-band kind,
  and exact rank/count agreement without constructing a subspace or gauge.
- [x] `PERIODIC-XWALK-020`: replace the campaign-local retained-band group with
  canonical `Periodic1DRetainedBandGroupDefinition`, compose each schema-one group
  with the explicit Fourier parent and a complete parent-qualified selected-band
  retention definition, and preserve the historical encoded JSON bytes.
- [x] `PERIODIC-XWALK-021`: keep `OrthogonalSpectralSubspace` as reusable numerical
  eigenspace data and compose it with a parent-qualified one-dimensional retained
  space through `Periodic1DOrthogonalSpectralRetainedSubspace`, requiring exact
  retained-rank and ambient-dimension agreement.
- [x] `PERIODIC-XWALK-022`: keep `ReciprocalBandFramePath1D` as gauge-dependent
  represented frame data and bind it separately to the scientific retained space
  through `Periodic1DBandFrameRetainedSubspace`, preserving rank, ambient dimension,
  mesh, frame order, sewing map, and the distinction between frame and subspace. The
  typed binding owns and reauthenticates the exact frame-content SHA-256 over canonical
  little-endian complex128 C-order frame bytes.
- [x] `PERIODIC-XWALK-023`: preserve the historical aggregate diagnostic result and
  exact source bytes; retain an authenticated deterministic replay sidecar containing
  the rank-one frame, reconstructed-projector identity, and separate complete,
  truncated, and directly fitted coefficient routes; then construct the untruncated
  Fourier parent, separately identified cutoff-11 finite plane-wave parent
  representation, finite-parent selected-band retention, retained mathematical space,
  represented frame, exact finite-parent restriction, one zone-center retained
  representation, complete hopping representation, and separately identified
  truncated and fitted effective models. The cutoff-11, dimension-23 parent
  representation retains its comparison against a separately identified cutoff-15
  finite reference over the declared momenta and first three bands. That observation
  is discretization evidence rather than a rigorous error bound for the untruncated
  parent. The adoption request accepts an explicit energy-valued absolute allowance or
  calculates separate scale- and dimension-adjusted binary64 allowances when the value
  is `None`; reciprocal-coordinate agreement owns a distinct calculated allowance.
  These remain software/numerical comparison policy rather than validation or UQ.
- [x] `PERIODIC-XWALK-024`: preserve the composite aggregate result and exact source
  bytes while constructing a distinct cutoff-15, dimension-31 finite plane-wave
  parent representation on the 128-point mesh. Each correlated rank-two group now has
  one finite-parent selected-band retained space and gauge-independent exact retained
  operator. The available smooth reciprocal matrices, complete smooth hopping family,
  and complete rough hopping family are separate represented retained operators with
  explicit ordered basis, energy reference, map, gauge, provenance, and authenticated
  array-content identities.
  Under the implemented
  [band-frame ownership decision](band-frame-ownership-decision.md), the reported
  smooth-projector digest remains a field of the exact source result and is not copied
  into the retained mathematical space. Projector bytes are unavailable, so the digest
  cannot be authenticated against projector content. The smooth-frame digest continues
  to qualify the available smooth representation basis without claiming retained frame
  bytes.
  Missing smooth or rough frame bytes, smooth projector bytes, and rough reciprocal
  matrices are not inferred or reconstructed.
- [x] `PERIODIC-XWALK-025`: leave every isolation, Wilson, gauge, range, route,
  representation-diagnostic, and artifact-identity channel with the unchanged
  `Periodic1DCompositeBandGroupResult`. The group adoption references that exact
  campaign result while separately binding the selected-band definition, retained
  space, exact retained operator, and represented forms. The adoption aggregate
  preserves the exact source-result object and therefore its reported
  `source_result.identities.smooth_projector_sha256` field; it cannot authenticate the
  digest without projector bytes and does not assign it to mathematical retained-space
  identity or a represented projector binding.
  Rank or Wilson data alone likewise do not define the retained space.
- [x] `PERIODIC-XWALK-026`: keep `ReciprocalOperatorSamples1D` as reusable numerical
  matrix data without a parent, projected, retained, or reconstructed operator role.
  Projection Actions establish input/output roles for their operation, while
  `Periodic1DRetainedOperatorReciprocalRepresentation` supplies the retained-operator,
  mesh, ordered-basis, gauge, energy-reference, map, provenance, and authenticated
  content identities when that scientific interpretation is claimed. Matrix shape is
  not used to infer the role.
- [x] `PERIODIC-XWALK-027`: keep `OperatorCompressionResult` as supporting finite
  real-matrix evidence for $Q^T H Q$ and $Q(Q^T H Q)Q^T=PHP$. Its intrinsic contract
  now correlates ambient and retained dimensions and requires both output units to
  match the input operator. The result does not decide invariance or supply scientific
  parent, retained-space, basis, gauge, energy-zero, or provenance identities. Row 023
  already uses a separately identified invariant selected-band route and is not
  retrofitted with an unrelated numerical result.
- [x] `PERIODIC-XWALK-028`: keep `OperatorRecord` as the complete general dense
  represented-operator record where its explicit state-space, ordered basis, geometry,
  energy-reference, and provenance contract applies.
- [x] `PERIODIC-XWALK-029`: keep `ScalarFiniteLatticeOperator` as the specialized
  sparse scalar finite-periodic record with explicit shape, twist fiber, gauge, basis,
  unit, energy reference, and provenance. Scientific aggregates may compose it without
  changing PhysKit's dependency direction.
- [x] `PERIODIC-XWALK-030`: the explicit-input supercell metadata and provenance
  contracts now require caller-supplied cell vectors and exact ordered labels before
  constructing the general `OperatorRecord`; historical artifacts lacking them remain
  unmigrated rather than being guessed.
- [x] `PERIODIC-XWALK-031`: canonical parent-qualified plane-wave requests retain
  stable model/operator/state-space identities and reciprocal-basis order.
- [x] `PERIODIC-XWALK-032`: canonical parent-qualified finite-difference requests
  preserve the half-open grid and directed conjugate Bloch-seam conventions.
- [x] `PERIODIC-XWALK-058`: move the complete isolated-band campaign family to
  `ksdft2effmass.periodic1d.campaign.isolated` without compatibility aliases. The
  move includes the version-one definition and serializer, exact encoded documents,
  typed retained result and serializer, calculation, correlation, independent
  verification, verified Workflow, and authenticated replay adoption. Shared wire
  infrastructure also moves to `periodic1d.campaign.result_documents` and
  `periodic1d.campaign.serialization`, preventing a canonical-to-transitional package
  dependency without assigning it isolated scientific meaning. Canonical campaign and
  leaf facades expose the same isolated class objects; former underscored and
  publication facades expose neither isolated nor moved shared-wire aliases. Exact
  `input.json` and
  `result.json` bytes and SHA-256 identities remain unchanged. The maintained
  `verify_result.py` import-only route update has catalog identity
  `376683ad8503c60477654cdb5972e5e3b3f4cc05cf2df108cd2ab7bb30ec372e`;
  this source identity change does not alter either wire. Controls, physical
  parents, finite representations, retained spaces/operators, represented forms,
  complete hopping representations, truncated/fitted effective models, campaign
  evidence, and scientific conclusions remain distinct. No calculator was invoked.
- [x] `PERIODIC-XWALK-059`: move the complete composite definition, exact documents,
  typed result hierarchy, correlation, campaign facade, independent verification,
  verified Workflow, and scientific adoption to
  `ksdft2effmass.periodic1d.campaign.composite` without compatibility aliases.
  Preserve exact input/result bytes while requiring every retained group to match the
  declared untruncated parent operator/domain and fit the separately declared finite
  representation. Scientific adoption constructs separate finite-parent-qualified
  retained spaces/operators and gauge-qualified represented forms. Unavailable
  projector bytes, frames, and rough reciprocal matrices remain unavailable.
- [x] `PERIODIC-XWALK-060`: rename and move the complete adversarial stress-study
  software family to `ksdft2effmass.periodic1d.campaign.reduction_challenge`. Canonical
  Python types and attributes use reduction-challenge terminology; former underscored,
  publication, deep-run, serializer, comparison, and `Periodic1DStress*` routes are
  removed without aliases. Exact historical `stress-input.json`, `stress-result.json`,
  version-one JSON keys, experiment identity, evidence-status text, `STRESS` wire kind,
  and wire bytes remain unchanged. Correlation validates the result-declared input
  SHA-256 before using input-owned controls. Independent numerical verification retains
  five separate finite-representation channels and does not convert expected trends
  into acceptance criteria. No calculator was invoked.
- [x] `PERIODIC-XWALK-062`: move the complete blind-alignment campaign family to
  `ksdft2effmass.periodic1d.campaign.alignment.blind` without a compatibility alias.
  Preserve exact input/result bytes and the separation among strict wire adaptation,
  authenticated baseline data, inference-visible observations, construction-only
  hidden truth, SVD polar-factor inference, post hoc evaluation, campaign orchestration,
  retained correlation, and independent reconstruction. Alignment and leaf facades
  expose only the reviewed campaign and encoded-document owners for this family; the
  broader campaign facade does not flatten the specialized family.
  Dense operations document cubic-time/quadratic-storage scaling and possible
  `MemoryError`; no arbitrary size cap or calculator execution is introduced. The
  authenticated baseline consumes the canonical matched-extraction records and
  finite-supercell operations supplied by rows 030--032 and 065; row 062 does not
  duplicate or infer missing scientific metadata. Importing the canonical family no
  longer loads `campaigns.periodic_1d`.
- [x] `PERIODIC-XWALK-063`: move the complete continuum-refinement family to
  `ksdft2effmass.periodic1d.campaign.refinement.continuum` without compatibility
  aliases. Preserve exact retained bytes, the five separated refinement axes,
  independent numerical reconstruction, and distinct discretization, domain, image,
  scale, profile, operator, spectral, and state error channels. Canonical imports load
  no transitional periodic campaign modules. Full NumPy-style source documentation,
  defining-module Sphinx, module/class architecture hierarchy, mirrored tests,
  ownership metadata, former-route removal, import independence, and the retained
  result identity are reconciled. No calculator was invoked.
- [x] `PERIODIC-XWALK-064`: move the complete finite-rank-oracle family to
  `ksdft2effmass.periodic1d.campaign.oracle.finite_rank` without compatibility
  aliases or a generic oracle strategy surface. Preserve the finite parent adaptation,
  rank-one resolvent, separate dense comparison, special controls, independent
  reconstruction, exact retained bytes, and bounded oracle validity domain. Canonical
  imports load no transitional periodic campaign modules. Full source/Sphinx/
  architecture/test evidence and the retained result identity are reconciled. No
  calculator was invoked and no general retention or material-validation claim is made.
- [x] `PERIODIC-XWALK-065`: move matched extraction as one cohesive family to
  `ksdft2effmass.periodic1d.campaign.extraction.matched`, remove the former route, and
  adapt its comparison envelope through row 030's general `OperatorRecord`. Preserve
  retained synthetic bytes and separate software/numerical consistency from material
  validation, continuum convergence, uncertainty quantification, and acceptance.
- [x] `PERIODIC-XWALK-066`: move the complete route-reconciliation family to
  `ksdft2effmass.periodic1d.campaign.reconciliation.route` without compatibility
  aliases. Preserve separate site-space and folded-fiber implementations, explicit
  coordinate maps and energy-reference shifts, stopped mismatch controls, declared
  reconciliations, independent verification, exact retained bytes, and separate
  representation/alignment/domain/truncation/route/spectral/eigenspace diagnostics.
  Canonical imports load no transitional periodic campaign modules. Full source,
  Sphinx, architecture, mirrored test, ownership, route-removal, import-independence,
  and retained-identity evidence is reconciled. No calculator was invoked.
- [x] All crosswalk rows assigned to Phase 5 have terminal implemented, keep, removed,
  or explicit unavailable dispositions.

## Required migration

1. Define a complete 1D periodic parent model rather than treating
   `PeriodicFourierPotential1D` as the whole system.
2. Migrate `Periodic1DFiniteHoppingToyModel` into nominal `Periodic1DModel`
   membership with stable identity and unchanged block semantics.
3. Treat `Periodic1DGaussianOnsitePerturbationDefinition` as perturbation data until a
   separate defect model composes it with an explicit pristine parent.
4. Connect isolated and composite band selections to parent-qualified retained spaces
   and exact retained operators.
5. Distinguish complete `BlockHoppingModel1D` representations from truncated or fitted
   effective models through their construction Results.
6. Migrate canonical new ownership from `ksdft2effmass.campaigns.periodic_1d` toward
   `ksdft2effmass.periodic1d` without preserving obsolete alpha import aliases.
7. Keep campaign definitions, execution, serializers, and verification outside the
   scientific-model hierarchy.

## Appendix G preservation

The migration preserves:

- lattice, reciprocal, energy, and dimensionless conventions;
- band and group ordering;
- frame, gauge, hopping, and Fourier conventions;
- exact encoded campaign documents and identities;
- complete versus truncated/fitted route identity;
- training and withheld sample separation; and
- the evidentiary status of every retained result.

## Excluded work

Phase 5 does not generalize 1D formulas to 2D or 3D by notation, register incomplete
models, alter historical Appendix G files, perform unapproved production or external
calculations, or promote numerical verification to scientific validation. The
separately authorized row-023 replay was bounded to the frozen local illustrative
input and retained new provenance-bound sidecar artifacts.

## Completion gate

- Every migrated concrete model has nominal 1D membership, stable identity, exact role,
  and complete documented physical/numerical conventions.
- Retained spaces and operators identify their parents and represented coordinates.
- Exact and approximate hopping objects cannot be confused by type or construction
  result.
- Campaigns consume models and scientific objects without becoming their bases.
- Existing encoded bytes and digests remain unchanged.
- Affected software and numerical tests, retained verifier CLIs, typing, formatting,
  Ruff, Sphinx, links, and diff checks pass.
