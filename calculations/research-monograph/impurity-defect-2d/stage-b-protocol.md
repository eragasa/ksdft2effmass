# Superseded Stage B protocol: scalar onsite extraction and D4 covariance

## Status and claim boundary

This single-route design was accepted for execution-free implementation by the
human response ``continue``. Implementation then exposed the twist-gauge
incompatibility documented in `stage-b-implementation-blocker.md`. The later
HC04 decision adopted `stage-b-multiroute-protocol.md`. This document is retained
as historical negative evidence and must not be implemented or executed.
No Stage B calculation execution is authorized, and no Stage B result exists.

The proposed evidence is synthetic software and numerical verification for one
finite scalar represented operator. It does not test directional or nonlocal
defects, finite-size convergence, composite bands, spin, DFT, Wannier90,
materials, scientific validation, or uncertainty quantification. The
human-accepted Stage A result and its scalar parent are immutable prerequisites
and are not rerun.

## Frozen represented problem

Stage B uses the isotropic separable scalar parent at
$(\lambda_x,\lambda_y,\lambda_{xy})=(0.5,0.5,0)$, truncated to
$R_x^2+R_y^2\leq18$, on an $8\times8$ periodic supercell. Sites are integer
pairs $s=(x,y)$ with $0\leq x,y<8$, ordered with $x$ outer and $y$ inner. The
represented space is $\mathbb C^{64}$, the energy unit is $E_G$, and twists are
measured in turns.

The two plants are single-site scalar onsite operators,

$$
\Delta_p=-0.25\,|p\rangle\langle p|,
$$

at the central site $p=(0,0)$ and the off-axis site $p=(1,2)$. The central case
tests extraction at a fixed point of the point group. The off-axis case owns the
full eight-element orbit test; it is used because its listed $D_4$ orbit has no
stabilizer duplication on the chosen cell.

## Exact D4 action

Coordinates are column vectors. Each integer orthogonal matrix $M$ acts first,
and coordinates are reduced modulo eight only afterward. The represented
permutation satisfies

$$
U_M|s\rangle=|Ms\bmod8\rangle.
$$

The same matrix maps a twist to $M\phi\bmod1$, with components reduced to
$[0,1)$. `stage-b-design.json` fixes the operation order, all eight matrices,
and the expected orbit

$$
(1,2),(6,1),(7,6),(2,7),(1,6),(7,2),(2,1),(6,7).
$$

Before any defect calculation, an implementation must verify matrix
orthogonality, group closure, exact permutation unitarity, composition
agreement, and exact orbit identity. These checks prevent an internally
consistent but differently named point-group convention from passing.

## Known-map extraction

For each canonical pristine-defect pair, the candidate representation applies
the antidiagonal reflection, then translation by $(2,3)$, then a source-site
phase,

$$
G|x,y\rangle
 =e^{i(0.137x-0.191y)}
  |M(x,y)+(2,3)\bmod8\rangle,
$$

and adds the scalar reference shift $c=0.137E_G$. The candidate twist is
$M\phi\bmod1$. The source-site phase convention is part of the contract; a
target-site convention is a distinct, invalid map.

The known inverse removes $cI$, phases, translation, and point-group action in
reverse order before subtraction. Two central cases use the frozen Gamma and
generic twists. Sixteen off-axis cases use base twist outer and the accepted
$D_4$ order inner. Every record retains compact support, full-matrix identities,
map metadata, recovery defects, onsite-class residual, and support and amplitude
checks.

The known-map route receives the authored map and shift by definition. It does
not establish that those quantities are inferable from the host.

## Covariance and the boundary-twist trap

For every off-axis operation, the extracted defect must obey

$$
\Delta_{Mp,M\phi}
 =U_M\Delta_{p,\phi}U_M^\dagger.
$$

Because a scalar onsite plant is independent of boundary twist, this equation
alone cannot verify twist transformation: it would also pass if a generic twist
were incorrectly held fixed. Stage B therefore separately checks the full
pristine-defect Hamiltonian,

$$
H_{\mathrm{def}}(M\phi,Mp)
 =U_M H_{\mathrm{def}}(\phi,p)U_M^\dagger.
$$

