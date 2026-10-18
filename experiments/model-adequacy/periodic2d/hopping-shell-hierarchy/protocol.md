# Prospective protocol: isotropic two-dimensional hopping-shell hierarchy

## Status

This is the maintained prospective protocol for

```text
ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy
```

It is not an immutable experiment version and has not been executed. The selected
controls below are reviewed development choices. They become immutable only when every
outcome-determining control is represented in a strict canonical input, exact dependency
and method identities are bound, independent verification is implemented, and a
content-addressed `.vN` identity is assigned before confirmatory execution.

## Scientific question

For one fixed finite scalar periodic parent, one weighted spectral objective, one
complete-block operator objective, and one pair of thresholds, determine the smallest
tested square-symmetric hopping-support class with a verified common witness. A smaller
class can be excluded only by direct channel emptiness or a reconstructed conservative
separation certificate.

Any result would be conditional on the exact parent, finite representation, symmetry
projection, coefficient box, weights, thresholds, metric, numerical policy, and sample
roles. It cannot establish a universal interaction range or material-model adequacy.

## Selected parent binding

The selected donor is the `lambda_xy = 0.30` member of the retained synthetic family

$$
H=-\nabla^2+0.5\cos x+0.5\cos y+0.30\cos x\cos y,
$$

with lattice period $a=2\pi$, reciprocal scale $G=1$, reciprocal energy scale $E_G=1$,
and one spinless scalar band. The donor coupling-continuation member uses plane-wave
cutoff 3, a $15\times15$ reciprocal transform mesh, and a $31\times31$ direct-parent
withheld mesh.

The current donor bytes are:

| Path | SHA-256 | Role |
|---|---|---|
| `calculations/research-monograph/periodic-2d/input.json` | `82e9915101e755f7cc77cb8901478f88d878ffaa808732036631b7ae5cfd78ec` | Parent controls and mesh/support inventory |
| `calculations/research-monograph/periodic-2d/result.json` | `4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6` | `lambda_xy = 0.30` source-mesh energies, 225 hopping coefficients, and aggregated 31-grid shell diagnostics; it does not retain all raw 31-grid energies |
| `calculations/research-monograph/periodic-2d/run_experiment.py` | `20f0f25f8e73578e0dbaa36e4e81d172c18c5042b9834158093d525a283cf3cc` | Donor computational procedure |
| `calculations/research-monograph/periodic-2d/SHA256SUMS` | `4f18c5f8d548374bdb74c865ba3aaa37ecdd44862ee5bc49e3747db9f28d1205` | Donor package checksum record |

These digests identify the selected development donor. The immutable experiment input
must copy every consumed compact value, retain source correlation, and carry its own
content digest; these paths are not a substitute for that input.

No parent calculation is rerun by this protocol work.

## Selected represented geometry

The maximal represented domain is

$$
\mathcal R_{\max}=\{-7,-6,\ldots,7\}^2,
\qquad |\mathcal R_{\max}|=225.
$$

The direct lattice basis is $(2\pi\mathbf e_x,2\pi\mathbf e_y)$ and reduced reciprocal
coordinates use the corresponding unit reciprocal basis. The Fourier convention is

$$
E_\theta(\mathbf k)=\sum_{\mathbf R\in\mathcal R_{\max}}
 t_\theta(\mathbf R)e^{+2\pi i\mathbf k\cdot\mathbf R}
 =\sum_o\theta_o\phi_o(\mathbf k),
\qquad
\phi_o(\mathbf k)=\sum_{\mathbf R\in o}
 e^{+2\pi i\mathbf k\cdot\mathbf R},
$$

with no additional normalization in forward evaluation. The finite inverse transform
that produced the donor hopping family remains separately provenance-bound.

The exact signed-permutation operations, canonical representatives, member order, 36
coefficient coordinates, multiplicities, and support prefixes are selected in
[`orbit-support-inventory.md`](orbit-support-inventory.md). That file is part of this
protocol, not an illustrative example.

## Selected symmetry projection

The future input builder must reconstruct all 225 donor blocks and retain the original
complex values before projection. It must independently measure:

- Hermiticity defect between $t(\mathbf R)$ and $t(-\mathbf R)^*$;
- maximum imaginary magnitude;
- supplied-operation coefficient defects for all eight selected operations; and
- source-mesh reconstruction defect under the declared Fourier convention.

Only after those defects pass separately selected numerical tolerances may the builder
replace each orbit by one real coefficient. The unshifted projection is

$$
\widetilde\theta_o=
\frac{1}{|o|}\sum_{\mathbf R\in o}\operatorname{Re}t(\mathbf R).
$$

