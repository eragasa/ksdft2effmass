"""Base ownership and final boundaries for model-system analysis verification."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import final

from ksdft2effmass.serialization import BaseTypedRecord
from ksdft2effmass.verification import CompositeVerification

from .verification import BaseModelAnalysisVerification
from .visualization import BaseModelAnalysisVisualizationData


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

    The base owns exact subject bytes, computes their SHA-256 identity, and
    reconstructs the concrete typed result from those same bytes. Concrete verifiers
    own independent scientific comparisons, visualization projection, and aggregate
    composition.
    """

    __slots__ = ("_result", "_subject_sha256")

    _result: ResultT
    _subject_sha256: str

    @final
    def __init__(self, *, result_wire: bytes) -> None:
        """Bind one typed result to the identity of its exact input bytes.

        Parameters
        ----------
        result_wire
            Complete typed JSON bytes of the calculation result under verification.

        Raises
        ------
        TypeError
            ``result_wire`` is not a built-in ``bytes`` value or a decoded field has
            the wrong type.
        ValueError
            The JSON representation or a concrete result invariant is invalid.

        Notes
        -----
        The digest is calculated before deserialization from the same immutable bytes
        used to reconstruct the result. Callers cannot pair a decoded result with an
        unrelated digest.
        """
        if type(result_wire) is not bytes:
            raise TypeError("result_wire must be built-in bytes")
        self._subject_sha256 = hashlib.sha256(result_wire).hexdigest()
        self._result = self._result_type().from_json(result_wire)

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

    @final
    def admit_stored(
        self,
        *,
        verification: VerificationT,
        visualization_data: VisualizationDataT,
    ) -> ModelAnalysisVerificationResult[VerificationT, VisualizationDataT]:
        """Recompute and admit exact stored verification outputs.

        Parameters
        ----------
        verification
            Decoded stored aggregate proposed for later consumption.
        visualization_data
            Decoded stored projection proposed for later consumption.

        Returns
        -------
        ModelAnalysisVerificationResult[VerificationT, VisualizationDataT]
            Independently recomputed aggregate and projection. Stored values are
            admitted only when their canonical bytes match these values exactly.

        Raises
        ------
        TypeError
            A stored value does not belong to the required shared boundary or has a
            different concrete type from the independently reconstructed value.
        ValueError
            Stored canonical aggregate or projection bytes differ from independent
            reconstruction.

        Notes
        -----
        Exact comparison avoids a second, separately maintained inventory of every
        dynamically named observation. It also prevents rendering from trusting a
        structurally valid aggregate from which a required observation was removed.
        """
        if not isinstance(verification, BaseModelAnalysisVerification):
            raise TypeError("verification must be BaseModelAnalysisVerification")
        if not isinstance(
            visualization_data,
            BaseModelAnalysisVisualizationData,
        ):
            raise TypeError(
                "visualization_data must be BaseModelAnalysisVisualizationData"
            )
        expected = self.result()
        if type(verification) is not type(expected.verification):
            raise TypeError(
                "stored verification type differs from independent reconstruction"
            )
        if type(visualization_data) is not type(expected.visualization_data):
            raise TypeError(
                "stored visualization-data type differs from independent reconstruction"
            )
        if verification.to_json() != expected.verification.to_json():
            raise ValueError(
                "stored verification differs from independent reconstruction"
            )
        if visualization_data.to_json() != expected.visualization_data.to_json():
            raise ValueError(
                "stored visualization projection differs from independent "
                "reconstruction"
            )
        return expected
