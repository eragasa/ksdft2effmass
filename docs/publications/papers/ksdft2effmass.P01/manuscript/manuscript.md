# Model-Class Expressiveness Beyond Spectral Fitting: A Gauge-Equivariant Operator Framework

> Status: Working P01 manuscript and repository projection. P01 remains `Waiting`; see the [publication record](../ksdft2effmass.P01.md) and workspace [proof status](../../../proofs/ksdft2effmass/proof-status.md). Prospective statements authorize the corresponding in-repository work described below, but do not represent that work as completed or scientifically validated.

Eugene Joseph M. Ragasa

## Working-Document Contract

This Markdown manuscript is a living projection of the scientific, mathematical, computational, and software work represented in the repository. It is not merely a narrative written after the work is finished.

- Links identify existing repository owners for definitions, assumptions, implementations, workflows, evidence, and proof obligations.
- A proposed link identifies an intended repository owner that does not yet exist or is not yet assigned; it is a work item, not evidence of completion.
- A prospective statement authorizes creation or refinement of the in-repository artifacts needed to realize that statement within the manuscript's declared scope.
- A statement becomes a calculated result, proved result, verified result, or validated claim only when its owning repository artifacts and required evidence exist.
- This authorization does not silently change frozen scientific settings, publication state, or human-acceptance status, and it does not replace the applicable checkpoint for protected external or production execution.

## Repository Projection

| Manuscript concern | Repository owner or proposed link | Projection status |
|---|---|---|
| Physical parent problem and bulk scope | [Physical specification](../../../../specification/ksdft2Effmass.physical-specification.v1.md) | Existing authoritative contract |
| Numerical protocols and provenance requirements | [Numerical specification](../../../../specification/ksdft2Effmass.numerical-specification.v1.md) | Existing authoritative contract |
| Kohn–Sham, projection, and Wannier distinctions | [Research foundation](../../../research/ksdft2Effmass.01.md) and [Wannier construction](../../../research/ksdft2Effmass.03.md) | Existing research owners |
| Parallel spectral and operator TB reductions | [Bulk reduction research](../../../research/ksdft2Effmass.05.md) | Existing research owner |
| Bulk computational stages | [Computational workflow index](../../../computational/ksdft2effmass.computational.00.md), [Stage 02](../../../computational/ksdft2Effmass.computational.02.md), [Stage 03](../../../computational/ksdft2Effmass.computational.03.md), and [Stage 04](../../../computational/ksdft2Effmass.computational.04.md) | Existing workflow owners; execution remains gate-controlled |
| State spaces and Bloch-fiber correspondence | [State-space assumptions](../../../proofs/ksdft2effmass/foundations/state-space-assumptions.md) and [Bloch-fiber correspondence](../../../proofs/ksdft2effmass/foundations/bloch-fiber-correspondence.md) | Proposed proof development |
| Gauge actions and aligned comparison | [Representation maps](../../../proofs/ksdft2effmass/foundations/representation-maps.md), [TB anchoring](../../../proofs/ksdft2effmass/operator-alignment/tb-anchored-identification.md), and [gauge equivariance](../../../proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md) | Proposed proof development |
| Model-class distance and compatibility | [Model-class expressiveness](../../../proofs/ksdft2effmass/compatibility/model-class-expressiveness.md) and [spectral–operator compatibility](../../../proofs/ksdft2effmass/compatibility/spectral-operator-compatibility.md) | Proposed proof development |
| Represented-operator software primitives | [`python/src/ksdft2effmass/operators/`](../../../../python/src/ksdft2effmass/operators/) | Existing implementation surface; manuscript-specific fitting actions are proposed |
| Model-class fitting implementation | Proposed link: manuscript-specific fitting owner under the approved Python architecture | Authorized in-repository work; owner path not yet fixed |
| Figures, tables, and retained result artifacts | Proposed links: versioned compact artifacts referenced from this manuscript | Authorized in-repository work; no calculated result yet |
| LaTeX realization | [`latex/`](latex/) | Reserved publication source surface |

## Abstract
Current tight-binding parameterization is formulated primarily as an optimization over model parameters. The resulting discrepancy between a first-principles Hamiltonian and a reduced model is typically interpreted as either optimization error or insufficient model complexity. This interpretation neglects the fact that operator representations possess residual gauge freedom arising from basis choices within retained subspaces.

We develop a gauge-equivariant framework in which reduced Hamiltonians are compared only after quotienting out physically admissible coordinate transformations. Rather than fitting coordinate representations, we compare equivalence classes of operators under symmetry-preserving gauge actions. This separates representation error from intrinsic model-class limitations.

