# Hierarchy of Reduced Impurity Operators

back_to: [[ksdft2Effmass.00]]

## Scope
This section defines a nested hierarchy of reduced models for the first-principles impurity operator $\Delta\mathbf{H}_{\mathrm{W},d}$ extracted in [[ksdft2Effmass.06]]. The objective is to identify the least expressive impurity model that preserves specified bound-state spectra, subspaces, and observables within stated tolerances.

All matrix decompositions in this section are defined in the aligned Wannier gauge established in [[ksdft2Effmass.04]]. Individual onsite and hopping components are gauge dependent; their physical interpretation therefore requires the gauge, orbital ordering, and spatial assignment to remain fixed.

Each reduced impurity operator must be embedded in a declared bulk host Hamiltonian. For the controlled reduction chain, that host is selected from the compatible bulk model class established in [[ksdft2Effmass.05]], so host-model error is not silently absorbed into the impurity fit.

## Full Atomistic Reference

For dopant $d\in\mathcal{D}=\{\mathrm{P},\mathrm{B}\}$, let
$$
\Delta\mathbf{H}_{\mathrm{ref},d}
=
\Delta\mathbf{H}_{\mathrm{W},d}
$$
denote the full atomistic impurity matrix in the retained Wannier space. Its elements are
$$
\left[
\Delta\mathbf{H}_{\mathrm{ref},d}
\right]_{ab},
$$
where $a$ and $b$ are composite site-orbital indices.

The reduced impurity model at level $m$ is denoted by
$$
\Delta\mathbf{H}_{m,d}
\in
\mathfrak{M}_{m,d},
$$
where $\mathfrak{M}_{m,d}$ is the corresponding admissible model class.

## Operator Decomposition

Separate the full matrix into onsite and offsite components:
$$
\Delta\mathbf{H}_{\mathrm{ref},d}
=
\Delta\mathbf{H}_{\mathrm{on},d}
+
\Delta\mathbf{H}_{\mathrm{off},d}.
$$
The onsite matrix contains elements whose two orbital indices belong to the same spatial site. The offsite matrix contains elements connecting distinct sites.

The onsite contribution may be decomposed further as
$$
\Delta\mathbf{H}_{\mathrm{on},d}
=
\Delta\mathbf{H}_{\mathrm{sc},d}
+
\Delta\mathbf{H}_{\mathrm{orb},d}
+
\Delta\mathbf{H}_{\mathrm{mix},d}.
$$
Here, $\Delta\mathbf{H}_{\mathrm{sc},d}$ is proportional to the identity within each local orbital block, $\Delta\mathbf{H}_{\mathrm{orb},d}$ is diagonal but orbital dependent, and $\Delta\mathbf{H}_{\mathrm{mix},d}$ contains onsite mixing between distinct local orbitals.

The offsite contribution is
$$
\Delta\mathbf{H}_{\mathrm{off},d}
=
\Delta\mathbf{H}_{\mathrm{hop},d},
$$
which contains impurity-induced changes in hopping, hybridization, and other nonlocal couplings.

## Scalar Onsite Component

Let $\mathcal{A}_i$ be the set of Wannier orbitals assigned to lattice site $i$, and let $n_i$ be the number of orbitals in that set. The scalar onsite shift at site $i$ is
$$
v_{i,d}
=
\frac{1}{n_i}
\sum_{a\in\mathcal{A}_i}
\left[
\Delta\mathbf{H}_{\mathrm{ref},d}
\right]_{aa}.
$$
The corresponding scalar onsite operator has matrix elements
$$
\left[
\Delta\mathbf{H}_{\mathrm{sc},d}
\right]_{ab}
=
v_{i,d}
\delta_{ab},
\qquad
a,b\in\mathcal{A}_i.
$$
The Kronecker delta $\delta_{ab}$ makes this contribution proportional to the identity within the local orbital block.

## Orbital-Dependent Onsite Component

The diagonal orbital-dependent residual is
$$
\left[
\Delta\mathbf{H}_{\mathrm{orb},d}
\right]_{aa}
=
\left[
\Delta\mathbf{H}_{\mathrm{ref},d}
\right]_{aa}
-
v_{i,d},
\qquad
a\in\mathcal{A}_i.
$$
This term measures how the impurity distinguishes different localized orbital channels on the same site.

