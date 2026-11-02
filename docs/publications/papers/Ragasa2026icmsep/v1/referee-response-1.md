# Response to technical referee review 1

## Review disposition

- **Review outcome:** `CHANGES_REQUIRED`
- **Operator request:** `NONE`
- **Manuscript status:** major revision in progress; not submission-ready

The review is accepted as technically well founded. The manuscript has been revised where the retained evidence is already sufficient. Independent reconstruction and provenance reconciliation remain publication blockers rather than prose-only tasks.

## Responses and revisions

### 1. Numerical evidence maturity

**Disposition:** `MUST_FIX`

The complete rank-two numerical headline and the silicon producer results have not yet received complete-scope independent reconstruction. The manuscript continues to label them as development evidence and no longer presents the silicon study as empirical validation of the rank-two theorem.

**Required before submission:**

1. independently reconstruct the complete rank-two range decision;
2. independently reconstruct the rank-10 attack, alignments, Fourier conversion, support hierarchy, and Parseval channels; and
3. independently reproduce the frozen fidelity ladder and band-edge calculations.

No new QE, Wannier90, SOC, Slater--Koster, or additional material-model calculation should precede this work.

### 2. Abstract scope and authentication language

**Disposition:** `NO_ACTION_REQUIRED` after revision

The abstract was reduced to three scientific results: the exact rank-two identity, the sampled finite-range consequence, and the silicon finding that global spectral fidelity does not ensure operator or band-edge fidelity. The literal 371-of-383 result was removed from the abstract.

“Authenticated” is now defined as verified provenance, byte identities, native optimizer completion, Hermiticity, pair closure, and reconstruction—not material validation.

### 3. Theoretical and computational architecture

**Disposition:** `NO_ACTION_REQUIRED` after revision

The introduction now explicitly separates:

- the controlled rank-two theorem and synthetic benchmark; and
- the source-specific rank-10 silicon case study.

The silicon study is not described as a general empirical proof of a rank-N theorem.

### 4. Gauge and alignment interpretation

**Disposition:** `NO_ACTION_REQUIRED` after revision

The manuscript now states that a momentum-dependent unitary can redistribute weight toward longer range for particular transformations and locality measures; it does not assert universal monotonic range increase.

The global residual is explicitly identified as a distance under the declared weighted global-unitary action, not an invariant metric between unrestricted gauge orbits.

### 5. Rank-two theorem exposition

**Disposition:** `NO_ACTION_REQUIRED` after revision

The main text now includes:

- explicit loss normalizations and weights;
- the second-harmonic form in `2 phi`;
- the role of parameter-rectangle containment in the ellipse-intersection criterion;
- the Bessel integral giving `J_0(2a)`;
- the derivative argument for monotonicity on the declared interval;
- the intermediate Parseval identity; and
- the renamed “rank-two residual--non-onsite-power identity,” preserving its assumptions in the theorem title and prose.

### 6. Synthetic rank-10 gauge attack

**Disposition:** `NO_ACTION_REQUIRED` after revision

The attack is now identified as a real orthogonal, hence complex-unitary, circuit in the authenticated Wannier coordinate order. The index sequence is not assigned atomic-orbital semantics. The manuscript states explicitly that the attack is a constructed stress test, not representative of typical Wannier90 gauge variation and not known to maximize range inflation.

### 7. Fourier conversion and FCC support geometry

**Disposition:** `MUST_FIX` for independent verification; manuscript description revised

The article now derives the FCC metric from `R = A n` and includes a machine-readable reconstruction ledger identifying the request, producer, result fields, displacement inventory, support records, and evaluation ordering.

The retained artifacts make the process auditable, but a second implementation must still reconstruct the arrays and checks independently before publication.

### 8. Refitted-shell optimization

**Disposition:** `NO_ACTION_REQUIRED` after revision

Terminology is restricted to observed witnesses and observed non-dominated sets. Missing witnesses are not called infeasible.

The manuscript now reports bound activity among the 444 successful records:

- 50 records have one lower-bound-active coefficient;
- 35 records have one upper-bound-active coefficient;
- bound activity occurs only for H-shell-02, H-shell-06, and H-shell-08; and
- no successful record has more than one active lower or upper coefficient.

The parameter bounds are therefore acknowledged as shaping portions of the observed witness set.

### 9. Frozen data roles

**Disposition:** `NO_ACTION_REQUIRED` after revision

A new table separates construction, fitting, selection, and evaluation roles for:

- the relaxed-cell/SCF/NSCF evidence;
- the 216-point construction grid;
- the ordered 408-point development geometry;
- the `12^3`, `20^3`, and `32^3` meshes;
- the bounded signed-axis valley searches; and
- the excluded 402-point confirmation set.

### 10. Valley-search terminology

**Disposition:** `NO_ACTION_REQUIRED` after revision

The manuscript now calls the outputs “identified sector minima.” It states that bounded multistart L-BFGS-B does not certify the global minimum of an entire sector.

### 11. Parent-gap provenance distinction

**Disposition:** `NO_ACTION_REQUIRED` after retained-identity audit

The two values belong to different candidate Hamiltonians compared with the same revealed DFT parent:

- `0.5226105 eV` belongs to the earlier lower-energy-frozen `4^3`/12-band candidate, with eligible HR SHA-256 `2139eb7f73525853a7e45fe9b3fc54fecb150f526c1834e9db3749c64664db03`;
- `0.6892447 eV` belongs to the current `C6-B20-W21` candidate, with eligible HR SHA-256 `24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55`.

The discrepancy was therefore a lineage-labeling problem, not two estimates for one source. The article now states the distinction explicitly and uses `0.6892447 eV` only for `C6-B20-W21`.

### 12. SOC and new calculations

**Disposition:** `SAFE_TO_DEFER`

SOC is unnecessary for the current non-SOC compression diagnosis. It becomes necessary only for physical HH/LH/split-off, Luttinger, or acceptor claims. New SOC or model-family calculations would broaden the manuscript before its existing evidence is independently secure. After this response was drafted, the operator separately authorized one fixed-density accepted-parent DFT band-path calculation for a conventional manuscript figure. That run changes no model, fitting inventory, threshold, or source construction and is retained as contextual path evidence only.

## Immediate next technical milestone

Perform independent, no-calculator reconstruction in this order:

1. rank-two range headline;
2. rank-10 gauge/Fourier/support/Parseval analysis; and
3. frozen fidelity and band-edge analysis.

Each reconstruction should consume authenticated source bytes directly, use independent arithmetic and implementation structure, and produce a retained comparison record without changing the frozen scientific selections.
