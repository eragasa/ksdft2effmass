# P1 Independent Architecture/Rust Review

**Verdict: FAIL**

The CPN execution architecture is generally well bounded and correctly excludes later-task scope, but material Python/schema/Rust contract inconsistencies prevent P1 acceptance.

## Findings

### MAJOR — Python and language-neutral schemas disagree on public value invariants

- `python/src/ksdft2effmass/workflows/cpn/tokens.py:97-107` requires a `real` `ContractValue` to contain exactly a Python `float`.
- `specification/workflow-cpn/v1/cpn-contract.schema.json:84-98` uses JSON Schema `type: number`, which also accepts integer-valued JSON numbers.
- `tokens.py:103-105` permits empty and duplicate strings in `STRING_SEQUENCE`.
- `cpn-contract.schema.json:27-32,117-130` reuses the unique, nonempty identifier-array schema for `string_sequence`, rejecting both cases.
- `execution.py:81-86` permits duplicate `FiringRequest.output_token_ids`, while `cpn-contract.schema.json:1001-1018` requires the unique `$defs/ids` representation.
- `execution.py:101-122` permits an empty `FiringResult.transition_id`, duplicate or empty consumed/read token IDs, while `cpn-contract.schema.json:1021-1058` rejects those states.

A direct probe confirmed:

- `{"kind":"real","value":1}`: schema-valid, Python-invalid.
- `{"kind":"string_sequence","value":[""]}`: schema-invalid, Python-valid.
- `{"kind":"string_sequence","value":["x","x"]}`: schema-invalid, Python-valid.

This violates the required agreement among runtime acceptance, schemas, fixed wire fields, and intended Rust mappings.

### MAJOR — Rust integer representation and overflow behavior are unspecified

- Public control integers use unbounded Python `int`: `tokens.py:189-192`, `markings.py:63-66`, `execution.py:95`.
- JSON schemas similarly impose no upper bound: `cpn-contract.schema.json:76-81,485-517,615-617,1040-1042`.
- The only Rust guidance says tuples become vectors and exceptions become exhaustive results, without selecting integer widths or overflow behavior: `specification/workflow-cpn/v1/README.md:23-27`; `docs/api/workflows-cpn.md:9-13`.
- Firing increments the revision without a portable overflow contract: `execution.py:417-419`.

A Rust implementation cannot determine whether these fields map to `u32`, `u64`, `usize`, a signed type, or arbitrary precision. Boundary validation and successor-revision overflow errors are consequently undefined.

### MODERATE — Public ResultObjects admit internally inconsistent states

- `TransitionEnablementResult` does not require each binding’s transition identity to match its own: `execution.py:42-58`.
- `FiringResult` does not require its binding transition to match `transition_id`, does not relate `previous_revision` to `marking.revision`, and does not require consumed/read identities to be unique or nonempty: `execution.py:89-122`.

A probe successfully constructed:

- `TransitionEnablementResult("declared", (TransitionBinding("other", ()),))`
- a `FiringResult` whose declared and bound transitions differed, whose previous revision was `99` while the marking revision was `7`, and whose consumed/read IDs were duplicated.

These are intrinsic ResultObject consistency rules and should not depend on callers using only `TransitionFirer`.

## Conforming architecture observed

- `CpnNetDefinition` explicitly represents $\mathcal N=(P,T,A,\Sigma,C,G,E,I)$ through places, transitions, arcs, colors, place color assignments, guards, inscriptions, and initial marking: `model.py:1-8,174-190`.
- Markings preserve complete place sets and token multiplicity rather than Boolean completion: `markings.py:15-88`.
- Guards and inscriptions form a closed declarative model without callable, source-text, `eval`, import, or I/O surfaces: `expressions.py:1-8,29-156`.
- Enablement and firing use deterministic arc, token, binding, and output ordering: `execution.py:128-238,295-438`.
- Multiple inputs, synchronization, read/consume behavior, output production, retry ancestry, iterations, authorization, correlation, provenance, and lineage references are representable.
- Outcome status, scope, identity, and terminality are explicit; terminal tokens are retained and excluded from consumption: `tokens.py:32-54,114-153`; `execution.py:178-187,317-336`.
- Validators and operational exceptions provide stable structured codes and immutable details: `validation.py:17-84`; `errors.py:12-72`.
- DataObjects and ResultObjects use frozen, slotted dataclasses with tuple-backed nested collections.
- No production module imports SNAKES or implements persistence, external execution, scientific payloads, concrete scientific workflows, or P2–P11 behavior.