The resulting framework defines gauge-invariant operator residuals, establishes equivariance of projection and alignment maps, identifies the gauge dependence of locality and truncation, and formulates tight-binding reduction as the distance between constrained operator manifolds. The theory provides a mathematically well-posed criterion for determining whether disagreement between Wannier and parameterized tight-binding Hamiltonians reflects gauge choice or insufficient expressive power of the model class.

## Introduction

Reduced electronic-structure models are commonly constructed by choosing a parameterized Hamiltonian and optimizing its parameters against selected first-principles observables. In empirical and semiempirical tight-binding methods, these observables are usually band energies, band gaps, valley locations, effective masses, or other spectral quantities. In Wannier-based constructions, a first-principles Hamiltonian is instead projected onto a retained band subspace and represented in a localized basis. Both approaches produce finite-dimensional matrix Hamiltonians, but they solve different reduction problems: spectral fitting constrains selected eigenvalues, whereas Wannier projection constructs a coordinate representation of a projected operator.

Comparisons between these models often treat their matrix representations as though they were expressed in a canonical basis. This assumption is generally false. A retained $M$-dimensional Bloch subspace admits unitary changes of frame,

$$
\mathbf V'(\mathbf k)
=
\mathbf V(\mathbf k)\mathbf Q(\mathbf k),
\qquad
\mathbf Q(\mathbf k)\in U(M),
$$

under which the projector onto the retained subspace remains unchanged,

$$
\mathbf{P}'(\mathbf k)
= \mathbf{V}'(\mathbf k)\mathbf V'(\mathbf k)^\dagger
= \mathbf{P}(\mathbf k),
$$

while the matrix representing an operator transforms covariantly,

$$
\mathbf H'(\mathbf k)
=
\mathbf Q(\mathbf k)^\dagger
\mathbf H(\mathbf k)
\mathbf Q(\mathbf k).
$$

The abstract projected operator is therefore unchanged, although its matrix elements, orbital blocks, and real-space hopping coefficients may differ. This residual freedom is central to the construction of localized Wannier functions and has long been recognized in Wannier theory [@marzari2012; @souza2001]. Its consequence for operator-level model reduction, however, is stronger than the statement that Wannier functions are nonunique: a discrepancy between two Hamiltonian matrices cannot be interpreted as model error until their retained spaces and admissible coordinate frames have been identified.

The central claim of this work is that **model reduction should be formulated on equivalence classes of operators rather than on individual coordinate representations**. Let $\mathfrak O(\mathcal H^{(P)})$ denote an appropriate space of operators on a retained subspace $\mathcal H^{(P)}$, and let $\mathcal G_{\mathrm{phys}}$ denote the group of physically admissible changes of frame. The relevant equivalence class of a represented Hamiltonian $\mathbf H$ is its gauge orbit,

$$
[\mathbf{H}]_{\mathcal{G}_{\mathrm{phys}}}
=
\left\{
  \mathbf{Q}^\dagger
  \mathbf{H}
  \mathbf{Q}
  :
  \mathbf{Q}\in\mathcal{G}_{\mathrm{phys}}
\right\}.
$$

A physically meaningful reduced Hamiltonian is then associated not with one matrix $\mathbf H$, but with a point in the quotient or orbit space

$$
\mathfrak O(\mathcal H^{(P)})
\big/
\mathcal G_{\mathrm{phys}}.
$$

The term “physically admissible” is essential. The full pointwise group $U(M)$ is generally too large for comparison with a localized tight-binding model. An arbitrary $\mathbf k$-dependent unitary transformation may preserve the fiberwise spectrum while changing Wannier localization, orbital centers, symmetry characters, and the range of the real-space Hamiltonian. For localized tight-binding comparison, the admissible group must therefore encode the structure that the reduced model is intended to preserve. Depending on the problem, this may require smoothness and periodicity in $\mathbf k$, compatibility with crystal symmetries, preservation of chosen Wannier centers and orbital identities, and consistency with the site-local or Slater–Koster structure of the model class. Symmetry adaptation restricts the gauge freedom but does not generally remove it [@sakuma2013; @koepernik2023].