The selected source-consistency fields are separate absolute tolerances of
`1.0e-12 * E_G` for Hermiticity, imaginary magnitude, supplied-operation symmetry,
orbit-projection adjustment, raw source-mesh reconstruction, projected source-mesh
reconstruction, and energy-zero correlation. Their disclosed design calculation and
observed defects are recorded in
[`projection-and-loss-design.md`](projection-and-loss-design.md).

The raw defects and projection adjustment remain evidence and cannot be erased by the
projection. The selected common shift is the projected onsite coefficient
`-0.08796825852205918 * E_G`, which is mathematically the complete-mesh average. The
shifted onsite target is assigned exact zero and all other projected orbit coefficients
are unchanged. The same shift is applied to source and withheld energies in both
channels; no channel-specific energy refit is admitted.

## Selected maximal coefficient space

The maximal parameter vector is the ordered tuple

$$
\theta=(\theta_0,\ldots,\theta_{35})\in\mathbb R^{36},
$$

where each coordinate has the donor energy unit and is repeated on every represented
block in its orbit. All candidate classes remain embedded in this same vector space.
An inactive coordinate is exactly zero; active coordinates are never reindexed or
renormalized by class.

The selected common coefficient box is

$$
\mathcal B=[-B,B]^{36},
\qquad
B=4\max_o|\theta_o^\star|
 =0.11426128163399648E_G.
$$

The minimum target-to-boundary margin is `0.08569596122549736 * E_G`. The global
zero-centered rule avoids encoding target decay as coordinate-specific prior
information and was selected before threshold or hierarchy inspection. Every class uses
the restriction of this same box and additionally fixes inactive coordinates to exact
zero; no class-specific bound rule is admitted.

## Selected nested support hierarchy

The ordered squared-radius limits are

```text
(0, 1, 2, 4, 8, 18, 50, 98)
```

For limit $S_k$, class $\mathcal M_k$ admits precisely orbit indices whose squared radius
is at most $S_k$ and fixes every later maximal-space coefficient to zero. The resulting
active coordinate and represented-block counts are:

| Class ID | Squared-radius limit | Active orbit indices | Active coefficients | Represented blocks |
|---|---:|---|---:|---:|
| `support-r2-000` | 0 | `0` | 1 | 1 |
| `support-r2-001` | 1 | `0..1` | 2 | 5 |
| `support-r2-002` | 2 | `0..2` | 3 | 9 |
| `support-r2-004` | 4 | `0..3` | 4 | 13 |
| `support-r2-008` | 8 | `0..5` | 6 | 25 |
| `support-r2-018` | 18 | `0..11` | 12 | 61 |
| `support-r2-050` | 50 | `0..26` | 27 | 161 |
| `support-r2-098` | 98 | `0..35` | 36 | 225 |

Every class is a strict prefix of the common orbit ordering, includes whole orbits,
preserves the selected square symmetry, and is nested in every later class. The complete
class contains the projected finite target by construction. Compatibility of an earlier
class is not assumed.

The represented-block counts agree with the donor's retained shell-study counts. That
agreement is a source-correlation check, not scientific validation and not a substitute
for independent reconstruction.

## Selected channel and metric semantics

The spectral and represented-operator losses remain the dimensionless quantities

$$
L_E(\theta)^2=
\frac{\sum_i w_i|E_\theta(\mathbf k_i)-E_{\mathrm{ref}}(\mathbf k_i)|^2}
{E_G^2\sum_i w_i},
$$

and

$$
L_H(\theta)^2=
\frac{\sum_o |o|\,|\theta_o-\theta_o^\star|^2}
{225E_G^2}.
$$

The operator channel therefore gives equal weight to every represented block, not every
free orbit, and compares all 225 target blocks for every class. Omitted target content
cannot disappear when a class fixes a coefficient to zero.

Every class uses the restriction of the same maximal-space metric

$$
d(\theta,\eta)=
\left[\frac{1}{225E_G^2}
\sum_o |o|\,|\theta_o-\eta_o|^2\right]^{1/2}.
$$

The selected nonuniform spectral weight is

$$
w(k_x,k_y)=
1+\frac{3}{4}\left[2+\cos(2\pi k_x)+\cos(2\pi k_y)\right].
$$

It is strictly positive, reciprocal-periodic, and square-symmetric, with theoretical
range `[1, 4]`. On the selected source mesh its binary64 range is
`[1.0327785988992915, 4.0]` and its sum is `562.5`. It emphasizes the neighborhood of
$\Gamma$ without selecting weights from hierarchy outcomes and avoids the equal-weight
finite-Parseval collapse into the operator channel. The exact ordered weights and their
formula identity must both be retained and independently correlated.

## Selected sample roles

