# COMPATIBILITY OF SPECTRAL AND OPERATOR REDUCTIONS OF A FIRST-PRINCIPLES SILICON HAMILTONIAN

Bryan D. Llenarizas  
Department of Physics, De La Salle University; <bryan_domingo_llenarizas@dlsu.edu.ph>

Eugene Joseph M. Ragasa  
Department of Physics, De La Salle University; <eugene.ragasa@dlsu.edu.ph>

## ABSTRACT

First-principles electronic Hamiltonians may be reduced to compact lattice models by preserving either selected spectral properties or an aligned localized operator. These criteria need not admit the same reduced representation. This study formulates their compatibility within a common hierarchy of orthogonal $sp^3s^\ast$ Slater–Koster models for bulk silicon. A validated ten-orbital Wannier Hamiltonian will be constructed from one converged density-functional-theory calculation.  For each tight-binding model class, the spectral and operator criteria define admissible sets satisfying declared error tolerances. Compatibility requires a nonempty intersection, corresponding to a single Hamiltonian satisfying both requirements. When the intersection is empty, a normalized real-space Hamiltonian metric will determine the minimum separation between the admissible sets and quantify the incompatibility of the prescribed model class with the retained first-principles information. Validation will use withheld band energies, the indirect gap, conduction-valley position, longitudinal and transverse electron effective masses, and operator residuals resolved by orbital block and neighbor shell. The study will identify the smallest tested model class admitting a common reduced representation satisfying both criteria and thereby establish a validated bulk reference for subsequent impurity-operator reduction.

**KEYWORDS:** silicon; Wannier Hamiltonian; tight-binding reduction; operator
compatibility; model selection

## INTRODUCTION

Density-functional theory (DFT) supplies a first-principles Kohn–Sham description of crystalline electronic structure, but its plane-wave representation is inconvenient for interpolation and reduced lattice calculations. Maximally localized Wannier functions provide a localized representation of a selected Kohn–Sham subspace and support accurate interpolation [5], [7], [9], [12]. Parameterized tight-binding models instead restrict the Hamiltonian to a prescribed orbital basis, hopping range, and symmetry structure [8], [11].

A spectral fit preserves selected eigenvalues, whereas an operator fit preserves matrix information in an aligned localized representation. Spectral agreement alone does not establish agreement of onsite terms, orbital couplings, or hopping amplitudes. These differences become consequential when the bulk Hamiltonian is later modified by dopants, defects, strain, or other local perturbations, since all such operators must ultimately be represented in the same reduced basis to form a consistent effective Hamiltonian. Before an operator residual can be evaluated, the Wannier and tight-binding orbital coordinates must therefore be identified through a stable, symmetry-compatible alignment [1], [4].

The present study asks whether the spectral and operator criteria admit a common reduced representation within a prescribed tight-binding model class. Rather than forcing two independently fitted parameter vectors to agree, it defines admissible model sets for each criterion and asks whether they intersect. Repeating this test over a nested hierarchy of tight-binding model classes identifies the smallest class admitting a common representation, or quantifies the obstruction when no compatible representation exists.

## METHODOLOGY

A converged bulk-silicon reference will be calculated with QUANTUM ESPRESSO[2] using PBE-GGA [6], a scalar-relativistic PseudoDojo optimized norm-conserving pseudopotential [3], [10], the PBE-relaxed lattice constant, and a non-spin-polarized, non-SOC parent problem. Plane-wave cutoffs, wavevector meshes, and the number of bands will be converged against the
indirect gap, conduction-valley position, and longitudinal and transverse
electron effective masses.

A ten-orbital target subspace containing the valence bands and the low conduction states required for the silicon valleys will then be constructed with Wannier90 [7], [9]. Its real-space Hamiltonian is

$$\begin{gather}
 \left[
 \mathbf H_{\mathrm W}(\mathbf R)
 \right]_{\alpha\beta}
 =
 \left\langle
 w_{\alpha\mathbf 0}
 \middle|
 \hat H_{\mathrm{KS}}
 \middle|
 w_{\beta\mathbf R}
 \right\rangle,
\end{gather}$$
where $\mathbf R$ is a direct-lattice translation; $\alpha$ and $\beta$ label Wannier orbitals in the reference and translated primitive cells, respectively; $\lvert w_{\alpha\mathbf 0}\rangle$ and $\lvert w_{\beta\mathbf R}\rangle$ are localized Wannier states; and $\hat H_{\mathrm{KS}}$ is the converged Kohn–Sham operator.

