# Bulk-Silicon Production Convergence Design

**Status:** Calculated finite-setting results awaiting human review. Task
[`bulk-silicon.production-reference.convergence`](../../harness/tasks/bulk-silicon.production-reference.convergence.json)
is active in phase `awaiting_human_review`. Human Option A authorized exactly the
committed 9-SCF and 9-NSCF primary campaign; all 18 invocations exited zero and
emitted `JOB DONE.` without retry. This does not accept a final cutoff, mesh,
lattice parameter, infinite-basis result, effective mass, or scientific
validation. Automatic successor activation is false. See the compact
[execution result](../../calculations/bulk-silicon/production-convergence-preflight/execution-result.md).

The prepared record is
[`execution-preflight.json`](../../calculations/bulk-silicon/production-convergence-preflight/execution-preflight.json).
All web sources below were accessed on **2026-08-13**. Literature values and
mathematical estimates are planning evidence, not project calculations.

## Authoritative context and artifact acquisition

The design starts at `origin/dev` revision
`7f2342ac07037549eb4351241ae1f5070a1d6b2c`. The frozen production artifact is
not the closed LDA tutorial artifact.

| Field | Verified production value |
|---|---|
| URL | `https://www.pseudo-dojo.org/pseudos/nc-sr-04_pbe_standard/Si.upf.gz` |
| Installed location | `~/opt/pseudodojo/1.0/pbe/nc-sr-04-standard/Si/` through the `user_opt` store |
| Compressed identity | `Si.upf.gz`, 61,592 bytes, SHA-256 `bfbd01ccd4b67584dcf19a490a76e9b688c25026775ce2f4a4b6a13f900dad81` |
| Decompressed identity | `Si.upf`, 225,602 bytes, SHA-256 `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282` |
| Metadata | UPF 2.0.1; ONCVPSP 3.3.0; PBE; norm-conserving; scalar-relativistic; four valence electrons |
| PseudoDojo hints | low/normal/high = 14/18/24 Ha = 28/36/48 Ry |

Both identities were recomputed after same-filesystem staged atomic publication.
The installed portable authority is:

```json
{
  "store": "user_opt",
  "relative_path": "pseudodojo/1.0/pbe/nc-sr-04-standard/Si/Si.upf",
  "version": "1.0",
  "sha256": "39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282"
}
```

`user_opt` resolves explicitly to canonical `~/opt`; traversal and symlink
escape are rejected as specified by
[`external-system-integration.md`](../architecture/external-system-integration.md).
The old production-input location was removed after verifying that it contained
no unrelated files. The campaign's `pseudo/Si.upf` has the same decompressed
identity but is a verified execution copy, not authority. No pseudopotential
bytes are committed.

The exact embedded text is:

```text
While it is not required under the terms of the GNU GPL, it is
suggested that you cite D. R. Hamann, Phys. Rev. B 88, 085117 (2013)
in any publication using these pseudopotentials.
```

The embedded statement identifies `GNU GPL` but gives no exact version or SPDX
identifier. No repository-level license declaration was found for the separate
PseudoDojo data repository inspected during preflight. This record makes no
legal conclusion: local execution use is prepared, while redistribution remains
unauthorized. Cite PseudoDojo, DOI `10.1016/j.cpc.2018.01.012`, and ONCVPSP, DOI
`10.1103/PhysRevB.88.085117`.

Static UPF inspection establishes metadata and byte identity, not readability by
`pw.x`. The first authorized SCF invocation is the readability test.
`pw2wannier90.x` compatibility remains later scope.

## Executable and workspace

The executable was inspected without invocation:

| Field | Value |
|---|---|
| Portable path | `~/projects/q-e-qe-7.2/build/bin/pw.x` |
| SHA-256 | `6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca` |
| Accepted version | Quantum ESPRESSO PWSCF 7.2 |
| File architecture | Mach-O 64-bit executable arm64 |

QE 7.2's retained `PW/Doc/INPUT_PW.html` has SHA-256
`766eed605095f9ff97d5a6ceaeed3daa4d691f22cf4b388883fa3ff02b1ade52`.
The external run-root descriptor is
`ksdft2effmass-runs/bulk-silicon-production-convergence-20260813T021128Z`, with
SHA-256 `9d84848b4abb0db89e70fa8f6af2dc5f94b122d9574397e60398986638b91bb5`
over that exact UTF-8 descriptor. At execution it is supplied explicitly,
canonicalized, and checked against that descriptor identity. Inputs,
pseudopotential copy, outputs, and one scratch tree per unique SCF case are
separated below that root.

