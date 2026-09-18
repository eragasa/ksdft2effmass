# Finite-rank resolvent oracle for one-dimensional defect bound states

## Abstract

A finite-rank resolvent identity provides an analytical oracle for synthetic bound states of the accepted two-orbital one-dimensional represented parent. For 20 rank-one attractive controls spanning five supercell sizes and four defect magnitudes, roots of a directly evaluated Bloch-fiber secular equation agree with independently diagonalized site-space defect energies within $6.11\times10^{-16}E_G$. The maximum bound-state projector defect is $6.14\times10^{-13}$ and every attractive control has exactly one state below the finite-host lower edge. Zero-coupling, repulsive, spin-degenerate, and unequal-rank controls retain threshold, no-lower-bound-state, rank-two projector, and structured-stop outcomes. This is synthetic software and numerical verification, not a continuum or material result.

## Question

The accepted extraction benchmarks verify represented impurity operators and route commutativity. They do not provide an analytical oracle for the spectral machinery applied to those operators. This exercise asks whether a finite-rank bound-state energy and subspace obtained without diagonalizing the defect Hamiltonian agree with the numerical eigensolver under the same finite represented-space conventions.

## Methods

The accepted `low_pair` parent retains two-orbital hopping blocks through $|R|\leq4$. A normalized local orbital vector $u=(\cos0.41,e^{0.37i}\sin0.41)^T$ defines $v=|0\rangle\otimes u$. The attractive defect is $V_g=-g|v\rangle\langle v|$.

For energy $E$ below the finite-host edge, the matrix determinant lemma reduces the bound-state condition to

$$
1-gG_N(E)=0,
\qquad
G_N(E)=\frac1N\sum_j u^\dagger[H(k_j)-EI]^{-1}u.
$$

The oracle evaluates only direct $2\times2$ Bloch-fiber inverses and resolves the unique below-edge root by bisection. Its state is reconstructed as $(H_0-EI)^{-1}v$ and normalized. The independent numerical route assembles the full site-space parent and diagonalizes $H_0+V_g$; it does not call the root resolver.

The frozen sweep uses $N=16,24,32,48,64$ and $g/E_G=0.02,0.08,0.20,0.50$. Exact formulas, root rules, tolerances, source identities, and reproduction commands are retained in `protocol.md`.

## Rank-one results

All 20 attractive controls produce one numerical state below the finite-host edge, matching the rank-one oracle. The maximum oracle/numerical energy discrepancy is $6.11\times10^{-16}E_G$. The maximum secular residual is $8.16\times10^{-13}$, below the frozen $10^{-11}$ rule. The maximum projector defect is $6.14\times10^{-13}$, below the frozen $10^{-9}$ rule.

For $g=0.02E_G$, the binding varies from $2.45\times10^{-4}E_G$ to $3.38\times10^{-4}E_G$ over the tested sizes and has the largest state sensitivity. At $g=0.08E_G$, the range narrows to approximately $7.6131\times10^{-3}E_G$. The $g=0.20E_G$ and $0.50E_G$ bindings are approximately $5.8187\times10^{-2}E_G$ and $2.5386\times10^{-1}E_G$, respectively, with little visible variation over this finite sequence. These are finite-size observations, not an infinite-system extrapolation.

## Boundary controls

At zero coupling, the host-edge state is not classified as an isolated bound state and the below-edge count is zero. For the repulsive $+0.20|v\rangle\langle v|$ control, positivity of the below-edge resolvent gives a positive secular value and the numerical below-edge count remains zero. This claim is restricted to the lower host edge; it does not exclude a repulsive state above the upper spectrum.

Tensoring the parent and attractive defect with the two-dimensional spin identity produces a rank-two bound eigenspace. The two numerical energies agree with the scalar oracle within $7.50\times10^{-16}E_G$, their splitting is $6.11\times10^{-16}E_G$, and the rank-two projector defect is $1.55\times10^{-14}$. Individual eigenvector fidelity is deliberately omitted because vectors inside a degenerate subspace are not unique.

A proposed rank-one comparison against that numerical rank-two sector stops with `ANALYTICAL_ORACLE.EIGENSPACE_RANK_MISMATCH`; no projector defect or state fidelity is manufactured.

## Independent verification

The verifier independently reconstructs the accepted hopping blocks, Bloch fibers, finite site-space operators, all 20 roots, oracle vectors, numerical spectra, projectors, digests, and four boundary controls without importing the runner. Every retained record agrees within the verifier's frozen floating-point comparison rule.

## Interpretation and limitations

The result verifies the finite-rank determinant identity and the numerical spectral machinery for one finite synthetic parent family. It supplies a spectral oracle independent of the full defect-Hamiltonian eigensolve and reinforces the requirement to compare degenerate states through projectors.

The supercell sequence does not establish a continuum limit, infinite-volume convergence, or uncertainty quantification. The generic spin lift is not explicit spin-orbit coupling. No silicon, dopant, DFT, production Wannier, material validity, transferability, scientific validation, release, or publication claim is made.
