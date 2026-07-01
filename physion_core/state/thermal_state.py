"""
thermal_state.py
================

Industrial Thermal State for Physion Framework.

Purpose
-------
Owns every thermal variable used throughout the Physion
Framework.

Architecture
------------
• Owns thermal variables only.
• Contains NO physics.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by ThermalSolver.

Categories
----------
• Temperature
• Temperature Gradient
• Heat
• Heat Capacity
• Heat Generation
• Heat Transfer
• Thermal Resistance
• Thermal Conductivity
• Boundary Conditions
• Cooling
• Heating
• Thermal Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to ThermalSolver.

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
class ThermalState(BaseState):
    """
    Industrial Thermal State.

    Stores every thermal quantity required by
    Physion.

    This object owns the thermal state of a cell.

    No computation is performed here.
    """
        # =====================================================
    # Temperature
    # =====================================================

    temperature: float = 298.15

    surface_temperature: float = 298.15

    core_temperature: float = 298.15

    ambient_temperature: float = 298.15

    reference_temperature: float = 298.15

    delta_temperature: float = 0.0
        # =====================================================
    # Temperature Gradient
    # =====================================================

    temperature_gradient: float = 0.0

    gradient_x: float = 0.0

    gradient_y: float = 0.0

    gradient_z: float = 0.0

    maximum_gradient: float = 0.0
        # =====================================================
    # Heat
    # =====================================================

    heat: float = 0.0

    internal_heat: float = 0.0

    stored_heat: float = 0.0

    released_heat: float = 0.0

    heat_flux: float = 0.0
        # =====================================================
    # Heat Capacity
    # =====================================================

    heat_capacity: float = 0.0

    specific_heat: float = 0.0

    effective_heat_capacity: float = 0.0

    volumetric_heat_capacity: float = 0.0
        # =====================================================
    # Heat Generation
    # =====================================================

    heat_generation: float = 0.0

    joule_heat: float = 0.0

    reaction_heat: float = 0.0

    entropic_heat: float = 0.0

    irreversible_heat: float = 0.0

    reversible_heat: float = 0.0

    side_reaction_heat: float = 0.0

    total_heat_generation: float = 0.0
        # =====================================================
    # Heat Transfer
    # =====================================================

    conduction_heat: float = 0.0

    convection_heat: float = 0.0

    radiation_heat: float = 0.0

    thermal_flux: float = 0.0

    heat_transfer_rate: float = 0.0
        # =====================================================
    # Thermal Resistance
    # =====================================================

    thermal_resistance: float = 0.0

    contact_thermal_resistance: float = 0.0

    interface_thermal_resistance: float = 0.0

    total_thermal_resistance: float = 0.0
        # =====================================================
    # Thermal Conductivity
    # =====================================================

    thermal_conductivity: float = 0.0

    effective_thermal_conductivity: float = 0.0

    conductivity_x: float = 0.0

    conductivity_y: float = 0.0

    conductivity_z: float = 0.0
        # =====================================================
    # Boundary Conditions
    # =====================================================

    boundary_temperature: float = 298.15

    boundary_heat_flux: float = 0.0

    boundary_convection: float = 0.0

    boundary_radiation: float = 0.0
        # =====================================================
    # Cooling
    # =====================================================

    cooling_power: float = 0.0

    cooling_rate: float = 0.0

    coolant_temperature: float = 298.15

    coolant_flow_rate: float = 0.0

    cooling_efficiency: float = 1.0
        # =====================================================
    # Heating
    # =====================================================

    heater_power: float = 0.0

    heater_efficiency: float = 1.0

    heater_enabled: bool = False
        # =====================================================
    # Thermal Diagnostics
    # =====================================================

    maximum_temperature: float = 298.15

    minimum_temperature: float = 298.15

    average_temperature: float = 298.15

    temperature_uniformity: float = 1.0

    thermal_runaway_detected: bool = False

    over_temperature: bool = False

    under_temperature: bool = False

    thermal_warning: bool = False

    thermal_fault: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    