## Claim-to-evidence map

| Decision | Candidate value | Evidence type | Source or derivation | Applicability | Limitation |
|---|---|---|---|---|---|
| Production functional | PBE | Primary literature and frozen specification | Perdew, Burke, Ernzerhof, DOI `10.1103/PhysRevLett.77.3865`; PBE definition | Defines the approximate XC parent used consistently with the UPF | Does not establish agreement with experiment |
| Pseudopotential method | PseudoDojo ONCV, exact identities above | Upstream metadata and primary literature | PseudoDojo FAQ/Si report; van Setten et al., DOI `10.1016/j.cpc.2018.01.012`; Hamann, DOI `10.1103/PhysRevB.88.085117` | Supports exact family metadata, ONCV construction, citations, and file-specific hints | Transferability and convergence for these observables remain to be tested |
| Cutoff sequence | 30, 36, 42, 48, 54, 60 Ry | Upstream hint plus conventional finite bracketing | PseudoDojo FAQ says low is a starting point, normal a safe quick guess, and high a convergence-testing setting; exact Si hints are 28/36/48 Ry | Brackets and extends normal/high hints with 6 Ry spacing | No source proves either endpoint converged; sequence is finite and conventional |
| Charge-density cutoff | `ecutrho=4*ecutwfc` | QE documentation | QE 7.2 `INPUT_PW`: default 4:1 and norm-conserving users should retain it; higher ratios may be tested for stress noise | Exact NC UPF and fixed-ratio primary scan | A later 4/6/8 ratio study is required if density/stress sensitivity controls |
| SCF meshes | shifted even $6^3,8^3,10^3,12^3$ | Primary method and QE semantics | Monkhorst--Pack, DOI `10.1103/PhysRevB.13.5188`; QE `K_POINTS automatic` documentation | Systematic refinement of one consistent quadrature family | The exact sizes are conventional candidates; shifted even sets are not literally nested |
| Preliminary mesh cutoff | 48 Ry | Upstream hint plus bounded reuse design | PseudoDojo high hint is 48 Ry; C48/K8 is reused | Gives an exact primary mesh series without claiming a final cutoff | Results may require repeating the mesh series at another selected cutoff |
| Provisional geometry | `ibrav=2`, `celldm(1)=10.20` bohr, two Si at 0 and $(1/4,1/4,1/4)$ | Retained local execution input and QE lattice semantics | Accepted QE tutorial input; QE `ibrav=2` definition | Holds a reproducible diamond primitive geometry fixed during candidate scans | Illustrative provisional geometry, not a PBE equilibrium estimate |
| Fixed occupations | no smearing | QE behavior and semiconductor context | QE `occupations='fixed'`; silicon band-edge sources Cardona--Pollak, DOI `10.1103/PhysRev.142.530`, and Jacoboni--Reggiani, DOI `10.1103/RevModPhys.55.645` | Closed-shell, non-spin-polarized primitive Si candidate | A calculation must still confirm insulating occupation behavior |
| Davidson | `diagonalization='david'` | QE documentation | QE 7.2 `INPUT_PW`: Davidson iterative diagonalization | Numerical eigensolver held fixed | Algorithm choice, not scientific evidence; observed stability controls suitability |
| Plain mixing | `mixing_mode='plain'` | QE documentation | QE 7.2 `INPUT_PW` mixing behavior | Numerical algorithm held fixed | Must be replaced or revised if observed SCF behavior is unstable |
| Mixing amplitude | `mixing_beta=0.7` | QE documented default/convention | QE 7.2 `INPUT_PW` default for ordinary SCF | Conventional candidate matching retained tutorial practice | Default status is not production justification; observed stability is required |
| Iteration ceiling | `electron_maxstep=100` | QE documentation | QE 7.2 `INPUT_PW` meaning | Failure ceiling preventing unbounded SCF iteration | Reaching it is failure, not convergence |
| Inner criterion | `conv_thr=1e-10 Ry` | Mathematical allocation and QE semantics | QE defines estimated-energy convergence threshold; $10^{-10}$ Ry is far below $10^{-5}$ Ry/atom outer energy change for a two-atom cell | Candidate inner-solver numerical criterion | QE's reported estimate is code-specific; passing it does not prove outer convergence |
| Processor count | one process | Operational reproducibility | Same executable/host retained tutorial measured one-process execution | Removes parallel decomposition as a campaign variable | Does not imply best performance |
| Stress criterion | 0.05 kbar | Linear-elastic derivation and literature planning bracket | $|\delta a|/a\simeq|\delta P|/(3B)$; silicon $B=85$--105 GPa planning range from Haas et al., DOI `10.1103/PhysRevB.79.085104`, and McSkimin--Andreatch, DOI `10.1063/1.1702821` | Provisional pressure/stress planning criterion for later EOS sensitivity | Literature bracket is not the project PBE curvature; replace it with fitted $B$ |
| Energy criterion | $10^{-5}$ Ry/atom | Internal contract plus finite-setting interpretation | `NumericalSpecification-v1`; compare adjacent retained settings and guards | Stability of the stated energy observable over tested candidates | Does not bound the infinite-basis error |
| Fixed-point band/gap criterion | 1 meV | Internal downstream scale plus difference-error logic | Aligned fixed-point energies and shift-invariant gaps; $|\delta(E_c-E_v)|\le|\delta E_c|+|\delta E_v|$ | Sensitivity at $\Gamma$, X, and nominal $\Delta_{0.85}$ only | Does not locate the valley, establish the true indirect gap, or converge an effective mass |
| Nominal $\Delta$ probe | `(0,0.85,0)` in `tpiba` | Silicon literature and QE coordinates | Cardona--Pollak; Jacoboni--Reggiani; QE `tpiba` definition | Reproducible sensitivity probe because `celldm(1)` is the conventional cubic $a$ and axes use QE fcc convention | Not a minimum search or curvature stencil |
| Four-corner interaction | mixed absolute difference $I_q$ below | Factorial contrast | NIST/SEMATECH two-factor interaction definition, stable URL below | Detects finite cutoff--mesh interaction in one tested rectangle | Small interaction does not prove global separability |
| EOS locator | $10^{-4}$ Å refinement target | Numerical-analysis boundary and EOS literature | Birch, DOI `10.1103/PhysRev.71.809`; Lejaeghere et al., DOI `10.1126/science.aad3000` | Later locator/grid refinement scale | Reported uncertainty must be no smaller than fit and numerical uncertainty |
| Resource reservation | 10 min/SCF, 5 min/NSCF, 2 GiB RAM, 2 GiB disk | Retained local measurement plus transparent scaling | Accepted QE 7.2 tutorial: 0.11 s wall, 544 KiB post-run scratch, 18 Ry, shifted $4^3$-equivalent list; planning proxy $(60/18)^{3/2}(12/4)^3\approx164$ | Conservative one-process local reservation; `/usr/bin/time -l` records RSS | Not a measurement of proposed PBE/ONCV cases; symmetry, FFTs, iteration count, and eight-band NSCF alter scaling |

