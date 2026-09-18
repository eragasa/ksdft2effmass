# Independent-route defect-extraction protocol

## Status and scope

This deterministic experiment produces **synthetic test data** and software/numerical-verification evidence. It asks whether defect extraction commutes with an independently implemented transformation from the accepted finite supercell representation to folded primitive Bloch fibers. It does not perform a silicon calculation, scientific validation, uncertainty quantification, continuum validation, or transferability study.

The route comparison begins only after applying the same declared candidate-to-reference coordinate map and scalar energy-reference correction. It therefore tests representation and extraction commutativity rather than repeating blind-map inference.

## Frozen sources

`input.json` fixes and SHA-256-identifies:

- the accepted defect-1D input;
- the accepted defect-1D result, including the compact planted controls; and
- the accepted periodic composite result containing the `low_pair` hopping blocks.

The nominal calculation uses the same 16-cell, two-orbital parent at $KN=0.17$, the same hopping range $|R|\leq4$, the same seven null/local/nonlocal/spin controls, and the same authored coordinate and energy-reference maps.

## Route A: direct finite-supercell extraction

For retained hopping blocks $h_R$, Route A independently assembles the site-space supercell matrix. If $n+R=qN+m$, its matrix element receives the supercell boundary phase $e^{2\pi iKNq}$. With candidate-to-reference map $T$, raw candidate $\widetilde H_d$, and scalar shift $c$, Route A computes

$$
H_d^{(A)}=T(\widetilde H_d-cI)T^\dagger,
\qquad
V^{(A)}=H_d^{(A)}-H_0^{(A)}.
$$

Spinful controls use an explicit tensor product with the spin identity before applying the accepted spin-frame map.

## Route B: direct primitive Bloch-fiber extraction

Route B does not call Route A. It evaluates each primitive fiber directly,

$$
H(k_j)=\sum_{R=-4}^{4}e^{2\pi i k_jR}h_R,
\qquad
k_j=K+\frac{j}{N}\pmod 1,
$$

and constructs the folding map

$$
F_{n\alpha,j\beta}=N^{-1/2}e^{2\pi i k_jn}\delta_{\alpha\beta}.
$$

Its candidate-to-fiber map is $F^\dagger T$. Route B computes

$$
H_d^{(B)}=F^\dagger T(\widetilde H_d-cI)T^\dagger F,
\qquad
V^{(B)}=H_d^{(B)}-\bigoplus_jH(k_j).
$$

The commutativity test is

$$
F^\dagger V^{(A)}F\stackrel{?}{=}V^{(B)}.
$$

Both routes share frozen observations but use separate assembly algorithms. Implementation independence here means neither route imports or invokes the other; it does not mean independent physical input data.

## Nominal controls and acceptance

The null, scalar-onsite, orbital-onsite, nearest-neighbor, range-two nonlocal, collinear-spin, and spin-mixing controls must each satisfy the frozen $10^{-11}$ tolerance for:

- folding-map unitarity;
- pristine representation discrepancy;
- coordinate-alignment defect;
- Route-A planted recovery;
- Route-B planted recovery; and
- route noncommutativity.

Physical spectra reconstructed by both paths are compared separately. The lowest physical eigenspace is compared by projector. A single-state fidelity is reported only when the lowest eigenspace is nondegenerate under the frozen $10^{-11}$ eigenspace rule.

## Deliberately unmatched routes

Four controls change one contract component at a time:

1. **Hopping truncation:** Route A retains $|R|\leq4$ while Route B retains $|R|\leq3$. The result is explicitly `noncommuting`; operator and reconstructed-spectrum discrepancies remain separate.
2. **Fiber domain:** a 15-fiber domain is proposed for a 16-cell supercell. The comparison stops before extraction.
3. **Quadrature weights:** a nonuniform amplitude-$0.02$ weight modifies the folding columns and violates unitarity. The comparison stops.
4. **Alignment map:** the route maps differ by one additional cell translation. The comparison stops before subtraction.

These noncommuting or fail-closed records prevent an invalid nominal comparison, but they are not the end of the analysis. All four are paired with explicit compatible constructions:

- **Common parent:** both routes are rebuilt with the declared $|R|\leq3$ parent. This changes the nominal $|R|\leq4$ pristine operator by a retained Frobenius norm and therefore does not make the original mixed-parent comparison commute.
- **Common domain:** both routes are rebuilt on the declared 15-cell/15-fiber space at the same total supercell phase. The planted range-two defect has zero norm in the excluded nominal cell, so restriction does not truncate it.
- **Weighted coordinates:** for nonuniform positive weights $W$, the synthesis map is $G=FW^{1/2}$. Because $G$ is not unitary, its adjoint is not used as its inverse. The protocol uses $G^{-1}=W^{-1/2}F^\dagger$ and retains the induced metric $M=G^\dagger G=W$. The transformed Hamiltonian is checked for $M$-self-adjointness.
- **Relative alignment:** if $T_A$ and $T_B$ are candidate-to-reference maps, the explicit unitary $R=T_AT_B^\dagger$ maps the second reference frame to the first. Both candidate and pristine operators are transformed through $R$ before subtraction and route comparison.

The original domain, weight, and map mismatches still stop, and the original mixed-range parent comparison remains noncommuting, because no common construction may be inferred silently. Their paired controls demonstrate agreement only after the missing common-space or common-parent information has been supplied explicitly. The common-range result is a comparison under a changed parent, not a repair of the original $|R|\leq4$ versus $|R|\leq3$ operator identity.

No changed domain, weight, truncation, or map is silently absorbed into a nominal residual. The $10^{-11}$ tolerance is an algebraic protocol threshold for this deterministic synthetic experiment, not a material criterion.

## Error ledger

The retained record keeps the following distinct:

- representation error between direct supercell and direct Bloch-fiber pristine operators;
- alignment error against the authored physical candidate;
- mesh/quadrature diagnostics through folding unitarity and domain agreement;
- hopping-truncation error;
- route noncommutativity;
- reconstructed spectral discrepancy; and
- lowest-eigenspace projector discrepancy or nondegenerate-state fidelity.

A small spectral discrepancy does not erase a large operator noncommutativity.

## Independent verification

`verify_result.py` does not import `run_experiment.py`. It reloads and verifies all source identities, reconstructs both routes with its own code, rebuilds every coordinate map and defect, recalculates all nominal, adversarial, and explicitly reconciled records and matrix digests, and checks the retained claim boundary.

Agreement verifies only the declared finite synthetic mathematics and its implementation.

## Reproduction

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-independent-route/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-independent-route/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-independent-route/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-independent-route/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-independent-route/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-independent-route/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-independent-route/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-independent-route/summary.png
```

Then run `sha256sum -c SHA256SUMS` from this directory.
