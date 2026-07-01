"""
mechanical_update.py
====================

Industrial Mechanical Update Object
for Physion Framework.

Purpose
-------
Carries the final mechanical solution produced by
MechanicalSolver.

Architecture
------------
MechanicalSolver
        ↓
MechanicalUpdate
        ↓
CommitManager
        ↓
MechanicalState

Mirror
------
This object is an exact mirror of MechanicalState.

Contains
--------
• NO mechanics equations
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
class MechanicalUpdate(BaseUpdate):

    # =====================================================
    # Stress
    # =====================================================

    stress: float
    axial_stress: float
    radial_stress: float
    tangential_stress: float
    hydrostatic_stress: float
    von_mises_stress: float
    maximum_principal_stress: float
    minimum_principal_stress: float
    equivalent_stress: float

    # =====================================================
    # Strain
    # =====================================================

    strain: float
    axial_strain: float
    radial_strain: float
    tangential_strain: float
    plastic_strain: float
    elastic_strain: float
    equivalent_strain: float
    volumetric_strain: float

    # =====================================================
    # Deformation
    # =====================================================

    displacement: float
    axial_displacement: float
    radial_displacement: float
    thickness_change: float
    volume_change: float
    deformation_rate: float

    # =====================================================
    # Pressure
    # =====================================================

    pressure: float
    contact_pressure: float
    internal_pressure: float
    external_pressure: float
    pore_pressure: float
    pressure_gradient: float

    # =====================================================
    # Crack
    # =====================================================

    crack_length: float
    crack_width: float
    crack_depth: float
    crack_density: float
    crack_growth_rate: float
    fracture_index: float

    fracture_detected: bool

    # =====================================================
    # Mechanical Diagnostics
    # =====================================================

    mechanical_warning: bool
    mechanical_fault: bool
    excessive_deformation: bool
    excessive_stress: bool
    excessive_strain: bool
    fracture_risk: bool
    measurement_valid: bool
    solver_converged: bool
    validation_passed: bool