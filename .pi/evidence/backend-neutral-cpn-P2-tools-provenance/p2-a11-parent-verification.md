# P2-A11 parent verification

Status: **PASS — P2-A11 audited_and_cleared; queue complete; P2 open at P2-HC07**

The durable start was `ea5b41f29f77a4bcf3877e356f99c2221ba07b47`, with
`HEAD == origin/dev`, a clean tree, P2-A10 cleared, no active item, and P2-A11 next.
Only P2-A11 was activated.

The decoded schema initially contained exactly 73 identifier, 5 SHA-256, and 2 version
patterns ending in `$`. All 80 now end with `(?![\s\S])`, and no vulnerable variant
remains. Strict JSON parsing, exact Draft 2020-12 declaration, metaschema compilation,
and the exact unchanged 17-definition/17-reference inventory pass. Supported
jsonschema regex behavior accepts ordinary identifier, digest, and version
representatives and rejects each representative plus final LF. Path and timestamp
patterns were not changed.

Four new compact sorted-key invalid fixtures contain escaped value LFs and exactly one
file-terminating LF: identifier, SHA-256, requested version, and observed version. Each
parses as strict JSON, fails the complete schema with active format checking, fails
public strict runtime deserialization, and becomes schema/runtime valid when only the
value LF is removed.

Five retained fixtures now isolate their named defects. The two legacy manifest fixtures
have valid timestamps; missing-attempt-id has sorted roles; impossible-calendar-date has
one valid and one impossible timestamp; surrogate places the escaped surrogate in the
declared artifact identifier and has no unknown key. Removing or correcting only the
named feature produces a complete schema-valid and runtime-valid record. The impossible
calendar date is structurally schema-valid and runtime-invalid, as expected from layer
ownership. The surrogate also violates identifier grammar if scalar prechecking is
absent, so it does not independently establish every validation-layer ordering.

The A09 invalid named inventory is 31 while its valid inventory remains 17. All 138
historical A09 nodes remain unchanged. The four fixtures create exactly four new
`SV-PROV-141` and four new `SV-PROV-068` nodes without predecessors. A11 adds
`SV-PROV-399`--`SV-PROV-401` and ten new nodes without predecessors. A11 contains three
test functions/evidence owners, four helpers, nine static parameter cases, and ten
collected cases; A09 contains 12 owners, four helpers, 141 static parameter cases, and
146 collected cases.

Focused A11 passed 10 cases, focused A09 passed 146, their combined run passed 156, the
complete provenance integration family passed 167 through the offline provisioned wheel
route, and the complete provenance class-owned suite passed 1085. Strict/canonical
artifact checks, structural validation, Ruff, mypy, evidence-ID uniqueness, ownership,
completion, checkpoint, selected local route, protected nonmutation, and diff checks
pass.

The sole targeted read-only review `3de5bc50` passed without findings. No correction pass,
second reviewer, mutation, or protected execution occurred.

Production provenance source, all 17 valid fixtures, package metadata, dependencies,
lockfile, harness validators and skills, and P2-A00--P2-A10 accepted test semantics are
unchanged. The queue has no active or next item and all 12 items are cleared. P2 is not
closed or accepted; final human authority is pending at
`.pi/checkpoints/P2-HC07-final-acceptance.json`. P3, H5, protected execution,
publication, and release remain inactive.
