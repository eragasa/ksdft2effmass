# Bulk-Silicon Production Convergence Design

**Status:** Proposed work; Task
[`bulk-silicon.production-reference.convergence`](../../harness/tasks/bulk-silicon.production-reference.convergence.json)
is active in phase `awaiting_human_parameter_selection`. This page selects no
numerical parameter and authorizes no calculation. The governing program is the
[bulk-silicon production program](bulk-silicon-production-program.md).

## Frozen pseudopotential authority and preflight

The maintained
[`NumericalSpecification-v1`](../../specification/ksdft2Effmass.numerical-specification.v1.md)
freezes the following production identity; this Task does not select a family.

| Field | Frozen or observed value |
|---|---|
| Family / table | PseudoDojo PBE standard table, `nc-sr-04_pbe_standard` |
| Exchange--correlation | PBE GGA |
| Element | Si |
| Type | Optimized norm-conserving Vanderbilt; NC |
| Relativistic treatment | Scalar relativistic; production bulk branch is non-SOC |
| Valence | 4 electrons, Si $3s^2 3p^2$, frozen core |
| Upstream release | PseudoDojo `1.0` |
| Canonical source | `https://www.pseudo-dojo.org/pseudos/nc-sr-04_pbe_standard/Si.upf.gz` |
| Canonical files | distributed `Si.upf.gz`; decompressed QE input `Si.upf` |
| Expected SHA-256 | compressed: `bfbd01ccd4b67584dcf19a490a76e9b688c25026775ce2f4a4b6a13f900dad81`; decompressed: `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282` |
| Authoritative cutoff hints | normal 18 Ha = 36 Ry; high 24 Ha = 48 Ry for `ecutwfc` |
| License | Not recorded in the maintained v1 specification; exact upstream grant and attribution must be verified during preflight before use or redistribution |
| QE expectation | Decompressed UPF must be readable by the selected `pw.x`; its declared element, XC, NC form, valence, and scalar-relativistic metadata must agree with this table |
| Wannier90 expectation | Wannier90 does not consume the UPF directly. Compatibility is inherited through outputs from the same accepted QE installation; `pw.x` and `pw2wannier90.x` must share an installation and a later interface smoke test must pass. |
| Local availability | Neither canonical filename was found in the repository or the bounded standard project/data/cache locations inspected for this design; no production bytes were identity-verified |

The preflight order is: observe an explicitly supplied local path without
changing it; compute compressed and, after controlled decompression, decompressed
SHA-256; compare both exact digests; parse the UPF metadata; record file size and
license/citation evidence; identify `pw.x` and `pw2wannier90.x`; then check format
compatibility without starting a scientific calculation. A missing file,
license record, digest match, or metadata match stops preflight. No same-named
file supplies authority.

These categories are not interchangeable:

```text
authority metadata
≠ local availability
≠ byte-identity verification
≠ scientific validation
```

The exact expected SHA-256 values are frozen, so there is no digest-authority
defect. The missing maintained license statement is a provenance/compatibility
item to resolve from identified upstream evidence, not permission to replace the
artifact. The legacy tutorial `Si.pz-vbc.UPF` is LDA, nonrelativistic, and
ineligible for production.

## Preliminary fixed structure

The only exact reusable silicon geometry retained by the repository is the QE
example01 tutorial structure. The recommendation is to reuse its geometry only
as a **provisional fixed structure**, while replacing its LDA pseudopotential and
numerical settings with the frozen production branch:

- conventional cubic lattice parameter $a_0=10.20$ bohr;
- two-atom fcc primitive vectors, in Cartesian bohr,

  $$
  \mathbf a_1=(-a_0/2,0,a_0/2),\quad
  \mathbf a_2=(0,a_0/2,a_0/2),\quad
  \mathbf a_3=(-a_0/2,a_0/2,0);
  $$

- Si sites at $(0,0,0)$ and $(a_0/4,a_0/4,a_0/4)$ in the same Cartesian
  convention; and
- fixed cell and fixed ionic positions for every cutoff and mesh case.

This value is tutorial geometry, not an experimental authority and not a
preliminary PBE calculation. It is not the accepted equilibrium production
lattice. The later zero-pressure PBE EOS Task owns that value.

## Staged study

### Stage 1 — controlled preliminary context

For all primary cases, hold fixed: the provisional structure; exact verified
pseudopotential; non-spin-polarized, non-SOC PBE branch; `occupations='fixed'`
with no smearing; `diagonalization='david'`; `mixing_mode='plain'`;
`mixing_beta=0.7`; `electron_maxstep=100`; `conv_thr=1e-10 Ry`; symmetry and
time-reversal enabled (`nosym=.false.`, `noinv=.false.`); one local process; and
identical explicit FFT-related policy except for grids deterministically induced
by the cutoffs. QE version, command, environment, and processor count are part
of every identity.

