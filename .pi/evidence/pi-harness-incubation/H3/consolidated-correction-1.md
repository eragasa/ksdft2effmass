# H3 consolidated post-review correction cycle

Status: correction applied; initial FAIL reviews retained byte-for-byte; final independent review pending.

This is the single consolidated correction cycle permitted after the initial
independent H3 review. It does not supersede or rewrite the initial findings.
The original reports remain at:

- `review-architecture-initial.md` — SHA-256 `671a311e7cf893b6fc39c20106fad0fa73bcd1995c80533f11b61211cc548b0c`;
- `review-evidence-vvuq-initial.md` — SHA-256 `6037677c392a2483e1c3f22bc75619aef123741f88c5f4879ba6de3ab0aa324a`;
- `review-integration-initial.md` — SHA-256 `d4fa01b8642be7a32a00efa5892b66f790137b419cff20582d3d6995641c8d1c`.

## Finding-to-correction map

| Initial finding | Corrected path(s) | Retained deterministic check |
|---|---|---|
| Architecture HIGH: JSON schemas accepted a generic manifest with a base and a project profile with only one local-manifest member. | `harness/pi/schemas/records/resource-manifest.schema.json`; `harness/pi/schemas/records/project-profile.schema.json`; `harness/pi/fixtures/semantic-invariants/cases/resource-manifest-generic-extends-nonnull.json`; `resource-manifest-local-extends-null.json`; `project-profile-local-id-without-version.json`; `project-profile-local-version-without-id.json` | `semantic-invariant.schema-boundary`, `semantic-invariant.schema-short-circuit`, and `semantic-invariant.boundary-counts` require four schema-level rejections. |
| Architecture HIGH: self-dependency, self-prerequisite, and absent activated task ID are cross-value invariants that Draft 2020-12 cannot portably express. | Schema boundary descriptions in `harness/pi/schemas/records/resource-reference.schema.json`, `task-reference.schema.json`, and `chain-view.schema.json`; negative oracle and cases under `harness/pi/fixtures/semantic-invariants/` | `semantic-invariant.cross-value-rejection` requires all three schema-accepted cases to fail at `DeserializeJsonRecord` with `PIH.WIRE.INVALID_VALUE`; `semantic-invariant.case-set` fixes the complete seven-case oracle. |
| Architecture MEDIUM: generic evidence grammar imposed a project-local filename policy. | `harness/pi/skills/document-research-python/references/test-evidence-documentation.md`; local ownership remains in `harness/local/extensions/evidence-documentation.md` | Full-tree leakage plus manifest byte-identity checks pass; generic prose now delegates module placement and filename policy to explicit project profiles/extensions. |
| Architecture LOW: the generic DiagnosticPath fixture used the current repository test root. | `harness/pi/fixtures/diagnostic-path/valid/directory-tree-scope.json`; `harness/pi/fixtures/diagnostic-path/oracle-index.json` | `diagnostic.fixture-coverage`, `diagnostic.path-oracle`, `diagnostic.exact-spelling`, and full-tree `leakage.generic-zero-local-dependencies` pass with a neutral directory spelling. |
| Evidence/VVUQ F1: retained evidence ambiguously left deterministic wire/hash checks inside a numerical-verification boundary. | `.pi/evidence/pi-harness-incubation/H3/validation-results.json`; `.pi/evidence/pi-harness-incubation/H3/h3-to-h2-handoff.json`; this correction record | The retained claim boundary now classifies every schema, fixture, wire, canonical-byte, and hash check as software verification and states numerical verification is entirely not applicable. |
| Evidence/VVUQ F2: WARN protected-gap classification text was not enforced. | `harness/pi/validation/validate_h3_resources.py` (`evidence_oracle_gate`) | `evidence.classification-and-claim` runs for both PASS and WARN; the protected WARN must equal `software_verification-only; no numerical/scientific claim`. |
| Integration Major: generic canonical fixture named the local successor and other generic fixtures contained local classification vocabulary. | `harness/pi/fixtures/canonical/canonical-json-vectors.json` and neutralized generic fixture corpus under `harness/pi/fixtures/` | `canonical.byte-identity`, `canonical.sha256`, `canonical.vector-set`, and full-tree `leakage.generic-zero-local-dependencies` pass. Future targets are neutral consumer-language labels rather than a local task ID. |
| Integration Major: the generic validator implicitly discovered `.pi`, hard-coded H3/task/chain state, and mixed project control-plane checks into portable validation. | `harness/pi/validation/validate_h3_resources.py`; project checks retained separately in `.pi/evidence/pi-harness-incubation/H3/external-control-validation.json` | Generic validator contains no `.pi` runtime-state coupling and passes 46 portable gates. Ownership, checkpoints, Git/staging, unrelated work, and dependency/lock/source nonmutation independently pass outside it. |
| Integration Major: leakage scanning omitted generic fixtures and validation source. | `harness/pi/validation/validate_h3_resources.py` (`leakage_gate`) | `leakage.generic-zero-local-dependencies` scans every file under `harness/pi/`, including fixtures and validator source, against explicit local identities, markers, prefixes, roots, task IDs, runtime-state spelling, and domain literals. |
| Evidence wording across H3 resources must remain software-verification-only. | `harness/pi/docs/evidence-grammar.md`; `.pi/evidence/pi-harness-incubation/H3/validation-results.json`; `.pi/evidence/pi-harness-incubation/H3/h3-to-h2-handoff.json` | Completion validation passes `docs.required-concepts`; retained claim boundaries explicitly state numerical verification, scientific validation, and uncertainty quantification are not applicable to H3. |

## Correction validation

Fresh corrected resource validation:

```text
RESOURCE VALIDATION PASS
gates_passed=46 defects=0
```

The corrected gate names and complete result are retained in
`validation-results.json`. Project-specific checks are retained separately in
`external-control-validation.json`; this separation is part of the correction,
not an omitted gate.

No final-review artifact, final checksum catalog, checkpoint, or human
acceptance is recorded by this correction. H2 remains inactive and requires
later H3 human acceptance plus separate explicit H2 authorization.
