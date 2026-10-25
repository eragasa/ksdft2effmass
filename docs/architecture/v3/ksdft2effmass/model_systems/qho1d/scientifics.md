# Scientific interpretation

The direct calculation is an illustrative controlled comparison of finite represented
operators. It varies box half-width, grid spacing, and retained number-state dimension
to expose their combined effect after common-coordinate alignment.

The reported difference is not a single continuum-discretization error. It combines:

1. finite-box closure;
2. boundary-adjacent finite-difference rows;
3. interior spatial discretization;
4. finite sampled-state Gram correction;
5. projection into retained coordinates; and
6. binary64 reconstruction.

Diagonal and off-diagonal difference norms separate two finite-matrix components. The
full-space residual `||H_h J - J D_K||_F` supplies an a-posteriori relation to the
pullback difference when `J` is isometric. Neither quantity proves convergence to the
real-line differential operator.

Passing verification establishes agreement between declared production and independent
finite constructions under stated tolerances. It does not establish semiconductor
relevance, physical uncertainty quantification, model adequacy for a material,
publication, or human acceptance.
