# Parent projection and loss design

## Status

This document records a disclosed exploratory design calculation over the already
retained periodic-2D donor. It selects prospective source-acceptance tolerances, the
projected coefficient values and energy shift, one common coefficient box, and one
positive nonuniform spectral-weight formula.

It is not an experiment run, immutable `.v1` input, retained result, separation
certificate, threshold study, scientific validation, or publication evidence. The
calculation did not execute Quantum ESPRESSO, Wannier90, or another external calculator.
No threshold, witness, admissible-set distance, or desired hierarchy transition was
inspected when selecting the box and weights.

## Inputs and arithmetic

The calculation uses the donor bytes and SHA-256 identities recorded in
[`protocol.md`](protocol.md), selects the `lambda_xy = 0.30` coupling-continuation
member, and reconstructs the exact operations and orbits in
[`orbit-support-inventory.md`](orbit-support-inventory.md).

Two local reconstruction paths were compared:

1. binary64 complex arithmetic with NumPy arrays and direct ordered Fourier sums; and
2. an 80-decimal-digit `mpmath` reconstruction from the JSON decimal tokens, using
   componentwise high-precision sums.

The high-precision path is a design cross-check of the reported scale; it does not turn
the binary64 donor into exact or interval evidence.

## Observed donor defects

All values below are energy-valued multiples of the declared $E_G=1$ unless stated
otherwise.

| Diagnostic | Observed maximum |
|---|---:|
| Hermiticity, $|t(R)-t(-R)^*|$ | `0.0` |
| Imaginary magnitude | `4.213700197059214e-16` |
| `reflect-y-axis` coefficient defect | `6.065621969995901e-16` |
| `reflect-x-axis` coefficient defect | `5.903592004042323e-16` |
| `rotate-180` coefficient defect | `8.427400394118428e-16` |
| `reflect-main-diagonal` coefficient defect | `6.577507398386017e-16` |
| `rotate-90-counterclockwise` coefficient defect | `8.546405214357388e-16` |
| `rotate-90-clockwise` coefficient defect | `8.546405214357388e-16` |
| `reflect-antidiagonal` coefficient defect | `6.528845821225595e-16` |
| Complex block adjustment under real orbit projection | `5.128169732720652e-16` |
| Real block adjustment under orbit projection | `4.3775168286892634e-16` |
| Raw hopping reconstruction versus retained source-mesh energies | `4.440892098500626e-16` |
| Raw reconstructed-band imaginary magnitude | `8.344541047370254e-18` |
| Projected hopping reconstruction versus retained source-mesh energies | `1.0796918914479647e-14` |
| Projected versus raw reconstructed band | `1.05748743611185e-14` |
| Projected reconstructed-band imaginary magnitude | `1.2648667294420152e-19` |

The high-precision reconstruction gave maximum supplied-operation defect
`8.546405226559894796352897e-16`, projection adjustment
`5.12816970021883625417914e-16`, and projected-band discrepancy
`1.076995260226752470652391e-14`. These values corroborate the binary64 scale but are
not certified enclosures.

## Selected prospective source tolerances

The first version will carry separate fields with the following selected values:

| Control | Selected absolute tolerance |
|---|---:|
| `source_hermiticity_absolute` | `1.0e-12 * E_G` |
| `source_imaginary_absolute` | `1.0e-12 * E_G` |
| `source_symmetry_absolute` | `1.0e-12 * E_G` |
| `orbit_projection_adjustment_absolute` | `1.0e-12 * E_G` |
| `source_mesh_reconstruction_absolute` | `1.0e-12 * E_G` |
| `projected_mesh_reconstruction_absolute` | `1.0e-12 * E_G` |
| `energy_zero_correlation_absolute` | `1.0e-12 * E_G` |

The controls remain semantically separate even though they currently share a numerical
value. They all govern reconstruction of one fixed binary64, energy-valued donor with
$E_G=1$; the common value is selected as a conservative source-admission scale above
the disclosed observed defects. A future change to one field does not implicitly change
the others.

These are numerical source-consistency tolerances, not uncertainties, physical error
bars, or evidence that the finite parent is scientifically adequate.

## Selected projection and energy zero

For orbit $o$, the unshifted real coefficient is

$$
\widetilde\theta_o=
\frac{1}{|o|}\sum_{R\in o}\operatorname{Re}t(R).
$$

The common energy shift is the projected onsite coefficient

