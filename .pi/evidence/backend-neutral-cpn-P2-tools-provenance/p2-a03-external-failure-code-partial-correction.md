# P2-A03 ExternalFailureCode partial correction

Status: **deterministic validation passed; P2-A03 remains open**

Starting revision: `09cafc0ac0719cbcd5c3563ece02deb33a36fa2a`.

The completed human file-level audit authorized correction of only
`test__ExternalFailureCode.py`. Production `external_execution.py` remained
byte-identical at SHA-256
`432cda6da77b46a9441b7f0465b789423bba3dc77f8b9c696ff368e9c55024c9`.

The correction preserves `SV-PROV-074`, `SV-PROV-188`, `SV-PROV-189`, and
`SV-PROV-190`. New `SV-PROV-286` owns successful declared-name lookup; new
`SV-PROV-287` owns wrong-semantic-type value construction. Ten historical
collected nodes map one-to-one to closest current successors. Six newly
independent successful name-lookup cases have no historical predecessors.

The module has six evidence owners and sixteen collected cases: exact
vocabulary, six value constructions, six name lookups, and independent unknown
value, wrong-type, and unknown-name rejection. Concrete `field`,
`method__call`, and `method__getitem` surfaces and literal public-member oracles
replace the combined protocol evidence. A narrow `Any` cast is limited to enum
class subscription required by mypy and changes no runtime behavior.

Validation results:

- supplied-path structural validator: PASS; one class-owned module, six evidence
  owners, two parameterized functions, twelve static parameter cases, no
  helpers, and zero findings;
- exact collection and execution: sixteen collected, sixteen passed;
- diagnostic containing-module coverage: 15% for `external_execution.py` (225
  statements, 166 missed, 158 branches, zero partial); the branchless enum's
  vocabulary and inherited lookup/rejection behavior were directly exercised;
- Ruff format and lint: PASS;
- focused mypy over production and corrected test: PASS;
- public package import/API module: three passed;
- production hash, unrelated-module preservation, and `git diff --check`: PASS.

The prior `ExternalExecutionStatus` and `ExternalFailureStage` partial
corrections remain durable and unchanged. The three P2-A03 record modules remain
untouched and incomplete. The next human-audit target is
`test__ExternalExecutionRequest.py`. P2-A03 remains `pending_read_only_audit`;
P2-HC06 remains pending and is not superseded.
