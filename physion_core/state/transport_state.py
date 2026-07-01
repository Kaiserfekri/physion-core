"""
transport_state.py
==================

Industrial Transport State for Physion Framework.

Purpose
-------
Owns every transport-related state variable used throughout
the Physion Framework.

Architecture
------------
• Owns transport variables only.
• Contains NO physics.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by TransportSolver.

Categories
----------
• Species Flux
• Mass Flux
• Diffusion Flux
• Migration Flux
• Convection Flux
• Transport Rates
• Transport Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to TransportSolver.

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
class TransportState(BaseState):
    """
    Industrial Transport State.

    Stores every transport-related quantity required
    by Physion.

    No computation is performed here.
    """
    # =====================================================
    # Species Flux
    # =====================================================

    lithium_flux: float = 0.0

    electrolyte_flux: float = 0.0

    solvent_flux: float = 0.0

    salt_flux: float = 0.0

    species_flux: float = 0.0

    average_species_flux: float = 0.0
    # =====================================================
    # Mass Flux
    # =====================================================

    mass_flux: float = 0.0

    mass_flux_anode: float = 0.0

    mass_flux_cathode: float = 0.0

    mass_flux_separator: float = 0.0

    net_mass_flux: float = 0.0

    average_mass_flux: float = 0.0
    # =====================================================
    # Diffusion Flux
    # =====================================================

    diffusion_flux: float = 0.0

    diffusion_flux_anode: float = 0.0

    diffusion_flux_cathode: float = 0.0

    effective_diffusion_flux: float = 0.0

    average_diffusion_flux: float = 0.0
    # =====================================================
    # Migration Flux
    # =====================================================

    migration_flux: float = 0.0

    ionic_migration_flux: float = 0.0

    electronic_migration_flux: float = 0.0

    average_migration_flux: float = 0.0
    # =====================================================
    # Convection Flux
    # =====================================================

    convection_flux: float = 0.0

    electrolyte_convection: float = 0.0

    solvent_convection: float = 0.0

    average_convection_flux: float = 0.0
    # =====================================================
    # Transport Rates
    # =====================================================

    transport_rate: float = 0.0

    diffusion_rate: float = 0.0

    migration_rate: float = 0.0

    convection_rate: float = 0.0
    # =====================================================
    # Transport Diagnostics
    # =====================================================

    transport_limitation: float = 0.0

    diffusion_limitation: float = 0.0

    migration_limitation: float = 0.0

    convection_limitation: float = 0.0

    transport_balance: float = 0.0

    transport_warning: bool = False

    transport_fault: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True

