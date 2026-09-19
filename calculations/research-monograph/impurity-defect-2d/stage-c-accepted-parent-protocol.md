# Proposed accepted-parent Stage C protocol

## Status and authority

HC11 authorized design and adversarial review only, and HC12 human-adopts this
protocol as the authoritative proposed accepted-parent Stage C contract. HC13
then authorized adversarial planning, execution-free implementation, and
adversarial implementation review with authored compact fixtures. The
implementation is complete at that bounded synthetic software-verification
boundary. The verbatim human response ``1`` resolves HC14, human-accepts that
exact execution-free boundary, and authorizes managed administrative closeout
only. HC15 records ``recommendation authorized`` and permits only the
execution-free accepted-artifact adapter, closed authorization/provenance
contracts, independent-verifier extension, maintained tests, and adversarial
review. HC16 separately records ``recommendation authorized`` for the instruction
``storage for all simulations should be in ~/projects/ksdft2effmass`` and binds
the expanded external native root `/Users/eugene/projects/ksdft2effmass` without
authorizing it to be populated. HC13--HC16 do not authorize an accepted-parent
read or calculation, external-root mutation, or Stage D. A later exact protected-
execution decision is reserved for HC17.

A future result would be controlled synthetic numerical verification. It would
not constitute DFT, production Wannier90, material transfer, silicon or dopant
validation, scientific validation, uncertainty quantification, publication, or
release evidence.

## Immutable parents and represented spaces

The calculation is bound to the accepted periodic input and result, the accepted
Stage A and Stage B results, and the human-accepted execution-free Stage C
contract by the SHA-256 identities in `stage-c-accepted-parent-design.json`.
Paths are canonical repository-relative paths beneath the repository root.

All finite defect matrices act on the scalar $8\times8$ site space of dimension
64, ordered with site $x$ outer and site $y$ inner. Units are $E_G=1$, $G=1$,
and $a=2\pi$; the energy reference is the identified periodic-parent zero. The
twist lifts are $(0,0)$ and $(0.37,-0.23)$ turns.

The isotropic parent $(\lambda_x,\lambda_y,\lambda_{xy})=(0.5,0.5,0)$ uses the
61 radius-18 hopping records retained in the accepted Stage B result. The
anisotropic control $(0.3,0.7,0)$ is reconstructed from the accepted periodic
input and anisotropy record at plane-wave cutoff 5 and reciprocal mesh
$15\times15$. Its complete mesh Fourier inventory, radius-18 truncation,
truncation residual, Hermiticity, and $D_2$ closure are retained separately.
The axis-swapped $(0.7,0.3,0)$ representation is identified separately and is
constructed only by swapping axes in the anisotropic compact inventory.

This anisotropic preprocessing does not revalidate or alter the accepted parent.
Its representation and truncation errors remain distinct from gauge and defect-
model errors.

## Defects and model hierarchy

At the aligned origin, the directional plant changes the positive-$x$ bond by
$+0.04E_G$ and the positive-$y$ bond by $-0.03E_G$. The diagonal nonlocal plant
changes the $(1,1)$ bond by $+0.025E_G$. Every plant includes its Hermitian
reverse.

Each recovered defect is fit, in order, to:

1. point scalar onsite;
2. finite-support diagonal onsite;
3. onsite plus isotropic nearest-neighbour;
4. onsite plus directional nearest-neighbour; and
5. finite-range nonlocal radius two.

Fits use real coefficients and stacked real and imaginary matrix entries. The
signed residual is recovered defect minus fitted model. The first class that
satisfies the maximum-entry, Frobenius, shell, and exact-support criteria is
retained as the selected class. The selector receives only the aligned recovered
defect, frozen bases, and tolerances; the planted expected class is evaluated
after selection. All five fit records remain in the result. Plant-aware
selection, changed class order, route or
schedule voting, and favorable averaging are forbidden.

## Routes, attack, and bridge

Route A constructs parent and defect matrices directly in the centered uniform-
link gauge from the unreduced twist lift. Route B independently constructs them
in the quotient seam gauge from the reduced twist. Route B may not consume
Route A matrices, caches, fit records, or diagnostics.

Both routes apply the known Stage B coordinate attack: reflection across the
antidiagonal, translation $(2,3)$ cells, source phase
$\theta(x,y)=0.137x-0.191y$, and energy shift $0.137E_G$. Each route inversely
aligns and corrects its own attacked candidate before subtraction.

The bridge is