The remaining onsite off-diagonal part is
$$
\left[
\Delta\mathbf{H}_{\mathrm{mix},d}
\right]_{ab}
=
\left[
\Delta\mathbf{H}_{\mathrm{ref},d}
\right]_{ab},
\qquad
a\neq b,
\quad
a,b\in\mathcal{A}_i.
$$
It describes impurity-induced mixing between local orbitals.

## Nonlocal Hopping Component

For orbitals assigned to distinct sites $i\neq j$,
$$
\left[
\Delta\mathbf{H}_{\mathrm{hop},d}
\right]_{ab}
=
\left[
\Delta\mathbf{H}_{\mathrm{ref},d}
\right]_{ab},
\qquad
a\in\mathcal{A}_i,
\quad
b\in\mathcal{A}_j.
$$
These matrix elements represent changes in hopping and hybridization caused by the impurity and its associated structural and electronic relaxation.

For a spatial cutoff $R_c$, define the truncated hopping perturbation
$$
\left[
\Delta\mathbf{H}_{\mathrm{hop},d}^{(R_c)}
\right]_{ab}
=
\begin{cases}
\left[
\Delta\mathbf{H}_{\mathrm{hop},d}
\right]_{ab},
&
\rho_{ab,d}\leq R_c,
\\
0,
&
\rho_{ab,d}>R_c,
\end{cases}
$$
where $\rho_{ab,d}$ is the matrix-element distance from the impurity defined in [[ksdft2Effmass.06]].

## Nested Lattice Model Classes
Define the following hierarchy:
$$
\mathfrak{M}_{\mathrm{scalar}}
\subset
\mathfrak{M}_{\mathrm{orbital}}
\subset
\mathfrak{M}_{\mathrm{onsite}}
\subset
\mathfrak{M}_{R_c}
\subset
\mathfrak{M}_{\mathrm{full}}.
$$
The classes have the following meanings:

1. $\mathfrak{M}_{\mathrm{scalar}}$ contains site-dependent scalar onsite shifts;
2. $\mathfrak{M}_{\mathrm{orbital}}$ adds orbital-dependent diagonal onsite terms;
3. $\mathfrak{M}_{\mathrm{onsite}}$ adds all onsite orbital mixing;
4. $\mathfrak{M}_{R_c}$ adds nonlocal perturbations within distance $R_c$;
5. $\mathfrak{M}_{\mathrm{full}}$ contains the complete extracted impurity matrix.

The hierarchy is nested only after the gauge, orbital partition, spatial metric, and cutoff convention have been fixed.

## Projection onto a Model Class

Let
$$
\mathfrak{M}_{m,d}
=
\operatorname{span}
\left\{
\mathbf{B}_{1,d}^{(m)},
\ldots,
\mathbf{B}_{N_m,d}^{(m)}
\right\}
$$
be the level-$m$ impurity model class. The matrices $\mathbf{B}_{a,d}^{(m)}$ are its allowed operator components, and $N_m$ is its number of independent parameters.

Using a specified operator norm, define the optimal level-$m$ model by
$$
\boxed{
\Delta\mathbf{H}_{m,d}^*
=
\Pi_{\mathfrak{M}_{m,d}}
\Delta\mathbf{H}_{\mathrm{ref},d}
=
\operatorname*{arg\,min}_{\Delta\mathbf{H}\in\mathfrak{M}_{m,d}}
\left\|
\Delta\mathbf{H}_{\mathrm{ref},d}
-
\Delta\mathbf{H}
\right\|^2
}.
$$
The projection $\Pi_{\mathfrak{M}_{m,d}}$ returns the closest operator in the selected model class according to the stated norm.

The discarded impurity content is
$$
\mathbf{E}_{m,d}
=
\Delta\mathbf{H}_{\mathrm{ref},d}
-
\Delta\mathbf{H}_{m,d}^*.
$$
This residual must be analyzed both globally and within the target bound-state subspace.

## Screened Scalar Potential