### Stage 2 — wavefunction-cutoff scan

The proposed source-backed sequence is the exact v1 example that brackets and
extends the 36 Ry normal and 48 Ry high PseudoDojo hints:

| Case | $E_{\mathrm{cut}}^\psi$ (Ry) | $E_{\mathrm{cut}}^\rho$ (Ry) | Ratio | SCF mesh |
|---|---:|---:|---:|---|
| C30 | 30 | 120 | 4 | $8\times8\times8$, shift $(1,1,1)$ |
| C36 | 36 | 144 | 4 | $8\times8\times8$, shift $(1,1,1)$ |
| C42 | 42 | 168 | 4 | $8\times8\times8$, shift $(1,1,1)$ |
| C48 | 48 | 192 | 4 | $8\times8\times8$, shift $(1,1,1)$ |
| C54 | 54 | 216 | 4 | $8\times8\times8$, shift $(1,1,1)$ |
| C60 | 60 | 240 | 4 | $8\times8\times8$, shift $(1,1,1)$ |

The $4:1$ rule is explicit and follows the frozen NC protocol. If density
sensitivity controls acceptance, a later bounded refinement at fixed selected
$E_{\mathrm{cut}}^\psi$ compares ratios 4, 6, and 8; it is not part of the
initial six-case scan.

### Stage 3 — SCF mesh scan

After provisional cutoff selection, vary only the mesh:

| Case | Dimensions | QE shifts | Symmetry | Irreducible count | High-symmetry content |
|---|---|---|---|---|---|
| K6 | $6\times6\times6$ | $(1,1,1)$ | space-group and time-reversal enabled | Record from exact QE reduction; not asserted before input/executable preflight | Shifted integration mesh; does not contain $\Gamma$ and is not a path or valley set |
| K8 | $8\times8\times8$ | $(1,1,1)$ | same | same | same |
| K10 | $10\times10\times10$ | $(1,1,1)$ | same | same | same |
| K12 | $12\times12\times12$ | $(1,1,1)$ | same | same | same |

All use fixed occupations and no smearing because the parent is an insulator.
The shifts preserve a consistent even-grid Monkhorst--Pack family. Exact
irreducible counts depend on the final cell representation and QE symmetry
analysis and will be retained rather than guessed. The K8 case reuses the
byte-identical selected-cutoff/K8 calculation from Stage 2; it is not rerun.
The tutorial ten-point list is not reused.

### Limited fixed-point band diagnostics

Total energy is not sufficient for a program that depends on band edges. Each
primary SCF case therefore has one lightweight, separately identified fixed-point
NSCF diagnostic using its converged density at conventional reciprocal
coordinates (units $2\pi/a_0$): $\Gamma=(0,0,0)$,
$X=(0,1,0)$, and $\Delta_{0.85}=(0,0.85,0)$. Use `nbnd=8`; for this
non-spin-polarized eight-valence-electron cell, ordered bands 1--4 are occupied
and bands 5--8 are unoccupied. Retain bands 4 and 5 at all three points and align
individual eigenvalues within each calculation as
$\widetilde\epsilon_{n\mathbf k}=\epsilon_{n\mathbf k}-\epsilon_{4\Gamma}$.
Retain direct probes $g_{\mathbf k}=\epsilon_{5\mathbf k}-\epsilon_{4\mathbf k}$
at all three points and indirect probes
$g_{\Gamma X}=\epsilon_{5X}-\epsilon_{4\Gamma}$ and
$g_{\Gamma\Delta}=\epsilon_{5\Delta_{0.85}}-\epsilon_{4\Gamma}$. Record any
ordering change or unresolved degeneracy as a warning rather than silently
relabeling bands. $\Delta_{0.85}$ is only a reproducible sensitivity probe, not
an accepted valley location. These three points are not a symmetry path, valley
search, curvature stencil, or physical validation.

### Stage 4 — coupling cross-check

After sequential provisional selections $(E_*,K_*)$, evaluate this bounded
four-corner set when separately authorized:

1. baseline $(E_*,K_*)$;
2. denser-mesh guard $(E_*,K_+)$;
3. higher-cutoff guard $(E_+,K_*)$; and
4. mixed corner $(E_+,K_+)$.

The interaction diagnostic for each scalar observable $q$ is

$$
I_q=\left|q(E_+,K_+)-q(E_+,K_*)-q(E_*,K_+)+q(E_*,K_*)\right|.
$$

