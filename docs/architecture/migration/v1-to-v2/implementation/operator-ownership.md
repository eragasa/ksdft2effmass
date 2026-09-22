# V2 represented-operator ownership decision

## Problem

**Observed fact.** Architecture v1 assigns finite represented-operator records,
schema-version-one serialization, exact compatibility, Hermiticity analysis,
represented differencing, residual metrics, and fixed-representation comparison to
`ksdft2effmass.operators`.

**Human choice.** Select the Architecture v2 owner for those responsibilities without
weakening alignment prerequisites or silently changing the accepted public API, wire
format, numerical behavior, or evidence classification.

## Observed current behavior

**Observed fact.** `OperatorRecord` stores a finite matrix together with explicit
state-space, ordered-basis, geometry, energy-reference, and provenance metadata.

**Observed fact.** Compatibility auditing is exact and precedes subtraction. It does
not align bases, gauges, geometries, units, spin conventions, or energy references.

**Observed fact.** Hermiticity, represented differencing, and residual metrics are
fixed-representation operations. Their successful execution establishes only their
declared software or numerical contract.

**Observed fact.** The research monograph repeatedly requires the sequence
metadata-complete represented operands, compatibility, guarded subtraction, and
representation-local residuals. It separately assigns alignment selection, model
fitting, continuum reduction, structured learning, and scientific interpretation to
higher methodological layers.

## Decision requirements

**Observed fact.** Any selected architecture must preserve basis, gauge,
energy-reference, unit, geometry, spin, and state-space prerequisites.

**Observed fact.** A generic represented difference must not automatically acquire
impurity-operator, approximation-error, or physical-potential meaning.

**Observed fact.** The existing public imports, schema-version-one wire, fixtures,
structured failures, and numerical definitions remain compatibility surfaces until a
separately authorized change says otherwise.

**Human choice.** Determine whether fixed-representation operations remain with their
represented-data owner, move to `analysis`, or move behind a new representation
namespace and migration facade.

## Option A

**Conceptual model**

Retain `ksdft2effmass.operators` as the cohesive owner of represented-operator
records, serialization, compatibility, Hermiticity, represented differencing,
primitive residuals, and fixed-representation comparison composition.

**Authority**

The package owns represented meaning and deterministic operations on already
identified finite representations. It owns no scientific acceptance or physical
interpretation.

**Ownership/dependency**

Higher-level `analysis` code may depend on `operators`. `operators` does not depend on
`analysis` and does not absorb alignment estimation, fitting, or scientific policy.

**Runtime/dispatch**

Callers construct or deserialize records, establish exact compatibility, and invoke
explicit ActionObjects. Results retain operand identities, units, and structured
failures without becoming scientific conclusions or Workflow history.

**Migration**

The existing package, public imports, wire contract, fixtures, and verified numerical
behavior remain in place. The records and analysis disposition Tasks plan later
bounded refinements without relocating this accepted kernel.

**Reversibility**

High. Later demonstrated scientific analyzers can be introduced above the kernel
without moving its records or wire identity.

**Failures**

Malformed-record, incompatibility, and fixed-representation numerical failures remain
domain-owned and distinct from alignment failure, model inadequacy, or scientific
rejection.

**Complexity**

Lowest migration and compatibility complexity.

**Maintenance**

The safety-critical compatibility-to-subtraction chain remains locally discoverable.
The package boundary must remain narrow to prevent general scientific analysis from
accumulating there.

**Context-window consequences**

A contributor can inspect represented records and their guarded primitive operations
within one bounded package. Scientific methods load that package only as an inward
contract.

**Future compatibility**

The kernel can support later finite nonlocal, spinor, or embedded represented
operators without claiming that all representation families share one universal data
model.

**Advantage**

It preserves the accepted public foundation and most directly enforces compatibility
before arithmetic.

**Risk**

The words “comparison” and “analysis” could invite model fitting, alignment policy, or
scientific interpretation into the package unless exclusions remain explicit.

## Option B

**Conceptual model**

Keep records, serialization, and exact compatibility in `operators`; move
Hermiticity, differencing, residuals, and comparison to `analysis`.

**Authority**

`operators` owns represented data while `analysis` owns every numerical operation.

**Ownership/dependency**

`analysis` depends on `operators`. The boundary requires an explicit compatibility
witness or equivalent guarded API so analysis cannot subtract unqualified arrays.

