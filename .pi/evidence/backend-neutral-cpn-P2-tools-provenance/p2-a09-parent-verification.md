# P2-A09 parent verification

Status: **PASS — P2-A09 audited_and_cleared; P2-A10 next and not started**

Starting revision: `9ff22cf882cc64e9930cfd572a309d115da4d77e`, with
`HEAD == origin/dev` and a clean working tree after fetching `origin/dev`. P2-A08 was
`audited_and_cleared`, P2-A09 was pending and inactive, `active_item` was null, and
P2-A09 was next. Only P2-A09 was activated.

The artifact-owned software-verification module now has one module-local literal tuple
`VALID_FIXTURE_CASES` containing 17 `pytest.param` entries and one literal tuple
`INVALID_FIXTURE_CASES` containing 27 entries. The valid inventory is reused by
`SV-PROV-140`, `SV-PROV-067`, `SV-PROV-135`, and `SV-PROV-136`; the invalid inventory
is reused by `SV-PROV-141` and `SV-PROV-068`. Every entry has a stable explicit semantic
ID. The newly accepted static validator reports seven parameterized functions and 133
static parameter cases without executing parameter expressions.

Visible ID-free helpers extract declared paths directly from those inventories and
require uniqueness plus exact bidirectional equality with the discovered directory
families. The 17 valid and 27 invalid declared paths equal their respective discovered
families. Controlled omissions from both families, one nonexistent valid declaration,
and one duplicate valid declaration all fail through the same exact mechanism.

`SV-PROV-135` preserves its ID and now maps every valid fixture to the exact public class
carried by its named case using `type(record) is expected_type`; no private serializer
mapping is inspected. `SV-PROV-067`, `SV-PROV-136`, `SV-PROV-068`, and `SV-PROV-103`
retain separate schema, canonical-text, strict-runtime-rejection, and relational-invalidity
layers. `legacy-retryable-field` is present in the invalid named inventory, the
`SV-PROV-142` required-stem set, and the `SV-PROV-079` rejection family.

All 135 historical collected nodes map one-to-one. The only three new nodes are the two
new exact-family owners, `SV-PROV-396` and `SV-PROV-397`, and the new
`SV-PROV-079[legacy_retryable_field]` parameter node. Focused collection found 138 cases
and focused pytest passed all 138.

The first complete-family invocation used the plain project virtual environment, whose
interpreter intentionally lacks pip, so only the two previously established wheel cases
reported setup errors while 146 other cases passed. The required controlled offline
provisioned route was then used:

```text
cd python && uv run --offline --with pip --with 'setuptools>=77' --with wheel \
  pytest -q tests/software_verification/ksdft2effmass/integration/provenance
```

That authoritative family regression passed all 148 cases.

Structural validation, Ruff, focused mypy, evidence-ID uniqueness, one-to-one migration,
P2 ownership/completion, checkpoints, selected local harness route, protected nonmutation,
and `git diff --check` pass. The sole targeted semantic review resumed after ownership
preflight and returned PASS with no material findings; no correction pass or repeated
review was needed.

Production provenance source, schema, fixtures, package metadata, dependencies,
lockfiles, P2-A10/P2-A11 artifacts, the named-inventory validator and conventions, and
the remaining inactive `TEST-EVIDENCE-CONVENTIONS-2` backlog are unchanged.

The queue retains `active_item: null`, marks P2-A09 `audited_and_cleared`, and names
P2-A10 as next without starting it. P2 remains open and unaccepted. P3, H5, protected
execution, publication, and release remain inactive.