This distinction exposes a limitation of purely spectral validation. At a fixed $\mathbf k$, two Hermitian matrices with identical eigenvalues are unitarily equivalent, subject to the usual treatment of degeneracies. However, pointwise spectral equivalence does not guarantee the existence of a single smooth, periodic, symmetry-compatible, and localization-preserving family $\mathbf Q(\mathbf k)$ relating the two Hamiltonians across the Brillouin zone. Consequently, agreement of band energies does not by itself establish equivalence of the corresponding localized operators. It does not determine orbital character, hopping structure, responses to local perturbations, or the form of an impurity operator obtained by subtracting two aligned Hamiltonians. Spectral fitting and operator fitting must therefore be treated as distinct constraints rather than interchangeable validation procedures.

The same reasoning clarifies the status of locality. If
$$
\mathbf H(\mathbf R)
=
\frac{1}{|\mathrm{BZ}|}
\int_{\mathrm{BZ}}
e^{-i\mathbf k\cdot\mathbf R}
\mathbf H(\mathbf k),
\mathrm d\mathbf k
$$

denotes the real-space Hamiltonian, then a $\mathbf k$-dependent transformation of $\mathbf H(\mathbf k)$ generally mixes its Fourier coefficients. Individual hopping amplitudes, orbital-block norms, neighbor-shell contributions, and the error produced by truncation at a prescribed range are therefore not invariants of the abstract operator. They are properties of the operator together with a chosen localized frame. Localization changes the representation; truncation changes the represented operator. A gauge-equivariant reduction framework must keep these two operations logically separate.

The model-class distance and joint spectral/operator admissibility construction are maintained in the supporting [model-class expressiveness proof unit](../../../proofs/ksdft2effmass/compatibility/model-class-expressiveness.md).

Within this framework, projection, subspace identification, Wannierization, aligned subtraction, tight-binding parameterization, and continuum reduction are treated as maps between operator spaces or their coordinate representations. A reduction map is physically consistent only when it is equivariant with respect to the admissible gauge actions on its domain and codomain. Gauge equivariance does not guarantee that two different reduction paths commute, nor does it establish that a reduced model is physically adequate. It provides the prior consistency condition required for a path residual to have an invariant interpretation.

This work develops that framework in four steps.
- First, we distinguish invariant retained subspaces and abstract operators from their gauge-covariant matrix representations and define the admissible gauge actions relevant to localized tight-binding models.
- Second, we establish the equivariance conditions for projection, alignment, and pristine–perturbed operator subtraction and construct residuals based on unitarily invariant norms.
- Third, we characterize how localization and finite-range truncation depend on the chosen localized gauge.
- Fourth, we formulate model-class expressiveness as the distance between a parameterized tight-binding class and a physically constrained operator orbit, connecting this distance to joint spectral and operator admissibility.

## Residual-Guided Model-Class Refinement

The first computational model is selected because it supplies a viable, physically interpretable orbital representation. Its identification convention is frozen before model-class fitting. The subsequent question is not whether one parameter vector can be optimized successfully, but which assumptions defining the model class are required to reproduce the aligned first-principles operator.

Let

$$
\mathcal M_0\subset\mathcal M_1\subset\cdots\subset\mathcal M_n
$$

be a declared hierarchy in which each inclusion relaxes one assumption, such as hopping range, orbital content, orthogonality, environment dependence, or allowed gauge structure. For each class, define the best admissibly aligned residual

$$
d_j
=
\inf_{H\in\mathcal M_j,\;G\in\mathcal G_{\mathrm{phys}}}
\left\|
H_{\mathrm{FP}}-G^\dagger H G
\right\|.
$$

The change from $d_j$ to $d_{j+1}$ measures the improvement associated with the declared relaxation under a fixed comparison protocol. Spatial, orbital, and wavevector-resolved residuals can then diagnose which restricted structures are inconsistent with the reference operator. A smaller fitted residual does not by itself establish that the added structure is the correct missing physics; each relaxation must also be tested against withheld wavevectors, observables, systems, or other declared transferability checks.

This produces an evidence-driven refinement sequence:

```text
select and freeze an interpretable anchor
→ fit the initial model class
→ resolve the residual by physical structure
→ relax one assumption
→ quantify improvement and added complexity
→ test held-out predictions and anchor sensitivity
```

The computational realization uses a projected Wannier Hamiltonian and an orthogonal $sp^3s^\ast$ Slater–Koster hierarchy for bulk silicon. Silicon serves as a controlled demonstration rather than as the source of the formalism: the purpose of the calculation is to determine whether apparent disagreement between first-principles and parameterized Hamiltonians can be removed by an admissible alignment or instead persists as a model-class residual. The resulting formulation provides the operator-level foundation required for subsequent bulk–dopant subtraction and atomistic-to-continuum reduction, where an inconsistent coordinate identification would otherwise be inherited by every downstream impurity operator.
