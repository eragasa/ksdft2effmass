# Scientific interpretation

PIAB1D is a controlled analytical model used to expose finite-representation,
discretization, reduction, and verification behavior. It is not semiconductor evidence
and does not validate a material Hamiltonian.

The successor keeps four error classes separate:

1. the parent physical-model limitation;
2. finite-difference discretization error;
3. numerical eigensolver and finite-algebra error; and
4. retained-space model-reduction error.

Agreement with the closed-form finite-difference spectrum verifies the represented
matrix and eigensolution. Agreement with continuum energies over a refinement series
measures discretization behavior for the declared fixed modes and grids. Algebraic
residuals measure discrete solver accuracy. Compression residuals measure declared
finite-space operations. None of these channels substitutes for another.

The full-spectrum sweep demonstrates nonuniform dispersion when the mode index grows
with grid dimension. Fixed low modes approach the expected second-order trend. Modes at
a fixed fraction of the grid retain substantial finite-difference error. This result
prevents a low-mode convergence statement from being generalized to the complete
spectrum.

The retained-dimension selection is an illustrative probability-tail calculation. It
does not define a physical thermal ensemble or a material truncation threshold.

The kinetic-potential decomposition demonstrates algebraic nonuniqueness. The declared
Dirichlet kinetic operator and zero potential carry the physical interpretation of the
model. The shifted decomposition reconstructs the same retained Hamiltonian but remains
explicitly illustrative and nonphysical. Restricted model-class residuals quantify
dependence on the declared admissible class and retained basis.

Independent verification establishes software and bounded numerical agreement for the
serialized result. Rendering establishes deterministic presentation of authenticated
data. Neither action establishes scientific validation, uncertainty quantification,
human acceptance, publication, or release.
