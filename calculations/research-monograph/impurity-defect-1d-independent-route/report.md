# Independent real-space and Bloch-fiber defect extraction

## Abstract

Two separately implemented routes extract the same seven synthetic represented defect operators after the accepted coordinate and energy-reference alignment. Route A assembles and subtracts finite supercell matrices directly in site space. Route B evaluates primitive Bloch matrices, constructs the folding transform, and subtracts directly in folded-fiber space. Across null, local, nonlocal, collinear-spin, and spin-mixing controls, the maximum pristine-representation discrepancy is $9.58\times10^{-15}E_G$, the maximum route noncommutativity is $9.61\times10^{-15}E_G$, and the maximum reconstructed eigenvalue discrepancy is $1.11\times10^{-15}E_G$. A deliberate hopping-range mismatch produces operator noncommutativity $2.83\times10^{-2}E_G$ while the reconstructed physical spectrum remains equal to $7.77\times10^{-16}E_G$. Unmatched fiber domains, quadrature weights, and alignment maps stop structurally. All four altered contracts then agree after explicit common-parent, common-domain, dual-map/metric, and relative-unitary reconciliation. These are synthetic software and numerical-verification results, not material validation.

## Question

The accepted known-map benchmark extracted planted defects in finite real space, and the blind-alignment benchmark tested when its coordinate map could be inferred. This follow-on asks whether extraction depends on the computational route after a valid map and energy reference have been declared.

The intended square commutes if direct site-space subtraction followed by folding equals alignment and subtraction performed directly in the folded primitive-fiber representation.

## Methods

The calculation reuses the accepted 16-cell `low_pair` parent, hopping range $|R|\leq4$, seven planted controls, coordinate transformation, and scalar shift $0.137E_G$. Route A constructs supercell matrix elements by finite-range hopping and boundary-phase assembly. Route B independently evaluates all 16 primitive momenta $k_j=K+j/N$, builds each $2\times2$ Bloch block, and constructs the discrete folding transform. Spinful controls lift both routes with an explicit spin identity before applying the accepted spin-frame transformation.

The routes share immutable mathematical inputs and the raw scrambled candidate operator, but neither route calls the other. The complete contracts, formulas, stopping rules, and reproduction commands are retained in `protocol.md`.

## Nominal results

All seven controls return `commuting`. For spinless controls, the pristine representation discrepancy is $6.77\times10^{-15}E_G$, and route noncommutativity ranges from $6.80\times10^{-15}E_G$ to $6.82\times10^{-15}E_G$. For collinear and spin-mixing controls, the corresponding values remain below $9.58\times10^{-15}E_G$ and $9.62\times10^{-15}E_G$.

Direct site-space planted recovery remains below $1.56\times10^{-15}E_G$. Direct fiber-space planted recovery remains below $9.70\times10^{-15}E_G$. The maximum folding unitarity defect is $1.93\times10^{-14}$, still below the frozen $10^{-11}$ algebraic tolerance.

Reconstructed physical eigenvalue lists agree within $1.11\times10^{-15}E_G$. The largest lowest-eigenspace projector discrepancy, in the range-two control, is $1.69\times10^{-13}$; every lowest eigenspace is nondegenerate under the frozen rule, and its reported state fidelity rounds to unity. These observable diagnostics remain separate from operator and representation discrepancies.

## Deliberately unmatched routes

Changing only the Bloch-fiber hopping range from four cells to three produces a pristine truncation discrepancy and route noncommutativity of $2.8324\times10^{-2}E_G$. The reconstructed physical operator is nevertheless the same raw aligned candidate, so the eigenvalue discrepancy remains $7.77\times10^{-16}E_G$. This control demonstrates that spectral agreement can coexist with a materially different extracted defect operator when the parent partition differs.

A 15-fiber domain against the 16-cell supercell stops with `INDEPENDENT_ROUTE.FIBER_DOMAIN_MISMATCH`. Nonuniform fiber weights of amplitude $0.02$ produce folding unitarity defect $0.0800$ and stop with `INDEPENDENT_ROUTE.QUADRATURE_WEIGHT_MISMATCH`. An alignment map shifted by one additional cell differs in Frobenius norm by $8.0$ and stops with `INDEPENDENT_ROUTE.ALIGNMENT_MAP_MISMATCH`. None returns a nominal extracted operator.

## Explicit reconciliation

All four altered contracts now have paired constructive controls. First, rebuilding both routes with the common $|R|\leq3$ parent gives representation discrepancy $6.77\times10^{-15}E_G$ and route noncommutativity $6.80\times10^{-15}E_G$. The parent differs from the nominal $|R|\leq4$ operator by $2.8324\times10^{-2}E_G$, so this is a declared changed-parent comparison rather than a claim that the original mixed-parent paths commute.

Second, rebuilding both routes on the same 15-cell/15-fiber domain retains the complete planted defect because its excluded-cell norm is zero. Its representation discrepancy is $6.71\times10^{-15}E_G$, and its route noncommutativity is $6.74\times10^{-15}E_G$.

Third, the nonuniform weighted synthesis $G=FW^{1/2}$ is treated as an invertible coordinate map rather than incorrectly as a unitary map. Its adjoint differs from its inverse by $8.00\times10^{-2}$, while the explicit dual $G^{-1}=W^{-1/2}F^\dagger$ has inverse defect $1.37\times10^{-14}$. The transformed operator is self-adjoint in the induced metric to $7.33\times10^{-15}E_G$, and weighted-coordinate route noncommutativity is $6.82\times10^{-15}E_G$.

Fourth, the two alignment frames are related explicitly by $R=T_AT_B^\dagger$. Transforming both candidate and pristine operators through this relative unitary gives physical-operator defect $1.16\times10^{-15}E_G$ and route noncommutativity $1.15\times10^{-15}E_G$. The original stops and mixed-parent noncommutativity remain valid guards: the reconciliations work because the missing common-space or common-parent contract is now declared, not because mismatched operators became directly comparable.

## Independent verification

The verifier independently reloads the identified accepted records and reconstructs all finite-supercell matrices, primitive fibers, folding maps, spin lifts, coordinate maps, defects, nominal comparisons, adversarial outcomes, common-parent truncation, common-domain restriction, weighted dual and induced metric, relative-unitary alignment, and matrix digests without importing the runner. Every retained field agrees within the frozen floating-point comparison rule.

## Interpretation

The nominal result verifies an algebraic commutative diagram for one finite synthetic representation. It provides a cross-route check that site-space extraction is not an artifact of one assembly path. The adversarial controls also show what the result does not imply: parent truncation, domain, quadrature, and map conventions are part of the mathematical operator definition and cannot be changed while retaining a route-equivalence claim.

In particular, the truncation example reinforces the separation between operator and observable metrics. An unchanged reconstructed spectrum does not certify agreement of extracted impurity operators when the pristine parent assigned to the subtraction differs.

## Limitations

All source observations, defects, and maps are synthetic or inherited synthetic records. The two implementations deliberately share the same frozen mathematical input data. Agreement is established only for one finite periodic 1D representation and does not establish continuum convergence. No silicon, dopant, DFT, production Wannier, material validity, scientific validation, transferability, uncertainty quantification, public API, release, or publication claim is made.
