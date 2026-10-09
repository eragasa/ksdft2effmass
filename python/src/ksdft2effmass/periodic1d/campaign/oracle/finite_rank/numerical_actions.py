"""Concrete numerical routes for the finite-rank-oracle campaign."""

from __future__ import annotations

import numpy as np

from ksdft2effmass.periodic1d.campaign.model.toy_defects import (
    Periodic1DPrimitiveFiberHamiltonianConstructor,
    Periodic1DPrimitiveFiberHamiltonianRequest,
    Periodic1DSupercellHamiltonianConstructor,
    Periodic1DSupercellHamiltonianRequest,
)

from .contracts import (
    ComplexMatrix,
    ComplexVector,
    FiniteRankOracleParentData,
    RankOneRootResult,
)


class FiniteRankSiteSpaceOperatorConstructor:
    """Identify one immutable source artifact.

    Parameters
    ----------
    path
        Nonempty repository-relative path of an authenticated compact source. sha256
        Lowercase 64-character SHA-256 content identity.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    __slots__ = ("_constructor",)

    def __init__(self) -> None:
        """Bind the maintained finite-hopping supercell constructor."""
        self._constructor = Periodic1DSupercellHamiltonianConstructor()

    def execute(
        self,
        parent: FiniteRankOracleParentData,
        cell_count: int,
        momentum: float,
    ) -> ComplexMatrix:
        """Construct and project one twisted finite site-space parent matrix.

        Parameters
        ----------
        parent
            Explicit parent contract or authenticated parent data used by the operation.
        cell_count
            Exact number of cells in the finite periodic supercell.
        momentum
            Finite dimensionless reduced primitive-cell crystal momentum.

        Returns
        -------
        ComplexMatrix
            Hermitian finite supercell parent matrix in site-major orbital order.

        Raises
        ------
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        result = self._constructor.execute(
            Periodic1DSupercellHamiltonianRequest(
                model=parent.model,
                cell_count=cell_count,
                reduced_momentum=momentum,
            )
        ).matrix
        antihermitian = np.linalg.norm(result - result.conj().T)
        if antihermitian > parent.model.hermiticity_tolerance:
            raise ValueError("supercell parent is not Hermitian")
        # Symmetrization removes only roundoff admitted by the explicit parent
        # tolerance; it must not repair a scientifically incompatible hopping sequence.
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)


