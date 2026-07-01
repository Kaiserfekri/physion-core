"""
chemistry_update.py
===================

Industrial Chemistry Update Object
for Physion Framework.

Purpose
-------
Carries the final chemistry solution produced by
ChemistrySolver.

Architecture
------------
ChemistrySolver
        ↓
ChemistryUpdate
        ↓
Commit Manager
        ↓
ChemistryState

Mirror
------
This object is an exact mirror of ChemistryState.

Contains
--------
• NO physics
• NO numerical methods
• NO solver logic
• NO commit logic
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ChemistryUpdate(BaseUpdate):

    # =====================================================
    # Species Concentration
    # =====================================================

    concentration_li: float
    concentration_li_plus: float
    concentration_electrolyte: float
    concentration_anode: float
    concentration_cathode: float
    concentration_surface: float
    concentration_bulk: float
    concentration_average: float

    # =====================================================
    # Lithium Inventory
    # =====================================================

    lithium_inventory: float
    lithium_inventory_loss: float
    cyclable_lithium: float
    trapped_lithium: float
    active_lithium: float
    inactive_lithium: float

    # =====================================================
    # Stoichiometry
    # =====================================================

    stoichiometry_anode: float
    stoichiometry_cathode: float
    average_stoichiometry: float
    stoichiometry_surface: float
    stoichiometry_bulk: float

    # =====================================================
    # Electrolyte
    # =====================================================

    electrolyte_concentration: float
    electrolyte_potential: float
    electrolyte_activity: float
    electrolyte_conductivity: float
    electrolyte_diffusivity: float
    electrolyte_porosity: float
    electrolyte_tortuosity: float

    # =====================================================
    # Solid Phase
    # =====================================================

    solid_potential: float
    solid_concentration: float
    solid_diffusivity: float
    solid_conductivity: float
    particle_surface_concentration: float
    particle_average_concentration: float

    # =====================================================
    # Diffusion
    # =====================================================

    diffusion_flux: float
    lithium_flux: float
    electrolyte_flux: float
    solid_flux: float
    diffusion_coefficient: float
    effective_diffusion: float
    diffusion_overpotential: float

    # =====================================================
    # Reaction
    # =====================================================

    reaction_rate: float
    reaction_current: float
    reaction_area: float
    reaction_extent: float
    reaction_progress: float
    faradaic_current: float

    # =====================================================
    # Exchange Current
    # =====================================================

    exchange_current_density: float
    exchange_current: float
    effective_exchange_current: float

    # =====================================================
    # Charge Transfer
    # =====================================================

    charge_transfer_rate: float
    transfer_coefficient_anode: float
    transfer_coefficient_cathode: float
    charge_transfer_overpotential: float

    # =====================================================
    # Thermodynamics
    # =====================================================

    gibbs_free_energy: float
    entropy: float
    enthalpy: float
    chemical_potential: float
    electrochemical_potential: float

    # =====================================================
    # Kinetics
    # =====================================================

    butler_volmer_rate: float
    tafel_slope: float
    reaction_constant: float
    activation_energy: float
    kinetic_factor: float

    # =====================================================
    # Transport Properties
    # =====================================================

    ionic_conductivity: float
    ionic_mobility: float
    transport_number: float

    # =====================================================
    # Solid Electrolyte Interphase (SEI)
    # =====================================================

    sei_thickness: float
    sei_growth_rate: float
    sei_resistance: float
    sei_porosity: float
    sei_conductivity: float
    sei_lithium_consumption: float
    sei_volume: float
    sei_mass: float

    # =====================================================
    # Lithium Plating
    # =====================================================

    plating_rate: float
    stripped_lithium: float
    plated_lithium: float
    plating_current: float
    plating_thickness: float
    plating_fraction: float

    # =====================================================
    # Side Reactions
    # =====================================================

    side_reaction_rate: float
    side_reaction_current: float
    gas_generation: float
    gas_pressure: float
    electrolyte_decomposition: float
    solvent_consumption: float
    salt_consumption: float

    # =====================================================
    # Electrochemical Diagnostics
    # =====================================================

    reaction_uniformity: float
    diffusion_limitation: float
    concentration_limitation: float
    lithium_balance: float
    charge_balance: float
    mass_balance: float

    chemistry_warning: bool
    chemistry_fault: bool
    measurement_valid: bool
    solver_converged: bool
    validation_passed: bool