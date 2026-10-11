# Model-adequacy ownership and data-flow schematic

## Package dependency direction

```mermaid
flowchart LR
    physkit["projectkoios.physkit\nlattice displacements + symmetry operations\nhopping + represented operators"]
    optimization["projectkoios.optimization @ ec3d290…\nParameterSpace + quadratic facade"]
    operators["operators\nrepresented records + primitive residuals"]
    periodic["periodic / periodic1d / periodic2d\nparents + model primitives"]
    bands["analysis periodic-band primitives\nexplicit sampled spectra"]
    adequacy["analysis.model_adequacy\nloss and admissible-set analysis"]
    campaigns["campaigns and retained calculations\ncontrols + provenance + orchestration"]
    publications["publications\nbounded interpretation"]

    physkit --> periodic
    physkit --> adequacy
    optimization --> adequacy
    operators --> adequacy
    periodic --> adequacy
    bands --> adequacy
    adequacy --> campaigns
    campaigns --> publications
```

The arrows show permitted outward consumption, not inheritance. Inward `operators` and
periodic model packages must not import `analysis.model_adequacy`. The adequacy layer
uses the exact-pinned optimization parameter-space contract directly; it does not create
a renamed coordinate-box wrapper. During migration, a legacy compatibility module may
re-export an outward class without becoming its implementation owner.

## Loss construction and evaluation

```mermaid
flowchart TD
    target["Declared target data"]
    candidate["Declared candidate family"]
    controls["Weights, units, normalization,\ncoordinates, and roles"]
    builder["Domain-specific loss constructor"]
    quadratic["Exact-pinned Optimization facade\nPositiveDefiniteQuadraticLoss"]
    wrapper["Domain wrapper\nchannel and coordinate meaning"]
    evaluation["Finite squared/root loss evaluation"]
    threshold["Caller-owned threshold"]
    set["Domain-specific admissible set"]

    target --> builder
    candidate --> builder
    controls --> builder
    builder --> quadratic
    quadratic --> wrapper
    wrapper --> evaluation
    evaluation --> threshold
    threshold --> set
```

The generic quadratic facade does not discover targets, fit a model, choose weights,
select an alignment, apply a threshold, or assign a disposition. It may represent either
$L_E^2$ or $L_H^2$ only after a domain constructor derives explicitly normalized
completed-square coefficients. The dependency is accepted and pinned; KSD-specific
wrappers remain prospective.

## Spectral and represented-operator channels

```mermaid
flowchart TD
    targetE["Ordered target energies"]
    candidateE["Ordered candidate energies"]
    spectral["Declared spectral samples, weights,\nrank, units, and energy scale"]
    LE["Dimensionless spectral loss L_E"]

    targetE --> spectral
    candidateE --> spectral
    spectral --> LE

    left["Reference represented operators"]
    right["Candidate represented operators"]
    compat["operators compatibility"]
    diff["operators signed differences"]
    policy["Outward declared sample/weight policy"]
    aggregation["PhysKit dimensionful aggregation\nweights + rank + units"]
    RH["Dimensional RMS residual R_H"]
    normalization["Adequacy normalization by E_0"]
    LH["Dimensionless operator loss L_H"]

    left --> compat
    right --> compat
    compat --> diff
    diff --> aggregation
    policy --> aggregation
    aggregation --> RH
    RH --> normalization
    normalization --> LH
```

Alignment and energy-reference selection occur before compatibility when required and
remain outward scientific-analysis policy. The outward loss definition selects samples
and weights; `operators` owns represented subtraction and primitive residuals, while
PhysKit owns reusable unit-bearing aggregation through $R_H$. Model adequacy owns the declared normalization
$L_H=R_H/E_0$. Neither layer may infer alignment or an energy reference from matrix
values.

## M3 compatibility path

```mermaid
flowchart LR
    m3current["Current periodic1d M3\nPeriodic1DQuadraticLoss"]
    common["Exact-pinned Optimization\nquadratic facade"]
    m3wrapper["M3 wrapper\nchannel_id + alignment_angle\nshift/splitting convention"]
    m3wire["Existing M3 schema v1"]
    verifier["Independent M3 verifier"]

    m3current -. behavior-preserving migration .-> m3wrapper
    common --> m3wrapper
    m3wrapper --> m3wire
    verifier -. reconstructs independently .-> m3wire
```

