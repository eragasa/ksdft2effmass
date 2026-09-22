# Bounded literature-review protocol

## Review question

Which established primary results and computational methods overlap the
one-dimensional synthetic impurity program, and what contribution remains
defensible after separating their operator classes, state spaces, scaling
limits, spectral regimes, and finite-volume assumptions?

The review covers six concept families:

1. finite-rank impurity resolvents and bound-state conditions;
2. weak binding and defect localization near periodic band edges;
3. discrete-to-continuum and finite-periodic-volume limits;
4. semiconductor multivalley effective-mass and central-cell models;
5. Wannier or localized-basis defect Hamiltonians, potential alignment, and
   electron--defect matrix elements; and
6. matching or stitching independently generated localized representations.

## Search interfaces and dates

Searches were run on 2026-09-17 and 2026-09-18 through:

- Google Search, including links surfaced from Google Scholar records;
- arXiv abstract, HTML, and PDF records;
- publisher landing pages and full-text pages where lawfully available;
- DOI landing pages; and
- Crossref metadata queries where available.

Crossref returned HTTP 429 for some requests, and Google returned an
"unusual traffic" interstitial for some late exact-phrase searches. Those
failures were retained as access limitations rather than silently treated as
negative search results.

## Query families

The search used combinations and exact-phrase variants of the following query
families:

| Family | Representative terms |
|---|---|
| Finite-rank impurity theory | `Koster Slater impurity Green function`, `finite rank perturbation bound state resolvent`, `rank one impurity secular equation` |
| Weak binding | `weakly coupled Schrödinger operator one two dimensions`, `arbitrarily weak defect periodic band gap localization` |
| Band-edge homogenization | `defect modes homogenization periodic Schrödinger operator`, `band edge effective mass localized defect` |
| Discrete continuum | `norm resolvent discrete Schrödinger continuum limit lattice spacing`, `square lattice continuum limit spectral projection` |
| Finite periodic volume | `periodic volume bound state energy shift`, `supercell image bound state exponential correction` |
| Semiconductor donors | `Kohn Luttinger donor silicon effective mass`, `multivalley effective mass central cell silicon donor` |
| Wannier defect operators | `Wannier impurity Hamiltonian difference`, `electron defect interaction Wannier interpolation`, `disordered system Wannier Hamiltonian` |
| Alignment and stitching | `matching Wannier functions phase spin orientation`, `stitching independently generated Wannier tight binding`, `Procrustes clean defect Wannier Hamiltonian` |
| Energy reference and finite size | `potential alignment Wannier defect supercell pristine`, `system size convergence silicon vacancy MLWF` |
| Diagnostic distinctiveness | `blind alignment Wannier Hamiltonian defect`, `independent route impurity Hamiltonian extraction Wannier`, `operator residual bound state error impurity model` |

Backward and forward citation chaining was used from the sources that most
directly matched each concept family. Reviews were used to orient the search,
but methodological claims in the final positioning were assigned to primary
papers.

## Inclusion and exclusion rules

A source was included when it was a primary paper or preprint and did at least
one of the following:

- defined a directly relevant impurity or defect operator;
- proved a directly relevant localization, homogenization, continuum, or
  finite-volume statement;
- implemented a localized-basis clean/defect subtraction, interpolation,
  embedding, or alignment method; or
- defined a semiconductor effective-mass or central-cell boundary directly
  relevant to the proposed material program.

A source was excluded from the claim matrix when it was only a secondary
review, did not identify the operator or limit behind its conclusion, or was
relevant only to a different use without providing a transferable method.
Excluded sources could still be used to discover primary references.

Recent preprints are included only with explicit preprint status. Search-result
snippets and metadata are not used to support detailed technical claims. An
abstract-only source can support only the content actually stated in the
abstract or publisher metadata.

## Access and claim levels

Each claim is assigned one access level:

- **full text**: the relevant passage, equations, or method was inspected in a
  lawful PDF, publisher HTML, or browser-rendered document;
- **abstract only**: only a verified abstract and metadata were available;
- **metadata only**: identity fields were verified but no technical claim was
  drawn; or
- **inaccessible**: an attempted source could not be lawfully inspected and is
  not used for a substantive claim.

Downloaded PDFs and extracted text in `/tmp/ksdft-lit` were transient review
inputs. Their SHA-256 identities are recorded in `source-register.md`; the files
are not repository artifacts. A file named `kohn-luttinger.pdf` was identified
as HTML rather than PDF and was not treated as a retained full-text file.

## Claim extraction

For each cited methodological precedent, the review records:

- operator class;
- spatial dimension;
- small or refinement parameter;
- state-space identification;
- spectral regime;
- defect assumptions;
- finite-volume assumptions;
- supported conclusion; and
- mismatch with the represented benchmark.

A source supports only the matrix row assigned to it. Similar terminology does
not transfer hypotheses or conclusions between rows. In particular, numerical
mesh refinement, represented lattice-scale refinement, weak slowly varying
band-edge scaling, finite-volume enlargement, and defect-profile changes are
not merged into one continuum claim.

## Stopping rule and coverage statement

The search stopped after:

1. every concept family had at least one checked primary source;
2. each manuscript positioning claim had a source and access classification;
3. backward/forward chaining and a second round of exact-phrase searches added
   no source that displaced the operator-class or limit distinctions in the
   matrix; and
4. one late-discovered 2026 preprint using assignment plus unitary Procrustes
   alignment for clean/defect Wannier models was added and the contribution
   statement was narrowed accordingly.

This is an exhaustive-enough bounded search only relative to the declared
concepts, query families, interfaces, dates, and stopping rule. It is not a
systematic-review claim, a proof that no other paper exists, or evidence of
priority.

## Candidate reusable workflow fields

A future workflow could require the following typed fields per source:
`source_id`, `publication_status`, `primary_identity`, `access_level`,
`accessed_at`, `content_identity`, `metadata_routes`, `operator_class`,
`dimension`, `scaling_parameter`, `state_space_map`, `spectral_regime`,
`defect_assumptions`, `finite_volume_assumptions`, `supported_claims`,
`declined_claims`, and `benchmark_mismatch`.

This record proposes fields only. It does not authorize a generic schema,
network acquisition behavior, manifest, reusable skill, or consumer migration.
