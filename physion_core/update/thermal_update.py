"""
thermal_update.py
=================

Industrial Thermal Update Object
for Physion Framework.

Purpose
-------
Carries the final thermal solution produced by
ThermalSolver.

Architecture
------------
ThermalSolver
        ↓
ThermalUpdate
        ↓
Commit Manager
        ↓
ThermalState

Contains
--------
Final thermal values only.

Contains NO equations.

Contains NO solver logic.

Contains NO commit logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(frozen=True, slots=True, kw_only=True)
class ThermalUpdate(BaseUpdate):
    """
    Immutable thermal update.

    Produced exclusively by ThermalSolver.
    """

    # =====================================================
    # Thermal Solution
    # =====================================================

    temperature: float

    ambient_temperature: float

    heat_generation: float

    reversible_heat: float

    irreversible_heat: float

    conductive_heat_flux: float

    convective_heat_flux: float

    radiative_heat_flux: float

    thermal_conductivity: float

    specific_heat_capacity: float

    thermal_resistance: float

    thermal_efficiency: float

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> bool:

        if self.temperature < 0.0:
            return False

        if self.ambient_temperature < 0.0:
            return False

        if self.thermal_conductivity < 0.0:
            return False

        if self.specific_heat_capacity < 0.0:
            return False

        if self.thermal_resistance < 0.0:
            return False

        return super().validate()