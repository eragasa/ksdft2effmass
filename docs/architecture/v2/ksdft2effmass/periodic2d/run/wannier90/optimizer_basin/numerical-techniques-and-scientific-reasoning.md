# Optimizer-basin numerical techniques and scientific reasoning

## Scope and claim status

This note explains the numerical design encoded by the row-052 optimizer-basin study
and the reasoning behind its retained negative convergence disposition. It documents
existing synthetic non-DFT evidence; it does not report a new calculation, rerun
Wannier90, authenticate the unavailable external native tree, or promote the compact
encoded documents into scientific oracles.

The study asks two bounded questions:

1. Do deterministic, smooth, reciprocal-periodic initial gauges repeatedly reach the
   same observed converged endpoint basin at fixed numerical controls?
2. Do both the best observed endpoint and the median across converged starts satisfy
   predeclared finest-pair mesh and cutoff stability gates?

The study does **not** ask whether a global optimum was found, whether Wannier90 is
generally convergent, or whether a material property is validated.

## Scientific decomposition

The numerical design keeps several sources of variation separate.

| Variation | Scientific/numerical role | What it does not establish |
|---|---|---|
| Initial gauge | Probes local-optimizer trajectory sensitivity inside one declared retained subspace | A probability distribution over all starts or exhaustive global search |
| Reciprocal mesh | Probes reciprocal sampling/discretization | Asymptotic convergence from four finite meshes |
| Plane-wave cutoff | Probes finite represented-parent basis truncation | Parent-model adequacy or material convergence |
| Auxiliary embedding | Probes a nonphysical interface construction | Convergence in a physical third direction |
| Common-estimator grid | Probes postprocessing discretization in a shared representation | Native Wannier90 objective convergence |
| Basin tolerances | Define an operational finite classifier | Mathematical identity of stationary points |

Parent-model, represented-basis, sampling, auxiliary-embedding, localization,
postprocessing, and comparison errors are therefore not combined into a single error
bar.

## Deterministic initial-gauge construction

Let \(A(\mathbf{k})\) be the baseline \(3\times3\) trial-overlap matrix. A declared
start \(s\) modifies the initial frame by right multiplication,

\[
A_s(\mathbf{k}) = A(\mathbf{k})U_s(\mathbf{k}),
\]

with

\[
U_s(\mathbf{k}) = \prod_j
\exp\!\left[
 i\alpha_{sj}
 \sin\!\left(2\pi\mathbf{m}_{sj}\!\cdot\!\mathbf{k}+\phi_{sj}\right)
 G_{sj}
\right].
\]

Here \(\alpha_{sj}\) is a frozen amplitude, \(\mathbf{m}_{sj}\) an integer reciprocal
harmonic, \(\phi_{sj}\) a phase, and \(G_{sj}\) a frozen Hermitian generator. Product
order is part of the input contract because the generators need not commute.

Each \(U_s(\mathbf{k})\) is constructed to be smooth, reciprocal-periodic, and unitary.
Consequently,

\[
A_s(\mathbf{k})A_s(\mathbf{k})^\dagger
 = A(\mathbf{k})U_s(\mathbf{k})U_s(\mathbf{k})^\dagger A(\mathbf{k})^\dagger
 = A(\mathbf{k})A(\mathbf{k})^\dagger.
\]

Thus the declared transformations preserve the overlap Gram matrix, its singular
values, and the rank-three retained subspace while changing the optimizer's initial
gauge trajectory. This is the key scientific control: endpoint variation is probed
without intentionally changing the selected subspace.

The eight starts are deterministic probes—identity plus seven prescribed smooth unitary
fields. They are neither random samples nor an exhaustive cover of \(U(3)\)-valued
periodic frames. Frequencies or occupancies cannot therefore be interpreted as
probabilities.

## Parameter design

The retained input declares nine unique configurations and eight starts per
configuration, for 72 localizations:

- mesh sequence \(N=11,15,19,23\) at \(P=4\) with balanced auxiliary length \(c=N\);
- cutoff sequence \(P=2,3,4,5\) at \(N=c=19\); and
- embedding controls \(c=15,19,23\) at \(P=4,N=19\).

