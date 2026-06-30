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
from math import isfinite

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
    
    # =====================================================
    # Validation
    # =====================================================

    def validate_impl(self) -> None:
        """
        Validate the internal consistency of the electrical state.

        Responsibilities
        ----------------
        • Verify numerical validity.
        • Verify state indicator ranges.
        • Verify capacity consistency.
        • Verify energy consistency.
        • Verify resistance consistency.
        • Verify efficiency consistency.

        Notes
        -----
        This method performs validation only.

        It must never:
            • modify state variables,
            • execute physics,
            • call solvers,
            • repair invalid values.
        """

            # -------------------------------------------------
        # Step 1
        # Finite Number Validation
        # -------------------------------------------------

        float_fields = (
            # Voltage
            self.terminal_voltage,
            self.ocv,
            self.equilibrium_voltage,
            self.overpotential,
            self.peak_voltage,
            self.minimum_voltage,
            self.average_voltage,
            self.voltage_drop,
            self.voltage_ripple,

            # Current
            self.current,
            self.current_density,
            self.current_ripple,
            self.maximum_current,
            self.minimum_current,
            self.average_current,

            # Charge
            self.charge,
            self.charge_transferred,
            self.charge_rate,

            # Capacity
            self.capacity_nominal,
            self.capacity_available,
            self.capacity_remaining,
            self.capacity_lost,
            self.usable_capacity,

            # Energy
            self.energy,
            self.energy_available,
            self.energy_remaining,
            self.energy_delivered,
            self.energy_charged,
            self.energy_loss,
            self.energy_efficiency,

            # Power
            self.power,
            self.power_charge,
            self.power_discharge,
            self.peak_power,
            self.average_power,
            self.power_loss,
            self.power_efficiency,

            # State Indicators
            self.soc,
            self.dod,
            self.soe,
            self.soh,
            self.sop,

            # Resistance
            self.ohmic_resistance,
            self.contact_resistance,
            self.electrolyte_resistance,
            self.electrode_resistance,
            self.separator_resistance,
            self.interfacial_resistance,
            self.film_resistance,
            self.charge_transfer_resistance,
            self.diffusion_resistance,
            self.total_resistance,
            self.effective_resistance,

            # Polarization
            self.activation_polarization,
            self.ohmic_polarization,
            self.concentration_polarization,
            self.diffusion_polarization,
            self.reaction_polarization,
            self.electrolyte_polarization,
            self.anode_polarization,
            self.cathode_polarization,
            self.interfacial_polarization,
            self.total_polarization,
            self.effective_overpotential,

            # Efficiency
            self.coulombic_efficiency,
            self.voltage_efficiency,
            self.charge_efficiency,
            self.discharge_efficiency,
            self.round_trip_efficiency,
            self.conversion_efficiency,

            # Losses
            self.ohmic_loss,
            self.activation_loss,
            self.concentration_loss,
            self.joule_heating_loss,
            self.side_reaction_loss,
            self.leakage_loss,
            self.parasitic_loss,
            self.total_electrical_loss,

            # Internal Validation Metrics
            self.charge_balance_error,
            self.capacity_balance_error,
            self.capacity_fade,
            self.soc_error,
            self.soe_error,
            self.soh_error,
            self.sop_error,
        )

        if not all(isfinite(value) for value in float_fields):
            raise ValueError(
                "ElectricalState contains NaN or infinite values."
            )
    charge_balance_error

    capacity_balance_error

    capacity_fade

    soc_error

    soe_error

    soh_error

    sop_error
    