# Three distinct two-dimensional Chern-band obstruction benchmarks

## Status

This is a calculated synthetic numerical-verification report. It implements the
human-selected combined Option E at
`RM-PERIODIC-2D-TOPOLOGICAL-MODEL-HC03`: Qi--Wu--Zhang, Hofstadter, and Haldane
are treated as three separate controlled benchmarks. They are not alternative
representations of one operator, their numerical errors are not combined, and
none is identified with the scalar continuum cosine parent.

## Question

Can three standard but structurally different finite-dimensional Bloch models
reproduce the numerical premises of a rank-one Chern obstruction: an isolated
band, a nonzero integer lattice Chern sum, and a Wilson-loop phase with nonzero
winding? Can declared trivial controls distinguish that result without changing
the diagnostic algorithm?

## Model contracts

All reciprocal coordinates are fractional torus coordinates $(u,v)\in[0,1)^2$.
The retained band is the lowest eigenvalue in every model.

### Qi--Wu--Zhang

The state space at each reciprocal point is $\mathbb C^2$, following the model
family introduced by [Qi, Wu, and Zhang
(2006)](https://doi.org/10.1103/PhysRevB.74.085308). With $k_x=2\pi u$ and
$k_y=2\pi v$,

$$
H_{\mathrm{QWZ}}(\mathbf k)
=\sin k_x\,\sigma_x+\sin k_y\,\sigma_y
 +(m+\cos k_x+\cos k_y)\sigma_z.
$$

Gap closings in this convention occur at $m=-2,0,2$. The topological case
$m=-1$ lies in the interval with lower-band Chern number $-1$, while the
$m=3$ control lies in the analytically trivial interval.

### Hofstadter flux $1/3$

The state space is $\mathbb C^3$ over the magnetic Brillouin torus, following
the rational-flux construction of [Hofstadter
(1976)](https://doi.org/10.1103/PhysRevB.14.2239). Its band Chern interpretation
uses the [Thouless--Kohmoto--Nightingale--den Nijs
construction](https://doi.org/10.1103/PhysRevLett.49.405). In Landau gauge,
orbitals $r=0,1,2$ have diagonal entries

$$
H_{rr}=-2t\cos(k_y+2\pi r/3)
       +\Delta\cos(2\pi r/3),
$$

with $t=1$. Adjacent magnetic-cell orbitals have hopping $-t$, and the boundary
hopping carries the magnetic Bloch phase $-t e^{i2\pi u}$. At $\Delta=0$, the
flux-$1/3$ Diophantine assignment gives the band tuple $(-1,+2,-1)$ in the
orientation used here. The $\Delta=4$ atomic-superlattice case is a declared
synthetic numerical negative control; no analytic transition threshold is
claimed for that finite value.

### Haldane

The state space is $\mathbb C^2$ in a periodic honeycomb Bravais-cell gauge,
following [Haldane (1988)](https://doi.org/10.1103/PhysRevLett.61.2015).
Writing $x=2\pi u$ and $y=2\pi v$, the off-diagonal element is
$t_1(1+e^{ix}+e^{iy})$, with $t_1=1$. The mass term is

$$
d_z=M-2t_2\sin\phi
 [\sin x-\sin y+\sin(y-x)],
$$

where $t_2=0.15$ and $\phi=\pi/2$. The analytic phase boundary is
$|M|=3\sqrt{3}|t_2\sin\phi|\simeq0.7794$. Thus $M=0$ is topological and the
$M=1$ control is trivial for the stated convention.

## Numerical method

Odd uniform meshes $N=21,31,51,81$ are evaluated independently for every case.
Normalized nearest-neighbor overlaps define Abelian link variables. Oriented
plaquette phases give the lattice Chern sum, and products of the horizontal
links give the Wilson phase as a function of transverse coordinate. The chosen
orientation yields Wilson winding $w=-C$ for the retained band.

A deterministic periodic phase attack is applied to every retained eigenvector.
The Chern sum and Wilson phases must remain unchanged. Projectors are also
compared at both reciprocal seams. The primary runner stops if a neighbor
overlap is smaller than $10^{-12}$.

The independent verifier does not import the runner. It reconstructs each Bloch
matrix and uses products and traces of rank-one projectors--Bargmann
invariants--rather than the runner's normalized eigenvector links. It separately
reconstructs all spectra, Chern sums, Wilson phases, windings, and seam
projectors.

## Calculated results

At $N=81$:

| Model and case | Minimum retained gap | Band Chern sums | Retained Wilson winding | Maximum plaquette phase |
|---|---:|---:|---:|---:|
| QWZ, topological | 2.0000 | $(-1,+1)$ | $+1$ | $3.01\times10^{-3}$ |
| QWZ, trivial | 2.0060 | $(0,0)$ | $0$ | $2.99\times10^{-3}$ |
| Hofstadter, topological | 1.2739 | $(-1,+2,-1)$ | $+1$ | $1.04\times10^{-2}$ |
| Hofstadter, trivial | 1.2685 | $(0,0,0)$ | $0$ | $3.43\times10^{-3}$ |
| Haldane, topological | 1.5588 | $(-1,+1)$ | $+1$ | $4.57\times10^{-3}$ |
| Haldane, trivial | 0.4412 | $(0,0)$ | $0$ | $4.91\times10^{-2}$ |

Every retained Chern sum is integer within $2.3\times10^{-16}$. The nonzero
integer and unit Wilson winding persist on all four meshes in every topological
case. Every trivial control has zero retained Chern sum and zero winding on all
four meshes. The maximum plaquette phase decreases with refinement in each
case.

A later separate $51^2$ phase sweep, retained in
`topological-phase-sweep-report.md`, recovers the analytic QWZ and Haldane phase
boundaries and numerically brackets the Hofstadter lower-band change between
$\Delta=1.8$ and $2.0$. The declared $\Delta=4$ control remains in the sampled
zero-Chern sector through $\Delta=12$; no exact Hofstadter critical value is
claimed.

The phase attack changes a Chern sum by at most $2.3\times10^{-16}$ and a Wilson
phase by at most $1.5\times10^{-15}$. Reciprocal-seam projector defects remain
below $1.9\times10^{-15}$. The independent projector-route verifier passes.

![Wilson flow, Chern convergence, gaps, and model-resolved band Chern sums.](topological-summary.png)

**Figure 1.** Three separately represented topological cases and their declared
trivial controls. A unit Wilson winding accompanies each nonzero retained-band
Chern integer. Model-specific gaps and curvature refinement remain separate.

## Interpretation and limitations

For each topological case, the calculated nonzero retained-band Chern integer
and Wilson winding establish the numerical hypotheses used by the standard
rank-one Wannier-obstruction theorem: no globally smooth periodic rank-one frame,
and therefore no translation-covariant exponentially localized orthonormal
Wannier basis for that isolated band. The finite computation does not prove the
general theorem; it evaluates its diagnostics for the three frozen models.

The result does not establish a topological phase of the scalar continuum cosine
model, does not compare the three models as approximations of one operator, and
does not combine their gap or discretization errors. It is not a material
calculation, a silicon claim, scientific validation, uncertainty quantification,
or evidence for interacting topology. The Hofstadter superlattice and the two
mass controls are declared synthetic negative controls.

## Reproduction

From `python/`:

```bash
uv run python \
  ../calculations/research-monograph/periodic-2d/run_topological.py \
  --input ../calculations/research-monograph/periodic-2d/topological-input.json \
  --output ../calculations/research-monograph/periodic-2d/topological-result.json

uv run python \
  ../calculations/research-monograph/periodic-2d/verify_topological.py \
  ../calculations/research-monograph/periodic-2d/topological-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-2d/plot_topological.py \
  ../calculations/research-monograph/periodic-2d/topological-result.json \
  --output ../calculations/research-monograph/periodic-2d/topological-summary.png
```