class FiniteRankResolventOracle:
    """Own the bounded Bloch-resolvent oracle and scalar root algorithm.

    This is one concrete analytical route for the synthetic finite-rank campaign, not
    a registry, plugin point, generic oracle engine, qualification record, or acceptance
    mechanism.
    """

    __slots__ = ("_fiber_constructor",)

    def __init__(self) -> None:
        """Bind the maintained finite-hopping Bloch-fiber constructor."""
        self._fiber_constructor = Periodic1DPrimitiveFiberHamiltonianConstructor()

    def bloch_matrix(
        self, parent: FiniteRankOracleParentData, momentum: float
    ) -> ComplexMatrix:
        """Construct and project the Hermitian two-orbital Bloch fiber.

        Parameters
        ----------
        parent
            Explicit parent contract or authenticated parent data used by the operation.
        momentum
            Finite dimensionless reduced primitive-cell crystal momentum.

        Returns
        -------
        ComplexMatrix
            Hermitian two-orbital parent Bloch matrix.

        Raises
        ------
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        result = self._fiber_constructor.execute(
            Periodic1DPrimitiveFiberHamiltonianRequest(
                model=parent.model, reduced_momentum=momentum
            )
        ).matrix
        antihermitian = np.linalg.norm(result - result.conj().T)
        if antihermitian > parent.model.hermiticity_tolerance:
            raise ValueError("Bloch parent is not Hermitian")
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)

    def lower_edge(
        self,
        parent: FiniteRankOracleParentData,
        cell_count: int,
        supercell_momentum: float,
    ) -> float:
        """Return the lower edge of the represented finite host.

        Parameters
        ----------
        parent
            Explicit parent contract or authenticated parent data used by the operation.
        cell_count
            Exact number of cells in the finite periodic supercell.
        supercell_momentum
            Finite reduced crystal momentum of the supercell fiber.

        Returns
        -------
        float
            Minimum eigenvalue across the folded finite-host fibers.
        """
        edge = np.inf
        for index in range(cell_count):
            # These are the primitive momenta folded into the requested supercell
            # fiber; their order is part of the finite represented convention.
            momentum = (supercell_momentum + index / cell_count) % 1.0
            edge = min(
                edge,
                float(np.min(np.linalg.eigvalsh(self.bloch_matrix(parent, momentum)))),
            )
        return float(edge)

    def local_green(
        self,
        parent: FiniteRankOracleParentData,
        cell_count: int,
        supercell_momentum: float,
        energy: float,
        orbital: ComplexVector,
    ) -> tuple[float, float, float]:
        """Evaluate the local contraction, imaginary residual, and derivative.

        Parameters
        ----------
        parent
            Explicit parent contract or authenticated parent data used by the operation.
        cell_count
            Exact number of cells in the finite periodic supercell.
        supercell_momentum
            Finite reduced crystal momentum of the supercell fiber.
        energy
            Candidate bound-state energy in the declared campaign energy unit.
        orbital
            Normalized complex defect orbital in parent basis order.

        Returns
        -------
        tuple[float, float, float]
            Real local Green contraction, imaginary residual, and positive energy
            derivative.
        """
        value = 0.0 + 0.0j
        derivative = 0.0
        # Average <v|(H(k)-E)^-1|v> over the folded primitive fibers.  The
        # derivative is the positive norm-square identity below the host spectrum.
        for index in range(cell_count):
            momentum = (supercell_momentum + index / cell_count) % 1.0
            shifted = self.bloch_matrix(parent, momentum) - energy * np.eye(2)
            solved = np.linalg.solve(shifted, orbital)
            value += complex(np.vdot(orbital, solved) / cell_count)
            derivative += float(np.vdot(solved, solved).real) / cell_count
        return float(value.real), float(value.imag), derivative

    def bound_vector(
        self,
        parent: FiniteRankOracleParentData,
        cell_count: int,
        supercell_momentum: float,
        energy: float,
        orbital: ComplexVector,
        defect_site: int,
    ) -> ComplexVector:
        """Construct the normalized represented oracle bound-state vector.

        Parameters
        ----------
        parent
            Explicit parent contract or authenticated parent data used by the operation.
        cell_count
            Exact number of cells in the finite periodic supercell.
        supercell_momentum
            Finite reduced crystal momentum of the supercell fiber.
        energy
            Candidate bound-state energy in the declared campaign energy unit.
        orbital
            Normalized complex defect orbital in parent basis order.
        defect_site
            Zero-based defect-cell index in finite supercell order.

        Returns
        -------
        ComplexVector
            Normalized finite-site bound-state vector reconstructed from resolvent
            fibers.
        """
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        # Inverse-fold the resolvent fibers with the same positive site phase used
        # by the site-space representation and the compensating defect-site phase.
        for index in range(cell_count):
            momentum = (supercell_momentum + index / cell_count) % 1.0
            shifted = self.bloch_matrix(parent, momentum) - energy * np.eye(2)
            fiber = np.linalg.solve(shifted, orbital) / np.sqrt(cell_count)
            fiber *= np.exp(-2j * np.pi * momentum * defect_site)
            for site in range(cell_count):
                result[2 * site : 2 * site + 2] += (
                    np.exp(2j * np.pi * momentum * site) / np.sqrt(cell_count) * fiber
                )
        return result / np.linalg.norm(result)

    def resolve_root(
        self,
        parent: FiniteRankOracleParentData,
        cell_count: int,
        momentum: float,
        orbital: ComplexVector,
        magnitude: float,
        edge: float,
        interval_tolerance: float,
    ) -> RankOneRootResult:
        """Resolve the unique attractive secular root below the finite-host edge.

        Parameters
        ----------
        parent
            Explicit parent contract or authenticated parent data used by the operation.
        cell_count
            Exact number of cells in the finite periodic supercell.
        momentum
            Finite dimensionless reduced primitive-cell crystal momentum.
        orbital
            Normalized complex defect orbital in parent basis order.
        magnitude
            Finite signed defect magnitude in the declared energy unit.
        edge
            Lower parent-band edge in the declared energy unit.
        interval_tolerance
            Positive absolute stopping tolerance for the scalar root bracket.

        Returns
        -------
        RankOneRootResult
            Energy, final bracket, secular residual, and iteration count.

        Raises
        ------
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        if magnitude <= 0.0:
            raise ValueError("attractive magnitude must be positive")

        def secular(energy: float) -> float:
            """Evaluate the rank-one secular equation at one trial energy."""
            green, imaginary, _derivative = self.local_green(
                parent, cell_count, momentum, energy, orbital
            )
            if abs(imaginary) > 1.0e-9 * max(1.0, abs(green)):
                raise ValueError(
                    "resolvent acquired an unexpected relative imaginary part"
                )
            return 1.0 - magnitude * green

        # The attractive rank-one secular function is monotone on the interval below
        # the finite-host edge, so a sign-changing bracket supports bounded bisection.
        upper = edge - max(interval_tolerance, 1.0e-8)
        upper_value = secular(upper)
        if upper_value >= 0.0:
            raise ValueError("root is not bracketed below the host edge")
        distance = max(1.0, 4.0 * magnitude)
        lower = edge - distance
        lower_value = secular(lower)
        while lower_value <= 0.0:
            distance *= 2.0
            lower = edge - distance
            lower_value = secular(lower)
            if distance > 1.0e6:
                raise ValueError("failed to bracket the secular root")
        iterations = 0
        while iterations < 256:
            midpoint = 0.5 * (lower + upper)
            if midpoint == lower or midpoint == upper:
                break
            value = secular(midpoint)
            if value > 0.0:
                lower = midpoint
            else:
                upper = midpoint
            iterations += 1
            if upper - lower <= interval_tolerance * 0.01:
                break
        energy = 0.5 * (lower + upper)
        residual = abs(secular(energy))
        return RankOneRootResult(energy, lower, upper, residual, iterations)
