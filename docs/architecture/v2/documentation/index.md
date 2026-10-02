# Architecture documentation standard

## Scope

This standard governs maintained architecture documentation for first-party Python
packages under `python/src/ksdft2effmass/`. It defines canonical pages for each
supported package, subpackage, module, and public class, plus optional detailed class
pages for implementation, mathematics, references, and testing.

Architecture pages describe current ownership, contracts, dependencies, implementation
mapping, and evidence status. They do not replace:

- source docstrings and supported API documentation under `doc/sphinx/api/`;
- scientific definitions under `specification/` or the research monograph;
- scientific assumptions under `docs/research/`;
- computational procedures under `docs/computational/`; or
- mutable task, checkpoint, run, or review state.

A documentation page does not make a Python symbol supported merely by naming it.
Supported routes still require an accepted contract, deliberate export, synchronized
source documentation, tests, and Sphinx documentation.

## Canonical source mirror

Architecture directories mirror the defining Python source path below
`docs/architecture/v2/ksdft2effmass/`.

```text
python/src/ksdft2effmass/__init__.py
    docs/architecture/v2/ksdft2effmass/index.md

python/src/ksdft2effmass/periodic/__init__.py
    docs/architecture/v2/ksdft2effmass/periodic/index.md

python/src/ksdft2effmass/periodic/model.py
    docs/architecture/v2/ksdft2effmass/periodic/model/index.md

class PeriodicModel in periodic/model.py
    docs/architecture/v2/ksdft2effmass/periodic/model/PeriodicModel/index.md
```

The rules are:

1. A package or subpackage initializer maps to the nearest directory `index.md`.
2. A source module maps to `<module-name>/index.md`; a new canonical module page does
   not use `<module-name>.md`.
3. A top-level class maps below its defining module as `<ClassName>/index.md`.
4. Re-exporting a class from `__init__.py` does not create a second class page. Package
   pages list supported exports and link to the defining class page.
5. Public functions and constants are documented on their defining module page unless
   a later accepted standard introduces a separate function-level hierarchy.
6. Nested implementation classes are documented under their top-level owner or module;
   they do not create parallel public hierarchy unless they become deliberate public
   contracts.
7. Path components that mirror Python symbols preserve exact spelling and case.
8. Topic, migration, decision-support, and historical pages may remain beside package
   indexes, but they do not count as canonical package, module, or class pages.

Existing topic pages and legacy module-shaped `.md` files are migration debt, not a
precedent. Untouched legacy documentation need not move. A materially changed public
contract adopts the canonical path for the smallest affected package, module, or class.
A behavior-preserving source rename updates mappings made false by the rename without
forcing unrelated documentation migration.

## Class detail hierarchy

Every canonical class page may own this exact optional detail hierarchy:

```text
<ClassName>/index.md
<ClassName>/implementation/index.md
<ClassName>/implementation/mathematics/index.md
<ClassName>/implementation/references/index.md
<ClassName>/implementation/testing/index.md
```

The class index remains the canonical contract and navigation page. Detail pages are
created only when their content is nontrivial:

- `implementation/index.md` for algorithms, data flow, representation choices, or
  external boundaries that would overwhelm the class contract;
- `mathematics/index.md` for implemented equations, approximations, domains, units,
  conditioning, and numerical limitations;
- `references/index.md` for verified primary-method sources, provenance interpretation,
  or claim-to-source mapping; and
- `testing/index.md` for substantial software/numerical evidence strategy, fixtures,
  parameter domains, and known evidence gaps.

Do not create empty detail pages for symmetry. Do not place `implementation.md`,
`mathematics.md`, `references.md`, or `testing.md` beside a class index.

## Required package and subpackage page

A package or subpackage `index.md` contains:

1. **Purpose and status** — implemented and prospective responsibility stated
   separately.
2. **Public contract** — supported child packages, modules, and exported routes.
3. **Ownership boundary** — behavior owned here and behavior explicitly owned
   elsewhere.
4. **Dependency rules** — permitted and forbidden direct dependencies.
5. **Child map** — links to canonical child package and module pages.
6. **Code mapping** — the initializer and applicable supported exports.
7. **Test mapping** — package/API/dependency tests that directly establish the stated
   contract.
8. **Provenance** — original-local declaration or complete source mapping.
9. **Evidence** — bounded evidence status without promotion between evidence classes.
10. **Limitations and deviations** — absent contracts, migration debt, and intentional
    departures from this standard.

A package page does not duplicate class fields, equations, serializer schemas, or test
assertions owned below it.

## Required module page