## Decision required: wire-value semantics

### Exact conflict

Python and JSON Schema disagree on whether integer-valued JSON numbers constitute `real` values and whether `string_sequence` permits empty or repeated strings.

### Files inspected

- `python/src/ksdft2effmass/workflows/cpn/tokens.py:75-111`: exact Python tagged-value acceptance.
- `specification/workflow-cpn/v1/cpn-contract.schema.json:27-132`: wire representation.
- `python/src/ksdft2effmass/workflows/cpn/expressions.py:53-108`: expression usage.
- `python/src/ksdft2effmass/workflows/cpn/execution.py:449-495`: output evaluation.

### Conflicting instructions

- `AGENTS.md`: runtime acceptance, annotations, schemas, tests, and Rust mappings must agree.
- Current Python and schema contracts encode different accepted sets.

### Options

1. **Change the schema to follow the current Python contract**
   - Consequence: real-number lexical/type behavior still requires a cross-language JSON convention; generic string sequences can preserve ordered duplicates.

2. **Change Python acceptance to follow the current schema**
   - Consequence: broadens `real` construction and narrows string sequences, potentially preventing `BOUND_TOKEN_IDS` from representing repeated read-token identities.

### Recommendation

Separate ordered `string_sequence` from set-like identifier arrays. Preserve ordered duplicates for bound-token sequences. Obtain human approval for the real-number canonicalization rule before changing either public surface.

### Work status

- Safe to continue: read-only review and deterministic diagnostics.
- Blocked: P1 acceptance and public schema correction.

## Decision required: Rust integer widths

### Exact conflict

The public contract uses unbounded integers, while the intended Rust mapping does not specify concrete widths or overflow behavior.

### Files inspected

- `python/src/ksdft2effmass/workflows/cpn/tokens.py:167-171,189-192`
- `python/src/ksdft2effmass/workflows/cpn/markings.py:52-66`
- `python/src/ksdft2effmass/workflows/cpn/execution.py:417-419`
- `specification/workflow-cpn/v1/README.md:23-27`
- `docs/api/workflows-cpn.md:9-13`

### Conflicting instructions

No conflicting instruction found. The required Rust-compatible mapping is incomplete.

### Options

1. **Adopt fixed-width unsigned control integers**
   - Consequence: schemas and Python constructors need explicit maxima and firing needs a structured overflow error.

2. **Require arbitrary-precision Rust integers**
   - Consequence: introduces a dependency and changes ownership, serialization, and interoperability assumptions.

### Recommendation

Human authority should select fixed widths and overflow taxonomy before P1 acceptance.

### Work status

- Safe to continue: existing Python-only synthetic verification.
- Blocked: attested Rust-translatability and cross-language conformance.

## Commands run

- Focused pytest: **36 passed**.
- Ruff over CPN source and focused tests: **passed**.
- mypy over all eight production CPN modules: **passed**.
- Targeted Python/JSON-Schema divergence probe: **confirmed three mismatches**.
- Public ResultObject consistency probe: **confirmed incoherent states are constructible**.
- `git diff --check` over reviewed P1 source/specification/docs: **passed**.
- Staged-diff check: **no staged files**.
- SNAKES/later-scope source scan: no prohibited imports or implementation found.

## Residual risks

- No Rust implementation or cross-language fixture test exists.
- No authoritative persistence or SNAKES-adapter verification was performed, appropriately deferred.
- Passing tests establish software verification only, not scientific validation or UQ.
- The working tree contains extensive pre-existing modifications and untracked files; this review made no changes.