Initial projections and outer and frozen disentanglement windows will be recorded. The Wannier Hamiltonian will be accepted as the common parent only after its dense-grid interpolation error, centers, spreads, sensitivity to window and projection choices, and real-space hopping decay have been validated.

For each candidate model class, the spectral loss is a weighted error over training-set Wannier eigenvalues and selected band-edge quantities. The operator loss is

$$\begin{align}
 \mathcal{L}_H
 \left(
 \mathbf{C},
 \boldsymbol{\theta}
 \right)
 =
 \sum_{\mathbf{R}}
 \omega_{\mathbf{R}}
 \left\|
 \mathbf{H}_{\mathrm{W}}(\mathbf{R})
 -
 \mathbf{C}
 \mathbf{H}_{\mathrm{TB}}
 \left(
 \mathbf{R};
 \boldsymbol{\theta}
 \right)
 \mathbf{C}^\dagger
 \right\|_{\mathrm{F}}^{2},
\end{align}$$

where $\mathbf C\in\mathcal U$ is a symmetry-compatible unitary alignment from the tight-binding orbital coordinates to the Wannier coordinates; $\boldsymbol{\theta}$ is the tight-binding parameter vector; $\mathbf{H}_{\mathrm{TB}}(\mathbf{R};\boldsymbol{\theta})$ is the tight-binding hopping matrix associated with $\mathbf{R}$; $\omega_{\mathbf{R}}\geq 0$ weights the contribution of each retained neighbor shell; and $\|\cdot\|_{\mathrm{F}}$ is the Frobenius norm.

The model hierarchy will begin with an orthogonal ten-orbital $sp^3s^\ast$ Hamiltonian with nearest-neighbor hopping. If that class is incompatible with the declared tolerances, second-neighbor and selected symmetry-allowed corrections will be introduced in a fixed sequence.

For a candidate model class $\mathfrak{M}_j$, the two losses define the admissible sets

$$\begin{gather}
 \mathfrak{A}_{E,j}(\tau_E)
 =
 \left\{
  \mathbf{H}(\boldsymbol{\theta}) \in \mathfrak{M}_j
  :
  \mathcal{L}_E(\boldsymbol{\theta}) \leq \tau_E
 \right\},
 \\
 \mathfrak{A}_{H,j}(\tau_H)
 =
 \left\{
  \mathbf{H}(\boldsymbol{\theta}) \in \mathfrak{M}_j
  :
  \min_{\mathbf{C} \in \mathcal{U}}
   \mathcal{L}_H
   \left(
     \mathbf{C}, \boldsymbol{\theta}
   \right)
   \leq
   \tau_H
 \right\},
\end{gather}$$

where $\mathcal L_E$ is the spectral loss; $\mathcal L_H$ is the aligned operator loss; $\tau_E$ is the declared spectral tolerance; $\tau_H$ is the declared operator tolerance; and $j$ indexes the nested tight-binding model classes.

The spectral tolerance includes targets of $5\%$ for the indirect gap, $3\%$ of the $\Gamma$–$X$ distance for the conduction-valley position, and $8\%$ for each electron effective mass. Operator and alignment tolerances will be normalized to the converged Wannier Hamiltonian and fixed before the compatibility search.

A dimensionless real-space Hamiltonian metric $d_{\mathrm{TB}}$ will compare models in their common canonical tight-binding coordinates. The minimum distance between the two admissible sets is

$$\begin{gather}
 \delta_j^\ast
 =
 \inf_{
 \substack{
 \mathbf H_E\in\mathfrak A_{E,j}\\
 \mathbf H_H\in\mathfrak A_{H,j}
 }
 }
 d_{\mathrm{TB}}
 \left(
 \mathbf H_E,
 \mathbf H_H
 \right),
\end{gather}$$

where $\mathbf H_E$ and $\mathbf H_H$ are models satisfying the spectral and operator criteria, respectively. A value of $\delta_j^\ast$ below the declared map tolerance establishes compatibility within $\mathfrak M_j$; otherwise, it quantifies the irreducible separation under the imposed spectral and operator requirements.

All accepted models will be tested on withheld wavevectors. The operator residual will be decomposed by onsite and hopping contribution, orbital block, crystal-symmetry channel, and neighbor shell. The analysis is restricted to bulk silicon; impurity operators are outside the present study.

All spectral and operator errors are measured relative to the converged PBE/Wannier parent Hamiltonian. The present study tests reduction fidelity and does not treat agreement with the experimental silicon band gap as an independent fitting target.

