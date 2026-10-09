# Migration to the general periodic framework

## Status and authority

This page is the index for the eight-phase migration from historically independent
periodic source surfaces to the accepted general periodic architecture. Each phase has
one owning page. Phase pages define bounded deliverables and gates; they do not
supersede the scientific definitions in the monograph or applicable specifications.

The migration does not authorize external calculation, dependency changes, defect
execution, scientific validation, publication, release, or modification of retained
numerical payloads and scientific claims.

## Current and target surfaces

| Current surface | Current role | Target disposition |
|---|---|---|
| `ksdft2effmass.periodic` | Implemented nominal scientific-model root, scientific-retention owners, toy-catalog contract, and transitional compatibility exports | Retain the hierarchy and retention foundation; migrate concrete models into them; retire compatibility exports through reviewed source migration |
| `ksdft2effmass.campaigns.periodic_1d` | 1D scientific behavior, encoded campaign documents historically named models, defects, serializers, and Workflows | Separate models, retained scientific objects, represented operators, encoded documents, results, and execution; migrate canonical new work toward `periodic1d` |
| `ksdft2effmass.periodic2d` | Canonical 2D represented mechanics, encoded campaign documents, and executable studies | Preserve capability work while separating model, retention, representation, and campaign ownership |
| `analysis.model_systems.periodic_1d` and `analysis.model_systems.periodic2d` | Reusable represented numerical constructions | Retain or migrate by demonstrated ownership; move cross-project mathematics to PhysKit only under an accepted contract |
| `calculations/research-monograph/periodic-1d` | In-development campaign evidence, provenance, and thin adapters | Preserve numerical payloads and provenance; migrate adapters and their checksum entries with the public campaign API |
| `calculations/research-monograph/periodic-2d` | Recorded evidence and provenance | Preserve paths and bytes |

The active
[`current-to-target-class-crosswalk.md`](current-to-target-class-crosswalk.md)
classifies boundary-defining types and supplies stable identifiers for source
migration. Its [`crosswalk-reconciliation.md`](crosswalk-reconciliation.md) companion
tracks implementation and documentation status separately for all 73 rows.

## Phase map

| Phase | Owner | Status | Outcome |
|---|---|---|---|
| 1 | [`migration-1.md`](migration-1.md) | Implemented on the work branch | Scientific-retention documentation correction |
| 2 | [`migration-2.md`](migration-2.md) | Implemented on the work branch | Current-to-target class crosswalk |
| 3 | [`migration-3.md`](migration-3.md) | Implemented on the work branch | Encoded-document terminology correction |
| 4 | [`migration-4.md`](migration-4.md) | Implemented on the work branch | Scientific-retention owners |
| 5 | [`migration-5.md`](migration-5.md) | Implemented on the work branch | Periodic1d scientific adoption |
| 6 | [`migration-6.md`](migration-6.md) | Proposed beyond the class crosswalk | Explicit toy catalog and catalog-consuming campaign |
| 7 | [`migration-7.md`](migration-7.md) | Implemented on the work branch | Periodic2d scientific adoption and parity dispositions |
| 8 | [`migration-8.md`](migration-8.md) | Implemented on the work branch | Campaign architecture correction |

“Implemented on the work branch” does not mean merged, reviewed, released, or
scientifically validated.

## Global migration invariants

- Do not rewrite preserved numerical payloads, experiment identifiers, or provenance
  paths solely for source reorganization. Update checksum-catalog entries only when a
  covered in-development software adapter changes.
- Reserve unqualified scientific `retained` names for retained spaces, operators, and
  representations; qualify preservation as evidence, artifact, result, or encoded
  campaign document.
- Keep campaign execution dependent on scientific models, never the reverse.
- Do not add empty 3D implementations to create apparent symmetry.
- Do not treat graphene or silicon material-reference labels as validation.
- Do not generalize operator subtraction across unidentified or unaligned state spaces.
- Do not combine parent-model, numerical, and model-reduction errors.
- Do not introduce generic calculation, verification, serializer, tolerance, or
  acceptance methods merely because models share a dimension.
- Use forward commits; do not rewrite the existing periodic2d branch history.
- Apply the scientist-facing
  [`documentation-and-evidence-gate.md`](documentation-and-evidence-gate.md) to every
  row. Completion requires synchronized Markdown, NumPy-style source docstrings,
  meaningful inline scientific comments, documented tests, Sphinx API/concept pages,
  and explicit evidence and claim boundaries.

## Program gate matrix

| Capability | 1D | 2D | 3D |
|---|---|---|---|
| Scientific model hierarchy | Foundation implemented; concrete 1D toy parents adopted | Foundation plus cosine-potential toy parent and scalar-hopping defect adopted on the work branch | Foundation implemented; no concrete models |
| Toy-model inventory | Adopted toy parents exist; catalog registration is reserved for the separate phase-6 proposal | Cosine-potential toy parent adopted; catalog registration is reserved for the separate phase-6 proposal | No registered models |
| Retained scientific objects | Shared owners implemented; Appendix G isolated-band and composite group/operator-form adoption implemented; scalar-hopping effective-model composition remains unavailable without complete parent/reduction metadata | Shared owners and represented mechanics implemented; retained-space/operator adoption remains explicitly unavailable without authenticated frame/projector coordinates | Shared owners implemented; no concrete 3D retention records |
| Defect-model hierarchy | Nominal base implemented; the Gaussian onsite owner is correctly bounded as parent-free perturbation data rather than a defect model | Scalar-hopping finite-extent defect adopted; demonstrated campaign parity rows are decomposed | Nominal base implemented; no concrete models |
| Material-reference family | No family selected | Graphene target selected; specification absent | Bulk silicon target selected; existing evidence requires integration |
| Catalog campaign | Not implemented | Not implemented | Not implemented |
| Cross-model comparison | Existing local comparisons only | Existing local common-space comparison only | Not implemented |

“Proposed” and “not implemented” are architecture status labels, not failed scientific
results. Existing calculated evidence retains its original status.

## Overall completion boundary

The eight-phase migration is complete only when source, typing, tests, public exports,
Sphinx documentation, applicable specifications, the crosswalk, and preserved-evidence
adapters agree. Every row must also have the completion dossier required by the
[scientist-facing documentation and evidence gate](documentation-and-evidence-gate.md),
including documented test evidence. Passing that software gate does not establish
production calculation, scientific validation, uncertainty quantification,
publication, or release.

After the final source audit, the completed class crosswalk is retired through the
pointer-only process in [`archives.md`](archives.md). These phase pages remain the
versioned architecture record unless a later architecture version supersedes them.

```{toctree}
:hidden:

migration-1
migration-2
migration-3
migration-4
migration-5
migration-6
migration-7
migration-8
documentation-and-evidence-gate
crosswalk-reconciliation
```
