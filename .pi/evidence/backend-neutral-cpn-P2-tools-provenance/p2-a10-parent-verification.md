# P2-A10 parent verification

Status: **PASS — P2-A10 audited_and_cleared; P2-A11 next and not started**

Starting revision: `719a4b2ee96d457542c3f106676e8d2471908952`, with
`HEAD == origin/dev` and a clean working tree after fetching `origin/dev`. P2-A09 was
`audited_and_cleared`, `active_item` was null, and P2-A10 was next. Only P2-A10 was
activated.

`SV-PROV-064` now requires the exact declared Draft 2020-12 URI, successful metaschema
compilation, exactly 17 definitions with the accepted names, and exactly 17 unique
unordered top-level references with the exact expected set. Its controlled defect keeps
17 entries while replacing one reference with a duplicate, so the common mechanism
reaches and fails the uniqueness guard independently of count.

`SV-PROV-065` compares one literal eight-key observed schema-vocabulary mapping with one
literal eight-key public-Python mapping. It includes
`ExecutionCorrelationResult.issues.items` against `CorrelationIssue` and preserves the
exact `ExternalExecutionResult.status`/`ExternalExecutionStatus.COMPLETED.value`
constant relation.

New `SV-PROV-398` separately verifies that `status` on
`ArtifactIdentityVerificationResult` and `ExecutionCorrelationResult` is absent from
public dataclass fields, schema properties, and serialized JSON while remaining an
actual public property descriptor. Valid representative records and the public
`ProvenanceJsonSerializer` are used; no private serializer map is inspected.

`SV-PROV-066` retains the representative active NFC format-checker boundary through the
visible `is_nfc_text` helper: `é/result.json` validates and the decomposed
`e\u0301/result.json` raises `jsonschema.ValidationError`. The visible schema loader reads
the exact UTF-8 schema path on every call and requires a JSON object.

All three historical nodes map one-to-one to renamed owners. The sole new node is
`SV-PROV-398`. The module has four test functions/evidence owners, three ID-free
helpers, no parameterized functions, no static parameter cases, and four collected
cases. Focused pytest passed all four; the complete provenance integration family passed
all 149 cases through the controlled offline provisioned wheel route.

The sole targeted review returned one material controlled-duplicate finding. The one
bounded correction pass preserved a 17-entry candidate and now exercises uniqueness;
post-correction focused checks passed. No second review was launched.

Structural validation, Ruff, focused mypy, evidence-ID uniqueness, migration, P2
ownership/completion, checkpoints, selected local harness route, protected nonmutation,
and `git diff --check` pass.

Production provenance source, schema, fixtures, package metadata, dependencies,
lockfiles, all P2-A09 evidence, P2-A11 artifacts, harness validator and skills, and the
inactive remainder of `TEST-EVIDENCE-CONVENTIONS-2` are unchanged.

The queue retains `active_item: null`, marks P2-A10 `audited_and_cleared`, and names
P2-A11 as next without starting it. P2 remains open and unaccepted. P3, H5, protected
execution, publication, and release remain inactive.