The exact coordinate inventories, ordering, counts, disjointness proof, and diagnostic
semantics are recorded in [`sample-role-design.md`](sample-role-design.md).

- Objective construction uses all 225 points `(i/15, j/15)` for `i,j = -7,...,7` and is the only reciprocal role that defines the spectral quadratic or decisive evidence.
- Evaluation uses the 480 nonzero points `(i/31, j/31)` with even `i+j`.
- Withheld evaluation uses the complementary 480 points with odd `i+j` and is not inspected during protocol design.
- Locality diagnostics use the 225-block, 36-orbit maximal real-space inventory rather than another reciprocal mesh.

The two diagnostic reciprocal sets are equal-sized, mutually disjoint, disjoint from the
objective-construction mesh, and individually closed under the eight selected symmetry
operations. Evaluation, withheld, and locality values are calculated only after decisive
class evidence is fixed and cannot alter thresholds, witnesses, certificates,
dispositions, or the hierarchy conclusion.

The finite direct-parent comparator on diagnostic coordinates is reconstructed from the
selected plane-wave-cutoff-3 parent because the donor result retains only aggregated
31-grid errors, not every raw 31-grid energy.

## Selected prospective thresholds and resolution

The disclosed outcome-informed design study in
[`threshold-design.md`](threshold-design.md) selects the exact decimal controls

```text
spectral RMS threshold = 0.001004
operator RMS threshold = 0.00007310
separation resolution  = 0.000005
```

These are pedagogical controls for the fixed normalized losses and metric. They are not
physical tolerances, uncertainty bounds, or blind validation criteria. Evaluation,
withheld, and locality data were not inspected during their selection. The parent,
projection, box, weights, supports, and sample roles were selected earlier and remained
unchanged.

The exploratory objective-construction geometry suggests direct early-class emptiness,
a six-coordinate individually nonempty but separated class, and a 12-coordinate common
witness. Those are design expectations, not retained experiment results or conservative
certificates.

## Selected evidence semantics

For each support class:

- direct channel emptiness requires a conservative lower bound on the corresponding
  box-constrained quadratic minimum above its threshold;
- nonemptiness requires an explicit box-feasible point at or below threshold;
- compatibility requires one explicit common point satisfying both channels;
- a feasible pair supplies only an upper distance bound;
- certified separation requires a reconstructed conservative lower distance bound above
  the frozen resolution; and
- failed search or solver status alone establishes none of those claims.

A smaller unresolved class blocks any minimum-class conclusion. Passing software tests
will establish only implementation behavior within the tested contract.

## Owner capability status

The experiment will call reviewed owner contracts directly.

- PhysKit revision
  `projectkoios-physkit@7157dcedd0d220673d443c1c025e35a6fd1ffa7a` provides
  lattice, scalar hopping, Bloch evaluation, and supplied-operation diagnostics.
- Numerics provides finite Fourier arithmetic. The exact eight-operation orbit contract
  above is ready to drive a separate owner review; KSD will not add a generic orbit
  kernel first.
- Optimization's arbitrary-dimensional closed-box positive-definite quadratic minimizer
  is reviewed and live development is bound at
  `projectkoios-optimization@d38e00ceef7f0fb1c137d5c3450d210c1ae4c99f`; the
  experiment will consume it directly. The public minimizer contract is unchanged from
  the earlier revision used by the disclosed threshold-design calculation.
  Intersection-feasibility and strict-separation contracts follow separately.
- Interval or directed-rounding primitives remain Numerics-owned when the selected
  certificate requires them.

The [selected package execution graph](execution-structure.md) mirrors the existing
experiments through `definition.py`, `experiment.py`, `results.py`, `verify.py`, and
`serialization.py`, with no nested execution framework. Selecting those module
boundaries does not yet authorize source implementation, and no KSD facade is admitted.

## Controls still open before an immutable version

The following remain intentionally unresolved:

1. active-dimension quadratic acceptance and reconstruction tolerances;
2. intersection-witness and separation-certificate methods;
3. conservative arithmetic, precision, and rounding policy;
4. strict input/result schemas and canonical serialization;
5. producer-independent retained-evidence verification;
6. exact experiment method identities beyond the bound box minimizer; and
7. evidence retention, failure, and interpretation policy.

None may be selected from confirmatory outcomes. Exploratory threshold design, if used,
must be explicitly separated and retained before a new canonical confirmatory input is
sealed.

## Immutable-version gate

The family receives `.v1` only after all open controls are represented in strict
canonical input bytes, all owner contracts and software revisions are exact, producer
and independent verifier are qualified, and the evidence policy is reviewed. Changing
any outcome-determining control after that point creates a new experiment version.

This protocol authorizes no experiment execution, retained result, publication figure,
KSD commit, release, or material claim.
