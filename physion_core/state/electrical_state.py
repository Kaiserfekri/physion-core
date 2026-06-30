"""
electrical_state.py
===================

Electrical state of a battery cell.

Responsibilities
----------------
• Terminal voltage
• Open-circuit voltage
• Current
• Power
• Capacity
• SOC / DOD
• Electrical resistance
• Polarization
• Electrical diagnostics

Contains NO physics equations.

Contains NO solver logic.

All values are updated only by the Electrical Solver.
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.state.base_state import BaseState


@dataclass(slots=True, kw_only=True)
class ElectricalState(BaseState):
    """
    Electrical state container.

    Owns every electrical variable inside the simulation.
    """

    # =====================================================
    # Voltage
    # =====================================================

    terminal_voltage: float = 0.0

    ocv: float = 0.0

    equilibrium_voltage: float = 0.0

    overpotential: float = 0.0

    # =====================================================
    # Current
    # =====================================================

    current: float = 0.0

    current_density: float = 0.0

    # =====================================================
    # Power / Energy
    # =====================================================

    power: float = 0.0

    energy: float = 0.0

    # =====================================================
    # Capacity
    # =====================================================

    capacity_nominal: float = 0.0

    capacity_available: float = 0.0

    capacity_remaining: float = 0.0

    # =====================================================
    # State of Charge
    # =====================================================

    soc: float = 0.0

    dod: float = 0.0

    # =====================================================
    # Resistance
    # =====================================================

    ohmic_resistance: float = 0.0

    contact_resistance: float = 0.0

    total_resistance: float = 0.0

    # =====================================================
    # Polarization
    # =====================================================

    activation_polarization: float = 0.0

    concentration_polarization: float = 0.0

    ohmic_polarization: float = 0.0

    total_polarization: float = 0.0

    # =====================================================
    # Diagnostics
    # =====================================================

    coulombic_efficiency: float = 1.0

    voltage_drop: float = 0.0

    power_loss: float = 0.0

    # =====================================================
    # Validation
    # =====================================================

    def validate_impl(self) -> None:
        """
        Validate electrical state.

        Real validation rules will be expanded as
        the framework evolves.
        """

        if not (0.0 <= self.soc <= 1.0):
            raise ValueError("SOC must be between 0 and 1.")

        if not (0.0 <= self.dod <= 1.0):
            raise ValueError("DOD must be between 0 and 1.")

        if self.total_resistance < 0.0:
            raise ValueError("Resistance cannot be negative.")

        if self.capacity_remaining < 0.0:
            raise ValueError("Remaining capacity cannot be negative.")