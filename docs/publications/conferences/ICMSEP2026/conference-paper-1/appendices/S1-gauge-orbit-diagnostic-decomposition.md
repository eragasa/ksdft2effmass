# Supplementary Appendix S1: Gauge-Orbit Diagnostic Decomposition

## S1.1 Purpose and scope

This appendix defines the invariant and frame-dependent parts of the operator
comparison used in the main paper. The decomposition applies to the diagnostic, not to
the Hamiltonian as a physical operator. It is defined relative to a frozen comparison
contract; changing the retained space, admissible alignment family, weights,
normalization, or finite translation domain changes the diagnostic.

The construction is analogous in purpose to the separation of the Wannier spread into
gauge-invariant and gauge-dependent contributions [1–3]. It is not the Wannier spread
functional and does not inherit that functional's physical or variational
interpretation.

## S1.2 Comparison contract

Let $V_{\mathrm{ref}}$ and $V_{\mathrm{red}}$ be retained finite-dimensional state
spaces of equal rank $r$. The operator channel requires a nonempty, declared family

$$
\mathcal U\subseteq
\left\{\mathbf C:V_{\mathrm{red}}\rightarrow V_{\mathrm{ref}}
\mid \mathbf C^\dagger\mathbf C=\mathbf C\mathbf C^\dagger=\mathbf I_r\right\}
$$

of admissible unitary identification maps. Restrictions imposed by continuity,
reciprocal-boundary sewing, symmetry, orbital semantics, or locality belong to the
definition of $\mathcal U$ rather than to a later interpretation of the residual.

For a finite translation domain $\mathcal S_H$, nonnegative weights
$\omega_{\mathbf R}$, and a positive frozen normalization

$$
Z_{\mathrm{ref}}=
\sum_{\mathbf R\in\mathcal S_H}\omega_{\mathbf R}
\left\|\mathbf H_{\mathrm{ref}}(\mathbf R)\right\|_{\mathrm F}^2,
$$

the aligned operator loss is

$$
\mathcal L_H(\mathbf C,\boldsymbol\theta)=
\frac{1}{Z_{\mathrm{ref}}}
\sum_{\mathbf R\in\mathcal S_H}\omega_{\mathbf R}
\left\|
\mathbf H_{\mathrm{ref}}(\mathbf R)
-\mathbf C\mathbf H_{\mathrm{red}}(\mathbf R;\boldsymbol\theta)\mathbf C^\dagger
\right\|_{\mathrm F}^2.
\tag{S1.1}
$$

A zero or unspecified normalization does not define this diagnostic. A different-rank
comparison likewise requires a separately declared projection or embedding; its
information loss cannot be absorbed into Eq. (S1.1).

## S1.3 Orbit loss and frame excess

**Attainment under a compact contract.** For fixed $\boldsymbol\theta$, the
finite-sum loss in Eq. (S1.1) is a continuous real-valued function of
$\mathbf C$. If $\mathcal U$ is nonempty and compact, the extreme-value theorem
therefore supplies $\mathbf C_\star\in\mathcal U$ such that

$$
\inf_{\mathbf C\in\mathcal U}\mathcal L_H(\mathbf C,\boldsymbol\theta)
=\min_{\mathbf C\in\mathcal U}\mathcal L_H(\mathbf C,\boldsymbol\theta)
=\mathcal L_H(\mathbf C_\star,\boldsymbol\theta).
$$

In the finite-rank contract used here, $U(r)$ is compact, so it is sufficient for the
admissible family to be a nonempty closed subset of $U(r)$. Sewing, symmetry, site,
and orbital restrictions imply this conclusion only when their frozen constraint maps
define a closed set; the names of those restrictions do not by themselves prove
compactness. For a merely nonempty noncompact family, the nonnegative loss still has a
well-defined infimum, but a minimizing alignment need not exist.

For nonempty $\mathcal U$, define the contract-invariant orbit loss

$$
\mathcal L_{H,\mathrm{orb}}(\boldsymbol\theta)
=\inf_{\mathbf C\in\mathcal U}\mathcal L_H(\mathbf C,\boldsymbol\theta).
\tag{S1.2}
$$

For a particular declared alignment $\mathbf C_0\in\mathcal U$, define the
frame-dependent excess

$$
\mathcal L_{H,\mathrm{frame}}(\mathbf C_0,\boldsymbol\theta)
=\mathcal L_H(\mathbf C_0,\boldsymbol\theta)
-\mathcal L_{H,\mathrm{orb}}(\boldsymbol\theta).
\tag{S1.3}
$$

For every $\mathbf C_0\in\mathcal U$, the defining greatest-lower-bound
property gives
$\mathcal L_{H,\mathrm{orb}}(\boldsymbol\theta)\leq
\mathcal L_H(\mathbf C_0,\boldsymbol\theta)$. Subtraction therefore proves

$$
\mathcal L_H(\mathbf C_0,\boldsymbol\theta)
=\mathcal L_{H,\mathrm{orb}}(\boldsymbol\theta)
+\mathcal L_{H,\mathrm{frame}}(\mathbf C_0,\boldsymbol\theta),
\qquad
\mathcal L_{H,\mathrm{frame}}\geq 0.
\tag{S1.4}
$$