$$
H_B(\phi\bmod1)=W(\phi)H_A(\phi)W(\phi)^\dagger,
\qquad
W_{x,y}(\phi)=
\exp\!\left[2\pi i\left(\frac{x\phi_x}{8}+\frac{y\phi_y}{8}\right)\right].
$$

It is checked separately for parent, defect, and attacked candidate matrices.
It is not an estimate, model vote, or authority to erase a route disagreement.

## Symmetry and axis-swap controls

For the isotropic parent, both full-Hamiltonian and recovered-defect covariance
are evaluated under all eight integer $D_4$ operations at the transformed
route-appropriate twist. For the anisotropic parent, covariance is evaluated
only under identity, half turn, reflection $x$, and reflection $y$. A diagonal
reflection is an axis-swap comparison to the separately identified
$(0.7,0.3,0)$ parent; it is not invariance of the $(0.3,0.7,0)$ parent. The
diagonal reflection is the single frozen representative of the $D_4/D_2$
axis-swap coset; composing it with the retained half turn gives the
antidiagonal reflection and does not add an independent case.

A fixed generic twist under quarter turn, a $D_4$ claim for the anisotropic
parent, and an axis-swapped defect without the swapped parent are retained as
separate adverse controls.

## Locality and inventories

Residual shells use the maximum periodic Chebyshev distance of either matrix
index from the aligned origin. Shells 0, 1, 2, and the exterior retain maximum
and Frobenius residuals. Core-exterior coupling and exact support identity are
also retained. Parent preprocessing, gauge bridge, alignment recovery, model
fit, and shell residuals are distinct quantities.

Per schedule there are 32 isotropic $D_4$ cases, 16 anisotropic $D_2$ cases, and
4 axis-swap cases. Each case has two matrix routes. Across two fresh spawned
schedule processes the result retains 208 route evaluations, 104 bridge records,
1,040 model-fit records, and 104 cross-schedule route comparisons. Each schedule
independently reconstructs the anisotropic hopping inventory, and the hopping
digests and preprocessing residuals must agree exactly. There is no
blind site inference in Stage C; the known attack is part of the control.
Canonical serialization order is independent of execution order.

## Criteria and failures

All matrices and diagnostics must be finite. Hopping Hermiticity and alignment
unitarity use $10^{-11}$ absolute criteria. Parent symmetry, recovered-defect
symmetry, axis swap, bridge, recovery, model-fit, and radius-two exterior
criteria use $10^{-10}E_G$. Clean schedule differences must be exactly zero.
Independent reconstruction uses a $10^{-10}$ relative criterion.

The wrong-isotropic and wrong-directional model residuals must each be at least
$0.03E_G$ in Frobenius norm. Omitting a reverse bond must produce at least
$0.03E_G$ Hermiticity defect. Raw gauge comparison must exceed $0.01E_G$;
fixed-twist covariance must exceed $10^{-6}E_G$; and the invalid anisotropic
$D_4$ and unswapped-parent controls must each exceed $10^{-3}E_G$.

A failed numerical criterion remains a retained reproduced failure. Route or
schedule disagreement is a software/protocol failure, not physical gauge or
order dependence. No result may be selected, ranked, averaged, or rerun because
another record is more favorable.

## Execution-free implementation and future authority

`run_stage_c_parent.py` implements the adopted dimensions, parent preprocessing,
routes, route-local attack and recovery, oriented bases, model selection,
locality records, bridges, schedules, adverse controls, and a closed adapter for
five separately identified parent records. Its maintained authored modes reject
accepted-parent status or consume only embedded synthetic records. The future
execution mode is present but fail-closed: before any semantic accepted-input
read, it requires repository root
`/Users/eugene/worktrees/ksdft2effmass-calculations`, Git revision
`9def2718ee763faf2060eb692739600485de5c72`, machine `minerva`, the exact existing
native root `/Users/eugene/projects/ksdft2effmass`, a resolved HC17-class decision,
ordered code/schema/input paths and SHA-256 identities, seven frozen compact
repository output paths, the exact operation inventory, declared resources, no
network, no external executable, no new dependency, one attempt, no retry, no
overwrite, and absent outputs. After this authority preflight and before the
first accepted-parent content hash/read, exclusive attempt-journal creation
consumes the authority. Every ordinary Python exception appends terminal FAILURE;
a process termination may leave STARTED, which still forbids retry. The future
authority path is frozen as
`stage-c-accepted-parent-execution-authorization.json` and its checkpoint as
`RM-IMPURITY-DEFECT-2D-STAGE-C-ACCEPTED-PARENT-EXECUTION-HC17`; the checkpoint
is pending and the executable authorization does not exist.

### Pre-attempt checksum prohibition

