# Read-only forward-validation findings

## Supplied scope and classification

The supplied paths were exactly seven current provenance record class modules—`ArtifactIdentity`, `ArtifactLocation`, `ArtifactReference`, `ArtifactSpecification`, `LineageRelation`, `ProvenanceRecord`, and `RunManifest`—plus `test__HermiticityAnalyzer__analytical_residuals.py`. No raw test was modified.

The provenance modules exercise public construction, fields, invariants, error taxonomy, immutability, and exact represented value semantics: **software verification**. The Hermiticity family checks stated residual mathematics against closed-form synthetic cases: **numerical verification**. Neither class establishes scientific validation or UQ.

## Machine structural result

The supplied-path validator returned diagnostic `FAIL` with 88 findings over 8 class-owned modules, 50 test functions, 4 helper functions, 12 parameterized functions, 52 explicitly statically collected parameter cases, and 50 unique evidence owners. Structured evidence-class counts are 7 software-verification modules, 1 numerical-verification module, 0 scientific-validation modules, and 0 UQ modules; artifact-owned count is 0.

| Structural code | Count | Interpretation |
|---|---:|---|
| `TE.HIDDEN_LOOP` | 14 | Meaningful field/value partitions are hidden inside function loops rather than collected cases. |
| `TE.PARAMETER_ID` | 52 | Each statically visible legacy parameter case omits its own explicit semantic ID. |
| `TE.TEST_NAME` | 5 | Legacy function names do not use the maintained surface/facet/behavior grammar. |
| `TE.EVIDENCE_ID` | 5 | Legacy test ID field/range representation is not the strict one-ID form. |
| `TE.DUPLICATE_ID` | 5 | Strict occurrence inventory sees repeated IDs in legacy range/support prose. |
| `TE.HELPER_ID` | 3 | Three helpers do not use the maintained explicit no-identifier declaration; referenced supported IDs are not treated as owned IDs. |
| `TE.HELPER_PRIVATE` | 1 | `test__RunManifest.py` defines private `_manifest`. |
| `TE.SUT_ASSIGNMENT` | 1 | The numerical facet module lacks strict `SUT = HermiticityAnalyzer` agreement. |
| `TE.MODULE_OPENING` | 1 | The numerical class-owned opening names analytical cases rather than exactly ``HermiticityAnalyzer`` as supplied by ownership. |
| `TE.MODULE_DOC` | 1 | The older numerical family does not yet use the maintained three module headings. |

**Heading correction:** none of the seven provenance modules received `TE.MODULE_DOC` or `TE.SUPERSEDED_HEADING`; they already use `Facet and represented meaning`, `Intrinsic and cross-object scope`, and `VVUQ and scientific exclusions`. The sole module-heading finding belongs to the numerical family. These are diagnostic legacy findings, not a gate or edit authorization.

## Independent semantic findings

These findings are deliberately separate from machine output because the structural validator cannot establish surface correctness or cohesion.

| Semantic category | Finding | Required disposition |
|---|---|---|
| Equality mislabeled `property` | Provenance functions named `test_property__...exact_value_semantics...` exercise Python equality and sometimes frozen assignment; equality is the explicitly classified `method`/`eq` surface, not an actual public `@property` or the generic `protocol` surface. | Diagnostic naming debt. Any rename to `test_method__eq__...` requires separately authorized migration and a complete one-to-one node map while preserving IDs and meaning. |
| Mixed surfaces | Some cases combine equality with immutability, timestamp semantic types with equality, multiple public fields, multiple invalid-value classes, or branch alternatives. | Semantic review must decide cohesion. Split only where requirement, oracle, acceptance, or failure interpretation differ; do not infer edits from this report. |
| Helper semantics | `_manifest` is private, while the numerical helper names are semantic but use legacy no-ID wording. | Diagnostic helper debt; helpers own no independent evidence. |
| Hidden partitions | Loops combine boundaries, fields, or invalid values inside one collected node. | Prefer explicit meaningful `pytest.param` cases under a separately authorized migration. |

## Numerical oracle and tolerance review

The Hermiticity family documents hand-derived values, exact-zero acceptance, and a local inclusive nonzero bound `abs(actual - expected) <= 64 * eps * abs(expected)` with zero rejection. A future semantic reviewer must still confirm independently that each analytical derivation is correct, no production algorithm is copied or disguised, `eV` and binary64 representation are applicable, exact zero is justified, the nonzero bound is inclusive and scale-appropriate, and the test-local bound is not confused with production or scientific acceptance policy. Structural validation establishes none of these matters.
