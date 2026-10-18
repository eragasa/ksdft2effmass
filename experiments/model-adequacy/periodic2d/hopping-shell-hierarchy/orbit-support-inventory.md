# Square-symmetry orbit and support inventory

## Status and scope

This file selects the exact finite operation order, orbit convention, maximal coefficient
order, and nested support prefixes for the prospective isotropic two-dimensional
hopping-shell hierarchy. It is outcome-independent protocol design, not calculated
experiment evidence.

The inventory is bounded to the centered odd-mesh domain

$$
\mathcal R_{\max}=\{-7,-6,\ldots,7\}^2.
$$

It does not define a generic lattice-orbit API or claim arbitrary-dimensional support.

## Admitted operation order

Each operation acts on the integer column vector $(x,y)^T$. Operations are applied in
the following exact order:

| Index | Operation ID | Matrix | Coordinate action |
|---:|---|---|---|
| 0 | `identity` | $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ | $(x,y)$ |
| 1 | `reflect-y-axis` | $\begin{pmatrix}-1&0\\0&1\end{pmatrix}$ | $(-x,y)$ |
| 2 | `reflect-x-axis` | $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ | $(x,-y)$ |
| 3 | `rotate-180` | $\begin{pmatrix}-1&0\\0&-1\end{pmatrix}$ | $(-x,-y)$ |
| 4 | `reflect-main-diagonal` | $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ | $(y,x)$ |
| 5 | `rotate-90-counterclockwise` | $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ | $(-y,x)$ |
| 6 | `rotate-90-clockwise` | $\begin{pmatrix}0&1\\-1&0\end{pmatrix}$ | $(y,-x)$ |
| 7 | `reflect-antidiagonal` | $\begin{pmatrix}0&-1\\-1&0\end{pmatrix}$ | $(-y,-x)$ |

The inventory uses these eight concrete signed-permutation maps rather than relying on an
unqualified group name. Every map preserves the centered domain and squared Euclidean
radius.

## Canonical representative and member ordering

For any $(x,y)\in\mathcal R_{\max}$, its canonical representative is

$$
(a,b)=\left(\max(|x|,|y|),\min(|x|,|y|)\right),
\qquad 0\le b\le a\le7.
$$

Canonical representatives are sorted by the exact key

```text
(a*a + b*b, a, b)
```

using ascending integer order. Orbit members are obtained by applying the admitted
operations to $(a,b)$ in operation-index order and retaining only the first occurrence
of each exact integer pair. No post-generation lexical sort is applied.

This gives multiplicity 1 for `(0, 0)`, multiplicity 4 when exactly one coordinate is
zero or both positive coordinates are equal, and multiplicity 8 otherwise.

## Complete maximal inventory

