"""
cell_state.py
=============

Industrial Cell State for Physion Framework.

Purpose
-------
Owns the identity, configuration and metadata
of a battery cell.

Notes
-----
CellState is NOT a physics state.

It never stores:

- Voltage
- Current
- Temperature
- Stress
- Concentration
- SOC
- SOH

Those belong to their dedicated states.

Physion Principles
------------------
✔ Separation of Concerns

✔ Single Source of Truth

✔ Passive State

✔ Explicit Validation

✔ High Readability

✔ Future Extensibility
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from physion_core.state.base_state import BaseState

from physion_core.cell.cell_enums import (
    CellFormat,
    CellChemistry,
    CellOperatingMode,
    CellLifecycleStatus,
    CellHealthStatus,
    DiagnosticStatus,
)

# ==========================================================
# Cell Identity
# ==========================================================

@dataclass(slots=True, kw_only=True)
class CellIdentity:

    manufacturer: str = ""

    model: str = ""

    serial_number: str = ""

    batch_number: str = ""

    production_date: date | None = None

    revision: str = ""
    
    # ==========================================================
# Cell Configuration
# ==========================================================

@dataclass(slots=True, kw_only=True)
class CellConfiguration:

    chemistry: CellChemistry = CellChemistry.NMC

    cell_format: CellFormat = CellFormat.CYLINDRICAL

    series_cells: int = 1

    parallel_cells: int = 1

    nominal_capacity_ah: float = 0.0

    nominal_voltage_v: float = 0.0

    nominal_energy_wh: float = 0.0


# ==========================================================
# Cell Operating Limits
# ==========================================================

@dataclass(slots=True, kw_only=True)
class CellLimits:

    maximum_voltage_v: float = 0.0

    minimum_voltage_v: float = 0.0

    maximum_charge_current_a: float = 0.0

    maximum_discharge_current_a: float = 0.0

    maximum_temperature_k: float = 0.0

    minimum_temperature_k: float = 0.0

    maximum_pressure_pa: float = 0.0
    
    # ==========================================================
# Cell Metadata
# ==========================================================

@dataclass(slots=True, kw_only=True)
class CellMetadata:

    operating_mode: CellOperatingMode = (
        CellOperatingMode.INITIALIZATION
    )

    lifecycle_status: CellLifecycleStatus = (
        CellLifecycleStatus.MANUFACTURED
    )

    health_status: CellHealthStatus = (
        CellHealthStatus.EXCELLENT
    )

    diagnostic_status: DiagnosticStatus = (
        DiagnosticStatus.NORMAL
    )

    enabled: bool = True

    initialized: bool = False

    validated: bool = False

    archived: bool = False

    user_tag: str = ""

    description: str = ""
    
    # ==========================================================
# Cell State
# ==========================================================

@dataclass(slots=True, kw_only=True)
class CellState(BaseState):
    """
    Industrial Cell State.

    Owns the identity, configuration and
    metadata of a battery cell.

    This class intentionally contains
    NO electrochemical variables.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    identity: CellIdentity = field(
        default_factory=CellIdentity
    )

    # ------------------------------------------------------
    # Configuration
    # ------------------------------------------------------

    configuration: CellConfiguration = field(
        default_factory=CellConfiguration
    )

    # ------------------------------------------------------
    # Operating Limits
    # ------------------------------------------------------

    limits: CellLimits = field(
        default_factory=CellLimits
    )

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    metadata: CellMetadata = field(
        default_factory=CellMetadata
    )
    
        # =====================================================
    # Validation
    # =====================================================

    def validate_impl(self) -> None:
        """
        Validate CellState.

        CellState owns only identity,
        configuration and metadata.

        No physics validation is performed here.
        """

        # ---------------------------------------------
        # Configuration
        # ---------------------------------------------

        if self.configuration.series_cells < 1:
            raise ValueError(
                "series_cells must be >= 1."
            )

        if self.configuration.parallel_cells < 1:
            raise ValueError(
                "parallel_cells must be >= 1."
            )

        if self.configuration.nominal_capacity_ah < 0.0:
            raise ValueError(
                "nominal_capacity_ah cannot be negative."
            )

        if self.configuration.nominal_voltage_v < 0.0:
            raise ValueError(
                "nominal_voltage_v cannot be negative."
            )

        if self.configuration.nominal_energy_wh < 0.0:
            raise ValueError(
                "nominal_energy_wh cannot be negative."
            )

        # ---------------------------------------------
        # Limits
        # ---------------------------------------------

        if (
            self.limits.maximum_voltage_v
            <
            self.limits.minimum_voltage_v
        ):
            raise ValueError(
                "Maximum voltage must be >= minimum voltage."
            )

        if (
            self.limits.maximum_temperature_k
            <
            self.limits.minimum_temperature_k
        ):
            raise ValueError(
                "Maximum temperature must be >= minimum temperature."
            )

        # ---------------------------------------------
        # Identity
        # ---------------------------------------------

        if not self.identity.serial_number.strip():
            raise ValueError(
                "serial_number cannot be empty."
            )
            
            
            