A module `index.md` contains:

1. **Purpose and status**;
2. **Public contract inventory** for classes, functions, constants, enums, exceptions,
   and supported routes defined by the module;
3. **Represented scientific or software objects** and their state spaces when
   applicable;
4. **Invariants, units, conventions, and failure behavior**;
5. **Dependency and neighboring-owner rules**;
6. **Class navigation** linking every canonical public class page;
7. **Code mapping**;
8. **Test mapping**;
9. **Sphinx mapping** to the canonical mirrored API page;
10. **Provenance**;
11. **Evidence**; and
12. **Limitations and deviations**.

A module page owns public module-level functions and constants. It does not hide
nontrivial reusable behavior in undocumented module-level callables.

## Required class page

A class `<ClassName>/index.md` contains:

1. **Purpose and status** — DataObject, ResultObject, ActionObject, serializer,
   Workflow, enum, exception, or framework-owned role.
2. **Public contract** — constructor, public properties and methods, domain/codomain,
   and supported import route.
3. **State and identity** — field meanings, units, shapes, ordering, canonicalization,
   and stable identity.
4. **Invariants and failure behavior** — exact type/value rules and exception taxonomy.
5. **Dependencies and collaborators** — composed owners and prohibited reverse
   dependencies.
6. **Data and action flow** — concise flow or link to the implementation page.
7. **Serialization and compatibility** when applicable.
8. **Scientific and numerical boundary** — represented mathematics, assumptions,
   tolerances, limitations, and excluded claims.
9. **Code mapping** for the class and its architecture-relevant public methods.
10. **Test mapping** with class-qualified pytest nodes.
11. **Sphinx mapping** to the canonical API page.
12. **Provenance**.
13. **Evidence**.
14. **Limitations and deviations**.
15. **Detail navigation** to every existing implementation child page.

Dataclass fields are documented in source docstrings and Sphinx. The architecture class
page summarizes relationships and invariants rather than duplicating parameter prose.

## Mapping tables

### Code mapping

Use exact repository-relative paths and qualified names.

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic/model.py` | Class | `ksdft2effmass.periodic.PeriodicModel` | Nominal periodic scientific-model root |

Supported symbol kinds are `Package`, `Module`, `Class`, `Method`, `Function`,
`Constant`, `Enum`, and `Exception`. Re-export mappings identify both the defining
symbol and supported route rather than pretending the initializer defines the class.

### Test mapping

Use exact class-qualified pytest nodes, consistent with the project test standard.

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py` | `TestPeriodicModel::test_class_definition__dimension_override__is_rejected` | Software verification | Nominal dimension cannot be overridden |

A mapping states only what the named assertions establish. Test success does not imply
scientific validation, uncertainty quantification, or human acceptance.

### Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | `ksdft2effmass.periodic` | Canonical user-facing API and scientific-software narrative |

Architecture pages link to Sphinx documentation; they do not reproduce autodoc output.

## Provenance standard

Original repository-local architecture uses:

```text
Original local work under the repository license.
```

Use a complete provenance table when the page contains an externally derived method,
research claim, equation, quotation, copied/adapted content, or extracted repository
lineage.

| Attribution ID | Claim or equation | Source | Version | Pinpoint locator | License | Role | Deviation |
|---|---|---|---|---|---|---|---|
| `ATTR-...` | `CLAIM-...` or `EQ-...` | DOI, ISBN, specification, publication, or repository | Exact edition, version, or commit | Page, section, equation, source span, or symbol | Verified license | Quoted, adapted, derived, or lineage | Exact difference |

Do not cite an architecture plan or historical agent report as scientific authority.
Repository-derived contracts link to their owning specification, protocol, manuscript
section, retained record, or exact source commit.

## Standard provenance

This project-specific standard adapts the ProjectKoios architecture-documentation
convention. It does not adopt that convention's validator, manifest, reserved system
pages, or whole-tree path restrictions. The local deviations preserve this
repository's versioned architecture and topic records, class-qualified pytest nodes,
five-way evidence separation, and existing Sphinx ownership.

| Attribution ID | Claim or equation | Source | Version | Pinpoint locator | License | Role | Deviation |
|---|---|---|---|---|---|---|---|
| `ATTR-ARCH-DOC-001` | Canonical package, module, class, and detail-page hierarchy; mapping, provenance, evidence, and adoption concepts | `https://github.com/eragasa/projectkoios` | `a756e0d2d755d4fe77345a2122bbfba7fdf34a2a` | `docs/architecture/README.md`, sections “Documentation Paths”, “Adoption Triggers”, “Provenance”, “Evidence”, and “Detailed Class Documentation” | Apache-2.0 | Adapted | Retains Architecture v2 topic pages; uses class-qualified pytest nodes and project evidence classes; does not add the external validator or dependency manifest |

