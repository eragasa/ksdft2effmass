# Appendix D. Read-Only Wannier90 Silicon Tutorial Preview

This appendix extracts the bounded silicon tutorial analysis formerly embedded in Paper
1 v2. It is historical read-only evidence and is excluded from the planned production
silicon admissible sets.

## Source and representation

The retained fixture is correlated post hoc to the official Wannier90 3.1.0
`examples/example11` silicon tutorial inputs. The executed `silicon.win` changed no
numerical setting and added only

```text
write_hr = true
write_u_matrices = true
```

to request additional artifacts. The source run used Quantum ESPRESSO 7.5, Wannier90
3.1.0, a legacy ultrasoft PBE pseudopotential, a 25-Ry wavefunction cutoff, 12 parent
bands, four retained Wannier functions, and a `4 x 4 x 4` Wannier mesh. These settings
are not a converged production silicon calculation.

At each of the 64 reciprocal samples, the analysis forms

$$
W(\mathbf k)=U_{\mathrm{dis}}(\mathbf k)U(\mathbf k)
$$

and constructs all three represented operators in the same rank-four frame:

$$
H^W(\mathbf k)
=W^\dagger(\mathbf k)\operatorname{diag}(\epsilon)W(\mathbf k),
$$

$$
T^W(\mathbf k)
=W^\dagger(\mathbf k)C_{\mathrm{PW}}^\dagger(\mathbf k)
\operatorname{diag}\!\left(\frac{|\mathbf k+\mathbf G|^2}{2}\right)
C_{\mathrm{PW}}(\mathbf k)W(\mathbf k),
$$

and

$$
R^W(\mathbf k)=H^W(\mathbf k)-T^W(\mathbf k).
$$

The finite represented remainder $R^W$ is not identified with a continuous local scalar
potential. The ultrasoft pseudopotential and finite representation prevent that
interpretation.

## Extracted finite-mesh checks

The same-frame identity had maximum discrepancy $1.52\times10^{-15}$ eV. An independent
route from the native `_hr.dat` file differed by $1.28\times10^{-5}$ eV in maximum
Frobenius norm.

At every nonzero canonical radius represented by this finite mesh, the maximum kinetic
block norm exceeded the maximum remainder block norm, by factors from approximately
1.24 to 2.67. The total block could be smaller than either component because the exact
sum contains cancellation. The nonmonotone 64-block inventory does not establish an
infinite-lattice decay exponent.

![Component-resolved finite-mesh block norms for the read-only Wannier90 silicon tutorial. Each point is the maximum Frobenius norm at one canonical representative radius. The curves do not establish an infinite-lattice decay law.](../../../../../calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/real-space-shell-block-norms.pdf)

A complete inverse finite transform contains 64 centered blocks. After retaining 57,
the maximum ordered-eigenvalue errors were:

| Represented component | Maximum error |
|---|---:|
| Total $H^W$ | 0.0207 eV |
| Kinetic $T^W$ | 0.0843 eV |
| Non-kinetic remainder $R^W$ | 0.0636 eV |

All 64 blocks recovered the sampled matrices to roundoff. The table therefore records a
negative result for one finite-mesh truncation, not a proof that every compact silicon
Hamiltonian class fails.

![Relative reciprocal-matrix errors under finite-block truncation for the read-only tutorial representation. The final drop at 64 blocks is complete discrete reconstruction, not continuum convergence.](../../../../../calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/real-space-truncation-relative-error.pdf)

## Evidence boundary

Post-hoc SHA-256 correspondence confirms the tutorial input bytes but does not establish
causal provenance for every source-run output. No Quantum ESPRESSO or Wannier90 run was
repeated for this extraction. No independent reciprocal-mesh, cutoff, projector,
effective-mass, or symmetry-alignment acceptance study is supplied.

This appendix may support statements about same-frame operator construction and failure
of the tested 57-block truncation. It may not supply production settings, production
thresholds, silicon effective masses, admissible-set membership, or model selection.
