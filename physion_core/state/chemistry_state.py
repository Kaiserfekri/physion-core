"""
chemistry_state.py
==================

Industrial Chemistry State for Physion Framework.

Purpose
-------
Owns every electrochemical variable used throughout the Physion
Framework.

Architecture
------------
• Owns chemistry variables only.
• Contains NO physics.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by ChemistrySolver.

Categories
----------
• Species Concentration
• Lithium Inventory
• Stoichiometry
• Electrolyte
• Solid Phase
• Diffusion
• Reaction
• Exchange Current
• Charge Transfer
• Thermodynamics
• Kinetics
• Transport
• SEI
• Lithium Plating
• Side Reactions
• Electrochemical Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to ChemistrySolver.

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
class ChemistryState(BaseState):
    """
    Industrial Chemistry State.

    Stores every electrochemical quantity required by
    Physion.

    This object owns the chemistry state of a cell.

    No computation is performed here.
    """
    # =====================================================
    # Species Concentration
    # =====================================================

    concentration_li: float = 0.0

    concentration_li_plus: float = 0.0

    concentration_electrolyte: float = 0.0

    concentration_anode: float = 0.0

    concentration_cathode: float = 0.0

    concentration_surface: float = 0.0

    concentration_bulk: float = 0.0

    concentration_average: float = 0.0
    # =====================================================
    # Lithium Inventory
    # =====================================================

    lithium_inventory: float = 0.0

    lithium_inventory_loss: float = 0.0

    cyclable_lithium: float = 0.0

    trapped_lithium: float = 0.0

    active_lithium: float = 0.0

    inactive_lithium: float = 0.0
    # =====================================================
    # Stoichiometry
    # =====================================================

    stoichiometry_anode: float = 0.0

    stoichiometry_cathode: float = 0.0

    average_stoichiometry: float = 0.0

    stoichiometry_surface: float = 0.0

    stoichiometry_bulk: float = 0.0
    # =====================================================
    # Electrolyte
    # =====================================================

    electrolyte_concentration: float = 0.0

    electrolyte_potential: float = 0.0

    electrolyte_activity: float = 0.0

    electrolyte_conductivity: float = 0.0

    electrolyte_diffusivity: float = 0.0

    electrolyte_porosity: float = 0.0

    electrolyte_tortuosity: float = 0.0
    # =====================================================
    # Solid Phase
    # =====================================================

    solid_potential: float = 0.0

    solid_concentration: float = 0.0

    solid_diffusivity: float = 0.0

    solid_conductivity: float = 0.0

    particle_surface_concentration: float = 0.0

    particle_average_concentration: float = 0.0
    # =====================================================
    # Diffusion
    # =====================================================

    diffusion_flux: float = 0.0

    lithium_flux: float = 0.0

    electrolyte_flux: float = 0.0

    solid_flux: float = 0.0

    diffusion_coefficient: float = 0.0

    effective_diffusion: float = 0.0

    diffusion_overpotential: float = 0.0
    # =====================================================
    # Reaction
    # =====================================================

    reaction_rate: float = 0.0

    reaction_current: float = 0.0

    reaction_area: float = 0.0

    reaction_extent: float = 0.0

    reaction_progress: float = 0.0

    faradaic_current: float = 0.0
    # =====================================================
    # Exchange Current
    # =====================================================

    exchange_current_density: float = 0.0

    exchange_current: float = 0.0

    effective_exchange_current: float = 0.0
    # =====================================================
    # Charge Transfer
    # =====================================================

    charge_transfer_rate: float = 0.0

    transfer_coefficient_anode: float = 0.0

    transfer_coefficient_cathode: float = 0.0

    charge_transfer_overpotential: float = 0.0
    # =====================================================
    # Thermodynamics
    # =====================================================

    gibbs_free_energy: float = 0.0

    entropy: float = 0.0

    enthalpy: float = 0.0

    chemical_potential: float = 0.0

    electrochemical_potential: float = 0.0
    # =====================================================
    # Kinetics
    # =====================================================

    butler_volmer_rate: float = 0.0

    tafel_slope: float = 0.0

    reaction_constant: float = 0.0

    activation_energy: float = 0.0

    kinetic_factor: float = 0.0
    # =====================================================
    # Transport Properties
    # =====================================================

    ionic_conductivity: float = 0.0

    ionic_mobility: float = 0.0

    transport_number: float = 0.0
    # =====================================================
    # Solid Electrolyte Interphase (SEI)
    # =====================================================

    sei_thickness: float = 0.0

    sei_growth_rate: float = 0.0

    sei_resistance: float = 0.0

    sei_porosity: float = 0.0

    sei_conductivity: float = 0.0

    sei_lithium_consumption: float = 0.0

    sei_volume: float = 0.0

    sei_mass: float = 0.0
    # =====================================================
    # Lithium Plating
    # =====================================================

    plating_rate: float = 0.0

    stripped_lithium: float = 0.0

    plated_lithium: float = 0.0

    plating_current: float = 0.0

    plating_thickness: float = 0.0

    plating_fraction: float = 0.0
    # =====================================================
    # Side Reactions
    # =====================================================

    side_reaction_rate: float = 0.0

    side_reaction_current: float = 0.0

    gas_generation: float = 0.0

    gas_pressure: float = 0.0

    electrolyte_decomposition: float = 0.0

    solvent_consumption: float = 0.0

    salt_consumption: float = 0.0
    # =====================================================
    # Electrochemical Diagnostics
    # =====================================================

    reaction_uniformity: float = 0.0

    diffusion_limitation: float = 0.0

    concentration_limitation: float = 0.0

    lithium_balance: float = 0.0

    charge_balance: float = 0.0

    mass_balance: float = 0.0

    chemistry_warning: bool = False

    chemistry_fault: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    