Shared reference points are counted once. The auxiliary coordinate exists to support
the interface construction and is not assigned physical three-dimensional meaning.
Only active-plane centers, spreads, hopping blocks, and represented operators are
interpreted.

## Process completion versus localization convergence

The study separates three statuses:

1. process completion and exit status;
2. the native Wannier90 convergence statement; and
3. postprocessing classification.

A zero process exit code does not imply localization convergence. A trajectory reaching
the frozen 5000-iteration limit without the native convergence statement remains
nonconverged evidence. It is not deleted, retried, or promoted because its final scalar
objective appears favorable.

The retained result records 72 completed processes, of which 51 carry the native
convergence statement and 21 do not. Row 052 preserves these encoded counts. The
repository-portable verifier reconstructs count consistency, but the encoded-document
owner itself proves none of them.

## Native and common localization estimators

The native Wannier90 Berry-link spread owns optimizer convergence and the original basin
and finite-parameter classifications. A separate common \(512^2\) finite-supercell
estimator reconstructs external and direct-projected gauges in one represented setting.
The two estimators answer different questions and are not substituted for one another.

The retained hopping-tail diagnostic is

\[
\tau_{50} = \left(
 \sum_{R_x^2+R_y^2>50}
 \lVert H_{\mathrm W}(\mathbf{R})\rVert_{\mathrm F}^2
\right)^{1/2},
\]

where \(H_{\mathrm W}(\mathbf{R})\) is a Wannier-gauge hopping block and
\(\lVert\cdot\rVert_{\mathrm F}\) is the Frobenius norm. The tail measures omitted
real-space weight beyond the declared radius; it is not by itself an operator-error
bound for every observable.

Centers are treated as unordered active-plane sets. Matching minimizes over orbital
permutation and periodic lattice wrapping, because orbital labels and unit-cell choices
must not create artificial differences.

## Operational observed-basin classifier

Only native-converged endpoints enter the original observed-basin classification. Two
endpoints share one observed basin only if both frozen conditions hold:

1. absolute native total-spread difference no greater than \(10^{-8}a^2\); and
2. maximum matched periodic center-set distance no greater than \(10^{-5}\) cell.

For every reported basin, the retained occupancy must equal the number of listed member
gauges, the representative must be a member, and the basin partition must contain each
converged start exactly once. Nonconverged endpoints remain outside every basin.

This is an operational classifier, not a proof that two classes are distinct stationary
points. The original classifier does not quotient all point-group operations or
continuous gauge equivalences, so it may conservatively over-separate endpoints.

The “best observed converged” endpoint minimizes native spread only among the declared
converged starts. It is deliberately not called a global minimum. The median summary is
computed only over converged starts; its center representative is a center-set medoid,
while spread and tail summaries are scalar medians.

## Frozen finite-parameter convergence gate

The mesh pair \(N=19\rightarrow23\) and cutoff pair \(P=4\rightarrow5\) are tested
separately. For each pair, both the best observed endpoint and the median converged-start
summary must simultaneously satisfy:

- relative native-spread change \(\le 1\%\);
- periodic center-set distance \(\le 0.01\) cell; and
- relative radius-50 hopping-tail change \(\le 10\%\).

In addition, the basin containing the best observed endpoint must have occupancy at
least two at both ends of each pair. Both the mesh and cutoff gates must pass. Embedding
sensitivity is reported separately and cannot replace either sequence.

These are finite, predeclared operational criteria. Even a pass would not establish an
asymptotic limit, global optimizer convergence, material validation, or uncertainty
quantification.

## Why the retained disposition is negative

The retained result states that the frozen criteria are not supported:

- every best observed basin has occupancy one, below the required occupancy two;
- only two of eight starts converge at the finest mesh point \(N=23\);
- the best mesh-pair spread changes by about \(7.77\%\), exceeding the \(1\%\) gate;
- the best mesh-pair center-set distance is about \(0.187\) cell, exceeding the
  \(0.01\)-cell gate;
- the cutoff-pair spread and tail are stable under their scalar thresholds, but the
  center-set distance is about \(0.118\) cell and basin occupancy still fails; and
- 21 of 72 starts do not satisfy the native localization-convergence statement.

