"""Base ownership and final boundaries for model-system analysis verification."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import final

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.verification import CompositeVerification

from .verification import BaseModelAnalysisVerification
from .visualization import BaseModelAnalysisVisualizationData


class BaseModelSystemAnalyzer:
    """Identify a model-system analyzer without imposing a shared operation."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class ModelAnalysisVerificationResult[
    VerificationT: BaseModelAnalysisVerification,
    VisualizationDataT: BaseModelAnalysisVisualizationData,
]:
    """Retain one verification value and authenticated visualization data.

    Parameters
    ----------
    verification
        Aggregate containing the authenticated projection digest.
    visualization_data
        Immutable projection whose canonical JSON bytes reproduce that digest.

    Raises
    ------
    TypeError
        Either value lies outside the model-analysis boundary.
    ValueError
        The stored digest differs from the projection's canonical JSON SHA-256.
    """

    verification: VerificationT
    visualization_data: VisualizationDataT

    def __post_init__(self) -> None:
        if not isinstance(self.verification, BaseModelAnalysisVerification):
            raise TypeError("verification must be BaseModelAnalysisVerification")
        if not isinstance(
            self.visualization_data,
            BaseModelAnalysisVisualizationData,
        ):
            raise TypeError(
                "visualization_data must be BaseModelAnalysisVisualizationData"
            )
        calculated_digest = hashlib.sha256(
            self.visualization_data.to_json()
        ).hexdigest()
        authenticated_digest = (
            self.verification.authenticated_visualization_data_sha256()
        )
        if type(authenticated_digest) is not str:
            raise TypeError(
                "authenticated visualization-data digest must be a built-in string"
            )
        if authenticated_digest != calculated_digest:
            raise ValueError(
                "verification and visualization-data SHA-256 digests differ"
            )


class BaseModelAnalysisVerifier[
    ResultT: BaseTypedRecord,
    VerificationT: BaseModelAnalysisVerification,
    VisualizationDataT: BaseModelAnalysisVisualizationData,
](ABC):
    """Bind, verify, and authenticate one typed model-analysis result.

    The base owns validation of the decoded subject mapping and its exact SHA-256
    identity. Concrete verifiers own result reconstruction, independent scientific
    comparisons, visualization projection, and aggregate composition.
    """

    __slots__ = ("_result", "_subject_sha256")

    _result: ResultT
    _subject_sha256: str

    @final
    def __init__(
        self,
        *,
        result: Mapping[str, SerializableValue],
        subject_sha256: str,
    ) -> None:
        """Bind a typed decoded result to its exact subject digest.

        Parameters
        ----------
        result
            String-keyed mapping decoded by the shared typed JSON deserializer.
        subject_sha256
            Lowercase SHA-256 digest of the exact result bytes under verification.

        Raises
        ------
        TypeError
            ``result`` is not a mapping or a key is not a built-in string.
        ValueError
            The digest is malformed or concrete result reconstruction fails.
        """
        if not isinstance(result, Mapping):
            raise TypeError("result must be a mapping")
        if (
            type(subject_sha256) is not str
            or len(subject_sha256) != 64
            or any(character not in "0123456789abcdef" for character in subject_sha256)
        ):
            raise ValueError("subject_sha256 must be a lowercase SHA-256 digest")
        copied: dict[str, SerializableValue] = {}
        for name, value in result.items():
            if type(name) is not str:
                raise TypeError("result keys must be built-in strings")
            copied[name] = value
        self._result = self._result_type().from_dict(copied)
        self._subject_sha256 = subject_sha256

    @classmethod
    @abstractmethod
    def _result_type(cls) -> type[ResultT]:
        """Return the concrete typed root result reconstructed by the verifier."""

    @abstractmethod
    def _visualization_data(self) -> VisualizationDataT:
        """Derive visualization data from authoritative analysis values."""

    @abstractmethod
    def _verification_types(
        self,
    ) -> tuple[type[CompositeVerification], ...]:
        """Return the exact ordered reusable verification class inventory."""

    @abstractmethod
    def _verification_components(
        self,
        visualization_data: VisualizationDataT,
    ) -> tuple[CompositeVerification, ...]:
        """Calculate verification values for the exact authenticated projection."""

    @abstractmethod
    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> VerificationT:
        """Compose the concrete aggregate from reusable verification values."""

    @final
    def result(
        self,
    ) -> ModelAnalysisVerificationResult[VerificationT, VisualizationDataT]:
        """Derive, authenticate, and verify one visualization projection.

        Returns
        -------
        ModelAnalysisVerificationResult[VerificationT, VisualizationDataT]
            Concrete aggregate verification paired with the exact typed projection
            whose canonical JSON digest it authenticates.

        Raises
        ------
        TypeError
            A concrete owner returns a value outside its declared domain contract.
        ValueError
            Component types, observation names, projection digest, or a concrete
            scientific invariant differs from the declared inventory.

        Notes
        -----
        The final order is derive projection, digest canonical projection bytes,
        calculate operation-specific components, and compose the aggregate. Concrete
        verifiers cannot accept a caller-authored projection digest.
        """
        visualization_data = self._visualization_data()
        visualization_data_sha256 = hashlib.sha256(
            visualization_data.to_json()
        ).hexdigest()
        component_types = self._verification_types()
        components = self._verification_components(visualization_data)
        if len(components) != len(component_types) or any(
            type(component) is not component_type
            for component, component_type in zip(
                components,
                component_types,
                strict=True,
            )
        ):
            raise ValueError(
                "calculated verification components must match the declared inventory"
            )
        observation_names: set[str] = set()
        for component in components:
            overlap = observation_names.intersection(component.observations)
            if overlap:
                raise ValueError(
                    "verification observation names must be globally unique"
                )
            observation_names.update(component.observations)
        verification = self._verification(
            visualization_data_sha256=visualization_data_sha256,
            components=components,
        )
        return ModelAnalysisVerificationResult(
            verification=verification,
            visualization_data=visualization_data,
        )