If a selected value is already the highest primary candidate, propose one
explicitly higher guard before execution rather than extrapolating. Any corner
that is byte-identical to a retained primary case is reused, not rerun. Both
one-axis changes at the higher opposite-axis setting must meet the applicable
observable criterion, and $I_q$ must not exceed that same absolute criterion.
A material failure triggers a human-reviewed expanded design; it does not
automatically trigger a full cutoff-by-mesh grid.

### Stage 5 — EOS feedback

```text
provisional structure
→ convergence settings
→ EOS/lattice refinement
→ convergence recheck if material
```

The EOS Task uses settings at least as strict as those provisionally accepted
for energy and stress. If its finalized lattice constant differs from the
provisional value by more than $10^{-4}$ Å, it repeats the selected case and the
three nonbaseline corners at the finalized geometry; this prospective trigger
uses the frozen lattice-refinement scale and does not wait for a convergence
failure to be observed. The EOS Task must also bound setting-induced equilibrium-
lattice sensitivity to $10^{-4}$ Å or the larger fitted uncertainty, using guard
EOS fits or a documented pressure-to-lattice bound based on the fitted curvature.
Cutoff, mesh, and lattice convergence are coupled numerical questions, not
independent certificates.

## Monitored observables and records

For every SCF candidate retain calculation identity; total energy per atom;
difference from the highest-resolution retained candidate; hydrostatic pressure
$P=-\operatorname{tr}(\boldsymbol\sigma)/3$ and maximum absolute stress-component
difference; SCF iteration count; final code-reported estimated SCF accuracy and
its exact QE definition/unit; wall time; peak or final disk use when observable;
all warnings; and the fixed-point diagnostic eigenvalues/gaps above. Retain raw
stress tensor and sign convention so pressure is reproducible.

The diagnostic NSCF is linked to its source density and records eigenvalue unit,
spin convention, coordinates, reciprocal basis, band labels, and energy
alignment. No full path or valley calculation is embedded in the scan.

## Proposed convergence criteria

For an observable $q_j$ and retained highest-resolution reference
$q_{\mathrm{ref}}$,

$$
\Delta q_j=|q_j-q_{\mathrm{ref}}|.
$$

This is a finite internal diagnostic, not evidence of the infinite-basis limit.
The primary frozen energy and band rules compare a candidate with the next finer
retained setting; the highest retained candidate acts as a guard.

| Observable | Mathematical rule and units | Reference and type | Scope / rationale |
|---|---|---|---|
| Energy per atom | $|E_j/N_{\rm Si}-E_{j+1}/N_{\rm Si}|\le10^{-5}$ Ry/atom and the selected case agrees with the retained guard at the same absolute tolerance | Next finer setting; absolute | Frozen `NumericalSpecification-v1`; numerical stability only |
| Pressure / stress | $|P_j-P_{\rm ref}|\le0.1$ kbar and $\max_{ab}|\sigma_{ab,j}-\sigma_{ab,\rm ref}|\le0.1$ kbar | Highest retained setting; absolute | Proposed engineering criterion aligned with later stress-sensitive EOS work; not a pressure-accuracy validation claim |
| Fixed diagnostic eigenvalue | for $n\in\{4,5\}$ and the three declared points, $\max|\widetilde\epsilon_{n\mathbf k,j}-\widetilde\epsilon_{n\mathbf k,\rm ref}|\le1$ meV | Highest retained setting; absolute after per-calculation $\epsilon_{4\Gamma}$ alignment | Proposed use of the specification's 1 meV band-energy scale for limited probes; not a full-band criterion |
| Fixed diagnostic gap | $|g_j-g_{\rm ref}|\le1$ meV for each of $g_\Gamma,g_X,g_{\Delta_{0.85}},g_{\Gamma X},g_{\Gamma\Delta}$ | Highest retained setting; absolute; gaps are shift-invariant | Consistent with the frozen indirect-gap numerical scale but does not establish the true indirect gap |
| SCF residual | final QE-reported estimated SCF accuracy $\le10^{-10}$ Ry and `conv_thr=1e-10 Ry` reached without exhausting `electron_maxstep` | Fixed zero target; absolute | Inner-solver error is kept well below outer energy and meV diagnostics; exact code quantity is retained |
| Any retained band-edge quantity | absolute change $\le1$ meV for energies; no valley position or effective mass is accepted in this Task | Highest retained setting; absolute | Prevents total-energy-only acceptance without converting later gap/mass targets into cutoff tolerances |

All criteria must pass for both cross-checks. Relative criteria are not used
where a quantity may cross zero. Project effective-mass, valley-position, and
parent-model gap targets remain separate and are not silently converted into
cutoff tolerances.

