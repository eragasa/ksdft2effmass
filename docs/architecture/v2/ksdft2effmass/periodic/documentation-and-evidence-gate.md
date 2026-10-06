# Periodic crosswalk documentation and evidence gate

## Purpose

This gate makes each `PERIODIC-XWALK-*` migration understandable and auditable by a
scientist who does not already know the source tree. A row is not complete merely
because a class was moved, renamed, or covered by unit tests. Its scientific meaning,
mathematical role, finite representation, provenance, limitations, and evidence status
must be visible through synchronized source and maintained documentation.

This page supplements the repository-wide
[architecture documentation standard](../../documentation/index.md). It does not
replace the physical or numerical specifications, create scientific authority, or
permit inference of missing metadata from names, array dimensions, spectra, hashes, or
historical usage.

## Reader-first explanation requirement

For every migrated public contract, the documentation must let a new scientific reader
answer these questions without reconstructing intent from implementation details:

1. **What is the object?** Is it a scientific model, mathematical retained space,
   exact retained operator, finite represented operator, effective model, campaign
   record, encoded document, or supporting numerical object?
2. **What space does it act in?** State the parent state space, retained space, finite
   basis, ordering, reciprocal domain, and relevant maps.
3. **Which conventions are fixed?** State basis, gauge, boundary sewing, geometry,
   units, energy reference, scalar dtype, shape, and ordering where applicable.
4. **How was it constructed?** Distinguish projection, spectral selection,
   disentanglement, basis transformation, interpolation, truncation, fitting, and
   downfolding.
5. **What is exact and what is approximate?** Identify finite-representation,
   discretization, interpolation, truncation, fitting, and comparison boundaries.
6. **What evidence exists?** Separate software verification, numerical verification,
   scientific validation, uncertainty quantification, and human acceptance.
7. **What is not claimed?** State missing provenance, unavailable coordinates,
   unconverged parameters, unsupported compatibility, or absent scientific validation
   explicitly.

## Required synchronized surfaces

Each implemented row must audit and update the applicable surfaces below in the same
change.

### Authoritative Markdown

- `specification/` owns physical and mathematical definitions.
- `docs/research/` owns scientific assumptions and intended-use limitations.
- `docs/computational/` owns computational procedures and provenance interpretation.
- `docs/architecture/` owns software categories, dependencies, class mappings, and the
  crosswalk disposition.
- `calculations/` owns retained inputs, compact evidence, manifests, and status reports.

Architecture prose links to these owners rather than copying or silently changing their
definitions.

### Python source documentation

Every new or materially changed public object has a NumPy-style docstring that documents
the applicable parameters, attributes, returns, failures, units, shapes, basis and gauge
conventions, parent identities, provenance, exactness, approximations, and excluded
claims.

A materially changed immutable record keeps `__post_init__` short and delegates
cohesive invariant families to documented `_check_args_<meaning>` methods. Validation
names describe the scientific or software invariant rather than generic checking.

### Inline scientific comments

Inline comments are required immediately before code whose scientific meaning is not
obvious from Python syntax. They explain, as applicable:

- how mathematical indices map to arrays or matrix blocks;
- why an order, sign, phase, gauge, seam direction, or energy zero is fixed;
- why two state spaces or representations must be aligned before comparison;
- where an exact construction ends and an approximation begins;
- why missing data must remain unavailable rather than reconstructed; and
- why provenance or identity remains attached to one component after composition.

There is no comment quota. Comments must explain meaning or rationale, not narrate
assignments. Clear typed owners and well-named methods remain preferable to repetitive
commentary.

### Sphinx documentation

- API pages document every supported import and its public contract.
- Concept pages explain the scientific-software distinctions and end-to-end data flow in
  language accessible to non-maintainers.
- Navigation exposes new pages; warnings-as-errors builds must pass.
- Architecture pages map each supported class to its code, tests, and canonical Sphinx
  page.

### Tests and retained evidence

Tests are maintained evidence and must be readable by a scientist who is not familiar
with the implementation. Each test module has a docstring stating its evidence scope
and each module groups collected tests beneath one cohesive `Test...` class whose
docstring names the contract being established. Each test method documents one named
behavior rather than relying on its Python statements to explain the claim.

Test documentation and nearby comments state, as applicable:

- the scientific or software invariant under test;
- whether values are analytic references, manufactured data, retained calculation
  evidence, literature values, or synthetic fixtures;
