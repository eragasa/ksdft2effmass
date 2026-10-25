"""PIAB1D diagnostic actions and their immutable aggregate."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum, auto
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import MatrixNorm
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.diagnostics import (
    BaseDiagnosticAnalyzer,
    DiagnosticObservation,
    MatrixNormDiagnosticOptions,
)
from ksdft2effmass.serialization import (
    SerializableValue,
    TypedJsonMappingDeserializer,
    TypedJsonMappingSerializer,
)


class DiagnosticMethodsEnum(Enum):
    """Identify each diagnostic retained by the PIAB1D analysis."""

    discrete_spectrum_maximum_absolute_error = auto()
    scaled_eigenpair_residuals = auto()
    spectral_reconstruction_error = auto()
    projector_idempotency_error = auto()
    weighted_gram_error = auto()
    weighted_projector_error = auto()


diagnostic_method_names: Mapping[DiagnosticMethodsEnum, str] = MappingProxyType(
    {method: method.name for method in DiagnosticMethodsEnum}
)


class DiscreteSpectrumMaximumAbsoluteErrorAnalyzer(
    BaseDiagnosticAnalyzer[DiagnosticMethodsEnum]
):
    """Compare a represented PIAB1D spectrum with its discrete closed form."""

    __slots__ = ("_atol", "_computed", "_reference", "_rtol")

    def __init__(
        self,
        computed: VectorQuantity,
        reference: VectorQuantity,
        atol: ScalarQuantity,
        rtol: float,
    ) -> None:
        if not isinstance(computed, VectorQuantity):
            raise TypeError("computed must be VectorQuantity")
        if not isinstance(reference, VectorQuantity):
            raise TypeError("reference must be VectorQuantity")
        if computed.unit != reference.unit:
            raise ValueError("computed and reference spectra must use the same unit")
        if computed.magnitude.shape != reference.magnitude.shape:
            raise ValueError("computed and reference spectra must have the same shape")
        self._computed = computed
        self._reference = reference
        self._atol = atol
        self._rtol = rtol

    @property
    def method(self) -> DiagnosticMethodsEnum:
        """Return the discrete-spectrum diagnostic identity.

        Returns
        -------
        DiagnosticMethodsEnum
            ``discrete_spectrum_maximum_absolute_error``.
        """
        return DiagnosticMethodsEnum.discrete_spectrum_maximum_absolute_error

    def result(self) -> DiagnosticObservation:
        """Evaluate the maximum absolute discrete-spectrum error.

        Returns
        -------
        DiagnosticObservation
            Energy-valued maximum discrepancy with the configured tolerance.
        """
        value = ScalarQuantity(
            float(np.max(np.abs(self._computed.magnitude - self._reference.magnitude))),
            self._computed.unit,
        )
        return DiagnosticObservation(
            value=value,
            atol=self._atol,
            rtol=self._rtol,
        )


class ScaledEigenpairResidualAnalyzer(BaseDiagnosticAnalyzer[DiagnosticMethodsEnum]):
    """Retain the precomputed scale-safe eigenpair residual observations."""

    __slots__ = ("_atol", "_residuals", "_rtol")

    def __init__(
        self,
        residuals: VectorQuantity,
        atol: ScalarQuantity,
        rtol: float,
    ) -> None:
        if not isinstance(residuals, VectorQuantity):
            raise TypeError("residuals must be VectorQuantity")
        if not isinstance(residuals.unit, Unitless):
            raise ValueError("scaled eigenpair residuals must be unitless")
        self._residuals = residuals
        self._atol = atol
        self._rtol = rtol

    @property
    def method(self) -> DiagnosticMethodsEnum:
        """Return the scaled-eigenpair-residual diagnostic identity.

        Returns
        -------
        DiagnosticMethodsEnum
            ``scaled_eigenpair_residuals``.
        """
        return DiagnosticMethodsEnum.scaled_eigenpair_residuals

    def result(self) -> DiagnosticObservation:
        """Return the scale-safe eigenpair residual observation.

        Returns
        -------
        DiagnosticObservation
            Unitless residual vector with the configured tolerance.
        """
        return DiagnosticObservation(
            value=self._residuals,
            atol=self._atol,
            rtol=self._rtol,
        )


class SpectralReconstructionErrorAnalyzer(
    BaseDiagnosticAnalyzer[DiagnosticMethodsEnum]
):
    """Measure reconstruction of a Hamiltonian from its represented eigensystem."""

    __slots__ = (
        "_atol",
        "_eigenvalues",
        "_eigenvectors",
        "_hamiltonian",
        "_options",
        "_rtol",
    )

    def __init__(
        self,
        hamiltonian: MatrixQuantity,
        eigenvalues: VectorQuantity,
        eigenvectors: MatrixQuantity,
        atol: ScalarQuantity,
        rtol: float,
        options: MatrixNormDiagnosticOptions,
    ) -> None:
        if not isinstance(hamiltonian, MatrixQuantity):
            raise TypeError("hamiltonian must be MatrixQuantity")
        if not isinstance(eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(eigenvectors, MatrixQuantity):
            raise TypeError("eigenvectors must be MatrixQuantity")
        if hamiltonian.unit != eigenvalues.unit:
            raise ValueError("hamiltonian and eigenvalues must use the same unit")
        if not isinstance(eigenvectors.unit, Unitless):
            raise ValueError("eigenvectors must be unitless")
        dimension = hamiltonian.magnitude.shape[0]
        if hamiltonian.magnitude.shape != (dimension, dimension):
            raise ValueError("hamiltonian must be square")
        if eigenvalues.magnitude.shape != (dimension,):
            raise ValueError("eigenvalues must match the Hamiltonian dimension")
        if eigenvectors.magnitude.shape != (dimension, dimension):
            raise ValueError("eigenvectors must match the Hamiltonian dimension")
        self._hamiltonian = hamiltonian
        self._eigenvalues = eigenvalues
        self._eigenvectors = eigenvectors
        self._atol = atol
        self._rtol = rtol
        self._options = options

    @property
    def method(self) -> DiagnosticMethodsEnum:
        """Return the spectral-reconstruction diagnostic identity.

        Returns
        -------
        DiagnosticMethodsEnum
            ``spectral_reconstruction_error``.
        """
        return DiagnosticMethodsEnum.spectral_reconstruction_error

    def result(self) -> DiagnosticObservation:
        """Evaluate the selected spectral-reconstruction residual norm.

        Returns
        -------
        DiagnosticObservation
            Energy-valued matrix-norm discrepancy and declared tolerance.
        """
        residual = MatrixQuantity(
            self._hamiltonian.magnitude
            - self._eigenvectors.magnitude
            @ np.diag(self._eigenvalues.magnitude)
            @ self._eigenvectors.magnitude.T,
            self._hamiltonian.unit,
        )
        return DiagnosticObservation(
            value=MatrixNorm(residual, self._options.matrix_norm).result(),
            atol=self._atol,
            rtol=self._rtol,
            options=self._options,
        )


class ProjectorIdempotencyAnalyzer(BaseDiagnosticAnalyzer[DiagnosticMethodsEnum]):
    """Measure idempotency of one represented orthogonal projector."""

    __slots__ = ("_atol", "_options", "_projector", "_rtol")

    def __init__(
        self,
        projector: MatrixQuantity,
        atol: ScalarQuantity,
        rtol: float,
        options: MatrixNormDiagnosticOptions,
    ) -> None:
        if not isinstance(projector, MatrixQuantity):
            raise TypeError("projector must be MatrixQuantity")
        if not isinstance(projector.unit, Unitless):
            raise ValueError("projector must be unitless")
        dimension = projector.magnitude.shape[0]
        if projector.magnitude.shape != (dimension, dimension):
            raise ValueError("projector must be square")
        self._projector = projector
        self._atol = atol
        self._rtol = rtol
        self._options = options

    @property
    def method(self) -> DiagnosticMethodsEnum:
        """Return the projector-idempotency diagnostic identity.

        Returns
        -------
        DiagnosticMethodsEnum
            ``projector_idempotency_error``.
        """
        return DiagnosticMethodsEnum.projector_idempotency_error

    def result(self) -> DiagnosticObservation:
        """Evaluate the selected projector-idempotency residual norm.

        Returns
        -------
        DiagnosticObservation
            Unitless norm of ``P @ P - P`` and declared tolerance.
        """
        residual = MatrixQuantity(
            self._projector.magnitude @ self._projector.magnitude
            - self._projector.magnitude,
            self._projector.unit,
        )
        return DiagnosticObservation(
            value=MatrixNorm(residual, self._options.matrix_norm).result(),
            atol=self._atol,
            rtol=self._rtol,
            options=self._options,
        )


class WeightedGramErrorAnalyzer(BaseDiagnosticAnalyzer[DiagnosticMethodsEnum]):
    """Measure deviation of the retained weighted Gram matrix from identity."""

    __slots__ = ("_atol", "_options", "_rtol", "_weighted_gram")

    def __init__(
        self,
        weighted_gram: MatrixQuantity,
        atol: ScalarQuantity,
        rtol: float,
        options: MatrixNormDiagnosticOptions,
    ) -> None:
        if not isinstance(weighted_gram, MatrixQuantity):
            raise TypeError("weighted_gram must be MatrixQuantity")
        if not isinstance(weighted_gram.unit, Unitless):
            raise ValueError("weighted_gram must be unitless")
        dimension = weighted_gram.magnitude.shape[0]
        if weighted_gram.magnitude.shape != (dimension, dimension):
            raise ValueError("weighted_gram must be square")
        self._weighted_gram = weighted_gram
        self._atol = atol
        self._rtol = rtol
        self._options = options

    @property
    def method(self) -> DiagnosticMethodsEnum:
        """Return the weighted-Gram diagnostic identity.

        Returns
        -------
        DiagnosticMethodsEnum
            ``weighted_gram_error``.
        """
        return DiagnosticMethodsEnum.weighted_gram_error

    def result(self) -> DiagnosticObservation:
        """Evaluate the selected weighted-Gram residual norm.

        Returns
        -------
        DiagnosticObservation
            Unitless norm of the retained weighted-Gram discrepancy.
        """
        residual = MatrixQuantity(
            self._weighted_gram.magnitude
            - np.eye(self._weighted_gram.magnitude.shape[0]),
            self._weighted_gram.unit,
        )
        return DiagnosticObservation(
            value=MatrixNorm(residual, self._options.matrix_norm).result(),
            atol=self._atol,
            rtol=self._rtol,
            options=self._options,
        )


class WeightedProjectorErrorAnalyzer(BaseDiagnosticAnalyzer[DiagnosticMethodsEnum]):
    """Measure agreement of quadrature and Euclidean projectors."""

    __slots__ = ("_atol", "_options", "_projector", "_rtol", "_weighted_projector")

    def __init__(
        self,
        weighted_projector: MatrixQuantity,
        projector: MatrixQuantity,
        atol: ScalarQuantity,
        rtol: float,
        options: MatrixNormDiagnosticOptions,
    ) -> None:
        if not isinstance(weighted_projector, MatrixQuantity):
            raise TypeError("weighted_projector must be MatrixQuantity")
        if not isinstance(projector, MatrixQuantity):
            raise TypeError("projector must be MatrixQuantity")
        if not isinstance(weighted_projector.unit, Unitless) or not isinstance(
            projector.unit, Unitless
        ):
            raise ValueError("weighted and Euclidean projectors must be unitless")
        if weighted_projector.magnitude.shape != projector.magnitude.shape:
            raise ValueError(
                "weighted and Euclidean projectors must have the same shape"
            )
        dimension = projector.magnitude.shape[0]
        if projector.magnitude.shape != (dimension, dimension):
            raise ValueError("projectors must be square")
        self._weighted_projector = weighted_projector
        self._projector = projector
        self._atol = atol
        self._rtol = rtol
        self._options = options

    @property
    def method(self) -> DiagnosticMethodsEnum:
        """Return the weighted-projector diagnostic identity.

        Returns
        -------
        DiagnosticMethodsEnum
            ``weighted_projector_error``.
        """
        return DiagnosticMethodsEnum.weighted_projector_error

    def result(self) -> DiagnosticObservation:
        """Evaluate the selected weighted-projector residual norm.

        Returns
        -------
        DiagnosticObservation
            Unitless discrepancy between weighted and Euclidean projectors.
        """
        residual = MatrixQuantity(
            self._weighted_projector.magnitude - self._projector.magnitude,
            self._weighted_projector.unit,
        )
        return DiagnosticObservation(
            value=MatrixNorm(residual, self._options.matrix_norm).result(),
            atol=self._atol,
            rtol=self._rtol,
            options=self._options,
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dDiagnostics:
    """Retain the complete immutable PIAB1D diagnostic inventory."""

    observations: Mapping[DiagnosticMethodsEnum, DiagnosticObservation]

    def __post_init__(self) -> None:
        if not isinstance(self.observations, Mapping):
            raise TypeError("observations must be a mapping")
        if set(self.observations) != set(DiagnosticMethodsEnum):
            raise ValueError("observations must contain every PIAB1D diagnostic")
        copied: dict[DiagnosticMethodsEnum, DiagnosticObservation] = {}
        matrix_methods = {
            DiagnosticMethodsEnum.spectral_reconstruction_error,
            DiagnosticMethodsEnum.projector_idempotency_error,
            DiagnosticMethodsEnum.weighted_gram_error,
            DiagnosticMethodsEnum.weighted_projector_error,
        }
        for method, observation in self.observations.items():
            if not isinstance(method, DiagnosticMethodsEnum):
                raise TypeError("observation keys must be DiagnosticMethodsEnum")
            if not isinstance(observation, DiagnosticObservation):
                raise TypeError("observation values must be DiagnosticObservation")
            if method in matrix_methods and observation.options is None:
                raise ValueError("matrix diagnostics must declare matrix-norm options")
            if method not in matrix_methods and observation.options is not None:
                raise ValueError("non-matrix diagnostics must not declare options")
            copied[method] = observation
        object.__setattr__(self, "observations", MappingProxyType(copied))

    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return observations keyed by stable diagnostic names.

        Returns
        -------
        Mapping[str, SerializableValue]
            Complete six-observation typed diagnostic mapping.
        """
        return {
            diagnostic_method_names[method]: observation
            for method, observation in self.observations.items()
        }

    @classmethod
    def from_dict(cls, values: Mapping[str, SerializableValue]) -> Piab1dDiagnostics:
        """Reconstruct the complete diagnostics aggregate.

        Parameters
        ----------
        values
            Typed mapping keyed by the six stable diagnostic names.

        Returns
        -------
        Piab1dDiagnostics
            Immutable validated aggregate.

        Raises
        ------
        TypeError
            The root or an observation has the wrong type.
        ValueError
            The diagnostic inventory is incomplete, duplicated, or unknown.
        """
        if not isinstance(values, Mapping):
            raise TypeError("values must be a mapping")
        methods_by_name = {
            name: method for method, name in diagnostic_method_names.items()
        }
        if set(values) != set(methods_by_name):
            raise ValueError("diagnostic names do not match the PIAB1D inventory")
        observations: dict[DiagnosticMethodsEnum, DiagnosticObservation] = {}
        for name, value in values.items():
            if not isinstance(value, Mapping):
                raise TypeError("diagnostic observations must be typed mappings")
            observations[methods_by_name[name]] = DiagnosticObservation.from_dict(value)
        return cls(observations=observations)

    def to_json(self) -> bytes:
        """Serialize the aggregate to canonical typed JSON bytes.

        Returns
        -------
        bytes
            Canonical UTF-8 diagnostic representation.
        """
        return TypedJsonMappingSerializer().serialize(self.to_dict())

    @classmethod
    def from_json(cls, wire: bytes) -> Piab1dDiagnostics:
        """Reconstruct diagnostics from canonical typed JSON bytes.

        Parameters
        ----------
        wire
            UTF-8 typed JSON bytes.

        Returns
        -------
        Piab1dDiagnostics
            Immutable complete diagnostic aggregate.

        Raises
        ------
        TypeError
            The wire or a decoded value has the wrong type.
        ValueError
            JSON metadata or diagnostic inventory is invalid.
        """
        values = TypedJsonMappingDeserializer().deserialize(wire)
        return cls.from_dict(values)
