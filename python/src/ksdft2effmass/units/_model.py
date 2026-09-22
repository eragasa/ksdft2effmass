"""Typed unit values, conversion definitions, and conversion results.

The records in this module are representation objects only. They do not infer units,
rewrite native calculation records, serialize a wire format, or claim that a numeric
conversion removes parent-model or numerical error.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class PhysicalDimension(StrEnum):
    """Identify physical dimensions represented by unit contracts.

    Attributes
    ----------
    ENERGY
        Energy, including the LAMMPS convention that torque uses energy units.
    LENGTH
        Spatial length.
    TIME
        Elapsed time.
    VELOCITY
        Length per time.
    FORCE
        Energy per length.
    TEMPERATURE
        Thermodynamic temperature.
    PRESSURE
        Mechanical pressure.
    DYNAMIC_VISCOSITY
        Dynamic viscosity.
    CHARGE
        Electric charge.
    DIPOLE
        Electric charge times length.
    ELECTRIC_FIELD
        Electric potential per length.
    DENSITY
        Mass density using a symbolic spatial-dimension exponent.
    ATOMIC_MASS
        Mass of one atom or particle.
    MOLAR_MASS
        Mass per amount of substance.
    """

    ENERGY = "energy"
    LENGTH = "length"
    TIME = "time"
    VELOCITY = "velocity"
    FORCE = "force"
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
    DYNAMIC_VISCOSITY = "dynamic_viscosity"
    CHARGE = "charge"
    DIPOLE = "dipole"
    ELECTRIC_FIELD = "electric_field"
    DENSITY = "density"
    ATOMIC_MASS = "atomic_mass"
    MOLAR_MASS = "molar_mass"


class UnitIdentity(StrEnum):
    """Identify exact source and canonical units without implicit conversion.

    Attributes
    ----------
    HARTREE
        Hartree source energy unit.
    RYDBERG
        Rydberg source energy unit.
    ELECTRON_VOLT
        Canonical energy and torque unit.
    BOHR
        Bohr-radius source length unit.
    ANGSTROM
        Canonical distance unit.
    PICOSECOND
        Canonical time unit.
    ANGSTROM_PER_PICOSECOND
        Canonical velocity unit.
    ELECTRON_VOLT_PER_ANGSTROM
        Canonical force unit.
    KELVIN
        Canonical temperature unit.
    BAR
        Canonical pressure unit.
    POISE
        Canonical dynamic-viscosity unit.
    ELEMENTARY_CHARGE_MULTIPLE
        Canonical charge represented as a multiple of elementary charge.
    ELEMENTARY_CHARGE_ANGSTROM
        Canonical dipole unit.
    VOLT_PER_ANGSTROM
        Canonical electric-field unit.
    GRAM_PER_CENTIMETER_POWER_DIMENSION
        Canonical density unit with the denominator exponent equal to the spatial
        dimension.
    UNIFIED_ATOMIC_MASS_UNIT
        Unified atomic mass source unit; it is not an alias for gram per mole.
    GRAM_PER_MOLE
        Canonical LAMMPS ``metal`` mass-value unit.
    """

    HARTREE = "hartree"
    RYDBERG = "rydberg"
    ELECTRON_VOLT = "electron_volt"
    BOHR = "bohr"
    ANGSTROM = "angstrom"
    PICOSECOND = "picosecond"
    ANGSTROM_PER_PICOSECOND = "angstrom_per_picosecond"
    ELECTRON_VOLT_PER_ANGSTROM = "electron_volt_per_angstrom"
    KELVIN = "kelvin"
    BAR = "bar"
    POISE = "poise"
    ELEMENTARY_CHARGE_MULTIPLE = "elementary_charge_multiple"
    ELEMENTARY_CHARGE_ANGSTROM = "elementary_charge_angstrom"
    VOLT_PER_ANGSTROM = "volt_per_angstrom"
    GRAM_PER_CENTIMETER_POWER_DIMENSION = "gram_per_centimeter^dimension"
    UNIFIED_ATOMIC_MASS_UNIT = "unified_atomic_mass_unit"
    GRAM_PER_MOLE = "gram_per_mole"

    @property
    def dimension(self) -> PhysicalDimension:
        """Return the physical dimension assigned to this unit identity.

        Returns
        -------
        PhysicalDimension
            Exact closed dimension associated with the unit.
        """
        return {
            UnitIdentity.HARTREE: PhysicalDimension.ENERGY,
            UnitIdentity.RYDBERG: PhysicalDimension.ENERGY,
            UnitIdentity.ELECTRON_VOLT: PhysicalDimension.ENERGY,
            UnitIdentity.BOHR: PhysicalDimension.LENGTH,
            UnitIdentity.ANGSTROM: PhysicalDimension.LENGTH,
            UnitIdentity.PICOSECOND: PhysicalDimension.TIME,
            UnitIdentity.ANGSTROM_PER_PICOSECOND: PhysicalDimension.VELOCITY,
            UnitIdentity.ELECTRON_VOLT_PER_ANGSTROM: PhysicalDimension.FORCE,
            UnitIdentity.KELVIN: PhysicalDimension.TEMPERATURE,
            UnitIdentity.BAR: PhysicalDimension.PRESSURE,
            UnitIdentity.POISE: PhysicalDimension.DYNAMIC_VISCOSITY,
            UnitIdentity.ELEMENTARY_CHARGE_MULTIPLE: PhysicalDimension.CHARGE,
            UnitIdentity.ELEMENTARY_CHARGE_ANGSTROM: PhysicalDimension.DIPOLE,
            UnitIdentity.VOLT_PER_ANGSTROM: PhysicalDimension.ELECTRIC_FIELD,
            UnitIdentity.GRAM_PER_CENTIMETER_POWER_DIMENSION: (
                PhysicalDimension.DENSITY
            ),
            UnitIdentity.UNIFIED_ATOMIC_MASS_UNIT: PhysicalDimension.ATOMIC_MASS,
            UnitIdentity.GRAM_PER_MOLE: PhysicalDimension.MOLAR_MASS,
        }[self]


@dataclass(frozen=True, slots=True)
class UnitScalar:
    """Represent one finite binary64 scalar with an explicit unit.

    Parameters
    ----------
    value
        Finite built-in ``float``. Booleans, integers, numeric strings, NumPy
        scalars, infinities, and NaNs are rejected.
    unit
        Exact unit identity. No conversion is performed during construction.

    Raises
    ------
    TypeError
        If ``value`` is not a built-in ``float`` or ``unit`` is not a
        :class:`UnitIdentity`.
    ValueError
        If ``value`` is NaN or infinite.
    """

    value: float
    unit: UnitIdentity

    def __post_init__(self) -> None:
        if type(self.value) is not float:
            raise TypeError("value must be a built-in float excluding bool")
        if not math.isfinite(self.value):
            raise ValueError("value must be finite")
        if type(self.unit) is not UnitIdentity:
            raise TypeError("unit must be UnitIdentity")

    @property
    def dimension(self) -> PhysicalDimension:
        """Return the physical dimension declared by the unit identity.

        Returns
        -------
        PhysicalDimension
            Dimension assigned by :attr:`UnitIdentity.dimension`.
        """
        return self.unit.dimension


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Identify exact external or retained content by SHA-256.

    Parameters
    ----------
    value
        Literal ``sha256:`` followed by exactly 64 lowercase hexadecimal digits.

    Raises
    ------
    TypeError
        If ``value`` is not a built-in ``str``.
    ValueError
        If the prefix, digest length, or lowercase hexadecimal grammar is invalid.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("content identity must be a built-in str")
        prefix = "sha256:"
        digest = self.value.removeprefix(prefix)
        if not self.value.startswith(prefix) or len(digest) != 64:
            raise ValueError(
                "content identity must be sha256 followed by 64 hex digits"
            )
        if any(character not in "0123456789abcdef" for character in digest):
            raise ValueError("content identity must use lowercase hexadecimal digits")


@dataclass(frozen=True, slots=True)
class AuthorityReference:
    """Identify one exact external authority document.

    Parameters
    ----------
    identity
        Stable nonempty authority-document identity.
    version
        Exact edition, adjustment, release tag, or document version.
    url
        Public source URL from which the identified bytes were retrieved.
    content_identity
        SHA-256 identity of those exact retrieved bytes.
    doi
        Nonempty DOI when the authority supplies one, otherwise ``None``.

    Raises
    ------
    TypeError
        If a text field has the wrong semantic type or ``content_identity`` is not a
        :class:`ContentIdentity`.
    ValueError
        If a required text field, or a present DOI, is empty.
    """

    identity: str
    version: str
    url: str
    content_identity: ContentIdentity
    doi: str | None = None

    def __post_init__(self) -> None:
        for field_name, value in (
            ("identity", self.identity),
            ("version", self.version),
            ("url", self.url),
        ):
            if type(value) is not str:
                raise TypeError(f"{field_name} must be a built-in str")
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if type(self.content_identity) is not ContentIdentity:
            raise TypeError("content_identity must be ContentIdentity")
        if self.doi is not None:
            if type(self.doi) is not str:
                raise TypeError("doi must be a built-in str or None")
            if not self.doi:
                raise ValueError("doi must not be empty when present")


@dataclass(frozen=True, slots=True)
class MetalUnitInventory:
    """Record the exact pinned LAMMPS ``metal`` dimensional inventory.

    Parameters
    ----------
    identity
        Stable nonempty semantic identity of this inventory contract.
    version
        Positive signed-64-bit contract version.
    content_identity
        SHA-256 identity of the exact documented inventory preimage.
    authority
        Exact pinned LAMMPS units-document reference.
    mass_unit
        Required canonical value ``gram_per_mole``.
    distance_unit
        Required canonical value ``angstrom``.
    time_unit
        Required canonical value ``picosecond``.
    energy_unit
        Required canonical value ``electron_volt``.
    velocity_unit
        Required canonical value ``angstrom_per_picosecond``.
    force_unit
        Required canonical value ``electron_volt_per_angstrom``.
    torque_unit
        Required canonical value ``electron_volt``.
    temperature_unit
        Required canonical value ``kelvin``.
    pressure_unit
        Required canonical value ``bar``.
    dynamic_viscosity_unit
        Required canonical value ``poise``.
    charge_unit
        Required canonical value ``elementary_charge_multiple``.
    dipole_unit
        Required canonical value ``elementary_charge_angstrom``.
    electric_field_unit
        Required canonical value ``volt_per_angstrom``.
    density_unit
        Required canonical symbolic value ``gram_per_centimeter^dimension``.

    Raises
    ------
    TypeError
        If identity, version, content identity, authority, or any unit role has the
        wrong semantic type.
    ValueError
        If identity is empty, version is outside positive signed-64-bit range, or a
        unit role differs from the pinned canonical inventory.
    """

    identity: str
    version: int
    content_identity: ContentIdentity
    authority: AuthorityReference
    mass_unit: UnitIdentity
    distance_unit: UnitIdentity
    time_unit: UnitIdentity
    energy_unit: UnitIdentity
    velocity_unit: UnitIdentity
    force_unit: UnitIdentity
    torque_unit: UnitIdentity
    temperature_unit: UnitIdentity
    pressure_unit: UnitIdentity
    dynamic_viscosity_unit: UnitIdentity
    charge_unit: UnitIdentity
    dipole_unit: UnitIdentity
    electric_field_unit: UnitIdentity
    density_unit: UnitIdentity

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("inventory identity must be a built-in str")
        if not self.identity:
            raise ValueError("inventory identity must not be empty")
        if type(self.version) is not int:
            raise TypeError("inventory version must be a built-in int")
        if self.version <= 0 or self.version > 2**63 - 1:
            raise ValueError("inventory version must be a positive signed i64")
        if type(self.content_identity) is not ContentIdentity:
            raise TypeError("content_identity must be ContentIdentity")
        if type(self.authority) is not AuthorityReference:
            raise TypeError("authority must be AuthorityReference")
        expected = (
            ("mass_unit", self.mass_unit, UnitIdentity.GRAM_PER_MOLE),
            ("distance_unit", self.distance_unit, UnitIdentity.ANGSTROM),
            ("time_unit", self.time_unit, UnitIdentity.PICOSECOND),
            ("energy_unit", self.energy_unit, UnitIdentity.ELECTRON_VOLT),
            (
                "velocity_unit",
                self.velocity_unit,
                UnitIdentity.ANGSTROM_PER_PICOSECOND,
            ),
            (
                "force_unit",
                self.force_unit,
                UnitIdentity.ELECTRON_VOLT_PER_ANGSTROM,
            ),
            ("torque_unit", self.torque_unit, UnitIdentity.ELECTRON_VOLT),
            ("temperature_unit", self.temperature_unit, UnitIdentity.KELVIN),
            ("pressure_unit", self.pressure_unit, UnitIdentity.BAR),
            (
                "dynamic_viscosity_unit",
                self.dynamic_viscosity_unit,
                UnitIdentity.POISE,
            ),
            (
                "charge_unit",
                self.charge_unit,
                UnitIdentity.ELEMENTARY_CHARGE_MULTIPLE,
            ),
            (
                "dipole_unit",
                self.dipole_unit,
                UnitIdentity.ELEMENTARY_CHARGE_ANGSTROM,
            ),
            (
                "electric_field_unit",
                self.electric_field_unit,
                UnitIdentity.VOLT_PER_ANGSTROM,
            ),
            (
                "density_unit",
                self.density_unit,
                UnitIdentity.GRAM_PER_CENTIMETER_POWER_DIMENSION,
            ),
        )
        for field_name, value, required in expected:
            if type(value) is not UnitIdentity:
                raise TypeError(f"{field_name} must be UnitIdentity")
            if value is not required:
                raise ValueError(f"{field_name} must be {required.value}")


@dataclass(frozen=True, slots=True)
class MetalUnitConversionAuthority:
    """Bind external authorities selected for canonical metal-unit conversion.

    Parameters
    ----------
    lammps_units_document
        Pinned LAMMPS document defining the canonical dimensional inventory.
    nist_codata_adjustment
        Pinned NIST 2022 CODATA listing defining recommended conversion values and
        standard uncertainties.
    bipm_si_brochure
        Pinned BIPM SI Brochure defining the applicable SI units and exact relations.

    Raises
    ------
    TypeError
        If any field is not an :class:`AuthorityReference`.
    """

    lammps_units_document: AuthorityReference
    nist_codata_adjustment: AuthorityReference
    bipm_si_brochure: AuthorityReference

    def __post_init__(self) -> None:
        for field_name, value in (
            ("lammps_units_document", self.lammps_units_document),
            ("nist_codata_adjustment", self.nist_codata_adjustment),
            ("bipm_si_brochure", self.bipm_si_brochure),
        ):
            if type(value) is not AuthorityReference:
                raise TypeError(f"{field_name} must be AuthorityReference")


@dataclass(frozen=True, slots=True)
class NumericalPolicy:
    """Identify the finite binary64 conversion policy.

    Parameters
    ----------
    identity
        Stable nonempty semantic identity of the arithmetic policy.
    version
        Positive signed-64-bit policy version.

    Notes
    -----
    The selected policy converts the exact input binary64 value to ``Decimal``,
    multiplies it by the retained exact decimal scale at decimal precision 80, and
    converts once to binary64 using round-to-nearest, ties-to-even. Nonfinite output,
    overflow, and nonzero input rounded to zero are represented as failures.

    Raises
    ------
    TypeError
        If identity is not a built-in ``str`` or version is not a built-in ``int``.
    ValueError
        If identity is empty or version is outside positive signed-64-bit range.
    """

    identity: str
    version: int

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("numerical-policy identity must be a built-in str")
        if not self.identity:
            raise ValueError("numerical-policy identity must not be empty")
        if type(self.version) is not int:
            raise TypeError("numerical-policy version must be a built-in int")
        if self.version <= 0 or self.version > 2**63 - 1:
            raise ValueError("numerical-policy version must be a positive signed i64")


@dataclass(frozen=True, slots=True)
class MetalUnitConversionDefinition:
    """Define one exact source-to-canonical conversion.

    Parameters
    ----------
    identity
        Stable nonempty semantic identity of the conversion definition.
    version
        Positive signed-64-bit definition version.
    content_identity
        SHA-256 identity of the exact documented definition preimage.
    source_unit
        Exact unit accepted on a conversion request.
    target_unit
        Exact unit produced by the conversion.
    source_dimension
        Dimension that must equal ``source_unit.dimension``.
    target_dimension
        Dimension that must equal ``target_unit.dimension``.
    decimal_scale
        Finite positive exact decimal multiplier from one source unit to the target
        unit.
    standard_uncertainty
        Finite nonnegative exact decimal standard uncertainty of the factor for one
        source unit, expressed in the target unit.
    numerical_policy
        Exact arithmetic, rounding, overflow, and underflow policy identity.
    authority
        Pinned LAMMPS, NIST CODATA, and BIPM authority references.
    implementation_identity
        Nonempty identity of the ActionObject implementation authorized to apply the
        definition.

    Notes
    -----
    The factor and standard uncertainty are retained exact decimal representations.
    This slice does not propagate factor uncertainty into a converted output scalar.

    Raises
    ------
    TypeError
        If any field has the wrong semantic type.
    ValueError
        If identity is empty, version is outside positive signed-64-bit range, a unit
        and dimension disagree, a decimal is nonfinite or outside its allowed range,
        or the implementation identity is empty.
    """

    identity: str
    version: int
    content_identity: ContentIdentity
    source_unit: UnitIdentity
    target_unit: UnitIdentity
    source_dimension: PhysicalDimension
    target_dimension: PhysicalDimension
    decimal_scale: Decimal
    standard_uncertainty: Decimal
    numerical_policy: NumericalPolicy
    authority: MetalUnitConversionAuthority
    implementation_identity: str

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("definition identity must be a built-in str")
        if not self.identity:
            raise ValueError("definition identity must not be empty")
        if type(self.version) is not int:
            raise TypeError("definition version must be a built-in int")
        if self.version <= 0 or self.version > 2**63 - 1:
            raise ValueError("definition version must be a positive signed i64")
        if type(self.content_identity) is not ContentIdentity:
            raise TypeError("content_identity must be ContentIdentity")
        if type(self.source_unit) is not UnitIdentity:
            raise TypeError("source_unit must be UnitIdentity")
        if type(self.target_unit) is not UnitIdentity:
            raise TypeError("target_unit must be UnitIdentity")
        if type(self.source_dimension) is not PhysicalDimension:
            raise TypeError("source_dimension must be PhysicalDimension")
        if type(self.target_dimension) is not PhysicalDimension:
            raise TypeError("target_dimension must be PhysicalDimension")
        if self.source_unit.dimension is not self.source_dimension:
            raise ValueError("source unit and source dimension must agree")
        if self.target_unit.dimension is not self.target_dimension:
            raise ValueError("target unit and target dimension must agree")
        if type(self.decimal_scale) is not Decimal:
            raise TypeError("decimal_scale must be Decimal")
        if not self.decimal_scale.is_finite() or self.decimal_scale <= 0:
            raise ValueError("decimal_scale must be finite and positive")
        if type(self.standard_uncertainty) is not Decimal:
            raise TypeError("standard_uncertainty must be Decimal")
        if not self.standard_uncertainty.is_finite() or self.standard_uncertainty < 0:
            raise ValueError("standard_uncertainty must be finite and nonnegative")
        if type(self.numerical_policy) is not NumericalPolicy:
            raise TypeError("numerical_policy must be NumericalPolicy")
        if type(self.authority) is not MetalUnitConversionAuthority:
            raise TypeError("authority must be MetalUnitConversionAuthority")
        if type(self.implementation_identity) is not str:
            raise TypeError("implementation_identity must be a built-in str")
        if not self.implementation_identity:
            raise ValueError("implementation_identity must not be empty")


@dataclass(frozen=True, slots=True)
class MetalUnitConversionCatalog:
    """Own one immutable closed collection of conversion definitions.

    Parameters
    ----------
    identity
        Stable nonempty semantic identity of the catalog.
    version
        Positive signed-64-bit catalog version.
    content_identity
        SHA-256 identity of the exact documented ordered catalog preimage.
    definitions
        Nonempty tuple of definitions with unique ordered source-target unit pairs.
        Tuple order is retained as part of catalog content.

    Raises
    ------
    TypeError
        If identity, version, content identity, or definitions have the wrong
        semantic type.
    ValueError
        If identity is empty, version is outside positive signed-64-bit range,
        definitions are empty, or an ordered unit pair is duplicated.
    """

    identity: str
    version: int
    content_identity: ContentIdentity
    definitions: tuple[MetalUnitConversionDefinition, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("catalog identity must be a built-in str")
        if not self.identity:
            raise ValueError("catalog identity must not be empty")
        if type(self.version) is not int:
            raise TypeError("catalog version must be a built-in int")
        if self.version <= 0 or self.version > 2**63 - 1:
            raise ValueError("catalog version must be a positive signed i64")
        if type(self.content_identity) is not ContentIdentity:
            raise TypeError("content_identity must be ContentIdentity")
        if type(self.definitions) is not tuple or any(
            type(value) is not MetalUnitConversionDefinition
            for value in self.definitions
        ):
            raise TypeError(
                "definitions must be a tuple of MetalUnitConversionDefinition"
            )
        if not self.definitions:
            raise ValueError("definitions must not be empty")
        keys = tuple(
            (definition.source_unit, definition.target_unit)
            for definition in self.definitions
        )
        if len(set(keys)) != len(keys):
            raise ValueError("source-target conversion pairs must be unique")

    def definition_for(
        self, source_unit: UnitIdentity, target_unit: UnitIdentity
    ) -> MetalUnitConversionDefinition | None:
        """Return the exact definition for one ordered unit pair, if present.

        Parameters
        ----------
        source_unit
            Exact source unit to match.
        target_unit
            Exact target unit to match.

        Returns
        -------
        MetalUnitConversionDefinition or None
            Matching definition, or ``None`` when the pair is unsupported.

        Raises
        ------
        TypeError
            If either argument is not a :class:`UnitIdentity`.
        """
        if type(source_unit) is not UnitIdentity:
            raise TypeError("source_unit must be UnitIdentity")
        if type(target_unit) is not UnitIdentity:
            raise TypeError("target_unit must be UnitIdentity")
        for definition in self.definitions:
            if (
                definition.source_unit is source_unit
                and definition.target_unit is target_unit
            ):
                return definition
        return None


@dataclass(frozen=True, slots=True)
class MetalUnitConversionSourceCorrelation:
    """Retain available identities of the native value being converted.

    Parameters
    ----------
    artifact_identity
        Nonempty source-artifact identity, or ``None`` when unavailable.
    result_identity
        Nonempty source-result identity, or ``None`` when unavailable.
    provenance_identity
        Nonempty source-producer-provenance identity, or ``None`` when unavailable.
    content_identity
        SHA-256 identity of exact retained source bytes, or ``None`` when the source
        is not a content-addressed artifact.

    Notes
    -----
    At least one identity must be present. Text values remain opaque because their
    owning source domains retain nominal identity classes and source bytes.

    Raises
    ------
    TypeError
        If a present text value is not a built-in ``str`` or a present content value
        is not a :class:`ContentIdentity`.
    ValueError
        If every identity is absent or a present text identity is empty.
    """

    artifact_identity: str | None = None
    result_identity: str | None = None
    provenance_identity: str | None = None
    content_identity: ContentIdentity | None = None

    def __post_init__(self) -> None:
        text_values = (
            self.artifact_identity,
            self.result_identity,
            self.provenance_identity,
        )
        if (
            all(value is None for value in text_values)
            and self.content_identity is None
        ):
            raise ValueError("at least one source correlation identity is required")
        for value in text_values:
            if value is not None:
                if type(value) is not str:
                    raise TypeError("source correlation identities must be str or None")
                if not value:
                    raise ValueError("source correlation identities must not be empty")
        if self.content_identity is not None and (
            type(self.content_identity) is not ContentIdentity
        ):
            raise TypeError("content_identity must be ContentIdentity or None")


@dataclass(frozen=True, slots=True)
class MetalUnitConversionRequest:
    """Request one explicit conversion without modifying its source record.

    Parameters
    ----------
    source
        Exact finite binary64 scalar and source unit.
    target_unit
        Explicit requested target unit. No target is inferred from dimension alone.
    source_correlation
        Optional exact source artifact/result/provenance correlation.

    Raises
    ------
    TypeError
        If source, target unit, or a present source correlation has the wrong
        semantic type.
    """

    source: UnitScalar
    target_unit: UnitIdentity
    source_correlation: MetalUnitConversionSourceCorrelation | None = None

    def __post_init__(self) -> None:
        if type(self.source) is not UnitScalar:
            raise TypeError("source must be UnitScalar")
        if type(self.target_unit) is not UnitIdentity:
            raise TypeError("target_unit must be UnitIdentity")
        if self.source_correlation is not None and (
            type(self.source_correlation) is not MetalUnitConversionSourceCorrelation
        ):
            raise TypeError(
                "source_correlation must be "
                "MetalUnitConversionSourceCorrelation or None"
            )


class MetalUnitConversionOutcome(StrEnum):
    """Identify closed outcomes of one unit-conversion request.

    Attributes
    ----------
    CONVERTED
        Conversion produced one finite correlated output scalar.
    UNSUPPORTED
        The catalog contains no definition for the requested ordered unit pair.
    OVERFLOW
        Exact decimal multiplication cannot be represented as finite binary64.
    UNDERFLOW
        Nonzero exact decimal output rounds to binary64 zero.
    """

    CONVERTED = "converted"
    UNSUPPORTED = "unsupported"
    OVERFLOW = "overflow"
    UNDERFLOW = "underflow"


class MetalUnitConversionFailureCode(StrEnum):
    """Identify closed failure reasons for one conversion request.

    Attributes
    ----------
    UNSUPPORTED_UNIT_PAIR
        No catalog definition matches the ordered source-target pair.
    BINARY64_OVERFLOW
        Conversion output is outside finite binary64 range.
    NONZERO_ROUNDED_TO_ZERO
        Nonzero conversion output rounds to binary64 zero.
    """

    UNSUPPORTED_UNIT_PAIR = "unsupported_unit_pair"
    BINARY64_OVERFLOW = "binary64_overflow"
    NONZERO_ROUNDED_TO_ZERO = "nonzero_rounded_to_zero"


class MetalUnitConversionLimitation(StrEnum):
    """Identify limitations retained by conversion results.

    Attributes
    ----------
    BINARY64_OUTPUT_ROUNDED
        Exact decimal output was rounded once to binary64.
    FACTOR_UNCERTAINTY_NOT_PROPAGATED
        Definition uncertainty remains available but was not propagated to an output
        uncertainty.
    """

    BINARY64_OUTPUT_ROUNDED = "binary64_output_rounded"
    FACTOR_UNCERTAINTY_NOT_PROPAGATED = "factor_uncertainty_not_propagated"


@dataclass(frozen=True, slots=True)
class MetalUnitConversionSuccess:
    """Retain one converted scalar and all definition/source correlations.

    Parameters
    ----------
    outcome
        Required closed value :attr:`MetalUnitConversionOutcome.CONVERTED`.
    request
        Exact source scalar, requested target, and optional source correlation.
    output
        Finite binary64 output whose unit equals the selected definition target.
    definition
        Exact definition whose source and target units equal the request pair.
    catalog_identity
        Nonempty identity of the catalog that selected the definition.
    catalog_version
        Positive signed-64-bit catalog version.
    catalog_content_identity
        SHA-256 identity of the exact catalog content used by conversion.
    limitations
        Unique tuple of represented conversion limitations.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If outcome is not converted, request/definition/output units contradict one
        another, catalog identity is empty, version is outside positive signed-64-bit
        range, or limitations are duplicated.
    """

    outcome: MetalUnitConversionOutcome
    request: MetalUnitConversionRequest
    output: UnitScalar
    definition: MetalUnitConversionDefinition
    catalog_identity: str
    catalog_version: int
    catalog_content_identity: ContentIdentity
    limitations: tuple[MetalUnitConversionLimitation, ...]

    def __post_init__(self) -> None:
        if type(self.outcome) is not MetalUnitConversionOutcome:
            raise TypeError("outcome must be MetalUnitConversionOutcome")
        if self.outcome is not MetalUnitConversionOutcome.CONVERTED:
            raise ValueError("outcome must be CONVERTED")
        if type(self.request) is not MetalUnitConversionRequest:
            raise TypeError("request must be MetalUnitConversionRequest")
        if type(self.output) is not UnitScalar:
            raise TypeError("output must be UnitScalar")
        if type(self.definition) is not MetalUnitConversionDefinition:
            raise TypeError("definition must be MetalUnitConversionDefinition")
        if self.definition.source_unit is not self.request.source.unit:
            raise ValueError(
                "definition source unit must equal the request source unit"
            )
        if self.definition.target_unit is not self.request.target_unit:
            raise ValueError(
                "definition target unit must equal the requested target unit"
            )
        if self.output.unit is not self.definition.target_unit:
            raise ValueError(
                "output unit must equal the selected definition target unit"
            )
        if type(self.catalog_identity) is not str:
            raise TypeError("catalog_identity must be a built-in str")
        if not self.catalog_identity:
            raise ValueError("catalog_identity must not be empty")
        if type(self.catalog_version) is not int:
            raise TypeError("catalog_version must be a built-in int")
        if self.catalog_version <= 0 or self.catalog_version > 2**63 - 1:
            raise ValueError("catalog_version must be a positive signed i64")
        if type(self.catalog_content_identity) is not ContentIdentity:
            raise TypeError("catalog_content_identity must be ContentIdentity")
        if type(self.limitations) is not tuple or any(
            type(value) is not MetalUnitConversionLimitation
            for value in self.limitations
        ):
            raise TypeError(
                "limitations must be a tuple of MetalUnitConversionLimitation"
            )
        if len(set(self.limitations)) != len(self.limitations):
            raise ValueError("limitations must be unique")


@dataclass(frozen=True, slots=True)
class MetalUnitConversionFailure:
    """Retain one represented conversion failure without a fabricated output.

    Parameters
    ----------
    outcome
        Closed non-converted outcome correlated with ``code``.
    code
        Exact closed failure reason.
    request
        Exact source scalar, requested target, and optional source correlation.
    definition
        ``None`` for an unsupported pair; otherwise the exact definition whose source
        and target units equal a numeric-failure request.
    catalog_identity
        Nonempty identity of the catalog consulted by conversion.
    catalog_version
        Positive signed-64-bit catalog version.
    catalog_content_identity
        SHA-256 identity of the exact catalog content consulted by conversion.
    limitations
        Unique tuple of represented limitations; unsupported pairs may use an empty
        tuple because no arithmetic was attempted.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If outcome and code disagree, converted outcome is used, definition presence
        disagrees with failure kind, a numeric definition pair contradicts the
        request, catalog identity is empty, version is outside positive signed-64-bit
        range, or limitations are duplicated.
    """

    outcome: MetalUnitConversionOutcome
    code: MetalUnitConversionFailureCode
    request: MetalUnitConversionRequest
    definition: MetalUnitConversionDefinition | None
    catalog_identity: str
    catalog_version: int
    catalog_content_identity: ContentIdentity
    limitations: tuple[MetalUnitConversionLimitation, ...]

    def __post_init__(self) -> None:
        if type(self.outcome) is not MetalUnitConversionOutcome:
            raise TypeError("outcome must be MetalUnitConversionOutcome")
        if self.outcome is MetalUnitConversionOutcome.CONVERTED:
            raise ValueError("failure outcome must not be CONVERTED")
        if type(self.code) is not MetalUnitConversionFailureCode:
            raise TypeError("code must be MetalUnitConversionFailureCode")
        expected = {
            MetalUnitConversionFailureCode.UNSUPPORTED_UNIT_PAIR: (
                MetalUnitConversionOutcome.UNSUPPORTED
            ),
            MetalUnitConversionFailureCode.BINARY64_OVERFLOW: (
                MetalUnitConversionOutcome.OVERFLOW
            ),
            MetalUnitConversionFailureCode.NONZERO_ROUNDED_TO_ZERO: (
                MetalUnitConversionOutcome.UNDERFLOW
            ),
        }[self.code]
        if self.outcome is not expected:
            raise ValueError("failure outcome must agree with failure code")
        if type(self.request) is not MetalUnitConversionRequest:
            raise TypeError("request must be MetalUnitConversionRequest")
        if self.definition is not None and (
            type(self.definition) is not MetalUnitConversionDefinition
        ):
            raise TypeError("definition must be MetalUnitConversionDefinition or None")
        if self.code is MetalUnitConversionFailureCode.UNSUPPORTED_UNIT_PAIR:
            if self.definition is not None:
                raise ValueError("unsupported conversion must not cite a definition")
        elif self.definition is None:
            raise ValueError("numeric conversion failure must cite its definition")
        elif self.definition.source_unit is not self.request.source.unit:
            raise ValueError(
                "definition source unit must equal the request source unit"
            )
        elif self.definition.target_unit is not self.request.target_unit:
            raise ValueError(
                "definition target unit must equal the requested target unit"
            )
        if type(self.catalog_identity) is not str:
            raise TypeError("catalog_identity must be a built-in str")
        if not self.catalog_identity:
            raise ValueError("catalog_identity must not be empty")
        if type(self.catalog_version) is not int:
            raise TypeError("catalog_version must be a built-in int")
        if self.catalog_version <= 0 or self.catalog_version > 2**63 - 1:
            raise ValueError("catalog_version must be a positive signed i64")
        if type(self.catalog_content_identity) is not ContentIdentity:
            raise TypeError("catalog_content_identity must be ContentIdentity")
        if type(self.limitations) is not tuple or any(
            type(value) is not MetalUnitConversionLimitation
            for value in self.limitations
        ):
            raise TypeError(
                "limitations must be a tuple of MetalUnitConversionLimitation"
            )
        if len(set(self.limitations)) != len(self.limitations):
            raise ValueError("limitations must be unique")


type MetalUnitConversionResult = MetalUnitConversionSuccess | MetalUnitConversionFailure
"""Closed in-memory result of an explicit metal-unit conversion."""
