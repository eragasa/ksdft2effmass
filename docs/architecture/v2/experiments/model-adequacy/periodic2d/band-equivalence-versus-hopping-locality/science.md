# Scientific method

The experiment now makes the spectral-to-tight-binding representation chain explicit.
For construction size `N`, the parent acts on

```math
\mathcal H_{p,N}^{(2)}=(\mathbb C^N)^{\otimes 2}\otimes\mathbb C^4.
```

Kronecker translation operators act on the two lattice factors; the orbital factor
remains four-dimensional. The tensor discrete Fourier transform converts this finite
cell--orbital operator exactly to the direct sum of four-state Bloch fibers

```math
K_\rho^{(2)}(\mathbf q)=T_0+\frac{\rho}{2}
\sum_{\alpha=x,y}(z_\alpha T_+ + z_\alpha^{-1}T_-).
```

Complete fiber spectra define the lower rank-two projectors. A qualified periodic frame
maps those projectors to a retained Bloch Hamiltonian, and the inverse tensor Fourier
transform maps that complete matrix field to its Wannier/TB hopping representation.
Eigenvalue lists are spectral data, not Hamiltonian operands.

The comparison uses

```math
U_a^{(2)}(\mathbf q)=R\!\left(\frac a2
[\sin(2\pi q_x)+\sin(2\pi q_y)]\right),
\qquad 0\le a\le\pi/4.
```

Under the full momentum-dependent gauge, the complete reference and comparison
operators are unitarily equivalent and their covariantly aligned subtraction vanishes.
The scientific residual is defined only after replacing that generally nonlocal Wannier-
space unitary by one cell-local global `SO(2)` rotation. Parent-space subtraction
requires an explicit projector lift; parent and retained matrices are never subtracted
across unequal spaces.

At the flat endpoint, the analytic correlation is `J_0(a)^2`, evaluated directly, and
Parseval equates the squared irreducible residual with non-onsite Fourier weight.
Dispersive parents do not inherit that equality. Post-truncation comparison uses every
attainable square signed-permutation shell through the declared cap. The primary cost is
retained-block inflation at the first passing sampled band-error shell. This is
representation cost, not physical inequivalence or material validation.