This distinction is scientifically important: stabilization of a scalar objective does
not demonstrate stable selection of a localized representation. Conversely, failure of
the frozen gate does not prove that no converged limit exists; it establishes only that
this bounded design does not support the declared classification.

## Repository-portable verification

`Periodic2DOptimizerBasinCampaignVerifier` performs a bounded compact-document
reconstruction without external execution. Before schema-specific reconstruction, the
shared strict JSON decoder rejects invalid UTF-8, duplicate object keys, nonstandard
nonfinite constants, unsupported primitive representations, and non-object roots. This
prevents ambiguous wire values from influencing a claim-bearing disposition.

The verifier first correlates experiment identity, authorization checkpoint, and the
exact bounded claim text while preserving the distinct authoritative-input and
calculated-result evidence-status roles. It then:

1. authenticates the encapsulated study input against a strictly represented lowercase
   SHA-256 digest declared by the result;
2. resolves directly declared extractor sources and rejects any normalized absolute,
   parent-traversal, or symlink target outside the explicit repository root;
3. authenticates the confined extractor sources against declared digests;
4. requires nine unique study declarations and nine unique result configurations before
   building identity maps, then correlates study axes and numerical controls;
5. requires exactly eight endpoints with unique gauge identities at every configuration;
6. requires a duplicate-free nonconverged identity list matching the endpoint partition;
7. reconstructs converged and nonconverged counts from endpoint flags;
8. verifies that observed basins partition converged endpoints exactly once;
9. identifies the minimum-native-spread converged endpoint and requires the complete
   retained `best_observed_converged` object to match that endpoint recursively with
   exact JSON representations, rejecting Python's Boolean/integer equality shortcut;
10. reconciles aggregate counts and the all-processes-completed disposition; and
11. derives the ordered mesh and cutoff pair identities from explicit study axes and
    declared finest-pair controls rather than names, then preserves their negative
    occupancy dispositions and the exact negative disposition text;
12. preserves the joint best-and-median stability requirement, every observed-only-best
    flag, and the aggregate non-global/non-general claim boundary; and
13. correlates each embedding-sensitivity summary's four selected fields with the
    corresponding fields in its identified configuration, without interpreting
    embedding as a physical dimension.

Source authentication, campaign declarations, configuration traversal,
per-configuration endpoint checks, aggregate summaries, basin partitions, and negative
predicates have separate private owners. Uniqueness is checked before dictionary
construction so duplicate identities cannot collapse silently. This decomposition keeps
the public Action boundary legible without introducing a generic verifier framework.

This verifier intentionally does not execute Wannier90 or read the external execution
result. Required-field absence is reported as `KeyError`, and confined source-read
failures retain their `OSError` category; both are documented public failure boundaries.
Its Action-produced passing result establishes internal consistency of authenticated
compact sources, not native-file availability or complete historical-execution
authentication. The immutable verification Result independently validates exact Boolean
flags, nonnegative exact integer counts, and lowercase SHA-256 syntax. Directly
constructing that Result validates intrinsic state only and does not prove that the
verifier Action executed.
The retained calculation directory contains separate historical independent-verification
scripts with broader native checks; row 052 neither reruns nor substitutes for them.

## Floating-point and threshold reasoning

The portable verifier rejects nonfinite real values before comparisons. Exact declared
integer controls and counts use equality. The auxiliary embedding value is checked with
zero absolute tolerance because it is expected to reproduce an exactly encoded
binary64 value from the same compact declarations, not an independently recomputed
floating-point observable.

Scientific tolerances belong to the frozen study input, not to the encoded-document
constructor. They are not silently relaxed to make a result pass. The negative result is
retained when any required predicate fails.

## Limitations and prohibited inferences

The retained study does not establish:

- exhaustive initialization coverage or a probability law over gauges;
- distinct mathematical local minima for every observed basin;
- a global minimum;
- asymptotic mesh or cutoff convergence;
- physical meaning for the auxiliary dimension;
- material, DFT, or production-Wannierization validation;
- uncertainty quantification; or
- a general theorem about localization algorithms.

No new calculator execution occurred during row-052 reconciliation. Exact-byte and
digest preservation establish software and content identity only.