$$
\Delta E=\widetilde\theta_0=-0.08796825852205918\,E_G.
$$

For a complete odd uniform mesh, this onsite value is mathematically the projected-band
mesh average. The binary64 projected mesh average was
`-0.08796825852205917`; the binary64 difference from the selected shift was
`1.3877787807814457e-17`. The 80-digit reconstruction from JSON tokens gave a difference
of `-2.911362217726392010242942e-18`.

The shifted target is defined by exact protocol assignment, not by subtracting two
nearly equal binary64 numbers:

$$
\theta_0^\star=0,
\qquad
\theta_o^\star=\widetilde\theta_o\quad(o>0).
$$

The same $\Delta E$ is subtracted from every source and withheld energy compared with
this target. It is never fitted separately by a channel.

## Selected 36 target coefficients

The values are decimal round-trip encodings of the binary64 orbit averages. The
canonical input builder and independent verifier must reproduce them from the copied raw
blocks; this table is not a substitute for that reconstruction.

| Index | Representative | Multiplicity | Unshifted coefficient | Shifted target coefficient |
|---:|---:|---:|---:|---:|
| 0 | `(0, 0)` | 1 | `-0.087968258522059181` | `0.0` |
| 1 | `(1, 0)` | 4 | `-0.028565320408499122` | `-0.028565320408499122` |
| 2 | `(1, 1)` | 4 | `0.00090935978446203883` | `0.00090935978446203883` |
| 3 | `(2, 0)` | 4 | `0.0030227330526022113` | `0.0030227330526022113` |
| 4 | `(2, 1)` | 8 | `-0.00022349781143431621` | `-0.00022349781143431621` |
| 5 | `(2, 2)` | 4 | `0.000060049158784476284` | `0.000060049158784476284` |
| 6 | `(3, 0)` | 4 | `-0.00052709900473655734` | `-0.00052709900473655734` |
| 7 | `(3, 1)` | 8 | `0.000062150284354422217` | `0.000062150284354422217` |
| 8 | `(3, 2)` | 8 | `-0.000018066516750956092` | `-0.000018066516750956092` |
| 9 | `(4, 0)` | 4 | `0.00011228749664266875` | `0.00011228749664266875` |
| 10 | `(4, 1)` | 8 | `-0.000018258295747484466` | `-0.000018258295747484466` |
| 11 | `(3, 3)` | 4 | `0.0000057791272337414904` | `0.0000057791272337414904` |
| 12 | `(4, 2)` | 8 | `0.0000057059467149575162` | `0.0000057059467149575162` |
| 13 | `(4, 3)` | 8 | `-0.0000019249370970545373` | `-0.0000019249370970545373` |
| 14 | `(5, 0)` | 4 | `-0.000026656081943615559` | `-0.000026656081943615559` |
| 15 | `(5, 1)` | 8 | `0.0000055237836171784391` | `0.0000055237836171784391` |
| 16 | `(5, 2)` | 8 | `-0.0000018447459814463958` | `-0.0000018447459814463958` |
| 17 | `(4, 4)` | 4 | `0.00000067023392877227053` | `0.00000067023392877227053` |
| 18 | `(5, 3)` | 8 | `0.000000652613970493102` | `0.000000652613970493102` |
| 19 | `(6, 0)` | 4 | `0.0000066633852144708397` | `0.0000066633852144708397` |
| 20 | `(6, 1)` | 8 | `-0.0000016623470277655575` | `-0.0000016623470277655575` |
| 21 | `(6, 2)` | 8 | `0.00000058810706366760027` | `0.00000058810706366760027` |
| 22 | `(5, 4)` | 8 | `-0.00000023617378983849402` | `-0.00000023617378983849402` |
| 23 | `(6, 3)` | 8 | `-0.00000021666505546404555` | `-0.00000021666505546404555` |
| 24 | `(7, 0)` | 4 | `-0.0000013169618637739095` | `-0.0000013169618637739095` |
| 25 | `(5, 5)` | 4 | `0.000000086008384011392198` | `0.000000086008384011392198` |
| 26 | `(7, 1)` | 8 | `0.0000003684876493498554` | `0.0000003684876493498554` |
| 27 | `(6, 4)` | 8 | `0.000000080985697654627978` | `0.000000080985697654627978` |
| 28 | `(7, 2)` | 8 | `-0.00000013537866728348236` | `-0.00000013537866728348236` |
| 29 | `(7, 3)` | 8 | `0.000000051194014650997786` | `0.000000051194014650997786` |
| 30 | `(6, 5)` | 8 | `-0.000000030303317965373213` | `-0.000000030303317965373213` |
| 31 | `(7, 4)` | 8 | `-0.000000019531036176134721` | `-0.000000019531036176134721` |
| 32 | `(6, 6)` | 4 | `0.000000010913630900481291` | `0.000000010913630900481291` |
| 33 | `(7, 5)` | 8 | `0.0000000074325725415682855` | `0.0000000074325725415682855` |
| 34 | `(7, 6)` | 8 | `-0.0000000027131012073695122` | `-0.0000000027131012073695122` |
| 35 | `(7, 7)` | 4 | `0.00000000067999586800877085` | `0.00000000067999586800877085` |

