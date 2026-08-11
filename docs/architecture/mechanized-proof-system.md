# Multi-Prover Mechanized-Proof System

## Status

Approved conceptual architecture. The nine initial `PRF-05` prover-neutral contracts are frozen as common backend targets; executable backend implementation is inactive.

This document authorizes the repository structure and dependency direction for a future mechanized-proof system using Lean 4, Isabelle/HOL, and Rocq. It authorizes maintained prover-neutral theorem contracts under `formal/theorem-catalog/`. It does not authorize installing toolchains, adding dependencies, creating executable prover projects, running external services, or representing any theorem as machine checked.

## Purpose

The mechanized-proof system will independently encode selected mathematical claims from the `ksdft2effmass` proof program in three proof assistants. Its first scope is the finite-dimensional algebraic layer required for gauge-equivariant operator comparison.

The system is intended to:

- expose missing assumptions and type mismatches;
- make elementary covariance and invariance arguments machine checkable;
- compare independent formal encodings of the same theorem contract;
- preserve traceability from scientific specifications to prose proofs and formal proofs; and
- distinguish checked derivations from numerical verification and scientific validation.

It is not intended to mechanize Kohn–Sham DFT, reproduce Quantum ESPRESSO or Wannier90, or treat formal consistency as evidence that a physical model adequately describes silicon.

## Novelty and claim boundary

The `PRF-05` identities are elementary consequences of standard finite-dimensional linear algebra. They are not presented as new mathematical theorems:

| Contract | Mathematical status |
|---|---|
| `PRF-05.01` | Standard invariance of an orthogonal projector under unitary rotation of its orthonormal frame. |
| `PRF-05.02` | Standard change-of-basis covariance for a compressed operator representation. |
| `PRF-05.03` | Standard covariance of an identification pullback. |
| `PRF-05.04` | Standard covariance and unitary-equivalence algebra, organized for the project's paired pristine-space and doped-space representations. |
| `PRF-05.05a` | Standard unitary invariance of the Frobenius norm. |
| `PRF-05.05b` | Standard unitary invariance of the induced Euclidean operator norm. |
| `PRF-05.06` | Immediate composition of common equivariance with the selected unitary norm invariance. |
| `PRF-05.07` | An explicit two-point witness for the established gauge dependence of real-space localization and truncation. |
| `PRF-05.08` | Blockwise Frobenius invariance summed over an unchanged shell. |

Wavevector-dependent unitary freedom and its relation to Wannier localization are established parts of Wannier theory. Relevant primary and review sources include:

