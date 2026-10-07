# Finite Wigner–Seitz represented-operator interpolation specification v1

Status: **adopted for software construction; scientific interpretation not yet validated**

Scope: typed interpolation and Cartesian differentiation of finite represented
Wannier operators whose canonical Born–von Karman blocks have already been
constructed in an identified retained frame. The Wigner–Seitz name and cell
construction follow Wigner and Seitz [^wigner-seitz-1933].

This specification defines finite matrix transformations. It does not parse native
Wannier90 files, establish artifact provenance, infer a Wigner–Seitz inventory from
array dimensions, execute a calculator, select a physical retained space, establish
infinite-lattice localization, or validate interpolation accuracy away from the source
mesh.

## Identified Wigner–Seitz inventory

Let the source reciprocal mesh have shape $(N_1,N_2,N_3)$. A Wigner–Seitz
interpolation inventory contains:

- an explicit inventory identifier and source-binding identifier;
- direct-lattice basis vectors as the rows of a nonsingular $3\times3$ matrix
  $A$ in a physical length unit;
- an ordered tuple of distinct integer representatives $\mathbf R_s\in\mathbb Z^3$;
  and
- a positive integer degeneracy $d_s$ for each representative.

Every residue in
$\mathbb Z_{N_1}\times\mathbb Z_{N_2}\times\mathbb Z_{N_3}$ must occur. For each
residue class, the number of supplied representatives must equal the degeneracy stored
on every member of that class. Nonsingularity is evaluated through a logarithmic
determinant so a finite nonsingular diagonal lattice is not accepted or rejected merely
because its raw determinant overflows or underflows binary64. Every representative
component must also survive exact integer-to-binary64 conversion before phase or
Cartesian-coordinate evaluation; otherwise construction raises `OverflowError` rather
than collapsing distinct lattice translations onto one numerical coordinate. This is
the finite Wigner–Seitz lift contract used by the interpolation below; it is not
inferred from filenames, labels, spectra, or matrix dimensions.

For a canonical centered finite-mesh block family $A^W(\bar{\mathbf R})$, the
lifted block assigned to representative $\mathbf R_s$ is the canonical block with the
same componentwise residue modulo $(N_1,N_2,N_3)$. No native-file decoding or
independent operator identification occurs at this step.

A concrete Wigner–Seitz represented-operator record retains operator role, operator
identifier, source binding, frame, energy reference, inventory, and one physical-energy
matrix per representative. This permits the same interpolation action to evaluate an
explicitly adapted native Hamiltonian for cross-route comparison without pretending
that it belongs to the canonical $H/T/R$ construction. It is an exact typed record,
not an erased generic-programming boundary or a source of inferred identity.

## Same-frame interpolation

For reduced reciprocal coordinates $\mathbf q$, interpolation uses the positive phase
and native degeneracy division

$$
A^W(\mathbf q)=\sum_s
\exp\!\left(2\pi i\,\mathbf q\cdot\mathbf R_s\right)
\frac{A^W(\bar{\mathbf R}_s)}{d_s}.
$$

The per-operator action evaluates one concrete Wigner–Seitz represented-operator
record. A separate aggregate action interpolates the represented Hamiltonian,
canonical kinetic operator, and represented non-kinetic remainder from one
`WannierKineticDecompositionResult`. Therefore operator identity, source binding,
retained frame, energy reference, matrix dimension, energy unit, and source mesh are
not reconstructed from structural similarity. The inventory source binding and mesh
shape must agree exactly with the decomposition.

The result retains all requested reduced coordinates and reports maximum Frobenius
Hermiticity defects for the three interpolated matrix families and the maximum
same-frame decomposition defect

$$
\max_{\mathbf q}\left\|H^W(\mathbf q)-T^W(\mathbf q)-R^W(\mathbf q)\right\|_F.
$$

A caller-provided absolute tolerance in the decomposition output-energy unit assesses
only those four finite-representation diagnostics. Passing does not establish artifact
provenance, source-mesh convergence, interpolation convergence, physical adequacy, or
scientific validation.

## Result-correlation construction

Public interpolation and derivative Result constructors accept no precomputed
numerical witness. Each Action owns request-to-value derivation and performs it once.
Results validate intrinsic types, shapes, units, algebraic relations, and diagnostics
computed from their retained values; they do not replay the Action. This rejects a
caller-forgeable witness boundary without bypassing immutable construction or doubling
the numerical work. Manual Result construction establishes only those intrinsic
invariants, not Action execution, provenance, scientific replication, or convergence.

## Cartesian derivatives

For one identified represented operator and reduced coordinate $\mathbf q_0$, define
the Cartesian representative

$$
\mathbf r_s=\mathbf R_s A,
$$

where direct-lattice basis vectors are rows of $A$. With Cartesian wavevector
$\mathbf k$ dual to that basis, the positive phase is
$\exp(i\mathbf k\cdot\mathbf r_s)$ and equals
$\exp(2\pi i\mathbf q\cdot\mathbf R_s)$. The value, Cartesian gradient, and Cartesian
Hessian at $\mathbf q_0$ are

$$
A^W(\mathbf q_0)=\sum_s \phi_s\frac{A_s}{d_s},
$$

$$
\partial_{k_a}A^W(\mathbf q_0)=
\sum_s i r_{s,a}\phi_s\frac{A_s}{d_s},
$$

$$
\partial_{k_a}\partial_{k_b}A^W(\mathbf q_0)=
-\sum_s r_{s,a}r_{s,b}\phi_s\frac{A_s}{d_s},
\qquad
\phi_s=\exp(2\pi i\mathbf q_0\cdot\mathbf R_s).
$$

If blocks use energy unit $E$ and direct-lattice vectors use length unit $L$, the value,
gradient, and Hessian use $E$, $E L$, and $E L^2$, respectively. The result reports
Frobenius anti-Hermitian defects in those corresponding units and the Cartesian-index
symmetry defect of the Hessian. It does not diagonalize the value, choose a degenerate
subspace, construct a Löwdin reduction, convert curvature to effective mass, or claim
that finite-mesh derivatives are converged physical derivatives.

## Separation of responsibilities

The integration owner remains responsible for native Wigner90 decoding, inventory and
source-binding authority, lattice convention, and correlation to a production run.
`ksdft2effmass.solid_state.wignerseitz` owns only the typed residue lift, finite
interpolation, same-frame diagnostics, and analytic derivative transformations defined
above. Degenerate-subspace reduction, effective-model selection, uncertainty,
convergence, and scientific acceptance remain separate operations.

## References and citation provenance

[^wigner-seitz-1933]: E. Wigner and F. Seitz, “On the Constitution of Metallic
    Sodium,” *Physical Review*, vol. 43, no. 10, pp. 804–810, 1933, doi:
    [10.1103/PhysRev.43.804](https://doi.org/10.1103/PhysRev.43.804). The title,
    authors, journal, volume, issue, pages, publication date, and DOI were checked
    against the Crossref DOI record on 2026-10-07. This citation preserves the
    provenance of the Wigner–Seitz name and cell construction; it does not validate
    this software's finite-mesh representative inventory, replica selection,
    normalization, interpolation accuracy, or scientific application.