This is an exact scalar decomposition of the diagnostic. It is not an orthogonal
decomposition of the residual matrix.

The orbit term is the greatest lower bound of the operator discrepancy over the frozen
admissible family. The frame term measures the excess associated with the selected
admissible representative. Both statements are relative to $\mathcal U$:
enlarging the family can decrease the orbit loss, while adding physical restrictions
can increase it.

## S1.4 Frame invariance

Consider independent frame changes $\mathbf A$ on $V_{\mathrm{ref}}$ and $\mathbf B$
on $V_{\mathrm{red}}$. They transform the represented operators and alignment map as

$$
\mathbf H_{\mathrm{ref}}'=\mathbf A\mathbf H_{\mathrm{ref}}\mathbf A^\dagger,
\qquad
\mathbf H_{\mathrm{red}}'=\mathbf B\mathbf H_{\mathrm{red}}\mathbf B^\dagger,
\qquad
\mathbf C'=\mathbf A\mathbf C\mathbf B^\dagger.
$$

If the admissible family is transported bijectively to
$\mathcal U'=\{\mathbf A\mathbf C\mathbf B^\dagger:\mathbf C\in\mathcal U\}$,
the residual corresponding to
$\mathbf C'=\mathbf A\mathbf C\mathbf B^\dagger$ is $\mathbf A$ times the
original residual times $\mathbf A^\dagger$. Unitary invariance of the Frobenius norm
gives

$$
\mathcal L_H'(\mathbf C',\boldsymbol\theta)
=\mathcal L_H(\mathbf C,\boldsymbol\theta).
$$

Because $\mathbf C\mapsto\mathbf A\mathbf C\mathbf B^\dagger$ is a bijection,

$$
\inf_{\mathbf C'\in\mathcal U'}\mathcal L_H'(\mathbf C',\boldsymbol\theta)
=\inf_{\mathbf C\in\mathcal U}
 \mathcal L_H'(\mathbf A\mathbf C\mathbf B^\dagger,\boldsymbol\theta)
=\inf_{\mathbf C\in\mathcal U}\mathcal L_H(\mathbf C,\boldsymbol\theta).
$$

Thus $\mathcal L_{H,\mathrm{orb}}$ is unchanged. Applying the same identity to the
corresponding representative
$\mathbf C_0'=\mathbf A\mathbf C_0\mathbf B^\dagger$ and subtracting the equal
orbit losses also proves equality of the two frame excesses. The numerical matrices
representing $\mathbf C_0$ and the residual may nevertheless change.

This invariance is contractual rather than absolute. A transformation that violates a
frozen symmetry, site, orbital, or sewing condition does not belong to the same
admissible comparison problem.

## S1.5 Outcomes when subtraction is unavailable

The diagnostic has three distinct outcomes:

1. If $\mathcal U$ is nonempty, the orbit loss is defined. A feasible alignment
   supplies an upper bound; a certified lower bound requires a separate global
   argument.
2. If the retained ranks differ but a scientifically authorized projection or
   embedding is supplied, comparison may proceed in the declared target space.
   Projection or embedding error remains a separate diagnostic.
3. If no admissible identification exists, the matrix-difference channel is undefined.
   The recorded outcome is a state-space mismatch, not a large operator residual.

Gauge-invariant channels can remain available in the third case. Spectra and trace
invariants may be compared after their own indexing and normalization contracts are
fixed. Projector distances require both retained subspaces to be embedded in the same
parent Hilbert space. Wilson-loop eigenphase multisets can be compared without choosing
an internal frame, provided the loop, rank, gap, and reciprocal sewing contracts agree.
These invariant channels do not create an operator identification map by themselves.

## S1.6 Relation to the Wannier decomposition

For a retained Bloch subspace, the Wannier spread admits the established separation

$$
\Omega=\Omega_{\mathrm I}+\widetilde\Omega,
$$

where $\Omega_{\mathrm I}$ depends only on the subspace projectors and
$\widetilde\Omega$ depends on the selected Bloch frame [1,2]. Equations (S1.2)–(S1.4) use
the same conceptual distinction between an equivalence class and its representative,
but they answer a different question. They quantify cross-model operator discrepancy
over a declared admissible orbit; they do not quantify Wannier localization.

Accordingly, a small orbit loss establishes agreement only for the finite operator
diagnostic that was defined. A small frame excess places the achieved loss near the
orbit infimum; it does not imply that the alignment matrix is close to a unique
optimizer. Neither quantity, by itself, establishes material validity, continuum
convergence, or locality outside the frozen comparison domain.

## References

1. Marzari N, Vanderbilt D. Maximally localized generalized Wannier functions for
   composite energy bands. *Physical Review B*. 1997;56:12847–12865.
   doi:10.1103/PhysRevB.56.12847.
2. Marzari N, Mostofi AA, Yates JR, Souza I, Vanderbilt D. Maximally localized Wannier
   functions: theory and applications. *Reviews of Modern Physics*.
   2012;84:1419–1475. doi:10.1103/RevModPhys.84.1419.
3. Panati G, Pisante A. Bloch bundles, Marzari–Vanderbilt functional and maximally
   localized Wannier functions. *Communications in Mathematical Physics*.
   2013;322:835–875. doi:10.1007/s00220-013-1741-y.
