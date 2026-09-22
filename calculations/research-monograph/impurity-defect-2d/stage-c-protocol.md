# Stage C directional and nonlocal model-class protocol

## Status and boundary

HC09 authorizes execution-free design and implementation only, and HC10
human-accepts the resulting exact software package and authorizes managed
closeout. The maintained behavior uses authored toy coefficients and does not
read the accepted periodic parent. A toy pass is software verification of this
protocol, not an accepted-parent calculation, material validation, scientific
validation, or uncertainty quantification.

Stage B is frozen and is not rerun. Accepted-parent Stage C execution, Stages D
and E, DFT, production Wannier90, material transfer, publication, release,
deposit, and external transmission remain unauthorized.

## Represented space

The toy uses an $8\times8$ scalar site space of dimension 64, ordered with site
$x$ outer and site $y$ inner. Units are $E_G=1$, $G=1$, and $a=2\pi$; the
energy reference is the identified common parent zero. Only represented defect
matrices are constructed. No physical parent Hamiltonian is read.

Two twist lifts are retained: $(0,0)$ and $(0.37,-0.23)$ turns. Route A uses a
centred uniform-link gauge. Route B uses a reduced seam gauge. For the same
represented defect, the bridge is

$$
D_B(\phi)=W(\phi)D_A(\phi)W(\phi)^\dagger.
$$

The bridge is an equivalence relation, not an independent estimate or vote.
A-then-B and B-then-A are each evaluated in a fresh spawned process; any
schedule dependence is a software failure.

## Authored defects

The directional nearest-neighbour plant has an origin-to-positive-$x$ bond
change $+0.04E_G$ and an origin-to-positive-$y$ bond change $-0.03E_G$. The
finite-range nonlocal plant has an origin-to-$(1,1)$ bond change $+0.025E_G$.
Each bond includes its Hermitian reverse.

The frozen model-class order is:

1. point scalar onsite;
2. finite-support diagonal onsite;
3. onsite plus isotropic nearest-neighbour;
4. onsite plus directional nearest-neighbour; and
5. finite-range nonlocal radius two.

Every class is fit by real least squares over stacked real and imaginary matrix
entries. For each route and twist, select the first class whose maximum-entry
and Frobenius residuals are both at most $10^{-12}E_G$. The expected first
classes are directional nearest-neighbour and finite-range nonlocal radius two,
respectively. Route or schedule voting, favorable selection, and averaging are
forbidden.

## Operator and locality diagnostics

Before interpretation, each represented defect must be Hermitian within
$10^{-12}E_G$. The signed model residual is

$$
R = D_{\mathrm{represented}}-D_{\mathrm{fit}}.
$$

Maximum-entry and Frobenius residuals are retained separately. Shells use the
maximum periodic Chebyshev distance of either matrix index from the defect
origin. Shells 0, 1, 2, and the exterior are reported separately. The authored
radius-two exterior must be exactly zero.

Directional defects are not asserted to be $D_4$ invariant. At Gamma, the
protocol tests covariance of each oriented bond inventory under all eight
integer $D_4$ operations by comparing $U_MD U_M^\dagger$ with an independently
constructed transformed inventory. The maximum covariance defect must be at
most $10^{-12}E_G$.

## Adverse controls

The following outcomes must remain explicit:

- fitting the directional plant with the isotropic class has Frobenius residual
  at least $0.03E_G$;
- fitting the diagonal nonlocal plant with the directional class has Frobenius
  residual at least $0.03E_G$;
- omitting a Hermitian reverse produces Hermiticity defect at least
  $0.03E_G$; and
- comparing the generic-twist routes without the bridge produces maximum-entry
  difference at least $0.01E_G$.

These are model-class and representation controls. They are not parent-model,
numerical-discretization, or physical uncertainties.

## Independent verification

`verify_stage_c.py` must not import `run_stage_c.py`. It reconstructs all sixteen
route matrices directly, checks their canonical byte digests, evaluates the
bridge independently, verifies both schedule inventories, and compares all
model-fit Frobenius residuals with hand-derived analytical values. Its maximum
reconstruction difference must not exceed $10^{-11}E_G$.

`stage-c-toy-result.schema.json` is a closed Draft 2020-12 schema. Maintained
tests create toy output only in pytest-provided scratch space. No toy result is
retained as calculated scientific evidence.
