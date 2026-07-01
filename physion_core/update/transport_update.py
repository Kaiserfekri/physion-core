"""
transport_update.py
===================

Industrial Transport Update Object
for Physion Framework.

Purpose
-------
Carries the final transport solution produced by
TransportSolver.

Architecture
------------
TransportSolver
        ↓
TransportUpdate
        ↓
CommitManager
        ↓
TransportState

Mirror
------
This object is an exact mirror of TransportState.

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
class TransportUpdate(BaseUpdate):

    # =====================================================
    # Species Flux
    # =====================================================

    lithium_flux: float

    electrolyte_flux: float

    solvent_flux: float

    salt_flux: float

    species_flux: float

    average_species_flux: float

    # =====================================================
    # Mass Flux
    # =====================================================

    mass_flux: float

    mass_flux_anode: float

    mass_flux_cathode: float

    mass_flux_separator: float

    net_mass_flux: float

    average_mass_flux: float

    # =====================================================
    # Diffusion Flux
    # =====================================================

    diffusion_flux: float

    diffusion_flux_anode: float

    diffusion_flux_cathode: float

    effective_diffusion_flux: float

    average_diffusion_flux: float

    # =====================================================
    # Migration Flux
    # =====================================================

    migration_flux: float

    ionic_migration_flux: float

    electronic_migration_flux: float

    average_migration_flux: float

    # =====================================================
    # Convection Flux
    # =====================================================

    convection_flux: float

    electrolyte_convection: float

    solvent_convection: float

    average_convection_flux: float

    # =====================================================
    # Transport Rates
    # =====================================================

    transport_rate: float

    diffusion_rate: float

    migration_rate: float

    convection_rate: float

    # =====================================================
    # Transport Diagnostics
    # =====================================================

    transport_limitation: float

    diffusion_limitation: float

    migration_limitation: float

    convection_limitation: float

    transport_balance: float

    transport_warning: bool

    transport_fault: bool

    measurement_valid: bool

    solver_converged: bool

    validation_passed: bool