## Selected common coefficient box

Every support class uses the restriction of one zero-centered box in the common
36-coordinate space. Define

$$
B=4\max_o|\theta_o^\star|
 =0.11426128163399648E_G,
$$

and

$$
\mathcal B=[-B,B]^{36}.
$$

The maximum target magnitude is the `(1, 0)` coefficient. The minimum target-to-boundary
margin is therefore

```text
0.08569596122549736 * E_G
```

or three times that maximum target magnitude. The multiplier `4.0` is selected before
threshold or distance inspection. A common global bound avoids encoding the target's
decay profile as coordinate-specific prior information. The box supplies numerical
compactness; it is not a physical hopping bound or uncertainty interval.

Inactive coordinates remain fixed to exact zero in addition to the box. The producer
and verifier must check target containment and every returned point's box membership.
Full-ellipsoid support cannot be treated as box-clipped support; containment of each
required support point remains a separate premise.

## Selected spectral weights

For each reduced source-mesh point $(k_x,k_y)$, select

$$
w(k_x,k_y)=
1+\frac{3}{4}\left[2+\cos(2\pi k_x)+\cos(2\pi k_y)\right].
$$

Properties fixed by this choice are:

- exact-arithmetic square signed-permutation symmetry and reciprocal periodicity;
- theoretical range $1\le w\le4$, so every objective-construction point remains active;
- increased emphasis near $\Gamma$ without selecting weights from hierarchy outcomes;
- nonuniformity, preventing the intended spectral loss from collapsing to the
  equal-block operator loss through equal-weight finite Parseval equivalence; and
- one raw weight per source-mesh point, normalized only by $\sum_iw_i$ in the declared
  loss.

On the selected $15\times15$ half-open mesh, binary64 evaluation gave:

| Diagnostic | Value |
|---|---:|
| Minimum sampled weight | `1.0327785988992915` |
| Maximum sampled weight | `4.0` |
| Weight sum | `562.5` |
| Number of distinct binary64 values | `36` |

Weighted design-rank diagnostics were:

| Support limit | Active dimension | Weighted design rank | Binary64 condition number |
|---:|---:|---:|---:|
| 0 | 1 | 1 | `1.0` |
| 1 | 2 | 2 | `2.15713403748754` |
| 2 | 3 | 3 | `2.461394091726753` |
| 4 | 4 | 4 | `2.502285948598418` |
| 8 | 6 | 6 | `3.229258891591702` |
| 18 | 12 | 12 | `3.511991020728635` |
| 50 | 27 | 27 | `3.7121856670415445` |
| 98 | 36 | 36 | `3.802258336035609` |

These rank and condition values are exploratory design diagnostics, not retained
numerical results or proof of downstream solver accuracy. The canonical input will store
the exact ordered binary64 weights as well as the formula identity; producer and verifier
must reconstruct their correlation independently.

## Threshold-design boundary

No spectral threshold, operator threshold, separation resolution, witness, support
direction, or expected critical class was calculated while selecting the controls on
this page. After the arbitrary-dimensional box-quadratic owner capability became
available and was bound, a separately disclosed
[`threshold-design.md`](threshold-design.md) study inspected objective-construction
geometry and selected prospective thresholds and resolution. That later study is
explicitly outcome-informed design provenance rather than a blind experiment result.

The projection, energy shift, box rule, multiplier, spectral-weight formula, supports,
and sample roles were not changed after threshold or hierarchy inspection. Any future
change to them would create a new disclosed design iteration rather than a silent edit.