## Mathematical interpretation of criteria

### Pressure and EOS resolution

For cubic hydrostatic strain, $V\propto a^3$ and
$B=-V\,\partial P/\partial V$, so to first order

$$
\frac{|\delta a|}{a}\approx\frac{|\delta P|}{3B}.
$$

With $a\approx5.40$ Å from the provisional 10.20-bohr geometry and the planning
range $B=85$--105 GPa, 0.1 kbar = 0.01 GPa gives

$$
|\delta a|\approx 5.40\ \text{Å}\frac{0.01}{3(85\text{--}105)}
=(1.7\text{--}2.1)\times10^{-4}\ \text{Å}.
$$

That is inconsistent with a nominal $10^{-4}$ Å EOS locator target. The revised
0.05-kbar criterion gives approximately $(0.86$--$1.06)\times10^{-4}$ Å and is
therefore a provisional planning criterion. The later EOS fit replaces the
literature $B$ bracket with its fitted PBE curvature.

The $10^{-4}$ Å value is only an EOS refinement target. Any lattice claim must
use

$$
\max\!\left(10^{-4}\ \text{Å},\sigma_{a,\mathrm{fit}},
\sigma_{a,\mathrm{numerical}}\right)
$$

or a more conservative explicitly justified combined uncertainty. Dense output
or optimizer precision does not establish physical or numerical knowledge at
that scale.

### Finite-setting stability

For any retained observable,

$$
|q_j-q_{j+1}|\le\tau
$$

demonstrates stability only between two finite settings. It does not bound

$$
|q_j-q_\infty|
$$

