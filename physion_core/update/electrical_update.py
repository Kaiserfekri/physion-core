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
CommitManager
        ↓
ElectricalState

Notes
-----
Mirror of ElectricalState.

Contains NO physics.

Contains NO solver logic.

Contains NO commit logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from physion_core.update.base_update import BaseUpdate


@dataclass(frozen=True, slots=True, kw_only=True)
class ElectricalUpdate(BaseUpdate):

    # =====================================================
    # Voltage
    # =====================================================

    terminal_voltage: float

    ocv: float

    equilibrium_voltage: float

    overpotential: float

    peak_voltage: float

    minimum_voltage: float

    average_voltage: float

    voltage_drop: float

    voltage_ripple: float

    # =====================================================
    # Current
    # =====================================================

    current: float

    current_density: float

    current_ripple: float

    maximum_current: float

    minimum_current: float

    average_current: float

    # =====================================================
    # Charge
    # =====================================================

    charge: float

    charge_transferred: float

    charge_rate: float

    # =====================================================
    # Capacity
    # =====================================================

    capacity_nominal: float

    capacity_available: float

    capacity_remaining: float

    capacity_lost: float

    usable_capacity: float

    # =====================================================
    # Internal Consistency Helpers
    # =====================================================

    charge_balance_error: float

    capacity_balance_error: float

    capacity_fade: float

    # =====================================================
    # Energy
    # =====================================================

    energy: float

    energy_available: float

    energy_remaining: float

    energy_delivered: float

    energy_charged: float

    energy_loss: float

    energy_efficiency: float

    # =====================================================
    # Power
    # =====================================================

    power: float

    power_charge: float

    power_discharge: float

    peak_power: float

    average_power: float

    power_loss: float

    power_efficiency: float

    # =====================================================
    # State Indicators
    # =====================================================

    soc: float

    dod: float

    soe: float

    soh: float

    sop: float

    # =====================================================
    # Indicator Diagnostics
    # =====================================================

    soc_error: float

    soe_error: float

    soh_error: float

    sop_error: float

    # =====================================================
    # Electrical Resistance
    # =====================================================

    ohmic_resistance: float

    contact_resistance: float

    electrolyte_resistance: float

    electrode_resistance: float

    separator_resistance: float

    interfacial_resistance: float

    film_resistance: float

    charge_transfer_resistance: float

    diffusion_resistance: float

    total_resistance: float

    effective_resistance: float

    # =====================================================
    # Polarization
    # =====================================================

    activation_polarization: float

    ohmic_polarization: float

    concentration_polarization: float

    diffusion_polarization: float

    reaction_polarization: float

    electrolyte_polarization: float

    anode_polarization: float

    cathode_polarization: float

    interfacial_polarization: float

    total_polarization: float

    effective_overpotential: float

    # =====================================================
    # Electrical Efficiency
    # =====================================================

    coulombic_efficiency: float

    energy_efficiency: float

    voltage_efficiency: float

    power_efficiency: float

    charge_efficiency: float

    discharge_efficiency: float

    round_trip_efficiency: float

    conversion_efficiency: float

    # =====================================================
    # Electrical Losses
    # =====================================================

    ohmic_loss: float

    activation_loss: float

    concentration_loss: float

    joule_heating_loss: float

    side_reaction_loss: float

    leakage_loss: float

    parasitic_loss: float

    total_electrical_loss: float

    # =====================================================
    # Diagnostics
    # =====================================================

    electrical_fault: bool

    short_circuit_detected: bool

    open_circuit_detected: bool

    reverse_current_detected: bool

    over_voltage: bool

    under_voltage: bool

    over_current: bool

    measurement_valid: bool

    solver_converged: bool

    validation_passed: bool

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> bool:

        numeric_values = (
            value
            for value in vars(self).values()
            if isinstance(value, float)
        )

        if not all(isfinite(v) for v in numeric_values):
            return False

        return super().validate()