# `ksdft2effmass.operators` package

## Responsibility

`ksdft2effmass.operators` is the cohesive, narrowly bounded owner of finite
represented-operator records and deterministic operations on already identified
representations. It retains:

- state-space, ordered-basis, geometry, energy-reference, matrix, and provenance
  metadata;
- strict versioned serialization;
- exact represented-metadata compatibility auditing;
- fixed-representation Hermiticity analysis;
- guarded signed subtraction for already compatible records;
- primitive maximum-entry, Frobenius, and spectral residual mechanics; and
- narrow composition of differencing and primitive residual analysis.

```mermaid
flowchart LR
    records["Represented-operator records"] --> compatibility["Exact compatibility"]
    records --> hermiticity["Fixed-representation Hermiticity"]
    compatibility --> difference["Guarded signed difference"]
    difference --> residuals["Primitive residuals"]
    residuals --> comparison["Fixed-representation comparison"]
    records --> serialization["Versioned serialization"]
```

## Boundary

The package does not select or estimate basis, gauge, geometry, spin, unit, or
energy-reference alignment. It does not convert units or energy zeros, determine
physical equivalence, fit model classes, perform continuum reduction or structured
learning, classify a generic difference as an impurity operator, decide scientific
acceptance, or own Workflow orchestration.

A successful compatibility audit establishes only the exact represented prerequisites
it checks. A successful subtraction or residual calculation establishes only its
declared fixed-representation software or numerical contract. Higher-level scientific
analysis consumes this package through the dependency
`ksdft2effmass.analysis → ksdft2effmass.operators`.

## Migration and status

Human-authorized Option A retains the Architecture v1 package owner. The selected
records-disposition plan is a provisional no-change baseline: it leaves
`operators.records`, `operators.serialization`, and `operators.compatibility` in
place, keeps the currently supported `ksdft2effmass.operators` imports and nominal
type identities, and leaves the version-1 specification and golden fixtures
unchanged. It does not freeze the final Architecture v2 scientific API. Controlled
manuscript exercises may identify later state-space, projection, embedding,
comparison, or model-class requirements, but any resulting public-contract change
requires separate authorization and migration evidence. No facade, duplicate record
type, v2 wire, or source cutover is introduced by this planning result. The
higher-level analysis disposition remains with its separate Task. This result changes
no implemented dependency and authorizes no scientific or protected execution.