without an asymptotic error model, monotonicity result, variational argument, or
higher-resolution evidence. Results must therefore be phrased as observed
stability over the tested domain. Even shifted Monkhorst--Pack meshes are
systematically refined but are not literally nested point sets, so nonmonotone
quadrature changes remain possible.

### Fixed-point energies versus effective mass

The 1-meV criterion is retained only for aligned fixed-point band energies and
fixed-point gaps. It does not establish effective-mass convergence. For

$$
\frac{\partial^2E}{\partial k_i^2}\approx
\frac{E(\mathbf k_0+h\hat{\mathbf e}_i)-2E(\mathbf k_0)+
E(\mathbf k_0-h\hat{\mathbf e}_i)}{h^2},
\qquad
(m^{-1})_{ii}=\frac{1}{\hbar^2}\frac{\partial^2E}{\partial k_i^2},
$$

pointwise errors bounded by $\varepsilon_E$ imply the worst-case amplification

$$
|\delta E''|\lesssim\frac{4\varepsilon_E}{h^2}.
$$

Mass convergence therefore requires joint selection of $h$, stencil or fit,
energy-error scale, fit window, and conditioning assessment. Task
`bulk-silicon.band-edge-characterization.effective-mass-analysis` owns that
later decision.

### Cutoff--mesh interaction

After $E_*$ and $K_*$ are known, define next-higher guards $E_+$ and $K_+$ and

$$
I_q=\left|q(E_+,K_+)-q(E_+,K_*)-q(E_*,K_+)+q(E_*,K_*)\right|.
$$

This is the finite two-factor interaction within the tested rectangle. It must
be evaluated for each consequential observable. A small $I_q$ does not establish
global separability or an infinite-setting bound. Only parameterized templates
are prepared now; no four-corner runnable input exists before the four settings
are determined.

## Prepared primary matrix

All cases use the provisional 10.20-bohr geometry, exact Si UPF, PBE,
`ecutrho=4*ecutwfc`, fixed occupations, one process, Davidson, plain mixing,
`mixing_beta=0.7`, `electron_maxstep=100`, `conv_thr=1e-10 Ry`, and QE symmetry
and time reversal. Every primary SCF has a linked three-point, eight-band NSCF
at $\Gamma$, X, and nominal $\Delta_{0.85}$.

| Series | Cases | Fixed setting | Reuse |
|---|---|---|---|
| Cutoff | C30, C36, C42, C48, C54, C60 | shifted $8^3$ mesh | none within series |
| Mesh | K6, K8, K10, K12 | 48 Ry wavefunction cutoff | K8 is exactly C48 and is not rerun |

The prepared campaign therefore has **9 unique SCFs + 9 unique NSCFs = 18
`pw.x` invocations**, rather than 10 + 10. The finite sequences establish no
result until run and analyzed. If the cutoff evidence does not support using 48
Ry for the mesh study, execution must stop and return to Option B rather than
silently changing inputs.

Prepared repository paths are under
`calculations/bulk-silicon/production-convergence-preflight/inputs/`.
`K8.reuse.txt` records deterministic reuse. Parameterized, non-runnable later
four-corner templates are under `templates/`.

## Commands, outputs, and resources

The exact proposed command is:

```bash
KSD_PRODUCTION_CONVERGENCE_AUTHORIZATION='A-EXECUTE-COMMITTED-PRIMARY' \
KSD_BOUNDARY_COMMIT='<reported boundary commit>' \
KSD_REPOSITORY_ROOT='<clean checkout at that commit>' \
KSD_PRODUCTION_CONVERGENCE_ROOT="$HOME/projects/ksdft2effmass-runs/bulk-silicon-production-convergence-20260813T021128Z" \
KSD_QE_PW_X="$HOME/projects/q-e-qe-7.2/build/bin/pw.x" \
  "$KSD_PRODUCTION_CONVERGENCE_ROOT/run-primary.sh"
```

The script first fails with exit 77 unless the exact authorization token shown
above is supplied after a human Option A. It then requires the reported boundary
commit at both `HEAD` and `origin/dev`, a clean checkout, byte equality between
the executing runner and committed runner, canonical portable paths, installed
and run-copy pseudopotential identities, executable identity without a version
probe, run-root identity, and the ordered input manifest. It invokes the explicit
executable once per unique SCF and once per linked NSCF, preserves each SCF
native state, copies only that case's `.save` tree to an isolated `-diagnostic`
scratch directory before NSCF mutation, captures stdout separately, captures
`/usr/bin/time -l` plus stderr, and requires `JOB DONE.`. On the first nonzero
invocation or missing `JOB DONE.`, it exits immediately and attempts no later
invocation. It performs no four-corner calculation. The script has passed
`bash -n`; it has not been run.

