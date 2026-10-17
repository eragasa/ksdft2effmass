# Numerics

The initial M0 action prospectively fixes nine strain fractions
\(s\in\{0,1/8,\ldots,1\}\), maximum gauge angle \(\pi/4\), tail-power tolerances
\(10^{-3}\) and \(10^{-5}\), and a \(24^3\) half-step tensor Monkhorst--Pack transform.
Exact mesh-origin phases are retained and centered Nyquist power is reported separately.

The separate M1/M2 smoke action uses `8 x 8 x 8` construction and shifted
`17 x 17 x 17` evaluation meshes. It reports the three approximation channels for both
the represented Hamiltonian and the gauge-aligned strain difference at each selected
support.

At each strain point, the M0 action validates unit metric determinant, preserves the same
reduced-coordinate Fourier blocks, computes physical squared distances
\(\mathbf R^\mathsf{T}G_3\mathbf R\), groups all distance ties, and scans every complete
radius in order. The first passing radius and block count are sampled development
decisions. A single transform size is not a convergence ladder, and no FCC/BCC operator
subtraction is permitted without the declared common basis.
