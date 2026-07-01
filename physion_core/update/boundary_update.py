"""
boundary_update.py
==================

Industrial Boundary Update Object
for Physion Framework.

Purpose
-------
Carries the final boundary-condition solution
produced by BoundarySolver.

Architecture
------------
BoundarySolver
        ↓
BoundaryUpdate
        ↓
CommitManager
        ↓
BoundaryState

Mirror
------
This object is an exact mirror of BoundaryState.

Contains
--------
• NO physics equations
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
class BoundaryUpdate(BaseUpdate):

    # =====================================================
    # Electrical Boundary
    # =====================================================

    applied_current: float

    applied_voltage: float

    applied_power: float

    load_resistance: float

    # =====================================================
    # Thermal Boundary
    # =====================================================

    ambient_temperature: float

    ambient_pressure: float

    heat_flux_boundary: float

    convective_heat_transfer_coefficient: float

    radiative_heat_transfer_coefficient: float

    # =====================================================
    # Mechanical Boundary
    # =====================================================

    applied_force: float

    applied_pressure: float

    displacement_constraint: float

    fixed_constraint: bool

    # =====================================================
    # Chemical Boundary
    # =====================================================

    concentration_boundary: float

    species_flux_boundary: float

    # =====================================================
    # Transport Boundary
    # =====================================================

    diffusion_flux_boundary: float

    migration_flux_boundary: float

    # =====================================================
    # Boundary Diagnostics
    # =====================================================

    boundary_warning: bool

    boundary_fault: bool

    boundary_valid: bool

    measurement_valid: bool

    solver_converged: bool

    validation_passed: bool