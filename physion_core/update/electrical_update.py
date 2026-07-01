"""
electrical_update.py
====================

Industrial Electrical Update Object
for Physion Framework.

Purpose
-------
Carries the final electrical solution produced by
ElectricalSolver.

Architecture
------------
ElectricalSolver
        ↓
ElectricalUpdate
        ↓
Commit Manager
        ↓
ElectricalState

Contains
--------
Final electrical values only.

Contains NO equations.

Contains NO solver logic.

Contains NO commit logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(frozen=True, slots=True, kw_only=True)
class ElectricalUpdate(BaseUpdate):
    """
    Immutable electrical update.

    Produced exclusively by ElectricalSolver.
    """

    # =====================================================
    # Electrical Solution
    # =====================================================

    voltage: float

    current: float

    power: float

    state_of_charge: float

    open_circuit_voltage: float

    terminal_voltage: float

    internal_resistance: float

    overpotential: float

    coulombic_efficiency: float

    electrical_efficiency: float

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> bool:

        if self.capacity < 0.0:

            return False

        if self.state_of_charge < 0.0:

            return False

        if self.state_of_charge > 1.0:

            return False

        if self.state_of_health < 0.0:

            return False

        if self.state_of_health > 1.0:

            return False

        return super().validate()