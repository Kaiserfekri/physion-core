# physion_core/chemistry/base.py

class BaseChemistry:
    """
    Base class for cell chemistry definitions.

    All methods here are interfaces; concrete chemistries must implement them
    using documented data (OCV curves, dUeq/dT, transport, kinetics, etc.).
    """

    def U_anode(self, soc, T_K):
        """Equilibrium potential of anode [V] as function of SOC and T."""
        raise NotImplementedError

    def U_cathode(self, soc, T_K):
        """Equilibrium potential of cathode [V] as function of SOC and T."""
        raise NotImplementedError

    def dUeq_dT(self, soc_anode, soc_cathode):
        """
        Temperature derivative of cell equilibrium voltage [V/K].

        U_eq = U_cathode - U_anode
        dUeq/dT = dU_cathode/dT - dU_anode/dT
        """
        raise NotImplementedError

    def capacity_anode(self):
        """Theoretical capacity of anode [mAh/g or Ah]."""
        raise NotImplementedError

    def capacity_cathode(self):
        """Theoretical capacity of cathode [mAh/g or Ah]."""
        raise NotImplementedError

    def diffusion_coeff_anode(self, soc, T_K):
        """Solid diffusion coefficient in anode [m^2/s]."""
        raise NotImplementedError

    def diffusion_coeff_cathode(self, soc, T_K):
        """Solid diffusion coefficient in cathode [m^2/s]."""
        raise NotImplementedError

    def kinetics_params_anode(self):
        """Kinetic parameters (exchange current, alpha, etc.) for anode."""
        raise NotImplementedError

    def kinetics_params_cathode(self):
        """Kinetic parameters (exchange current, alpha, etc.) for cathode."""
        raise NotImplementedError

    def electrolyte_params(self):
        """Electrolyte transport and thermodynamic parameters."""
        raise NotImplementedError

    def mechanical_params(self):
        """Mechanical parameters (E, alpha_vol, beta_soc, swelling_coeff)."""
        raise NotImplementedError

    def degradation_params(self):
        """Degradation parameters (k_LLI, k_LAM, SEI growth, etc.)."""
        raise NotImplementedError