Before exclusive attempt-journal creation, no preparation or review command may
run an aggregate checksum catalog that contains any of the five accepted inputs.
Preparation checks must use an explicit safe-file allowlist and must not byte-
read, hash, or parse the accepted periodic input/result, Stage A result, Stage B
result, or execution-free Stage C contract. Their already-frozen identities are
copied into the pending question without re-observation. The protected Workflow
may validate those identities only after STARTED has durably consumed the sole
attempt. Its later package-specific checksum catalog covers only newly retained
Stage C products and never the accepted inputs.

The maintained original authored fixture contains a 61-term isotropic hopping
inventory and a $15\times15$ anisotropic energy grid. A second authored adapter
fixture embeds closed periodic-input, periodic-result, Stage A, Stage B, and
execution-free Stage C records; the accepted-artifact adapter converts these to
the same compact parents without opening the accepted files. Each fresh schedule
process independently reconstructs all 225 Fourier coefficients, applies the
radius-18 mask, and retains pretruncation, compact, swapped-parent, and
truncation identities and residuals. Both fixtures are synthetic test data and
are not surrogate accepted-parent results.

The closed result contains exactly 208 route evaluations, 104 bridge records,
1,040 fit records, and 104 cross-schedule comparisons. The selector receives no
expected-class identity. The authored behavior meets both predeclared
anisotropic adverse floors: invalid $D_4$ invariance and omission of the swapped
parent each produce $6.0\times10^{-3}E_G$, above the $10^{-3}E_G$ floor.
Spectral, bound-state, wavefunction, and physical-observable claims remain
outside Stage C acceptance.

## Independent verification and retention

The verifier may not import the runner or consume runner matrices or caches. It
reconstructs the isotropic parent from the 61 retained hoppings. It independently
recomputes anisotropic one-dimensional Bloch energies, explicit Fourier sums,
and the radius-18 mask. It assigns localized bonds directly in both gauges and
uses direct orthogonal projections where applicable or an independent QR fit;
normal equations are forbidden.

Every case identity, parent inventory, attack, energy correction, bridge,
symmetry relation, model fit, shell diagnostic, adverse control, criterion, and
schedule comparison is reconstructed. Verifier disagreement is distinct from a
reproduced numerical failure. For each execution-free authored fixture,
`verify_stage_c_parent.py` uses NumPy inverse Fourier transformation rather than
the runner's explicit coefficient sums, direct independent matrix construction,
and QR fits. It imports no runner. The original compact fixture reports a maximum
independent scalar metric difference of $1.922\times10^{-15}E_G$ across 208 route
records and 1,040 fits; the adapter fixture also reconstructs all records and
checks its five embedded input identities. A complete authored operation also
exercises exclusive attempt consumption, result serialization, independent log,
accepted-capable SVG, report, native evidence manifest, checksum finalization,
and terminal success/failure without accepted inputs. The verifier's dormant accepted mode
independently rebinds checkpoint, repository root and revision, machine, native root, code/schema/
input identities, attempt policy, compact output paths, result provenance, and
all numerical records. It cannot itself grant execution authority.

A future package is one append-only attempt journal, closed compact JSON result,
independent verification log, deterministic retained-data SVG, report, native-
evidence manifest, and package-specific checksum catalog under repository
`calculations/**`. Every output is exclusively created. The ordered Workflow
creates the attempt journal first and finalizes it last; no partial failure may
be replaced or rerun. Native simulation work is separately
bound to `/Users/eugene/projects/ksdft2effmass`; the accepted execution process
would use that directory as its working root while compact records remain in the
repository. Dense matrices are reconstructed from compact data and are not retained
in JSON. Existing evidence is never overwritten. Spectral, bound-state,
wavefunction, and physical-observable claims are not Stage C acceptance criteria
and remain proposed later evidence.

## Proposed resource envelope

The implementation uses local Python with existing dependencies, no network,
and no external executable. Matrix dimension is 64, with two schedules, 208
route evaluations, 104 bridges, and 1,040 model fits. A measured authored-fixture
run completed in 1.56 seconds with 99,041,280 bytes maximum resident set size and
a 2,205,921-byte JSON result. These values satisfy the proposed 600-second,
2-GiB, and 20-MiB envelope. They characterize synthetic implementation behavior,
not accepted-parent runtime or resource use. The runner observes runtime and peak
memory after computation and then rejects an over-limit result; it does not
proactively enforce a 600-second timeout or a 2-GiB operating-system sandbox.
HC17 must state this exact limitation unless hard enforcement is separately
implemented and reviewed.