The negative quarter-turn control deliberately retains the original generic
twist. Its maximum-entry mismatch must exceed $10^{-6}E_G$. If it does not, the
control is nondiscriminating and Stage B fails; neither the twist nor the floor
is tuned after inspection. Symmetry-related spectra are retained as a
supplementary check, not as an oracle for operator covariance.

## Blind alignment is an identifiability control

The blind route receives the two Hamiltonians, geometry and twist metadata, the
parent hopping graph, the search group, and tolerances. It does not receive the
plant, authored map, shift, or known-map errors.

For each point-group operation compatible with the candidate twist within the
frozen absolute tolerance $10^{-14}$ and each periodic translation, site phases
are synchronized from ratios on nonzero off-diagonal parent edges with
$\theta(0,0)=0$. The frozen objective is the Frobenius mismatch over off-diagonal
site blocks. An onsite defect does not enter that objective.

This makes the absolute site map non-identifiable from the homogeneous host:

- at Gamma, all eight $D_4$ operations and all 64 translations are tied, giving
  512 candidates;
- at the generic twist, twist metadata identifies the authored point-group
  operation but all 64 translations remain tied.

The expected result is therefore
`DEFECT_2D.SITE_MAP_UNRESOLVED`, with the complete ordered ambiguity set but no
selected map and no extracted operator. This is intended negative evidence, not
an optimizer failure. Using the planted site or known-map error to select a
candidate is prohibited.

A shift diagnostic may still be retained for the tied candidates. It is the
median real aligned diagonal difference, which returns the common shift because
63 of 64 sites are unmodified. A trace mean is forbidden because it is biased by
the onsite plant. The shift diagnostic does not authorize subtraction after the
site-map stop.

## Adverse controls

Three independent adverse controls are retained:

1. **Pre-alignment subtraction.** Mismatched coordinate metadata returns
   `DEFECT_2D.SITE_MAP_UNRESOLVED` and no residual.
2. **Omitted energy correction.** After otherwise correct alignment, omitting
   $cI$ produces the known error $cI$, with maximum entry $0.137E_G$ and
   Frobenius norm $8c=1.096E_G$. This is a false extended term, not an impurity
   estimate.
3. **Fixed generic twist under a quarter turn.** The defect-only covariance can
   remain zero, but the full-Hamiltonian covariance must fail the declared
   discrimination floor.

A fourth software control inspects the blind input and callable boundary for
plant or known-map leakage before a nominal result can be interpreted.

## Criteria and failure disposition

Known-map Hermiticity, extraction, onsite projection, support, and amplitude
checks use the accepted absolute algebraic tolerance $10^{-11}$. Correct
covariance uses $10^{-10}$. Independent reconstruction compares retained values
with relative tolerance $10^{-10}$ and bounded absolute tolerances appropriate
to the same finite arithmetic.

The result owns a separate criterion disposition. If runner and verifier agree
that a frozen numerical criterion failed, the result is verified negative
evidence. A retained-value or reconstruction mismatch is a verification
failure. These outcomes must not be conflated.

Stage B does not run the full nested model hierarchy: every nominal plant is
already in the point-scalar-onsite class. Directional and nonlocal class
selection belongs to Stage C.

## Independent verification

A future verifier must not import the runner. It must independently reconstruct
the parent from retained hopping coefficients; generate $D_4$ matrices and
permutations from integer formulas; reconstruct the compact plants and attacked
operators; enumerate exact nominal and blind inventories; implement separate
phase synchronization and median shift estimation; and reproduce covariance,
adverse controls, criteria, and matrix identities.

Execution authorization cannot be requested until execution-free toy tests
mutate operation order, orbit sites, phase convention, twist transformation,
shift estimator, blind information fields, ambiguity disposition, and
criterion status and demonstrate fail-closed behavior.

## Proposed resource envelope and outputs

The implementation may use only existing Python, NumPy, and SciPy dependencies.
The largest matrix is $64\times64$; at most 18 known-map cases and 512 blind
candidates per blind case are permitted. A future execution is bounded by 180
seconds, 2 GiB peak memory, 10 MiB retained output, no network access, and no
external executable.

Planned retained outputs are an exact result, independent verification log,
result-only deterministic figure, report, and checksum catalog. These are
planned artifacts, not completed evidence. Passing Stage B would require a
separate human acceptance and would not activate Stage C.
