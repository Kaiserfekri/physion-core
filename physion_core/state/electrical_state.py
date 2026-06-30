"""
electrical_state.py
===================

Industrial Electrical State for Physion Framework.

Purpose
-------
Owns every electrical variable used throughout the Physion
Framework.

Architecture
------------
• Owns electrical variables only.
• Contains NO physics.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by ElectricalSolver.

Categories
----------
• Voltage
• Current
• Charge
• Capacity
• Energy
• Power
• State Indicators
• Resistance
• Polarization
• Efficiency
• Losses
• Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to the appropriate solver.

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
class ElectricalState(BaseState):
    """
    Industrial Electrical State.

    Stores every electrical quantity required by
    Physion.

    This object owns the electrical state of a cell.

    No computation is performed here.
    """

    # =====================================================
    # Voltage
    # =====================================================

    terminal_voltage: float = 0.0

    ocv: float = 0.0

    equilibrium_voltage: float = 0.0

    overpotential: float = 0.0

    peak_voltage: float = 0.0

    minimum_voltage: float = 0.0

    average_voltage: float = 0.0

    voltage_drop: float = 0.0

    voltage_ripple: float = 0.0

    # =====================================================
    # Current
    # =====================================================

    current: float = 0.0

    current_density: float = 0.0

    current_ripple: float = 0.0

    maximum_current: float = 0.0

    minimum_current: float = 0.0

    average_current: float = 0.0

    reverse_current: bool = False
    # =====================================================
    # Charge
    # =====================================================

    charge: float = 0.0

    charge_transferred: float = 0.0

    charge_rate: float = 0.0

    # =====================================================
    # Capacity
    # =====================================================

    capacity_nominal: float = 0.0

    capacity_available: float = 0.0

    capacity_remaining: float = 0.0

    capacity_lost: float = 0.0

    usable_capacity: float = 0.0

    # =====================================================
    # Internal Consistency Helpers
    # =====================================================

    charge_balance_error: float = 0.0

    capacity_balance_error: float = 0.0

    capacity_fade: float = 0.0
    # =====================================================
    # Energy
    # =====================================================

    energy: float = 0.0

    energy_available: float = 0.0

    energy_remaining: float = 0.0

    energy_delivered: float = 0.0

    energy_charged: float = 0.0

    energy_loss: float = 0.0

    energy_efficiency: float = 1.0

    # =====================================================
    # Power
    # =====================================================

    power: float = 0.0

    power_charge: float = 0.0

    power_discharge: float = 0.0

    peak_power: float = 0.0

    average_power: float = 0.0

    power_loss: float = 0.0

    power_efficiency: float = 1.0

    # =====================================================
    # State Indicators
    # =====================================================

    soc: float = 0.0

    dod: float = 0.0

    soe: float = 0.0

    soh: float = 1.0

    sop: float = 1.0

    # =====================================================
    # Indicator Diagnostics
    # =====================================================

    soc_error: float = 0.0

    soe_error: float = 0.0

    soh_error: float = 0.0

    sop_error: float = 0.0
    # =====================================================
    # Electrical Resistance
    # =====================================================

    ohmic_resistance: float = 0.0

    contact_resistance: float = 0.0

    electrolyte_resistance: float = 0.0

    electrode_resistance: float = 0.0

    separator_resistance: float = 0.0

    interfacial_resistance: float = 0.0

    film_resistance: float = 0.0

    charge_transfer_resistance: float = 0.0

    diffusion_resistance: float = 0.0

    total_resistance: float = 0.0

    effective_resistance: float = 0.0

    # =====================================================
    # Polarization
    # =====================================================

    activation_polarization: float = 0.0

    ohmic_polarization: float = 0.0

    concentration_polarization: float = 0.0

    diffusion_polarization: float = 0.0

    reaction_polarization: float = 0.0

    electrolyte_polarization: float = 0.0

    anode_polarization: float = 0.0

    cathode_polarization: float = 0.0

    interfacial_polarization: float = 0.0

    total_polarization: float = 0.0

    effective_overpotential: float = 0.0
    # =====================================================
    # Electrical Efficiency
    # =====================================================

    coulombic_efficiency: float = 1.0

    energy_efficiency: float = 1.0

    voltage_efficiency: float = 1.0

    power_efficiency: float = 1.0

    charge_efficiency: float = 1.0

    discharge_efficiency: float = 1.0

    round_trip_efficiency: float = 1.0

    conversion_efficiency: float = 1.0

    # =====================================================
    # Electrical Losses
    # =====================================================

    ohmic_loss: float = 0.0

    activation_loss: float = 0.0

    concentration_loss: float = 0.0

    joule_heating_loss: float = 0.0

    side_reaction_loss: float = 0.0

    leakage_loss: float = 0.0

    parasitic_loss: float = 0.0

    total_electrical_loss: float = 0.0

    # =====================================================
    # Diagnostics
    # =====================================================

    electrical_fault: bool = False

    short_circuit_detected: bool = False

    open_circuit_detected: bool = False

    reverse_current_detected: bool = False

    over_voltage: bool = False

    under_voltage: bool = False

    over_current: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    