The continuum-motivated scalar model assigns a potential value to each Wannier center. Let $q_e=-e$ be the electron charge, let $Q_d$ be the effective charge associated with the ionized impurity, and let $\varepsilon_{\mathrm{Si}}$ be the static relative dielectric constant of silicon. The screened Coulomb interaction energy is
$$
V_{\mathrm{C},d}(r)
=
\frac{
q_eQ_d
}{
4\pi\varepsilon_0\varepsilon_{\mathrm{Si}}r
},
$$
where $\varepsilon_0$ is the vacuum permittivity and $r$ is the distance from the impurity.

Its Wannier-basis scalar approximation is
$$
\left[
\Delta\mathbf{H}_{\mathrm{C},d}
\right]_{ab}
=
V_{\mathrm{C},d}(\rho_{a,d})
\delta_{ab},
$$
where $\rho_{a,d}$ is the distance of orbital $a$ from the impurity. This expression neglects the finite spatial extent of the Wannier orbital and all nonlocal matrix elements; a more accurate representation may use the expectation value of $V_{\mathrm{C},d}(\hat{\mathbf{r}})$ in the Wannier basis.

The point-charge expression is not used at $r=0$. Matrix elements associated with the impurity site require a finite short-range regularization or an explicitly fitted central-cell operator.

## Central-Cell Residual

Define the central-cell residual relative to the screened scalar model by
$$
\Delta\mathbf{H}_{\mathrm{cc},d}
=
\Delta\mathbf{H}_{\mathrm{ref},d}
-
\Delta\mathbf{H}_{\mathrm{C},d}.
$$
This residual contains all short-range scalar deviations, orbital dependence, onsite mixing, hopping changes, and other nonlocal corrections not represented by the screened Coulomb model.

A central-cell model is therefore not assumed to be purely local. Its required operator structure is determined by which components of $\Delta\mathbf{H}_{\mathrm{cc},d}$ are needed to reproduce the target bound-state physics. The spatial localization of this residual must be demonstrated rather than inferred from its name.

## Minimal Acceptable Model

Let $\boldsymbol{\varepsilon}_{m,d}$ denote the collection of operator, spectral, subspace, and observable errors for model level $m$, and let $\boldsymbol{\tau}_d$ denote the corresponding prescribed tolerances. The least acceptable model is
$$
m_d^*
=
\min
\left\{
m
:
\boldsymbol{\varepsilon}_{m,d}
\leq
\boldsymbol{\tau}_d
\right\}.
$$
The vector inequality means that every required error metric must satisfy its corresponding tolerance.

This definition makes model simplicity conditional on the target physics. A scalar onsite model may be sufficient for one observable and inadequate for another.

## Validation Requirements

For every model level, report:

1. the retained operator components and number of parameters;
2. the global residual matrix and its spatial decay;
3. the residual projected into the target bound-state subspace;
4. impurity binding energies and level splittings;
5. bound-state or subspace fidelity;
6. sensitivity to gauge, spatial cutoff, and model-fitting weights;
7. the improvement obtained when the next operator class is added.

The error measures used for these comparisons are defined in [[ksdft2Effmass.08]].

## Role in the Reduction Program

The reduction hierarchy is
$$
\boxed{
\Delta\mathbf{H}_{\mathrm{W},d}
\longrightarrow
\Delta\mathbf{H}_{R_c,d}
\longrightarrow
\Delta\mathbf{H}_{\mathrm{onsite},d}
\longrightarrow
\Delta\mathbf{H}_{\mathrm{orbital},d}
\longrightarrow
\Delta\mathbf{H}_{\mathrm{scalar},d}
}.
$$
The arrows represent projections into successively more restrictive model classes. Moving from left to right corresponds to systematic simplification.

The purpose is not to assume that effective-mass theory is correct, but to determine the least operator structure required before the continuum limit is attempted.

## References

[1] W. Kohn and J. M. Luttinger, "Theory of donor states in silicon," *Phys. Rev.*, vol. 98, pp. 915-922, 1955, doi: 10.1103/PhysRev.98.915.

[2] C. J. Wellard and L. C. L. Hollenberg, "Donor electron wave functions for phosphorus in silicon: Beyond effective-mass theory," *Phys. Rev. B*, vol. 72, Art. no. 085202, 2005, doi: 10.1103/PhysRevB.72.085202.