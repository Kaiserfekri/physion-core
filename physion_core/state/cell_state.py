"""
cell_state.py
=============

Industrial Cell State for Physion Framework.

Purpose
-------
Owns every cell-level variable used throughout
the Physion Framework.

Architecture
------------
• Owns cell identity only.
• Contains NO battery physics.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by CellSolver.

Categories
----------
• Cell Identity
• Configuration
• Operating Mode
• Operating Limits
• Diagnostics

Notes
-----
This class is intentionally passive.

All calculations belong to CellSolver.

Physion Principles
------------------
✔ Separation of Concerns
✔ Single Source of Truth
✔ Passive State
✔ Solver Ownership
✔ Explicit Validation
✔ Industrial Readability
✔ High Performance
✔ Future Extensibility
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.state.base_state import BaseState


@dataclass(slots=True, kw_only=True)
class CellState(BaseState):
    """
    Industrial Cell State.
    """

    # =====================================================
    # Identity
    # =====================================================

    cell_name: str = ""

    cell_type: str = ""

    chemistry: str = ""

    manufacturer: str = ""

    serial_number: str = ""

    # =====================================================
    # Configuration
    # =====================================================

    parallel_cells: int = 1

    series_cells: int = 1

    nominal_capacity: float = 0.0

    nominal_voltage: float = 0.0

    nominal_energy: float = 0.0

    # =====================================================
    # Operating Mode
    # =====================================================

    charging: bool = False

    discharging: bool = False

    resting: bool = True

    balancing: bool = False

    # =====================================================
    # Operating Limits
    # =====================================================

    maximum_voltage: float = 0.0

    minimum_voltage: float = 0.0

    maximum_current: float = 0.0

    maximum_temperature: float = 0.0

    minimum_temperature: float = 0.0

    # =====================================================
    # Diagnostics
    # =====================================================

    cell_warning: bool = False

    cell_fault: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    
        # =====================================================
    # Validation
    # =====================================================

    def validate_impl(self) -> None:
        """
        Validate CellState.

        Validation only.

        No physics.
        No solver.
        No state modification.
        """

        # -------------------------------------------------
        # Cell Counts
        # -------------------------------------------------

        if self.parallel_cells < 1:
            raise ValueError(
                "parallel_cells must be at least 1."
            )

        if self.series_cells < 1:
            raise ValueError(
                "series_cells must be at least 1."
            )

        # -------------------------------------------------
        # Nominal Values
        # -------------------------------------------------

        if self.nominal_capacity < 0.0:
            raise ValueError(
                "Nominal capacity cannot be negative."
            )

        if self.nominal_voltage < 0.0:
            raise ValueError(
                "Nominal voltage cannot be negative."
            )

        if self.nominal_energy < 0.0:
            raise ValueError(
                "Nominal energy cannot be negative."
            )

        # -------------------------------------------------
        # Limits
        # -------------------------------------------------

        if self.maximum_voltage < 0.0:
            raise ValueError(
                "Maximum voltage cannot be negative."
            )

        if self.minimum_voltage < 0.0:
            raise ValueError(
                "Minimum voltage cannot be negative."
            )

        if (
            self.maximum_voltage > 0.0
            and self.minimum_voltage > self.maximum_voltage
        ):
            raise ValueError(
                "Minimum voltage cannot exceed maximum voltage."
            )

        if self.maximum_current < 0.0:
            raise ValueError(
                "Maximum current cannot be negative."
            )

        if (
            self.maximum_temperature > 0.0
            and self.minimum_temperature > self.maximum_temperature
        ):
            raise ValueError(
                "Minimum temperature cannot exceed maximum temperature."
            )

        # -------------------------------------------------
        # Operating Mode
        # -------------------------------------------------

        active_modes = (
            int(self.charging)
            + int(self.discharging)
            + int(self.resting)
        )

        if active_modes != 1:
            raise ValueError(
                "Exactly one operating mode must be active."
            )

        if self.balancing and self.resting:
            raise ValueError(
                "Balancing cannot be active while resting."
            )
            
            