- the represented state space, basis, gauge, geometry, units, dtype, shape, and
  ordering needed to interpret inputs and expected values;
- the oracle or independently derived expected result;
- the comparator, norm, tolerance, and reason that tolerance is appropriate;
- the parameter and validity domain covered by the evidence;
- the failure mode established by a negative test; and
- what the test does **not** establish about convergence, physical adequacy,
  scientific validation, uncertainty, or acceptance.

Fixture and builder names expose their scientific role. Non-obvious fixture
construction, transformations, and expected values receive concise comments or helper
docstrings explaining why they are valid; comments do not narrate routine setup or
reproduce the production algorithm.

A class-owned test suite may be split when that makes the evidence easier to understand.
Use `test__ClassName__method_name.py` for one public method or
`test__ClassName__specific_behavior.py` for one cohesive invariant family, numerical
case, serialization contract, or scientific scenario. Every split module still has one
cohesive `Test...` class, documents its narrower scope, and remains mapped to the same
production owner. Maintained ownership records and architecture test mappings list all facets explicitly;
split files must not duplicate assertions merely to appear self-contained.

Route- or artifact-owned smoke and integration evidence lives beside the corresponding
package or module tests. Smoke files use
`test__smoke__<smoke_test_slug>.py`; integration files use
`test__integration__<integration_test_slug>.py`. Each file carries
`pytest.mark.smoke` or `pytest.mark.integration` at module scope and the applicable
VVUQ evidence marker. A smoke route that crosses an artifact, file, or owner boundary
carries both markers. Its documentation states the representative route, excluded work,
runtime or resource boundary, and bounded meaning of a pass.

Numerical comparisons state norms, tolerances, units, and validity domains. Retained
artifacts and checksums remain unchanged unless the owning in-development adapter and
manifest are deliberately updated together.

Passing tests establishes software or bounded numerical behavior only. It does not
establish physical adequacy, convergence, scientific validation, uncertainty
quantification, or acceptance.

## Per-row completion dossier

Before a row receives a terminal `Complete` disposition, its phase page or linked
architecture page records the following evidence:

| Field | Required content |
|---|---|
| Crosswalk identity | Exact `PERIODIC-XWALK-*` identifier and source owner |
| Scientific category | One accepted category or an explicitly named supporting role |
| Target ownership | Defining package/module/class and supported import route |
| Preserved meaning | Equations, values, ordering, bytes, identities, and provenance that remain unchanged |
| Changed meaning | Exact rename, split, move, replacement, or removal |
| Representation contract | State space, basis, gauge, geometry, units, energy reference, dtype, shape, and ordering as applicable |
| Construction route | Selection, projection, transform, truncation, fit, interpolation, or other exact action |
| Error boundaries | Separate parent-model, discretization, reduction, interpolation, derivative, and comparison limitations as applicable |
| Source documentation | NumPy-style docstrings and meaningful inline comments inspected or changed |
| Public documentation | Architecture and Sphinx API/concept paths |
| Verification | Exact software and numerical test nodes, documented evidence claims, fixture class, comparators, tolerances, and validity domain |
| Retained evidence | Artifact paths and content identities, or an explicit not-applicable statement |
| Unavailable information | Data that remain unavailable and are not inferred |
| Claim boundary | Explicit scientific-validation, uncertainty, and acceptance status |

A phase-wide statement may cover several rows only when their owner, preservation
contract, documentation surfaces, and evidence are genuinely identical. Convenience
alone is not sufficient to collapse distinct rows.

## Reconciliation procedure

The active crosswalk audit proceeds row by row:

1. compare the main table, owning phase page, current source, exports, tests, Sphinx
   pages, and retained evidence;
2. correct stale status language without changing scientific meaning;
3. mark the row `Complete`, `Pending`, or `Blocked` and state the evidence or exact
   missing authority;
4. create or repair the completion dossier;
5. implement pending work only in dependency order and without compatibility aliases;
6. run affected source, test, documentation, link, checksum, and diff gates; and
7. obtain fresh-context review before recommending a commit.

A blocked row remains active. It is not converted into technical debt when required
scientific identity, coordinates, metadata, or authority are missing.

## Completion boundary

The periodic crosswalk cannot be retired until all rows have terminal implemented
dispositions, every applicable documentation surface is synchronized, a final source
inventory finds no omitted boundary-defining type, preserved evidence has been checked,
and the complete software/documentation gate passes. Crosswalk completion still does
not establish scientific validation or authorize protected execution, publication,
release, dependency changes, or deletion.