## EXPECTED RESULT

The required outputs are one converged bulk-silicon DFT dataset, one validated ten-orbital Wannier Hamiltonian, admissible spectral and operator model sets for each tested tight-binding class, their minimum metric separation, and one common validation record. Numerical entries will be reported only after the econvergence, fitting, and sensitivity calculations are complete.

| Quantity               | Mathematical criterion                 | Decision role                                   |
| ---------------------- | -------------------------------------- | ----------------------------------------------- |
| Spectral admissibility | Spectral loss within threshold         | Retains selected bands and band-edge quantities |
| Operator admissibility | Aligned operator loss within threshold | Retains real-space matrix information           |
| Map compatibility      | Set distance within map threshold      | Establishes a common reduced Hamiltonian        |
| Model selection        | Lowest-order compatible class          | Selects the minimal common Hamiltonian class    |

The decisive result is the smallest tested model class for which the spectral and operator admissible sets intersect within tolerance. If no tested class is compatible, the nonzero set separation and its decomposition will identify the orbital or hopping content responsible for the obstruction. Either outcome provides a controlled basis for determining whether the chosen reduced representation can consistently support subsequent dopant, defect, or impurity operators.

This work addresses compatibility for a single pair of reduction criteria. The same framework naturally extends to additional operator families, where the objective is to determine whether a common reduced representation exists for the bulk Hamiltonian together with perturbation operators describing dopants, defects, strain, or electron–phonon interactions.
## REFERENCES

[1] A. Björck and G. H. Golub, “Numerical methods for computing angles between linear subspaces,” *Math. Comp.*, vol. 27, no. 123, pp. 579–594, 1973, doi: 10.1090/S0025-5718-1973-0348991-3.

[2] P. Giannozzi et al., “QUANTUM ESPRESSO: A modular and open-source software project for quantum simulations of materials,” *J. Phys.: Condens. Matter*, vol. 21, Art. no. 395502, 2009, doi: 10.1088/0953-8984/21/39/395502.

[3] D. R. Hamann, “Optimized norm-conserving Vanderbilt pseudopotentials,” *Phys. Rev. B*, vol. 88, Art. no. 085117, 2013, doi: 10.1103/PhysRevB.88.085117.

[4] N. J. Higham, “Computing the polar decomposition—with applications,” *SIAM J. Sci. Stat. Comput.*, vol. 7, no. 4, pp. 1160–1174, 1986, doi: 10.1137/0907079.

[5] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally localized Wannier functions: Theory and applications,” *Rev. Mod. Phys.*, vol. 84, pp. 1419–1475, 2012,
doi: 10.1103/RevModPhys.84.1419.

[6] J. P. Perdew, K. Burke, and M. Ernzerhof, “Generalized gradient approximation made simple,” *Phys. Rev. Lett.*, vol. 77, pp. 3865–3868, 1996, doi: 10.1103/PhysRevLett.77.3865.

[7] G. Pizzi et al., “Wannier90 as a community code: New features and applications,” *J. Phys.: Condens. Matter*, vol. 32, Art. no. 165902, 2020, doi: 10.1088/1361-648X/ab51ff.

[8] J. C. Slater and G. F. Koster, “Simplified LCAO method for the periodic potential problem,” *Phys. Rev.*, vol. 94, pp. 1498–1524, 1954, doi: 10.1103/PhysRev.94.1498.

[9] I. Souza, N. Marzari, and D. Vanderbilt, “Maximally localized Wannier functions for entangled energy bands,” *Phys. Rev. B*, vol. 65, Art. no. 035109, 2001, doi: 10.1103/PhysRevB.65.035109.

[10] M. J. van Setten et al., “The PseudoDojo: Training and grading a 85 element optimized norm-conserving pseudopotential table,” *Comput. Phys. Commun.*, vol. 226, pp. 39–54, 2018, doi: 10.1016/j.cpc.2018.01.012.

[11] P. Vogl, H. P. Hjalmarson, and J. D. Dow, “A semi-empirical tight-binding theory of the electronic structure of semiconductors,” *J. Phys. Chem. Solids*, vol. 44, no. 5, pp. 365–378, 1983, doi: 10.1016/0022-3697(83)90064-1.

[12] J. R. Yates, X. Wang, D. Vanderbilt, and I. Souza, “Spectral and Fermi surface properties from Wannier interpolation,” *Phys. Rev. B*, vol. 75, Art. no. 195121, 2007, doi: 10.1103/PhysRevB.75.195121.