**Runtime/dispatch**

Callers load operator records and pass them to analysis-owned operations that retain
all prerequisite and policy identities.

**Migration**

Existing action/result imports and consumers require a public compatibility and
retirement plan while the record wire remains stable.

**Reversibility**

Moderate. The wire does not move, but public behavioral APIs would need another
compatibility transition to return.

**Failures**

Record failures remain in `operators`; numerical and policy failures move to
`analysis`. Cross-package failure correlation becomes required.

**Complexity**

Moderate, with a real package seam in the middle of one guarded operation chain.

**Maintenance**

Numerical policy is centralized, but representation-local mechanics and their operands
change under different owners.

**Context-window consequences**

Even basic compatible subtraction and residual calculation require both packages.

**Future compatibility**

It accommodates broad analysis growth but risks mixing primitive matrix mechanics
with model-class, continuum, and scientific policy.

**Advantage**

It makes the data-versus-analysis distinction explicit.

**Risk**

It weakens ownership locality around the manuscript’s central alignment-before-
subtraction safeguard and creates avoidable public-API migration.

## Option C

**Conceptual model**

Introduce `ksdft2effmass.representations.operators` for records, serialization, and
compatibility; place numerical behavior in `analysis`; retain
`ksdft2effmass.operators` temporarily as a migration facade.

**Authority**

A new representation namespace becomes the canonical data owner while the facade
owns compatibility only.

**Ownership/dependency**

`analysis` depends on the new owner, and the legacy facade forwards to it. Domain
packages retain their physical meaning through explicit adapters.

**Runtime/dispatch**

New callers use two canonical packages while existing callers pass through the
facade.

**Migration**

This option requires a new package, import redirection, type-identity protection,
documentation changes, a deprecation policy, and a facade-retirement gate.

**Reversibility**

Moderate to low while three surfaces coexist.

**Failures**

In addition to record and numerical failures, the facade can introduce divergent
exports, duplicate-looking identities, and stale compatibility behavior.

**Complexity**

Highest.

**Maintenance**

The naming expresses the matrix-representation distinction, but no demonstrated
second representation domain requires this shared namespace.

**Context-window consequences**

Contributors must inspect the new owner, analysis, and compatibility facade during
migration.

**Future compatibility**

It may become useful if a genuine cross-domain representation aggregate is later
demonstrated, but selecting it now anticipates that evidence.

**Advantage**

It gives the strongest namespace-level distinction between abstract operators and
finite representations.

**Risk**

It creates speculative framework and migration work without directly advancing a
proof, calculation, or scientific claim.

## Three-option comparison

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Existing API and wire continuity | Best | Moderate | Weakest during migration |
| Compatibility-before-arithmetic locality | Best | Split | Split |
| Fixed primitive/scientific-policy separation | Strong with explicit exclusions | Strong but coarse | Strong but speculative |
| Migration cost | Lowest | Moderate | Highest |
| Context burden | One bounded kernel | Two packages | Three surfaces during cutover |
| Manuscript support | Stable inward foundation | Public churn without new capability | Broader abstraction than demonstrated |

## Recommendation

**Recommendation: Option A.** Retain a cohesive, narrowly bounded
`ksdft2effmass.operators` kernel. Higher-level alignment, model-class fitting,
continuum reduction, structured learning, transferability analysis, evidence-bearing
findings, and scientific interpretation remain with `analysis`, workflows, or their
applicable domain owners.

**Implementation consequence.** The records-disposition and analysis-disposition
Tasks may now plan against a stable retained operator owner. This decision alone
moves no source, changes no dependency, and activates no successor.

## Deferred questions

**Deferred question.** Exact child-Task plans for operator records, public imports,
wire compatibility, and internal module disposition.

**Deferred question.** Exact `analysis` request/result boundaries for alignment,
fitting, continuum reduction, and scientific findings.

**Deferred question.** Whether future demonstrated cross-domain representation needs
ever justify a broader namespace.

## Human decision required

The human selected **Option A** with the verbatim response
`Option A authorized` on 2026-08-20. The durable checkpoint
`.pi/checkpoints/migration.v2.operators-ownership.decision.json` records the decision
and its authorization boundary. Implementation, dependency changes, protected
execution, and automatic successor activation remain unauthorized.
