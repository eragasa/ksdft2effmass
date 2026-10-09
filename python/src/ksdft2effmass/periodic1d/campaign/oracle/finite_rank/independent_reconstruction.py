"""Independent numerical reconstruction for finite-rank verification."""

from __future__ import annotations

import hashlib

import numpy as np
import numpy.typing as npt

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealArray = npt.NDArray[np.float64]


class FiniteRankOracleIndependentReconstructor:
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

    __slots__ = ("_decoder",)

    def __init__(self) -> None:
        """Bind shared JSON primitives without importing maintained numerical routes."""
        self._decoder = Periodic1DCampaignJsonDecoder()

    def rank_one_record(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        orbital: ComplexVector,
        site: int,
        magnitude: float,
        root_tolerance: float,
        edge_margin: float,
    ) -> dict[str, JsonValue]:
        """Implement the owner-local rank one record operation.

        Parameters
        ----------
        hoppings
            Ordered finite hopping coefficients or blocks in their declared displacement
            order.
        cell_count
            Exact number of cells in the finite periodic supercell.
        momentum
            Finite dimensionless reduced primitive-cell crystal momentum.
        orbital
            Normalized complex defect orbital in parent basis order.
        site
            Zero-based finite-supercell site index.
        magnitude
            Finite signed defect magnitude in the declared energy unit.
        root_tolerance
            Positive absolute tolerance for the finite secular equation.
        edge_margin
            Positive energy margin used to classify a finite eigenvalue as bound.

        Returns
        -------
        dict[str, JsonValue]
            Independently reconstructed rank-one result record.
        """
        edge = self._lower_edge(hoppings, cell_count, momentum)
        energy, lower, upper, residual, iterations = self._root(
            hoppings,
            cell_count,
            momentum,
            orbital,
            magnitude,
            edge,
            root_tolerance,
        )
        host = self._host(hoppings, cell_count, momentum)
        site_vector = self._site_vector(cell_count, site, orbital)
        # Construct the dense rank-one perturbation independently of the campaign's
        # maintained defect Action; only authenticated hopping observations are shared.
        defect = -magnitude * np.outer(site_vector, site_vector.conj())
        physical = host + defect
        values, vectors = np.linalg.eigh(physical)
        oracle_vector = self._bound_vector(
            hoppings, cell_count, momentum, energy, orbital, site
        )
        numerical_vector = vectors[:, 0]
        oracle_projector = np.outer(oracle_vector, oracle_vector.conj())
        numerical_projector = np.outer(numerical_vector, numerical_vector.conj())
        return {
            "id": f"rank-one-N{cell_count}-g{magnitude:.3f}",
            "status": "oracle_agreement",
            "cell_count": cell_count,
            "attractive_magnitude": magnitude,
            "operator_rank": int(np.linalg.matrix_rank(defect, tol=1.0e-12)),
            "host_lower_edge": edge,
            "host_edge_route_discrepancy": abs(
                edge - float(np.min(np.linalg.eigvalsh(host)))
            ),
            "oracle_energy": energy,
            "numerical_energy": float(values[0]),
            "binding_below_host_edge": edge - energy,
            "energy_absolute_discrepancy": abs(energy - float(values[0])),
            "oracle_secular_residual": residual,
            "oracle_final_bracket_width": upper - lower,
            "oracle_iteration_count": iterations,
            "numerical_bound_state_count": int(np.sum(values < edge - edge_margin)),
            "oracle_eigen_residual": self._norm(
                physical @ oracle_vector - energy * oracle_vector
            ),
            "projector_frobenius_defect": self._norm(
                oracle_projector - numerical_projector
            ),
            "state_fidelity": float(
                np.clip(
                    abs(np.vdot(oracle_vector, numerical_vector)) ** 2,
                    0.0,
                    1.0,
                )
            ),
            "defect_sha256": self._matrix_sha256(defect),
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }

    def special_records(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        momentum: float,
        orbital: ComplexVector,
        site: int,
        special: dict[str, JsonValue],
        root_tolerance: float,
        edge_margin: float,
    ) -> dict[str, JsonValue]:
        """Implement the owner-local special records operation.

        Parameters
        ----------
        hoppings
            Ordered finite hopping coefficients or blocks in their declared displacement
            order.
        momentum
            Finite dimensionless reduced primitive-cell crystal momentum.
        orbital
            Normalized complex defect orbital in parent basis order.
        site
            Zero-based finite-supercell site index.
        special
            Closed threshold, repulsive, and degeneracy controls.
        root_tolerance
            Positive absolute tolerance for the finite secular equation.
        edge_margin
            Positive energy margin used to classify a finite eigenvalue as bound.

        Returns
        -------
        dict[str, JsonValue]
            Independently reconstructed threshold, repulsive, and degeneracy records.
        """
        cell_count = self._decoder.integer(special["cell_count"], "special cell count")
        attractive = self._decoder.real(
            special["attractive_magnitude"], "special attraction"
        )
        repulsive = self._decoder.real(special["repulsive_magnitude"], "repulsion")
        threshold = self._decoder.real(special["threshold_magnitude"], "threshold")
        spin_count = self._decoder.integer(special["spin_degeneracy"], "spin count")
        host = self._host(hoppings, cell_count, momentum)
        edge = self._lower_edge(hoppings, cell_count, momentum)
        site_vector = self._site_vector(cell_count, site, orbital)
        threshold_count = int(np.sum(np.linalg.eigvalsh(host) < edge - edge_margin))
        probe = edge - max(edge_margin, 1.0e-4)
        green, green_imaginary = self._green(
            hoppings, cell_count, momentum, probe, orbital
        )
        repulsive_defect = repulsive * np.outer(site_vector, site_vector.conj())
        repulsive_count = int(
            np.sum(np.linalg.eigvalsh(host + repulsive_defect) < edge - edge_margin)
        )
        energy, _lower, _upper, _residual, _iterations = self._root(
            hoppings,
            cell_count,
            momentum,
            orbital,
            attractive,
            edge,
            root_tolerance,
        )
        spin_identity = np.eye(spin_count)
        spin_host = np.asarray(np.kron(host, spin_identity), dtype=np.complex128)
        spin_defect = -attractive * np.asarray(
            np.kron(np.outer(site_vector, site_vector.conj()), spin_identity),
            dtype=np.complex128,
        )
        values, vectors = np.linalg.eigh(spin_host + spin_defect)
        base_oracle = self._bound_vector(
            hoppings, cell_count, momentum, energy, orbital, site
        )
        oracle_columns = np.column_stack(
            [
                np.kron(base_oracle, spin_identity[:, index])
                for index in range(spin_count)
            ]
        )
        oracle_projector = oracle_columns @ oracle_columns.conj().T
        numerical_columns = vectors[:, :spin_count]
        numerical_projector = numerical_columns @ numerical_columns.conj().T
        degenerate: dict[str, JsonValue] = {
            "id": "spin-degenerate-rank-two-oracle",
            "status": "oracle_agreement",
            "cell_count": cell_count,
            "attractive_magnitude": attractive,
            "operator_rank": int(np.linalg.matrix_rank(spin_defect, tol=1.0e-12)),
            "oracle_eigenspace_rank": spin_count,
            "numerical_eigenspace_rank": spin_count,
            "numerical_bound_state_count": int(np.sum(values < edge - edge_margin)),
            "oracle_energy": energy,
            "maximum_energy_absolute_discrepancy": float(
                np.max(np.abs(values[:spin_count] - energy))
            ),
            "numerical_energy_splitting": float(np.ptp(values[:spin_count])),
            "projector_frobenius_defect": self._norm(
                oracle_projector - numerical_projector
            ),
            "individual_state_fidelity": None,
            "comparison_rule": "equal-rank eigenspace projectors",
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }
        return {
            "threshold": {
                "id": "zero-coupling-threshold",
                "status": "threshold_no_isolated_state",
                "attractive_magnitude": threshold,
                "oracle_root_energy": None,
                "numerical_bound_state_count": threshold_count,
                "edge_state_is_not_counted_as_bound": True,
            },
            "repulsive": {
                "id": "repulsive-no-lower-bound-state",
                "status": "no_bound_state_below_lower_edge",
                "repulsive_magnitude": repulsive,
                "oracle_root_energy": None,
                "secular_value_near_lower_edge": 1.0 + repulsive * green,
                "secular_imaginary_part": green_imaginary,
                "numerical_bound_state_count": repulsive_count,
                "scope": "below the finite-host lower edge only",
            },
            "spin_degenerate": degenerate,
            "unequal_rank": {
                "id": "spin-degenerate-rank-one-comparison",
                "status": "stopped",
                "issue_codes": ["ANALYTICAL_ORACLE.EIGENSPACE_RANK_MISMATCH"],
                "numerical_eigenspace_rank": spin_count,
                "oracle_eigenspace_rank": 1,
                "projector_frobenius_defect": None,
                "state_fidelity": None,
            },
        }

    def _root(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        orbital: ComplexVector,
        magnitude: float,
        edge: float,
        interval_tolerance: float,
    ) -> tuple[float, float, float, float, int]:
        """Implement the owner-local root operation."""

        def secular(energy: float) -> float:
            """Evaluate the independently reconstructed secular equation."""
            green, _imaginary = self._green(
                hoppings, cell_count, momentum, energy, orbital
            )
            return 1.0 - magnitude * green

        # Reimplement bracketing and bisection here so verifier agreement cannot be
        # produced by replaying the campaign's private root kernel.
        upper = edge - max(interval_tolerance, 1.0e-8)
        if secular(upper) >= 0.0:
            raise ValueError("independent root is not bracketed")
        distance = max(1.0, 4.0 * magnitude)
        lower = edge - distance
        while secular(lower) <= 0.0:
            distance *= 2.0
            lower = edge - distance
            if distance > 1.0e6:
                raise ValueError("independent bracketing failed")
        iterations = 0
        while iterations < 256:
            midpoint = 0.5 * (lower + upper)
            if midpoint == lower or midpoint == upper:
                break
            if secular(midpoint) > 0.0:
                lower = midpoint
            else:
                upper = midpoint
            iterations += 1
            if upper - lower <= interval_tolerance * 0.01:
                break
        energy = 0.5 * (lower + upper)
        return energy, lower, upper, abs(secular(energy)), iterations

    def _green(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        energy: float,
        orbital: ComplexVector,
    ) -> tuple[float, float]:
        """Implement the owner-local green operation."""
        value = 0.0 + 0.0j
        for index in range(cell_count):
            primitive = (momentum + index / cell_count) % 1.0
            solved = np.linalg.solve(
                self._bloch(hoppings, primitive) - energy * np.eye(2), orbital
            )
            value += complex(np.vdot(orbital, solved) / cell_count)
        return float(value.real), float(value.imag)

    def _bound_vector(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        energy: float,
        orbital: ComplexVector,
        site: int,
    ) -> ComplexVector:
        """Implement the owner-local bound vector operation."""
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        for index in range(cell_count):
            primitive = (momentum + index / cell_count) % 1.0
            fiber = np.linalg.solve(
                self._bloch(hoppings, primitive) - energy * np.eye(2), orbital
            ) / np.sqrt(cell_count)
            fiber *= np.exp(-2j * np.pi * primitive * site)
            for target in range(cell_count):
                result[2 * target : 2 * target + 2] += (
                    np.exp(2j * np.pi * primitive * target)
                    / np.sqrt(cell_count)
                    * fiber
                )
        return result / np.linalg.norm(result)

    def _lower_edge(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
    ) -> float:
        """Implement the owner-local lower edge operation."""
        return min(
            float(
                np.min(
                    np.linalg.eigvalsh(
                        self._bloch(hoppings, (momentum + index / cell_count) % 1.0)
                    )
                )
            )
            for index in range(cell_count)
        )

    def _bloch(
        self, hoppings: tuple[tuple[int, ComplexMatrix], ...], momentum: float
    ) -> ComplexMatrix:
        """Implement the owner-local bloch operation."""
        result = sum(
            (
                np.exp(2j * np.pi * momentum * displacement) * matrix
                for displacement, matrix in hoppings
            ),
            start=np.zeros((2, 2), dtype=np.complex128),
        )
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)

    def _host(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
    ) -> ComplexMatrix:
        """Implement the owner-local host operation."""
        result = np.zeros((2 * cell_count, 2 * cell_count), dtype=np.complex128)
        for source in range(cell_count):
            for displacement, matrix in hoppings:
                raw = source + displacement
                target = raw % cell_count
                # Count signed supercell seam crossings before wrapping the target;
                # this preserves the authored twist orientation for negative hops.
                crossings = (raw - target) // cell_count
                result[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += np.exp(2j * np.pi * momentum * cell_count * crossings) * matrix
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)

    def _site_vector(
        self, cell_count: int, site: int, orbital: ComplexVector
    ) -> ComplexVector:
        """Implement the owner-local site vector operation."""
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        result[2 * site : 2 * site + 2] = orbital
        return result

    def hoppings(
        self, composite: dict[str, JsonValue], group_id: str, hopping_range: int
    ) -> tuple[tuple[int, ComplexMatrix], ...]:
        """Adapt the selected authenticated parent hopping sequence.

        Parameters
        ----------
        composite
            Strictly decoded parent composite-result mapping.
        group_id
            Exact retained parent-band-group identity.
        hopping_range
            Nonnegative maximum primitive-cell hopping displacement.

        Returns
        -------
        tuple[tuple[int, ComplexMatrix], ...]
            Selected hopping blocks as ordered displacement–matrix pairs.

        Raises
        ------
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        groups = tuple(
            self._decoder.mapping(item, "groups")
            for item in self._decoder.array(composite["groups"], "groups")
        )
        matches = [item for item in groups if item["id"] == group_id]
        if len(matches) != 1:
            raise ValueError("parent group mismatch")
        result: list[tuple[int, ComplexMatrix]] = []
        hopping_values = self._decoder.array(
            matches[0]["smooth_hopping_blocks"], "hoppings"
        )
        for value in hopping_values:
            record = self._decoder.mapping(value, "hopping")
            displacement = self._decoder.integer(
                record["representative_cells"], "displacement"
            )
            if abs(displacement) <= hopping_range:
                result.append(
                    (
                        displacement,
                        self._decoder.complex_matrix(record["matrix"], "hopping"),
                    )
                )
        return tuple(result)

    def _matrix_sha256(self, matrix: ComplexMatrix) -> str:
        """Implement the owner-local matrix sha256 operation."""
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        # Normalize both signed-zero encodings before hashing the explicit little-endian
        # real/imaginary pair representation.
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    def _norm(self, value: ComplexMatrix | ComplexVector | RealArray) -> float:
        """Implement the owner-local norm operation."""
        return float(np.linalg.norm(value))
