"""Typed adoption of retained periodic-1D isolated-band replay artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import cast

import numpy as np
import numpy.typing as npt

from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitter1D,
    BlockHoppingModelComparator1D,
)
from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.operators import (
    Basis,
    ComplexMatrixQuantity,
    EnergyReference,
    Geometry,
    OperatorRecord,
    ScalarQuantity,
    StateSpace,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import (
    PeriodicHermiticityStatus,
    PeriodicOperatorReference,
    PeriodicRepresentedRetainedOperator,
    PeriodicRepresentedRetainedOperatorConstructor,
    PeriodicRetainedOperator,
    PeriodicRetainedOperatorConstructionKind,
    PeriodicRetainedOperatorConstructor,
    PeriodicRetainedSubspace,
    PeriodicRetainedSubspaceConstructor,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import (
    Periodic1DBandFrameRetainedSubspace,
    Periodic1DCompleteHoppingRepresentationResult,
    Periodic1DFittedHoppingEffectiveModelResult,
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DSelectedBandRetentionDefinition,
    Periodic1DTruncatedHoppingEffectiveModelResult,
)
from ksdft2effmass.solid_state import (
    BlockHoppingModel1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    PlaneWaveReciprocalSewingConstructor,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorFourierTransformer1D,
)

from .isolated import (
    Periodic1DIsolatedBandCampaignDefinition,
    Periodic1DIsolatedBandCampaignJsonSerializer,
)
from .isolated_results import Periodic1DIsolatedBandCampaignResult

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexArray = npt.NDArray[np.complex128]

PERIODIC_1D_ISOLATED_BAND_DEFAULT_ABSOLUTE_TOLERANCE = ScalarQuantity(
    1.0e-10, Unitless()
)
"""Default unitless tolerance inherited from the retained campaign verifier."""


@dataclass(frozen=True, slots=True)
class Periodic1DReplaySourceCorrelation:
    """Retain SHA-256 identities proving correlation to immutable replay sources."""

    input_sha256: str
    reference_result_sha256: str
    producer_script_sha256: str
    replay_script_sha256: str
    replayed_result_sha256: str
    exact_result_bytes_match: bool

    def __post_init__(self) -> None:
        """Validate exact digest syntax and replay-result agreement."""
        for name, value in (
            ("input_sha256", self.input_sha256),
            ("reference_result_sha256", self.reference_result_sha256),
            ("producer_script_sha256", self.producer_script_sha256),
            ("replay_script_sha256", self.replay_script_sha256),
            ("replayed_result_sha256", self.replayed_result_sha256),
        ):
            if type(value) is not str or len(value) != 64:
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
            if any(character not in "0123456789abcdef" for character in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        if type(self.exact_result_bytes_match) is not bool:
            raise TypeError("exact_result_bytes_match must be a built-in bool")
        if not self.exact_result_bytes_match:
            raise ValueError("replay artifacts require exact retained-result agreement")
        if self.replayed_result_sha256 != self.reference_result_sha256:
            raise ValueError("replayed and retained result identities must agree")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRangeEffectiveModelArtifacts:
    """Retain separate truncated and fitted coefficient models for one range."""

    hopping_range_cells: int
    truncated_model: BlockHoppingModel1D
    fitted_model: BlockHoppingModel1D
    truncated_coefficients_content_sha256: str
    fitted_coefficients_content_sha256: str

    def __post_init__(self) -> None:
        """Validate range, scalar model dimensions, representatives, and digests."""
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be a nonnegative built-in int")
        if type(self.truncated_model) is not BlockHoppingModel1D:
            raise TypeError("truncated_model must be BlockHoppingModel1D")
        if type(self.fitted_model) is not BlockHoppingModel1D:
            raise TypeError("fitted_model must be BlockHoppingModel1D")
        expected = tuple(range(-self.hopping_range_cells, self.hopping_range_cells + 1))
        if self.truncated_model.representatives != expected:
            raise ValueError("truncated representatives must match the declared range")
        if self.fitted_model.representatives != expected:
            raise ValueError("fitted representatives must match the declared range")
        if (
            self.truncated_model.matrix_dimension != 1
            or self.fitted_model.matrix_dimension != 1
        ):
            raise ValueError("isolated-band effective models must be scalar")
        for name, value in (
            (
                "truncated_coefficients_content_sha256",
                self.truncated_coefficients_content_sha256,
            ),
            (
                "fitted_coefficients_content_sha256",
                self.fitted_coefficients_content_sha256,
            ),
        ):
            if type(value) is not str or len(value) != 64:
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
            if any(character not in "0123456789abcdef" for character in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandReplayArtifacts:
    """Retain authenticated frame/projector and effective-model replay data."""

    experiment_id: str
    source_payload: bytes
    source_payload_sha256: str
    source_correlation: Periodic1DReplaySourceCorrelation
    frame_path: ReciprocalBandFramePath1D
    frame_content_sha256: str
    projector_path_content_sha256: str
    complete_hopping_model: BlockHoppingModel1D
    complete_coefficients_content_sha256: str
    range_artifacts: tuple[Periodic1DRangeEffectiveModelArtifacts, ...]

    def __post_init__(self) -> None:
        """Validate immutable payload identity and typed artifact inventory."""
        if type(self.experiment_id) is not str or not self.experiment_id:
            raise ValueError("experiment_id must be a nonempty built-in str")
        if type(self.source_payload) is not bytes:
            raise TypeError("source_payload must be bytes")
        if (
            hashlib.sha256(self.source_payload).hexdigest()
            != self.source_payload_sha256
        ):
            raise ValueError("source_payload_sha256 must authenticate source_payload")
        if type(self.source_correlation) is not Periodic1DReplaySourceCorrelation:
            raise TypeError("source_correlation has the wrong exact type")
        if type(self.frame_path) is not ReciprocalBandFramePath1D:
            raise TypeError("frame_path must be ReciprocalBandFramePath1D")
        if self.frame_path.rank != 1:
            raise ValueError("isolated-band replay frame must have rank one")
        if type(self.complete_hopping_model) is not BlockHoppingModel1D:
            raise TypeError("complete_hopping_model must be BlockHoppingModel1D")
        if self.complete_hopping_model.matrix_dimension != 1:
            raise ValueError("isolated-band complete hopping model must be scalar")
        if not isinstance(self.range_artifacts, tuple) or not self.range_artifacts:
            raise TypeError("range_artifacts must be a nonempty tuple")
        if any(
            type(value) is not Periodic1DRangeEffectiveModelArtifacts
            for value in self.range_artifacts
        ):
            raise TypeError("range_artifacts members have the wrong exact type")
        ranges = tuple(value.hopping_range_cells for value in self.range_artifacts)
        if ranges != tuple(sorted(set(ranges))):
            raise ValueError("effective-model ranges must be unique and increasing")
        for name, value in (
            ("frame_content_sha256", self.frame_content_sha256),
            ("projector_path_content_sha256", self.projector_path_content_sha256),
            (
                "complete_coefficients_content_sha256",
                self.complete_coefficients_content_sha256,
            ),
        ):
            if type(value) is not str or len(value) != 64:
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
            if any(character not in "0123456789abcdef" for character in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRangeEffectiveModelAdoption:
    """Bind retained coefficients to explicit truncation and fitting routes."""

    hopping_range_cells: int
    truncated: Periodic1DTruncatedHoppingEffectiveModelResult
    fitted: Periodic1DFittedHoppingEffectiveModelResult

    def __post_init__(self) -> None:
        """Validate one exact range and route-result pair."""
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be a nonnegative built-in int")
        if type(self.truncated) is not Periodic1DTruncatedHoppingEffectiveModelResult:
            raise TypeError("truncated has the wrong exact result type")
        if type(self.fitted) is not Periodic1DFittedHoppingEffectiveModelResult:
            raise TypeError("fitted has the wrong exact result type")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandScientificAdoptionRequest:
    """Declare correlated replay sources under the documented default tolerance.

    ``absolute_tolerance`` defaults to the campaign's retained ordinary numerical
    verification policy, :math:`10^{-10}` in dimensionless reciprocal-energy units.
    It applies independently to reciprocal-coordinate agreement, full-mesh
    reconstruction, and coefficient-route reconciliation. It is not a scientific
    validation or uncertainty-quantification threshold.
    """

    definition: Periodic1DIsolatedBandCampaignDefinition
    result: Periodic1DIsolatedBandCampaignResult
    replay: Periodic1DIsolatedBandReplayArtifacts
    absolute_tolerance: ScalarQuantity = (
        PERIODIC_1D_ISOLATED_BAND_DEFAULT_ABSOLUTE_TOLERANCE
    )

    def __post_init__(self) -> None:
        """Validate exact sources and the finite nonnegative unitless tolerance."""
        if type(self.definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition has the wrong exact type")
        if type(self.result) is not Periodic1DIsolatedBandCampaignResult:
            raise TypeError("result has the wrong exact type")
        if type(self.replay) is not Periodic1DIsolatedBandReplayArtifacts:
            raise TypeError("replay has the wrong exact type")
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must be unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandScientificAdoptionResult:
    """Retain the migrated scientific hierarchy and all effective-model routes."""

    parent_model: Periodic1DFourierHamiltonianToyModel
    selected_bands: Periodic1DSelectedBandRetentionDefinition
    retained_subspace: PeriodicRetainedSubspace
    represented_subspace: Periodic1DBandFrameRetainedSubspace
    retained_operator: PeriodicRetainedOperator
    represented_zone_center_operator: PeriodicRepresentedRetainedOperator
    complete_hopping: Periodic1DCompleteHoppingRepresentationResult
    effective_models: tuple[Periodic1DRangeEffectiveModelAdoption, ...]

    def __post_init__(self) -> None:
        """Validate exact types and shared retained-space/operator identities."""
        expected_types = (
            (self.parent_model, Periodic1DFourierHamiltonianToyModel),
            (self.selected_bands, Periodic1DSelectedBandRetentionDefinition),
            (self.retained_subspace, PeriodicRetainedSubspace),
            (self.represented_subspace, Periodic1DBandFrameRetainedSubspace),
            (self.retained_operator, PeriodicRetainedOperator),
            (
                self.represented_zone_center_operator,
                PeriodicRepresentedRetainedOperator,
            ),
            (self.complete_hopping, Periodic1DCompleteHoppingRepresentationResult),
        )
        if any(type(value) is not expected for value, expected in expected_types):
            raise TypeError("scientific adoption members have incorrect exact types")
        if (
            self.selected_bands.retention is not self.retained_subspace.definition
            or self.represented_subspace.retained_subspace is not self.retained_subspace
            or self.retained_operator.retained_subspace is not self.retained_subspace
        ):
            raise ValueError("adoption members must share one retained space")
        if (
            self.represented_zone_center_operator.retained_operator
            is not self.retained_operator
            or self.complete_hopping.retained_operator is not self.retained_operator
        ):
            raise ValueError("operator representations must share one exact operator")
        if not isinstance(self.effective_models, tuple) or not self.effective_models:
            raise TypeError("effective_models must be a nonempty tuple")
        if any(
            type(value) is not Periodic1DRangeEffectiveModelAdoption
            for value in self.effective_models
        ):
            raise TypeError("effective_models members have the wrong exact type")
        if any(
            value.truncated.retained_operator is not self.retained_operator
            or value.fitted.retained_operator is not self.retained_operator
            for value in self.effective_models
        ):
            raise ValueError("effective models must share one exact retained operator")


class Periodic1DIsolatedBandReplayArtifactDecoder:
    """Decode and authenticate one closed replay-artifact JSON document."""

    __slots__ = ()

    def execute(
        self,
        payload: bytes,
        *,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        result: Periodic1DIsolatedBandCampaignResult,
        input_payload: bytes,
        reference_result_payload: bytes,
        producer_script_payload: bytes,
        replay_script_payload: bytes,
    ) -> Periodic1DIsolatedBandReplayArtifacts:
        """Return typed artifacts after source, frame, projector, and model checks."""
        for name, value in (
            ("payload", payload),
            ("input_payload", input_payload),
            ("reference_result_payload", reference_result_payload),
            ("producer_script_payload", producer_script_payload),
            ("replay_script_payload", replay_script_payload),
        ):
            if type(value) is not bytes:
                raise TypeError(f"{name} must be bytes")
        if type(definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition has the wrong exact type")
        if type(result) is not Periodic1DIsolatedBandCampaignResult:
            raise TypeError("result has the wrong exact type")
        root = self._document(payload)
        expected = {
            "artifact_kind",
            "effective_model_artifacts",
            "evidence_status",
            "experiment_id",
            "limitations",
            "retained_space_representation",
            "runtime",
            "schema_version",
            "source_correlation",
        }
        if set(root) != expected:
            raise ValueError("replay-artifact fields must match schema version one")
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported replay-artifact schema version")
        if self._string(root["artifact_kind"], "artifact_kind") != (
            "periodic-1d-isolated-band-replay-artifacts"
        ):
            raise ValueError("unsupported replay-artifact kind")
        experiment_id = self._string(root["experiment_id"], "experiment_id")
        if experiment_id != definition.experiment_id:
            raise ValueError(
                "replay artifact and campaign experiment identities differ"
            )
        if result.source_document.record_id != experiment_id:
            raise ValueError("replay artifact and retained result identities differ")
        source = self._mapping(root["source_correlation"], "source_correlation")
        decoded_definition = Periodic1DIsolatedBandCampaignJsonSerializer().deserialize(
            input_payload
        )
        definition_serializer = Periodic1DIsolatedBandCampaignJsonSerializer()
        if definition_serializer.serialize(decoded_definition) != (
            definition_serializer.serialize(definition)
        ):
            raise ValueError("definition differs from the authenticated input source")
        correlation = Periodic1DReplaySourceCorrelation(
            input_sha256=self._correlated_hash(source, "input_sha256", input_payload),
            reference_result_sha256=self._correlated_hash(
                source, "reference_result_sha256", reference_result_payload
            ),
            producer_script_sha256=self._correlated_hash(
                source, "producer_script_sha256", producer_script_payload
            ),
            replay_script_sha256=self._correlated_hash(
                source, "replay_script_sha256", replay_script_payload
            ),
            replayed_result_sha256=self._digest(
                source["replayed_result_sha256"], "replayed_result_sha256"
            ),
            exact_result_bytes_match=self._boolean(
                source["exact_result_bytes_match"], "exact_result_bytes_match"
            ),
        )
        if result.source_document.source_sha256 != correlation.reference_result_sha256:
            raise ValueError("result differs from the authenticated result source")
        retained = self._mapping(
            root["retained_space_representation"],
            "retained_space_representation",
        )
        frame_path, frame_hash, projector_hash = self._frame_path(retained, definition)
        effective = self._mapping(
            root["effective_model_artifacts"], "effective_model_artifacts"
        )
        complete, complete_hash, range_artifacts = self._effective_models(
            effective, definition
        )
        if complete.representatives != result.reduction.hopping_model.representatives:
            raise ValueError(
                "replay complete representatives differ from retained result"
            )
        if any(
            not np.array_equal(replay_block.magnitude, result_block.magnitude)
            for replay_block, result_block in zip(
                complete.hopping_blocks,
                result.reduction.hopping_model.hopping_blocks,
                strict=True,
            )
        ):
            raise ValueError("replay complete hopping differs from retained result")
        return Periodic1DIsolatedBandReplayArtifacts(
            experiment_id=experiment_id,
            source_payload=payload,
            source_payload_sha256=hashlib.sha256(payload).hexdigest(),
            source_correlation=correlation,
            frame_path=frame_path,
            frame_content_sha256=frame_hash,
            projector_path_content_sha256=projector_hash,
            complete_hopping_model=complete,
            complete_coefficients_content_sha256=complete_hash,
            range_artifacts=range_artifacts,
        )

    def _frame_path(
        self,
        value: dict[str, JsonValue],
        definition: Periodic1DIsolatedBandCampaignDefinition,
    ) -> tuple[ReciprocalBandFramePath1D, str, str]:
        mesh = CenteredUniformReciprocalMesh1D(
            definition.reciprocal_vector, definition.reciprocal_mesh_size
        )
        retained_mesh = np.asarray(
            self._reals(value["reciprocal_mesh"], "reciprocal_mesh"),
            dtype=np.float64,
        )
        if not np.array_equal(retained_mesh, mesh.coordinates.magnitude):
            raise ValueError(
                "retained reciprocal mesh differs from campaign definition"
            )
        indices = self._integers(
            value["ambient_plane_wave_indices"], "ambient_plane_wave_indices"
        )
        if len(indices) % 2 != 1:
            raise ValueError("ambient plane-wave inventory must have odd dimension")
        basis = PlaneWaveBasis1D(definition.reciprocal_vector, len(indices) // 2)
        if indices != basis.reciprocal_indices:
            raise ValueError("ambient plane-wave indices are not cutoff ordered")
        shape = self._integers(value["frame_shape"], "frame_shape")
        if shape != (mesh.point_count, basis.dimension, 1):
            raise ValueError("frame_shape differs from mesh and basis dimensions")
        frame_rows = self._array(value["parallel_transport_frame"], "frame")
        frame = np.asarray(
            [self._complex_vector(row, "frame row") for row in frame_rows],
            dtype=np.complex128,
        )
        if frame.shape != (mesh.point_count, basis.dimension):
            raise ValueError("frame values differ from declared frame shape")
        frame_hash = self._digest(value["frame_content_sha256"], "frame hash")
        self._require_array_hash(frame, frame_hash, "frame")
        projectors = np.einsum("ki,kj->kij", frame, frame.conj(), optimize=True)
        projector_hash = self._digest(
            value["projector_path_content_sha256"], "projector hash"
        )
        self._require_array_hash(projectors, projector_hash, "projector path")
        sewing = PlaneWaveReciprocalSewingConstructor().execute(basis)
        orthonormality_absolute_tolerance = float(
            np.finfo(np.float64).eps * basis.dimension
        )
        path = ReciprocalBandFramePath1D(
            mesh=mesh,
            frames=tuple(
                ComplexMatrixQuantity(row[:, None], Unitless()) for row in frame
            ),
            sewing_map=sewing.coefficient_map,
            orthonormality_absolute_tolerance=orthonormality_absolute_tolerance,
        )
        return path, frame_hash, projector_hash

    def _effective_models(
        self,
        value: dict[str, JsonValue],
        definition: Periodic1DIsolatedBandCampaignDefinition,
    ) -> tuple[
        BlockHoppingModel1D,
        str,
        tuple[Periodic1DRangeEffectiveModelArtifacts, ...],
    ]:
        representatives = self._integers(
            value["complete_representatives_cells"],
            "complete_representatives_cells",
        )
        coefficients = self._complex_vector(
            value["complete_coefficients"], "complete_coefficients"
        )
        complete_hash = self._digest(
            value["complete_coefficients_content_sha256"], "complete hash"
        )
        self._require_array_hash(coefficients, complete_hash, "complete coefficients")
        complete = self._hopping_model(
            definition.reciprocal_vector, representatives, coefficients
        )
        ranges = tuple(
            self._range_artifact(item, definition.reciprocal_vector)
            for item in self._objects(value["range_artifacts"], "range_artifacts")
        )
        if tuple(item.hopping_range_cells for item in ranges) != (
            definition.hopping_ranges
        ):
            raise ValueError("replay ranges differ from campaign definition")
        return complete, complete_hash, ranges

    def _range_artifact(
        self, value: dict[str, JsonValue], reciprocal_period: ScalarQuantity
    ) -> Periodic1DRangeEffectiveModelArtifacts:
        hopping_range = self._integer(
            value["hopping_range_cells"], "hopping_range_cells"
        )
        representatives = self._integers(
            value["representatives_cells"], "representatives_cells"
        )
        truncated = self._complex_vector(
            value["truncated_coefficients"], "truncated_coefficients"
        )
        fitted = self._complex_vector(
            value["fitted_coefficients"], "fitted_coefficients"
        )
        truncated_hash = self._digest(
            value["truncated_coefficients_content_sha256"], "truncated hash"
        )
        fitted_hash = self._digest(
            value["fitted_coefficients_content_sha256"], "fitted hash"
        )
        self._require_array_hash(truncated, truncated_hash, "truncated coefficients")
        self._require_array_hash(fitted, fitted_hash, "fitted coefficients")
        return Periodic1DRangeEffectiveModelArtifacts(
            hopping_range_cells=hopping_range,
            truncated_model=self._hopping_model(
                reciprocal_period, representatives, truncated
            ),
            fitted_model=self._hopping_model(
                reciprocal_period, representatives, fitted
            ),
            truncated_coefficients_content_sha256=truncated_hash,
            fitted_coefficients_content_sha256=fitted_hash,
        )

    @staticmethod
    def _hopping_model(
        reciprocal_period: ScalarQuantity,
        representatives: tuple[int, ...],
        coefficients: ComplexArray,
    ) -> BlockHoppingModel1D:
        if coefficients.shape != (len(representatives),):
            raise ValueError("coefficient count must equal representative count")
        return BlockHoppingModel1D(
            reciprocal_period=reciprocal_period,
            representatives=representatives,
            hopping_blocks=tuple(
                ComplexMatrixQuantity(
                    np.asarray([[coefficient]], dtype=np.complex128), Unitless()
                )
                for coefficient in coefficients
            ),
        )

    def _document(self, payload: bytes) -> dict[str, JsonValue]:
        try:
            decoded = cast(JsonValue, json.loads(payload.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid UTF-8 JSON") from error
        return self._mapping(decoded, "root")

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    def _objects(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        return tuple(self._mapping(item, name) for item in self._array(value, name))

    @staticmethod
    def _array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

    def _complex_vector(self, value: JsonValue, name: str) -> ComplexArray:
        pairs = tuple(self._reals(item, name) for item in self._array(value, name))
        if any(len(pair) != 2 for pair in pairs):
            raise ValueError(f"{name} must contain real/imaginary pairs")
        return np.asarray(
            [complex(pair[0], pair[1]) for pair in pairs], dtype=np.complex128
        )

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        return tuple(self._real(item, name) for item in self._array(value, name))

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        return tuple(self._integer(item, name) for item in self._array(value, name))

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if type(value) is not str or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _boolean(value: JsonValue, name: str) -> bool:
        if type(value) is not bool:
            raise TypeError(f"{name} must be a built-in bool")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a real number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        return value

    def _digest(self, value: JsonValue, name: str) -> str:
        digest = self._string(value, name)
        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        return digest

    def _correlated_hash(
        self, source: dict[str, JsonValue], field: str, payload: bytes
    ) -> str:
        digest = self._digest(source[field], field)
        if hashlib.sha256(payload).hexdigest() != digest:
            raise ValueError(f"{field} does not authenticate its supplied source")
        return digest

    @staticmethod
    def _require_array_hash(values: ComplexArray, digest: str, name: str) -> None:
        canonical = np.asarray(values, dtype="<c16", order="C")
        if hashlib.sha256(canonical.tobytes(order="C")).hexdigest() != digest:
            raise ValueError(f"{name} content digest differs")


class Periodic1DIsolatedBandScientificAdoption:
    """Adopt replay evidence through explicit retention and reduction actions."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DIsolatedBandScientificAdoptionRequest
    ) -> Periodic1DIsolatedBandScientificAdoptionResult:
        """Construct the parent, retained space/operator, and reduction routes."""
        if type(request) is not Periodic1DIsolatedBandScientificAdoptionRequest:
            raise TypeError("request has the wrong exact type")
        definition = request.definition
        result = request.result
        replay = request.replay
        if definition.experiment_id != replay.experiment_id:
            raise ValueError("definition and replay experiment identities differ")
        if result.source_document.record_id != replay.experiment_id:
            raise ValueError("result and replay experiment identities differ")

        identity = definition.experiment_id
        parent = Periodic1DFourierHamiltonianToyModel(
            model_id=f"{identity}.parent-model",
            state_space_id=f"{identity}.parent-bloch-state-space",
            reciprocal_domain_id=f"{identity}.primitive-reciprocal-domain",
            potential=PeriodicFourierPotential1D(
                period=definition.lattice_period,
                constant_coefficient=ScalarQuantity(0.0, Unitless()),
                cosine_coefficients=VectorQuantity(
                    np.asarray([definition.potential_strength.magnitude]), Unitless()
                ),
                sine_coefficients=VectorQuantity(np.asarray([0.0]), Unitless()),
            ),
            recoil_energy=definition.reciprocal_energy,
        )
        parent_reference = PeriodicOperatorReference(
            model_id=parent.model_id,
            operator_id=f"{identity}.parent-hamiltonian",
            state_space_id=parent.state_space_id,
            spatial_dimension=1,
        )
        retention = PeriodicRetentionDefinition(
            retention_id=f"{identity}.lowest-band-retention",
            parent_operator=parent_reference,
            retained_space_id=f"{identity}.lowest-band-space",
            kind=PeriodicRetentionKind.SELECTED_BANDS,
            rank=1,
            ordered_state_labels=("band-0",),
            reciprocal_domain_id=parent.reciprocal_domain_id,
            construction_record_id=f"{identity}.selected-band-0",
            assumption_ids=(f"{identity}.isolated-band-assumption",),
            provenance_id=replay.source_payload_sha256,
        )
        selected = Periodic1DSelectedBandRetentionDefinition(
            retention=retention,
            selection=ContiguousBandSelection(lower_index=0, upper_index=0),
        )
        frame = replay.frame_path
        subspace = PeriodicRetainedSubspaceConstructor().execute(
            definition=retention,
            ambient_state_space_id=parent.state_space_id,
            ambient_dimension=frame.ambient_dimension,
            projector_or_frame_record_id=replay.frame_content_sha256,
            spin_convention="spinless scalar toy model",
            internal_degree_convention="one retained band",
            reciprocal_boundary_convention=(
                "finite-cutoff upper reciprocal-index sewing"
            ),
            provenance_id=replay.source_payload_sha256,
        )
        represented_subspace = Periodic1DBandFrameRetainedSubspace(
            retained_subspace=subspace,
            frame_path=frame,
        )
        energy_reference = EnergyReference(
            zero="unshifted parent Hamiltonian zero",
            unit="dimensionless reciprocal-energy unit",
        )
        retained_operator = PeriodicRetainedOperatorConstructor().execute(
            operator_id=f"{identity}.lowest-band-hamiltonian",
            parent_operator=parent_reference,
            retained_subspace=subspace,
            construction_kind=(
                PeriodicRetainedOperatorConstructionKind.INVARIANT_RESTRICTION
            ),
            energy_reference=energy_reference,
            hermiticity_status=PeriodicHermiticityStatus.DECLARED_HERMITIAN,
            provenance_id=replay.source_payload_sha256,
        )
        represented_zone_center = self._zone_center_representation(
            retained_operator=retained_operator,
            result=result,
            lattice_period=definition.lattice_period,
            energy_reference=energy_reference,
            provenance_id=replay.source_payload_sha256,
        )

        transform = ReciprocalOperatorFourierTransformer1D().execute(
            source=result.reduction.reciprocal_samples,
            mesh=replay.frame_path.mesh,
            coordinate_absolute_tolerance=request.absolute_tolerance.magnitude,
            reconstruction_absolute_tolerance=request.absolute_tolerance.magnitude,
        )
        complete = Periodic1DCompleteHoppingRepresentationResult(
            retained_operator=retained_operator,
            transform=transform,
        )
        complete_comparison = BlockHoppingModelComparator1D().execute(
            reference=replay.complete_hopping_model,
            candidate=transform.hopping_model,
            comparison_coordinates=result.reduction.reciprocal_samples.coordinates,
        )
        if (
            complete_comparison.coefficient_l2_frobenius_defect.magnitude
            > request.absolute_tolerance.magnitude
        ):
            raise ValueError("complete action route differs from replay coefficients")
        effective_models = tuple(
            self._effective_model_routes(
                retained_operator=retained_operator,
                result=result,
                complete=replay.complete_hopping_model,
                artifacts=value,
                identity=identity,
                absolute_tolerance=request.absolute_tolerance,
            )
            for value in replay.range_artifacts
        )
        return Periodic1DIsolatedBandScientificAdoptionResult(
            parent_model=parent,
            selected_bands=selected,
            retained_subspace=subspace,
            represented_subspace=represented_subspace,
            retained_operator=retained_operator,
            represented_zone_center_operator=represented_zone_center,
            complete_hopping=complete,
            effective_models=effective_models,
        )

    @staticmethod
    def _zone_center_representation(
        retained_operator: PeriodicRetainedOperator,
        result: Periodic1DIsolatedBandCampaignResult,
        lattice_period: ScalarQuantity,
        energy_reference: EnergyReference,
        provenance_id: str,
    ) -> PeriodicRepresentedRetainedOperator:
        coordinates = result.reduction.reciprocal_samples.coordinates.magnitude
        zone_center_index = int(np.flatnonzero(coordinates == 0.0)[0])
        matrix = result.reduction.reciprocal_samples.matrices[
            zone_center_index
        ].magnitude
        identity = result.source_document.record_id
        record = OperatorRecord(
            identifier=f"{identity}.zone-center-represented-operator",
            operator_kind="lowest-band Hamiltonian at reduced momentum zero",
            matrix=matrix,
            state_space=StateSpace(
                identifier=retained_operator.retained_subspace.retained_space_id,
                kind="one-dimensional selected-band fiber",
                dimension=1,
            ),
            basis=Basis(
                identifier=f"{identity}.parallel-transport-zone-center-frame",
                kind="retained band frame",
                ordering=("band-0",),
                orthonormal=True,
            ),
            geometry=Geometry(
                system="dimensionless one-dimensional periodic toy system",
                cell=(
                    (lattice_period.magnitude, 0.0, 0.0),
                    (0.0, 1.0, 0.0),
                    (0.0, 0.0, 1.0),
                ),
                boundary_conditions="periodic",
                coordinate_convention=(
                    "row lattice vectors; first row is the physical toy period"
                ),
                length_unit="dimensionless",
            ),
            energy_reference=energy_reference,
            provenance={"replay_artifact_sha256": provenance_id},
        )
        return PeriodicRepresentedRetainedOperatorConstructor().execute(
            representation_id=f"{identity}.zone-center-representation",
            retained_operator=retained_operator,
            operator_record=record,
            representation_map_id=f"{identity}.zone-center-frame-map",
            gauge_id=f"{identity}.parallel-transport-gauge",
            provenance_id=provenance_id,
        )

    @staticmethod
    def _effective_model_routes(
        retained_operator: PeriodicRetainedOperator,
        result: Periodic1DIsolatedBandCampaignResult,
        complete: BlockHoppingModel1D,
        artifacts: Periodic1DRangeEffectiveModelArtifacts,
        identity: str,
        absolute_tolerance: ScalarQuantity,
    ) -> Periodic1DRangeEffectiveModelAdoption:
        hopping_range = artifacts.hopping_range_cells
        truncation = BlockHoppingTruncator1D().execute(
            source=complete,
            maximum_range=hopping_range,
        )
        truncation_comparison = BlockHoppingModelComparator1D().execute(
            reference=artifacts.truncated_model,
            candidate=truncation.truncated,
            comparison_coordinates=result.reduction.reciprocal_samples.coordinates,
        )
        if (
            truncation_comparison.coefficient_l2_frobenius_defect.magnitude
            > absolute_tolerance.magnitude
        ):
            raise ValueError("truncation action route differs from replay coefficients")
        representatives = tuple(range(-hopping_range, hopping_range + 1))
        weights = VectorQuantity(
            np.ones(len(result.reduction.reciprocal_samples.matrices)), Unitless()
        )
        fit = BlockHoppingLeastSquaresFitter1D().execute(
            source=result.reduction.reciprocal_samples,
            representatives=representatives,
            weights=weights,
        )
        fit_comparison = BlockHoppingModelComparator1D().execute(
            reference=artifacts.fitted_model,
            candidate=fit.fitted_model,
            comparison_coordinates=result.reduction.reciprocal_samples.coordinates,
        )
        if (
            fit_comparison.coefficient_l2_frobenius_defect.magnitude
            > absolute_tolerance.magnitude
        ):
            raise ValueError("fitting action route differs from replay coefficients")
        return Periodic1DRangeEffectiveModelAdoption(
            hopping_range_cells=hopping_range,
            truncated=Periodic1DTruncatedHoppingEffectiveModelResult(
                effective_model_id=f"{identity}.truncated-range-{hopping_range}",
                retained_operator=retained_operator,
                truncation=truncation,
            ),
            fitted=Periodic1DFittedHoppingEffectiveModelResult(
                effective_model_id=f"{identity}.fitted-range-{hopping_range}",
                retained_operator=retained_operator,
                fit=fit,
            ),
        )


__all__ = [
    "PERIODIC_1D_ISOLATED_BAND_DEFAULT_ABSOLUTE_TOLERANCE",
    "Periodic1DIsolatedBandReplayArtifactDecoder",
    "Periodic1DIsolatedBandReplayArtifacts",
    "Periodic1DIsolatedBandScientificAdoption",
    "Periodic1DIsolatedBandScientificAdoptionRequest",
    "Periodic1DIsolatedBandScientificAdoptionResult",
    "Periodic1DRangeEffectiveModelAdoption",
    "Periodic1DRangeEffectiveModelArtifacts",
    "Periodic1DReplaySourceCorrelation",
]