The dotted M3 migration is prospective, but target integration and dependency repinning
are complete. Existing source and wire identity do not change because this diagram exists.
The verifier must not call the producer evaluator to establish independent
reconstruction.

## HSH ownership path

```mermaid
flowchart LR
    lattice["PhysKit periodic lattice primitives"]
    parameterSpace["Optimization ParameterSpace"]
    parent["periodic2d parent/model/Fourier primitives"]
    hsh["analysis.model_adequacy\nHSH-specific outward analyzer"]
    common["Exact-pinned Optimization\nquadratic facade"]
    wrapper["HSH wrapper\nshell + channel + active-index mapping"]
    certificate["HSH support certificate\nmetric + outward rounding"]
    hierarchy["HSH class and hierarchy disposition"]

    lattice --> hsh
    parameterSpace --> hsh
    parent --> hsh
    hsh --> wrapper
    common --> wrapper
    wrapper --> certificate
    certificate --> hierarchy
```

HSH selects its shell-radius sequence, source correlation, coefficient bounds, weights,
normalization, thresholds, certificate meaning, and hierarchy minimality. The inclusive
bound container and quadratic facade come from exact-pinned Optimization; lattice
operations, orbit/shell construction, projection, multiplicities, and dimensionful
hopping geometry come from PhysKit.

## Common coefficient box and exact shell slices

```mermaid
flowchart TD
    names["Canonical maximal orbit names\nfixed order"]
    bounds["HSH-selected finite lower and upper bounds\ncontain zero and target with margin"]
    commonBox["Optimization ParameterSpace\ncommon inclusive coefficient box"]
    shell["HSH shell mask\nactive maximal-space indices"]
    activeBounds["Active coordinates\nretain common bounds"]
    inactiveBounds["Inactive coordinates\nfixed bound [0, 0]"]
    classSpace["Derived maximal-coordinate ParameterSpace\nexact affine shell slice"]
    solver["Bounded solver candidate"]
    projection["Exact inactive-zero projection\nretain pre-projection defect"]
    proofPoint["Retained proof point"]

    names --> commonBox
    bounds --> commonBox
    commonBox --> activeBounds
    shell --> activeBounds
    shell --> inactiveBounds
    activeBounds --> classSpace
    inactiveBounds --> classSpace
    classSpace --> solver
    solver --> projection
    projection --> proofPoint
```

The common box and every shell slice use the same maximal-coordinate ordering. Equal
endpoints represent mathematical equality, not a numerical tolerance. The HSH builder
must prove that each active bound is copied unchanged and each inactive coordinate is
fixed exactly to zero.

## Export promotion boundary

```mermaid
flowchart LR
    oldDraft["Superseded Optimization donor draft\nexternal recovery only"]
    optCommit["Optimization quadratic owner commit\nec3d290…"]
    optPin["Current exact KSD dependency pin"]
    optRuntime["Supported quadratic facade"]
    optExport["exports/optimization\naffine and metric candidates"]
    optReview["Optimization owner review"]
    optFuture["Future immutable Optimization commit"]
    physExport["exports/physkit\nactive non-runtime candidates"]
    physReview["PhysKit owner review"]
    physCommit["Future immutable PhysKit commit"]
    futurePins["Future separately authorized exact dependency pins"]
    hsh["Future HSH composition"]

    oldDraft -. not transferred .-> optCommit
    optCommit --> optPin
    optPin --> optRuntime
    optExport -. candidate .-> optReview
    optReview --> optFuture
    physExport -. candidate .-> physReview
    physReview --> physCommit
    optRuntime --> hsh
    optFuture --> futurePins
    physCommit --> futurePins
    futurePins --> hsh
```

The Optimization owner supplied its own quadratic implementation; KSD does not consume
the superseded quadratic donor bytes. The new affine/metric and PhysKit candidates still
require their respective owner reviews and immutable owner commits. No arrow runs
directly from active `exports/` source to runtime. Dependency integration, HSH
implementation, scientific execution, and scientific acceptance remain separate
decisions.

## Training and withheld roles

```mermaid
flowchart TD
    training["Frozen training data"] --> construction["Loss construction"]
    construction --> decision["Witness/certificate decision objects"]
    withheld["Disjoint withheld data"] --> diagnostics["Post-decision diagnostics"]
    decision --> report["Bounded result"]
    diagnostics --> report
```

There is no arrow from withheld diagnostics back to loss construction, thresholds,
witnesses, or certificates unless a different protocol explicitly declares a second
training stage.
