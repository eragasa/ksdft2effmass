# M3 semantic self-review

Status: **PASS for the supplied M3 scope**. Structural PASS is separate and does not establish human acceptance.

## Ownership and public surfaces

- Reviewed 59 modules: 56 are class-owned and three integration artifacts are artifact-owned. The concrete `OperatorRecordComparator` remains a genuine class-owned Workflow.
- Filename, public import, `SUT`, module opening, marker, and evidence class agree. Equality, hash, and repr use method ownership; `HermiticityResult.is_hermitian` uses property ownership; exception text uses the string protocol; serializer, analyzer, differencer, residual, artifact, and Workflow operations use their actual public surfaces.
- `operator_record_fixtures.py` owns setup only, has no evidence identifiers, and documents constructed public objects, defaults, pass-through behavior, coercion exclusions, synthetic status, and limitations.

## Cohesion and invariant partitions

- Wrong semantic types, invalid accepted-type values, unknown values, malformed JSON, duplicate keys, nonstandard constants, constructor arity, represented-field absence, schema shape, runtime semantics, and fixture orchestration have distinct owners where their method/oracle/error interpretation differs.
- All hidden `for`-statement case loops were removed. Meaningful cases use explicit semantic `pytest.param` IDs; mechanical aggregate absence/dependency checks use one exact inventory assertion.
- Frozen/equality review covered declared represented fields independently in the value-semantics evidence: StateSpace (3), Basis (4), Geometry (5), EnergyReference (2), OperatorRecord (8 represented roles), HermiticityResult (3), compatibility/difference/comparison Results, and compatibility Issues. Matrix/provenance nested ownership and OperatorRecord unhashability remain separate.

## Numerical oracles and controlled faults

- The four numerical modules retain analytical diagonal/triangular/dependence, Hermiticity residual, exact norm, binary64 normal/subnormal, ULP, nonzero-exclusion, unit, shape, dtype, scale, and RuntimeWarning-as-error contracts. Production private routines are not expected-value oracles.
- Strict threshold equality is separated from clearly below/above cases. Exact zeros remain exact; nonzero tiny values retain criteria that cannot accept zero. No tolerance or expected value was changed.
- SVD/LAPACK and nonfinite arithmetic faults remain controlled public translation-boundary evidence: valid finite inputs cannot reliably induce those failures, the controlled dependency and public translation are named, and dependency correctness is not claimed.

## Schema/runtime layering

- Public schema validity and expressible fixture rejection remain artifact-owned.
- Serializer structure/type/value/canonicalization behavior remains class-owned runtime evidence.
- Golden fixture inventory and serializer interoperability remain artifact-owned. A schema pass is not claimed to establish runtime cross-field semantics, and a round trip is not claimed to establish physical correctness.

## Preservation and exclusions

- 920 historical nodes map one-to-one to successors; 39 new split nodes are separate. All historical IDs were preserved, and 36 authorized new owners close prior gaps or own new splits.
- Passing establishes only the stated software and numerical contracts for synthetic/version-1 cases. It does not establish physical correctness, basis/gauge/energy alignment, scientific validation, UQ, portability, Rust agreement, release readiness, or human acceptance.
