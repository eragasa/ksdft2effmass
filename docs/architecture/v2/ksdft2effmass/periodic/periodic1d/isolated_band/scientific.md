# M1 scientific boundary

## Represented objects

M1 starts from the toy Bloch Hamiltonian represented by
`Periodic1DFourierHamiltonianToyModel`. In the frozen model convention, the direct
period is carried by the Fourier potential, the reciprocal period is the positive
`reciprocal_vector`, and the represented energy unit is the unit of `recoil_energy`.

The parent-model, numerical-discretization, and reduced-model channels remain distinct:

1. plane-wave and finite-difference calculations approximate the same parent operator;
2. the selected parent eigenvalue samples define one finite reciprocal representation;
3. a discrete Fourier transform changes representation without reducing range;
4. truncation or direct fitting creates a finite-range reduced model; and
5. training and staggered evaluation errors assess different sample roles.

## Parent fiber

<a id="eq-m1-parent-fiber-001"></a>

$$
H_{nn'}(k)
=E_R(k+n)^2\delta_{nn'}+V_{n-n'}.
\tag{EQ-M1-PARENT-FIBER-001}
$$

Here $k$ is the declared reduced Bloch coordinate, $n,n'$ are reciprocal-basis
indices, $E_R$ is `recoil_energy`, and $V_q$ is the finite Fourier potential. The
implemented parent constructors own their exact basis ordering and unit conversion.

## Complete hopping transform

For a uniform $N$-point reciprocal mesh $k_j$, the complete scalar hopping
representation is the finite discrete Fourier transform

<a id="eq-m1-fourier-002"></a>

$$
T_R=\frac{1}{N}\sum_{j=0}^{N-1}E(k_j)e^{-2\pi i k_jR},
\qquad
E(k_j)=\sum_R T_Re^{2\pi i k_jR}.
\tag{EQ-M1-FOURIER-002}
$$

This is a basis transformation on the finite mesh. It is not Wannier localization and
is not range truncation.

## Finite-range models

For declared range $L$, mediated truncation retains representatives with
$|R|\leq L$. The separate direct route solves a least-squares problem on the same
training coordinates and representatives. Comparing their coefficients and sampled
operators distinguishes a transformation-then-truncation route from a direct fit.

## Sample roles

The training mesh determines Fourier blocks, direct-fit coefficients, and all declared
finite-range models. If its extent is $N$ and the evaluation extent is $M$, evaluation
coordinate $i$ is

<a id="eq-m1-withheld-mesh-003"></a>

$$
\widetilde k_i=-\frac12+\frac{i+1/(N+1)}{M},
\qquad i=0,\ldots,M-1.
\tag{EQ-M1-WITHHELD-MESH-003}
$$

The stagger is deterministic and disjoint from the training mesh. Evaluation values
cannot update the transform, fit, ranges, tolerances, or result disposition.

## Claims and exclusions

M1 supports the bounded claim that the maintained implementation reproduces the frozen
finite calculation and that complete and finite-range channels satisfy their retained
diagnostics. It does not establish physical isolation, material accuracy, continuum
convergence, localization, transferability, uncertainty bounds, or acceptance.

## Code and evidence mapping

| Equation or claim | Implementing owner | Direct evidence |
|---|---|---|
| `EQ-M1-PARENT-FIBER-001` | parent constructors composed by `Periodic1DIsolatedBandCalculator` | parent-refinement and verifier tests |
| `EQ-M1-FOURIER-002` | `ReciprocalOperatorFourierTransformer1D`, composed by M1 | deterministic reconstruction and Parseval channels |
| `EQ-M1-WITHHELD-MESH-003` | `Periodic1DIsolatedBandCalculationDefinition.withheld_reduced_momenta` | sample-role separation test |

## Provenance

The equations document repository-owned implementation conventions. Physical and
mathematical definitions remain subordinate to `specification/`; retained controls and
chronology remain subordinate to the M1 protocol and freeze record.