Expected outputs per case are stdout, time/stderr, QEXSD, charge density, and
wavefunctions/restart state under the case-specific external scratch directory.
Compact post-execution records must retain iteration count, final QE estimated
accuracy, total energy/atom, full stress and pressure convention, fixed-point
bands/gaps, warnings, elapsed time, peak RSS, and disk use.

Retained local baseline evidence is the accepted one-process QE 7.2 tutorial
SCF: 0.11 s code-reported wall, six iterations, and 544 KiB post-run scratch at
18 Ry with a shifted $4^3$-equivalent ten-point irreducible list. A transparent
largest-case proxy is

$$
(60/18)^{3/2}(12/4)^3\approx164,
$$

using plane-wave count $\propto E_\mathrm{cut}^{3/2}$ and full-grid count
$\propto N^3$. It is not a benchmark law. Plan 0.5--2 minutes for a largest SCF,
below 1 minute for a diagnostic, and below 30 minutes for the campaign; reserve
10 minutes per SCF, 5 minutes per NSCF, 2.25 hours total, 2 GiB peak RSS, and
2 GiB total external storage. Peak baseline RSS was not retained, so 2 GiB is a
conservative operational reservation, not a measured prediction. The script
records peak RSS for every future invocation.

## Bibliography and exact claim boundary

| Source | Stable identity | Supported claim | Limitation |
|---|---|---|---|
| PseudoDojo FAQ | `https://www.pseudo-dojo.org/faq.html` | Hint units and qualitative low/normal/high meanings; required citations | Hints are not calculation-specific convergence |
| PseudoDojo Si report | `https://www.pseudo-dojo.org/pseudos/nc-sr-04_pbe_standard/Si.html` | Exact Si generator input/report context | HTML report does not establish QE 7.2 readability |
| PseudoDojo paper | DOI `10.1016/j.cpc.2018.01.012` | Library methodology, grading, citation | Library validation is not project-observable convergence |
| Hamann (2013) | DOI `10.1103/PhysRevB.88.085117` | ONCV construction and plane-wave optimization method | Does not select this campaign's final cutoff |
| QE input documentation | `https://www.quantum-espresso.org/Doc/INPUT_PW.html`; pinned local QE 7.2 copy identified above | Input semantics, defaults, algorithms, units | Online page is currently 7.5; pinned 7.2 local copy controls executable-specific semantics |
| Giannozzi et al. | DOI `10.1088/0953-8984/21/39/395502`; DOI `10.1088/1361-648X/aad1d0` | QE method and software context | Papers do not justify project-specific convergence settings |
| Monkhorst--Pack (1976) | DOI `10.1103/PhysRevB.13.5188` | Uniform special-point construction | Does not endorse $6^3$--$12^3$ for this case |
| Haas et al. (2009) | DOI `10.1103/PhysRevB.79.085104` | PBE solid structural/bulk-modulus scale | Different computational details; planning bracket only |
| McSkimin--Andreatch (1964) | DOI `10.1063/1.1702821` | Experimental silicon elastic scale | Experiment is not fitted PBE EOS curvature |
| Cardona--Pollak (1966) | DOI `10.1103/PhysRev.142.530` | Silicon $\Delta$ conduction-valley context | Conventional valley location is not a PBE result |
| Jacoboni--Reggiani (1983) | DOI `10.1103/RevModPhys.55.645` | Six-valley silicon band-edge context | Transport review does not define this numerical scan |
| Birch (1947) | DOI `10.1103/PhysRev.71.809` | Finite-strain/EOS relations | EOS form is not an uncertainty estimate |
| Lejaeghere et al. (2016) | DOI `10.1126/science.aad3000` | Whole-EOS numerical reproducibility context | Code-comparison protocol is not a $10^{-4}$ Å accuracy guarantee |
| NIST/SEMATECH factorial design | `https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm` | Two-factor interaction contrast | One rectangle cannot prove global separability |

## Ending boundary and human decision

No pseudopotential is redistributed, no final parameter or scientific result is
accepted, no checkpoint is created, and no successor is activated. The one
committed primary campaign has executed; no retry or follow-on calculation is
authorized. The Task remains active awaiting human review with automatic
successor activation false.