| Index | Representative | Squared radius | Multiplicity | Ordered members |
|---:|---:|---:|---:|---|
| 0 | `(0, 0)` | 0 | 1 | `(0, 0)` |
| 1 | `(1, 0)` | 1 | 4 | `(1, 0), (-1, 0), (0, 1), (0, -1)` |
| 2 | `(1, 1)` | 2 | 4 | `(1, 1), (-1, 1), (1, -1), (-1, -1)` |
| 3 | `(2, 0)` | 4 | 4 | `(2, 0), (-2, 0), (0, 2), (0, -2)` |
| 4 | `(2, 1)` | 5 | 8 | `(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)` |
| 5 | `(2, 2)` | 8 | 4 | `(2, 2), (-2, 2), (2, -2), (-2, -2)` |
| 6 | `(3, 0)` | 9 | 4 | `(3, 0), (-3, 0), (0, 3), (0, -3)` |
| 7 | `(3, 1)` | 10 | 8 | `(3, 1), (-3, 1), (3, -1), (-3, -1), (1, 3), (-1, 3), (1, -3), (-1, -3)` |
| 8 | `(3, 2)` | 13 | 8 | `(3, 2), (-3, 2), (3, -2), (-3, -2), (2, 3), (-2, 3), (2, -3), (-2, -3)` |
| 9 | `(4, 0)` | 16 | 4 | `(4, 0), (-4, 0), (0, 4), (0, -4)` |
| 10 | `(4, 1)` | 17 | 8 | `(4, 1), (-4, 1), (4, -1), (-4, -1), (1, 4), (-1, 4), (1, -4), (-1, -4)` |
| 11 | `(3, 3)` | 18 | 4 | `(3, 3), (-3, 3), (3, -3), (-3, -3)` |
| 12 | `(4, 2)` | 20 | 8 | `(4, 2), (-4, 2), (4, -2), (-4, -2), (2, 4), (-2, 4), (2, -4), (-2, -4)` |
| 13 | `(4, 3)` | 25 | 8 | `(4, 3), (-4, 3), (4, -3), (-4, -3), (3, 4), (-3, 4), (3, -4), (-3, -4)` |
| 14 | `(5, 0)` | 25 | 4 | `(5, 0), (-5, 0), (0, 5), (0, -5)` |
| 15 | `(5, 1)` | 26 | 8 | `(5, 1), (-5, 1), (5, -1), (-5, -1), (1, 5), (-1, 5), (1, -5), (-1, -5)` |
| 16 | `(5, 2)` | 29 | 8 | `(5, 2), (-5, 2), (5, -2), (-5, -2), (2, 5), (-2, 5), (2, -5), (-2, -5)` |
| 17 | `(4, 4)` | 32 | 4 | `(4, 4), (-4, 4), (4, -4), (-4, -4)` |
| 18 | `(5, 3)` | 34 | 8 | `(5, 3), (-5, 3), (5, -3), (-5, -3), (3, 5), (-3, 5), (3, -5), (-3, -5)` |
| 19 | `(6, 0)` | 36 | 4 | `(6, 0), (-6, 0), (0, 6), (0, -6)` |
| 20 | `(6, 1)` | 37 | 8 | `(6, 1), (-6, 1), (6, -1), (-6, -1), (1, 6), (-1, 6), (1, -6), (-1, -6)` |
| 21 | `(6, 2)` | 40 | 8 | `(6, 2), (-6, 2), (6, -2), (-6, -2), (2, 6), (-2, 6), (2, -6), (-2, -6)` |
| 22 | `(5, 4)` | 41 | 8 | `(5, 4), (-5, 4), (5, -4), (-5, -4), (4, 5), (-4, 5), (4, -5), (-4, -5)` |
| 23 | `(6, 3)` | 45 | 8 | `(6, 3), (-6, 3), (6, -3), (-6, -3), (3, 6), (-3, 6), (3, -6), (-3, -6)` |
| 24 | `(7, 0)` | 49 | 4 | `(7, 0), (-7, 0), (0, 7), (0, -7)` |
| 25 | `(5, 5)` | 50 | 4 | `(5, 5), (-5, 5), (5, -5), (-5, -5)` |
| 26 | `(7, 1)` | 50 | 8 | `(7, 1), (-7, 1), (7, -1), (-7, -1), (1, 7), (-1, 7), (1, -7), (-1, -7)` |
| 27 | `(6, 4)` | 52 | 8 | `(6, 4), (-6, 4), (6, -4), (-6, -4), (4, 6), (-4, 6), (4, -6), (-4, -6)` |
| 28 | `(7, 2)` | 53 | 8 | `(7, 2), (-7, 2), (7, -2), (-7, -2), (2, 7), (-2, 7), (2, -7), (-2, -7)` |
| 29 | `(7, 3)` | 58 | 8 | `(7, 3), (-7, 3), (7, -3), (-7, -3), (3, 7), (-3, 7), (3, -7), (-3, -7)` |
| 30 | `(6, 5)` | 61 | 8 | `(6, 5), (-6, 5), (6, -5), (-6, -5), (5, 6), (-5, 6), (5, -6), (-5, -6)` |
| 31 | `(7, 4)` | 65 | 8 | `(7, 4), (-7, 4), (7, -4), (-7, -4), (4, 7), (-4, 7), (4, -7), (-4, -7)` |
| 32 | `(6, 6)` | 72 | 4 | `(6, 6), (-6, 6), (6, -6), (-6, -6)` |
| 33 | `(7, 5)` | 74 | 8 | `(7, 5), (-7, 5), (7, -5), (-7, -5), (5, 7), (-5, 7), (5, -7), (-5, -7)` |
| 34 | `(7, 6)` | 85 | 8 | `(7, 6), (-7, 6), (7, -6), (-7, -6), (6, 7), (-6, 7), (6, -7), (-6, -7)` |
| 35 | `(7, 7)` | 98 | 4 | `(7, 7), (-7, 7), (7, -7), (-7, -7)` |

The inventory contains 36 disjoint orbits and the multiplicities sum exactly to 225.
The immutable input builder and independent verifier must reconstruct both facts rather
than trust the table.

## Nested support prefixes

| Class ID | Limit | Active indices | Orbit count | Multiplicity sum | Newly admitted indices |
|---|---:|---|---:|---:|---|
| `support-r2-000` | 0 | `0` | 1 | 1 | `0` |
| `support-r2-001` | 1 | `0..1` | 2 | 5 | `1` |
| `support-r2-002` | 2 | `0..2` | 3 | 9 | `2` |
| `support-r2-004` | 4 | `0..3` | 4 | 13 | `3` |
| `support-r2-008` | 8 | `0..5` | 6 | 25 | `4..5` |
| `support-r2-018` | 18 | `0..11` | 12 | 61 | `6..11` |
| `support-r2-050` | 50 | `0..26` | 27 | 161 | `12..26` |
| `support-r2-098` | 98 | `0..35` | 36 | 225 | `27..35` |

For each class, the active mask is true exactly on the listed prefix. Inactive
coefficients are fixed to exact real zero in the common 36-coordinate space. Support
expansion never changes an earlier coordinate's identity, multiplicity, metric weight,
or coefficient bounds.

## Required reconstruction checks

The future producer and independent verifier must separately establish:

1. exact operation matrices and order;
2. closure of each orbit under all eight operations;
3. canonical-representative and first-occurrence member ordering;
4. disjoint complete coverage of every pair in `{-7, ..., 7}^2`;
5. multiplicities and total 225;
6. exact maximal coefficient order;
7. prefix masks, nestedness, and the eight multiplicity sums;
8. inclusion of the complete domain by `support-r2-098`; and
9. exact-zero inactive coordinates in every retained point.

A future generic orbit-enumeration kernel belongs to Numerics. This experiment owns the
specific operations, domain, order, and square-symmetry interpretation and will call the
owner contract directly once reviewed.