## Mathematics standard

An implemented equation receives a stable lowercase HTML anchor and uppercase equation
identifier:

```text
<a id="eq-owner-001"></a>

$$
... \tag{EQ-OWNER-001}
$$
```

Every equation page defines:

- all symbols, units, domains, shapes, and ordering;
- assumptions and limiting conditions;
- the exact source class or method implementing the equation;
- direct tests and comparator, norm, and tolerance;
- numerical method, conditioning, and failure behavior;
- validity domain and excluded claims; and
- provenance or an explicit repository-derived basis.

Equations copied from the monograph are linked to the authoritative chapter or
appendix. Architecture documentation explains software representation and does not
create a competing mathematical definition.

## Evidence standard

Every canonical page has an evidence table. Include all evidence classes materially
implicated by the claims; a mathematics page always lists all five.

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported, Not evaluated, or Not applicable | Exact bounded result or reason | Test or artifact | Exact assertion or rule | Runtime/backend | Inputs covered | Not applicable |
| Numerical verification | Supported, Not evaluated, or Not applicable | Exact bounded result or reason | Oracle/artifact | Norm and tolerance | Runtime/backend | Numerical domain | Not applicable |
| Scientific validation | Supported, Not evaluated, or Not applicable | Exact bounded result or reason | Independent reference | Metric and tolerance | Scientific setup | Intended-use domain | Not applicable |
| Uncertainty quantification | Supported, Not evaluated, or Not applicable | Exact bounded result or reason | Dataset/model | Propagation rule | Scientific setup | Uncertainty domain | Not applicable |
| Human acceptance | Supported, Not evaluated, or Not applicable | Exact decision or reason | Decision record | Not applicable | Not applicable | Accepted boundary | Named human authority |

Use `Supported` only when the exact mapped evidence exists. Never use a successful build,
unit test, or reviewer statement to fill a scientific-validation, UQ, or human-
acceptance row.

## Detail-page requirements

### Implementation page

The implementation page documents algorithm and data flow, representation choices,
complexity or resource behavior where material, external boundaries, and direct code
and test mappings. It links to the class page's provenance and evidence rather than
copying them.

### Mathematics page

The mathematics page documents the implemented mathematical model, equations, symbols,
units, assumptions, code/test/attribution mappings, all five evidence classes, and
limitations. It links to the class page's provenance.

### References page

The references page maps exact claim/equation identifiers to verified primary sources
and the class provenance table. It records interpretive notes and deviations but does
not become a second bibliography.

### Testing page

The testing page documents evidence strategy, direct class-qualified pytest nodes,
fixtures/resources, parameter domains, oracles, norms, tolerances, environments,
coverage, and limitations. It links to the class page's evidence and provenance.

## Adoption triggers

| Change | Required documentation action |
|---|---|
| New supported package or subpackage | Add its canonical `index.md` and parent navigation. |
| New supported module | Add the module directory and `index.md`, Sphinx mapping, and parent navigation. |
| New supported public class | Add `<module>/<ClassName>/index.md`, applicable detail pages, source docstrings, Sphinx page, and direct test mapping. |
| Material contract, invariant, numerical, serialization, dependency, or evidence change | Update all affected canonical pages in the same change. |
| Behavior-preserving rename or move | Update mappings and paths made false; do not rewrite unrelated content. |
| Untouched legacy source | No forced migration. |
| Touched legacy public contract | Add or migrate the smallest canonical page needed for the changed contract. |
| Proposed class without implementation | Document it only when architecture needs the target; label it prospective and provide no false code/test mapping. |

## Synchronization and completion gate

For an implemented supported class, completion requires agreement among:

- source behavior and NumPy-style docstrings;
- package and subpackage exports;
- architecture package, module, and class pages;
- canonical Sphinx API and applicable concept pages;
- tests and maintained resources;
- serializers, schemas, and fixtures when applicable; and
- scientific specifications, computational procedures, or publication definitions when
  they own the represented meaning.

Validate changed documentation with local-link checks, `git diff --check`, and the
Sphinx warnings-as-errors build. Run applicable source/test checks when documentation
changes accompany implementation. Generated Sphinx output is never retained.

No deterministic validator currently proves semantic completeness of these pages.
Review must verify prose, mappings, evidence classification, provenance, and scientific
status against authoritative source.
