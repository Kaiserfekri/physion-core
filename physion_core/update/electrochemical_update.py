"""
electrochemical_update.py
=========================

Industrial Electrochemical Update Object
for Physion Framework.

Purpose
-------
Carries immutable electrochemical interface updates
from ElectrochemicalSolver to CommitManager.

Architecture
------------
ElectrochemicalSolver
          │
          ▼
ElectrochemicalUpdate
          │
          ▼
CommitManager
          │
          ▼
ElectrochemicalState

Notes
-----
This object is immutable.

It contains NO solver logic.

It contains NO electrochemical equations.

It contains NO validation logic other than
BaseUpdate generic validation.

Mirror Rule
-----------
Every public data field of ElectrochemicalState
is mirrored here one-to-one.
"""

from __future__ import annotations

from dataclasses import dataclass

from physion_core.update.base_update import BaseUpdate


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ElectrochemicalUpdate(BaseUpdate):
    """
    Immutable snapshot of ElectrochemicalState.
    """

    # =====================================================
    # Interface Potential
    # =====================================================

    equilibrium_potential: float

    interface_potential: float

    electrode_electrolyte_potential_difference: float

    open_circuit_interface_potential: float

    # =====================================================
    # Overpotential
    # =====================================================

    activation_overpotential: float

    concentration_overpotential: float

    ohmic_overpotential: float

    diffusion_overpotential: float

    total_overpotential: float

    # =====================================================
    # Interfacial Current
    # =====================================================

    interfacial_current_density: float

    faradaic_current_density: float

    exchange_current_density: float

    effective_current_density: float

    # =====================================================
    # Charge Transfer
    # =====================================================

    charge_transfer_rate: float

    charge_transfer_coefficient: float

    effective_charge_transfer: float

    # =====================================================
    # Reaction Interface
    # =====================================================

    interface_reaction_rate: float

    reaction_utilization: float

    reaction_uniformity: float

    interface_activity: float

    # =====================================================
    # Electrochemical Indicators
    # =====================================================

    polarization_index: float

    electrochemical_efficiency: float

    interface_utilization: float

    reaction_stability: float

    # =====================================================
    # Diagnostics
    # =====================================================

    electrochemical_warning: bool

    electrochemical_fault: bool

    measurement_valid: bool

    solver_converged: bool

    validation_passed: bool