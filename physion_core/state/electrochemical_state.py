"""
electrochemical_state.py
========================

Industrial Electrochemical State for Physion Framework.

Purpose
-------
Owns every electrochemical interface variable used
throughout the Physion Framework.

Architecture
------------
• Owns electrochemical interface variables only.
• Contains NO battery physics.
• Contains NO numerical methods.
• Contains NO solver logic.
• Updated exclusively by ElectrochemicalSolver.

Categories
----------
• Interface Potential
• Overpotential
• Interfacial Current
• Charge Transfer
• Reaction Interface
• Electrochemical Indicators
• Diagnostics

Notes
-----
This class is intentionally passive.

It stores simulation state only.

All calculations are delegated to
ElectrochemicalSolver.

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
class ElectrochemicalState(BaseState):
    """
    Industrial Electrochemical State.

    Stores interface electrochemical quantities.

    No computation is performed here.
    """

    # =====================================================
    # Interface Potential
    # =====================================================

    equilibrium_potential: float = 0.0

    interface_potential: float = 0.0

    electrode_electrolyte_potential_difference: float = 0.0

    open_circuit_interface_potential: float = 0.0

    # =====================================================
    # Overpotential
    # =====================================================

    activation_overpotential: float = 0.0

    concentration_overpotential: float = 0.0

    ohmic_overpotential: float = 0.0

    diffusion_overpotential: float = 0.0

    total_overpotential: float = 0.0

    # =====================================================
    # Interfacial Current
    # =====================================================

    interfacial_current_density: float = 0.0

    faradaic_current_density: float = 0.0

    exchange_current_density: float = 0.0

    effective_current_density: float = 0.0

    # =====================================================
    # Charge Transfer
    # =====================================================

    charge_transfer_rate: float = 0.0

    charge_transfer_coefficient: float = 0.0

    effective_charge_transfer: float = 0.0

    # =====================================================
    # Reaction Interface
    # =====================================================

    interface_reaction_rate: float = 0.0

    reaction_utilization: float = 0.0

    reaction_uniformity: float = 0.0

    interface_activity: float = 0.0

    # =====================================================
    # Electrochemical Indicators
    # =====================================================

    polarization_index: float = 0.0

    electrochemical_efficiency: float = 1.0

    interface_utilization: float = 0.0

    reaction_stability: float = 1.0

    # =====================================================
    # Diagnostics
    # =====================================================

    electrochemical_warning: bool = False

    electrochemical_fault: bool = False

    measurement_valid: bool = True

    solver_converged: bool = True

    validation_passed: bool = True
    
    # =====================================================
    # Validation
    # =====================================================

    def validate_impl(self) -> None:
        """
        Validate electrochemical interface state.

        Responsibilities
        ----------------
        • Verify non-negative current densities.
        • Verify valid efficiency range.
        • Verify valid stability range.
        • Verify transfer coefficient range.
        • Verify diagnostic consistency.

        Notes
        -----
        Validation only.

        No physics.
        No solver.
        No state modification.
        """

        # -------------------------------------------------
        # Non-negative Quantities
        # -------------------------------------------------

        non_negative_values = (
            self.interfacial_current_density,
            self.faradaic_current_density,
            self.exchange_current_density,
            self.effective_current_density,
            self.charge_transfer_rate,
            self.effective_charge_transfer,
            self.interface_reaction_rate,
            self.interface_utilization,
        )

        for value in non_negative_values:

            if value < 0.0:

                raise ValueError(
                    "Electrochemical quantities cannot be negative."
                )

        # -------------------------------------------------
        # Transfer Coefficient
        # -------------------------------------------------

        if not (
            0.0
            <= self.charge_transfer_coefficient
            <= 1.0
        ):

            raise ValueError(
                "Charge transfer coefficient must be between 0 and 1."
            )

        # -------------------------------------------------
        # Efficiencies
        # -------------------------------------------------

        if not (
            0.0
            <= self.electrochemical_efficiency
            <= 1.0
        ):

            raise ValueError(
                "Electrochemical efficiency must be between 0 and 1."
            )

        # -------------------------------------------------
        # Stability
        # -------------------------------------------------

        if not (
            0.0
            <= self.reaction_stability
            <= 1.0
        ):

            raise ValueError(
                "Reaction stability must be between 0 and 1."
            )

        # -------------------------------------------------
        # Utilization
        # -------------------------------------------------

        if not (
            0.0
            <= self.interface_utilization
            <= 1.0
        ):

            raise ValueError(
                "Interface utilization must be between 0 and 1."
            )

        # -------------------------------------------------
        # Reaction Uniformity
        # -------------------------------------------------

        if not (
            0.0
            <= self.reaction_uniformity
            <= 1.0
        ):

            raise ValueError(
                "Reaction uniformity must be between 0 and 1."
            )

        # -------------------------------------------------
        # Activity
        # -------------------------------------------------

        if self.interface_activity < 0.0:

            raise ValueError(
                "Interface activity cannot be negative."
            )