- N. Marzari and D. Vanderbilt, “Maximally localized generalized Wannier functions for composite energy bands,” *Physical Review B* **56**, 12847–12865 (1997), [doi:10.1103/PhysRevB.56.12847](https://doi.org/10.1103/PhysRevB.56.12847).
- I. Souza, N. Marzari, and D. Vanderbilt, “Maximally localized Wannier functions for entangled energy bands,” *Physical Review B* **65**, 035109 (2001), [doi:10.1103/PhysRevB.65.035109](https://doi.org/10.1103/PhysRevB.65.035109).
- N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012), [doi:10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419).

The potential contribution of `PRF-05` is therefore its coordinated mechanization and composition for this operator-reduction framework: exact application-specific contracts, independent Lean–Isabelle–Rocq encodings, semantic conformance review across those encodings, the dual-orientation organization of `PRF-05.04`, and the explicit witness in `PRF-05.07`. No priority claim is made that this exact collection has never been formalized elsewhere; that would require a dedicated prior-art review. Current mathlib documentation confirms relevant infrastructure for the [unitary group](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/UnitaryGroup.html) and [matrix norms](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Matrix/Normed.html), but library infrastructure alone does not establish that these application-specific exported contracts already exist.

The defensible project claim is:

> The individual identities are standard; their coordinated machine-checked formulation and composition into a gauge-equivariant operator-reduction framework may be new.

Accordingly, `PRF-05` is the prospective machine-checked foundational layer for later scientific arguments, not a package of novel mathematical proofs. Potential research-theorem scope begins only where separately specified and supported, for example:

- equivariance or uniqueness of the tight-binding-anchored identification;
- gauge-invariant distances between operator equivalence classes;
- sufficient conditions under which gauge fixing and real-space truncation commute;
- quantitative truncation-error bounds under restricted gauges;
- operator-to-binding-energy or fidelity bounds; and
- sufficient conditions for an atomistic-to-continuum crossover.

These are proposed theorem families, not completed proofs, verified numerical results, or scientifically validated claims. Integrating later checked lemmas into a DFT-to-tight-binding-to-effective-mass verification workflow would likewise establish only the declared formal or software-verification properties.

## Authority

Interpret mechanized material in this order:

1. current human scientific decisions;
2. applicable versioned contracts under `specification/`;
3. accepted assumptions and conventions under `docs/research/`;
4. definitions and assumptions in the owning prose proof under `docs/proofs/`;
5. the prover-neutral theorem contract identified by the proof registry;
6. backend-specific formal definitions and theorem statements;
7. checked proof terms or proof objects;
8. generated reports and manuscript summaries.

A prover can establish that a formal conclusion follows from encoded assumptions. It cannot establish that the encoded assumptions are physically correct, complete, or applicable to a calculation.

If backend encodings disagree, the disagreement is a formalization finding. No backend silently becomes authoritative by passing its own checker.

## Conceptual architecture

The architecture has one theorem-identity layer and three independent proof backends:

```text
specification/ and docs/research/
                ↓
docs/proofs/ksdft2effmass/
                ↓
PRF theorem identity and assumption contract
                ↓
     ┌──────────┼──────────┐
     ↓          ↓          ↓
 Lean 4    Isabelle/HOL   Rocq
     └──────────┼──────────┘
                ↓
       conformance summary
                ↓
   manual proof-status update
```

The three backends must not generate one another's theorem statements or proofs. Independent encoding is required so that agreement can reveal specification ambiguity or backend-specific modeling choices rather than reproduce one translation error three times.

## Repository layout

The theorem catalog is an active maintained documentation surface. Lean, Isabelle, and Rocq paths remain prospective and are not created by this architecture phase.

```text
formal/
├── theorem-catalog/
│   ├── README.md
│   └── PRF-05.md
├── lean/
│   ├── lakefile.toml
│   ├── lake-manifest.json
│   ├── lean-toolchain
│   └── Ksdft2Effmass/
│       ├── Spaces.lean
│       ├── Gauge.lean
│       ├── Alignment.lean
│       ├── Residuals.lean
│       ├── Truncation.lean
│       └── PathConsistency.lean
├── isabelle/
│   ├── ROOT
│   ├── ROOTS
│   └── Ksdft2Effmass/
│       ├── Spaces.thy
│       ├── Gauge.thy
│       ├── Alignment.thy
│       ├── Residuals.thy
│       ├── Truncation.thy
│       └── Path_Consistency.thy
└── rocq/
    ├── _CoqProject
    ├── rocq-project.toml
    └── Ksdft2Effmass/
        ├── Spaces.v
        ├── Gauge.v
        ├── Alignment.v
        ├── Residuals.v
        ├── Truncation.v
        └── PathConsistency.v
```

Generated build products, caches, downloaded package stores, compiled proof artifacts, and editor state are not maintained source and must not be committed.

## Ownership and dependency direction

### Theorem catalog

The prospective `formal/theorem-catalog/` surface owns cross-backend theorem identity, not mathematical derivations. Each entry must identify:

- the `PRF-*` proof obligation;
- the prose proof owner;
- authoritative specification and research references;
- state spaces and scalar fields;
- assumptions;
- conclusion;
- intended backend theorem names;
- admitted differences between backend encodings; and
- backend completion and review evidence.

The catalog must not duplicate full proofs or redefine scientific assumptions.

### Lean backend

The prospective `formal/lean/` surface owns Lean definitions and proofs. It depends on the theorem catalog and a pinned Lean 4/mathlib toolchain. It does not own Python behavior or scientific assumptions.

Official Lean learning and reference material:

- [Lean learning portal](https://lean-lang.org/learn/)
- [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/) — programming-language introduction
- [Theorem Proving in Lean 4](https://lean-lang.org/theorem_proving_in_lean4/) — dependent type theory and interactive theorem proving
- [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/) — mathematical formalization with mathlib
- [Lean Language Reference](https://lean-lang.org/doc/reference/latest/) — language and elaborator reference
- [Lean FAQ](https://lean-lang.org/faq)
- [Mathlib API reference](https://leanprover-community.github.io/mathlib4_docs/) — searchable Lean core, standard-library, and mathlib declarations

These links identify documentation resources only. Exact toolchain and mathlib versions remain deferred until the dependency decision is resolved; version-specific local documentation should accompany any future pinned environment.

### Isabelle backend

The prospective `formal/isabelle/` surface owns Isabelle theories and session structure. It depends on the same theorem catalog and a pinned Isabelle distribution. It does not import generated Lean or Rocq artifacts.

### Rocq backend

The prospective `formal/rocq/` surface owns Rocq definitions and proofs and any explicitly selected formal libraries. It depends on the same theorem catalog. It does not import generated Lean or Isabelle artifacts.

### Python and scientific software

Python may later consume compact, reviewed formal conformance fixtures only through a separately specified boundary. Python must not invoke a theorem prover as part of its ordinary runtime API, and formal backends must not depend on Python implementations as definitions of mathematical truth.

## Theorem identity and conformance

One conceptual theorem receives one stable proof identifier, for example `PRF-05.03`. Backend declarations use that identity in comments or metadata while retaining idiomatic backend names.

Backend agreement requires more than similarly named theorems. A conformance review must compare:

- scalar field;
- finite-dimensionality assumptions;
- equality notion;
- matrix or operator representation;
- unitarity and adjoint definitions;
- norm definition;
- quantifier order;
- locality and index-set definitions; and
- all explicit and type-class-supplied assumptions.

The conformance states are:

| State | Meaning |
|---|---|
| `unencoded` | No backend statement exists. |
| `encoded` | A backend theorem statement exists but has no complete checked proof. |
| `checked` | The selected backend accepts the proof under the pinned toolchain. |
| `cross-checked` | All three backends check reviewed encodings judged semantically conformant. |
| `reviewed` | Independent mathematical review confirms the theorem contract and backend correspondence. |

`cross-checked` is not scientific validation and does not automatically advance the parent manuscript or publication state.

## Initial PRF-05 decomposition

The first mechanized package is limited to elementary finite-dimensional results:

| ID | Theorem obligation |
|---|---|
| `PRF-05.01` | A retained-space projector is invariant under unitary rotation of its orthonormal frame. |
| `PRF-05.02` | A represented operator transforms covariantly under unitary change of coordinates. |
| `PRF-05.03` | An identification pullback is covariant under compatible source and target gauges. |
| `PRF-05.04` | The pristine-space and doped-space aligned differences are separately covariant and are unitarily equivalent when the identification is unitary. |
| `PRF-05.05a` | The Frobenius norm is invariant under unitary conjugation. |
| `PRF-05.05b` | The induced Euclidean operator norm is invariant under unitary conjugation. |
| `PRF-05.06` | The norm of the difference between conformant equivariant paths is gauge invariant. |
| `PRF-05.07` | A two-point example shows that a wavevector-dependent gauge need not commute with real-space truncation. |
| `PRF-05.08` | Shell-resolved Frobenius diagnostics are invariant under the declared lattice-local constant unitary rotations. |

Continuum limits, Feshbach analysis, compactness arguments, certified optimization, and silicon-specific asymptotics remain outside the initial mechanization package.

## Build and runtime boundaries

Each backend has an explicit, separately pinned build. No backend is loaded by the Python package, Pi startup, manuscript renderer, or proof-status reader.

A future build interface may run the three checks independently and aggregate exit status, but it must preserve per-backend diagnostics. A passing aggregate means only that all selected backend checkers accepted their inputs.

No checker may mutate:

- `specification/`;
- `docs/research/`;
- proof status;
- manuscript claims;
- Python expected values; or
- scientific acceptance records.

Proof status is updated manually after checking and review evidence are inspected.

## Versioning and dependency policy

Each backend must pin its toolchain and formal-library versions using its native reproducibility mechanism. Toolchain upgrades are dependency decisions and require compatibility review of all checked theorems.

The three prover ecosystems are development and verification toolchains, not Python runtime dependencies. They must not be added to `python/pyproject.toml` or `python/uv.lock`.

Selecting exact versions, package managers, library subsets, CI images, and installation methods is deferred to an explicitly authorized implementation task and applicable dependency checkpoint.

## Migration sequence

The architecture supports all three backends but does not require simultaneous implementation.

1. Reconcile `PRF-00` definitions and freeze the initial `PRF-05` theorem contracts.
2. Establish the theorem catalog and cross-backend naming rules.
3. Encode and check the complete `PRF-05` set in Lean.
4. Independently encode the same contracts in Isabelle/HOL.
5. Independently encode the same contracts in Rocq.
6. Perform semantic conformance review across all three encodings.
7. Record per-backend status and only then consider `cross-checked` status.
8. Evaluate whether a later analytical theorem package is justified.

The staged sequence limits specification churn while retaining the approved all-three-backend destination.

## Failure and disagreement handling

Failures are classified separately:

- **statement mismatch:** backend theorem propositions are not semantically equivalent;
- **missing assumption:** a proof requires an assumption absent from the theorem contract;
- **library mismatch:** the desired abstraction is unavailable or materially different;
- **proof incomplete:** the statement is encoded but not proved;
- **toolchain failure:** the pinned checker cannot execute reproducibly;
- **cross-backend disagreement:** individually checked statements encode materially different mathematics;
- **scientific ambiguity:** authoritative project conventions do not determine one formal statement.

Scientific ambiguity stops formalization and returns to the owning specification or research decision. It is not resolved by majority agreement among proof assistants.

## Reversibility

The formal tree is isolated from Python runtime and serialized scientific records. A backend can be replaced or retired without changing public Python APIs, provided theorem history and the reason for retirement are retained.

Removing one backend changes an all-three `cross-checked` claim and therefore requires updating the theorem catalog, proof status, documentation, and any publication statement relying on that claim.

## Deferred implementation decisions

This architecture does not select:

- exact prover or library versions;
- installation or package-management methods;
- CI providers or images;
- automated theorem-catalog parsers;
- generated documentation tooling;
- formal-to-Python fixture formats;
- licenses of newly introduced formal dependencies; or
- ownership assignments for implementation writers and reviewers.

Those decisions belong to a separately authorized implementation task. No formal toolchain may be installed or added until its dependency and licensing boundary is explicitly resolved.