## Planned diagnostic outputs

The Task will later produce, but does not now implement:

1. total-energy difference per atom versus $E_{\mathrm{cut}}^\psi$;
2. pressure and stress summary versus $E_{\mathrm{cut}}^\psi$;
3. fixed diagnostic eigenvalue differences versus cutoff;
4. total-energy difference per atom versus SCF mesh density ($n^3$ and dimensions stated);
5. pressure and stress summary versus mesh density;
6. fixed diagnostic eigenvalue differences versus mesh density;
7. SCF iterations and wall time versus numerical resolution; and
8. a compact table marking provisional settings and cross-checks.

Every plot identifies source calculations, axes and units, comparison reference,
and accepted criterion when one exists. Captions state “numerical convergence
diagnostic” and make no physical-validation claim.

## Human decision table

No row is normalized until the human responds.

| Decision | Candidate values | Recommendation | Consequence |
|---|---|---|---|
| Frozen pseudopotential identity | Exact maintained authority table above; no alternative family | Use only that identity if both digests, metadata, license evidence, and compatibility preflight are complete; otherwise stop | Determines all production calculations |
| Preliminary lattice | Repository-supported tutorial diamond geometry: $a_0=10.20$ bohr; or a separately identified human-supplied preliminary PBE value | Tutorial geometry, explicitly provisional | Fixed cell/ions during convergence; not final EOS acceptance |
| $E_{\mathrm{cut}}^\psi$ trial set | `30, 36, 42, 48, 54, 60 Ry`; revise only with source-backed reason | Use the six-value ordered set | Six primary cutoff SCFs plus diagnostics |
| $E_{\mathrm{cut}}^\rho$ rule | ratios 4; or 4, 6, 8 refinement if density sensitivity controls | Start at 4 explicitly | Six primary values; optional bounded ratio refinement only if triggered |
| Preliminary SCF mesh | $8\times8\times8$ shift $(1,1,1)$; alternatives from the mesh sequence | $8\times8\times8$ shift $(1,1,1)$ | Held fixed during cutoff scan |
| SCF mesh sequence | $6^3,8^3,10^3,12^3$, all shift $(1,1,1)$; revised explicitly shifted or Gamma-centered family | Use the four shifted meshes | Three additional mesh SCFs plus diagnostics; reuse the Stage-2 K8 case |
| Occupation policy | fixed occupations/no smearing; or a separately justified smearing branch | Fixed occupations/no smearing | Insulating parent; avoids an added smearing axis |
| SCF threshold | `1e-10 Ry` or `1e-12 Ry` with the same max-step rule | `1e-10 Ry` | Inner-solver cost and residual floor |
| Monitored observables | Full list above; or human-specified additions without embedding path/valley studies | Full list including three fixed-point probes | Defines retained convergence evidence |
| Convergence criteria | Per-observable table above; human may revise named values/rationale | Use the proposed table | Numerical acceptance boundary only |
| Cross-check cases | Four corners $(E_*,K_*)$, $(E_*,K_+)$, $(E_+,K_*)$, $(E_+,K_+)$; expanded grid only after material coupling | Use the bounded four-corner check and mixed-difference diagnostic | Zero to two additional SCFs plus diagnostics after exact-case reuse |
| Resource ceiling | One local process; at most 2 GiB peak RSS; at most 30 min and 0.25 GiB new disk per SCF, 10 min and 0.05 GiB per diagnostic; at most 8 process-hours and 2 GiB retained scratch for at most 11 unique SCF/diagnostic pairs; stop before exceeding | Use this conservative primitive-cell ceiling, subject to executable-preflight timing/memory estimate and scratch-retention confirmation | Protected execution limit; no execution is authorized by accepting design |

## Execution exclusions and claim limits

This design runs no QE or Wannier90 executable, downloads no pseudopotential,
modifies no external artifact, and implements no plotting or analysis code. It
selects no final parameter, accepts no EOS lattice, activates no SCF successor,
and creates no checkpoint. Human acceptance of the design authorizes only the
explicit preflight option below; calculation execution still requires a new
exact protected-execution authorization after executable, inputs, scale,
outputs, runtime, and resources are reported.

The possible response is:

- **A — Accept the recommended convergence design and authorize execution preflight only.**
- **B — Revise specified parameters or criteria.**
- **C — Defer production convergence.**

Agreement among retained calculations would establish only numerical stability
for the stated PBE Kohn--Sham parent, provisional geometry, observables, and
finite tested domain. It would not establish an infinite-basis result,
scientific validation, experimental agreement, valley curvature, effective
masses, Wannier fidelity, or reduction accuracy.
