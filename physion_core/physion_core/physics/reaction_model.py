import numpy as np
from physion_core.fullcell.physics_state import PhysicsState


class ReactionModel:
    """
    Hybrid Reaction Model:
    - استفاده از OCV واقعی (U_anode, U_cathode)
    - Butler–Volmer برای j_BV
    - حفظ مدل ساده برناردی قبلی (J * (η_an + η_ca)) برای سازگاری
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.chemistry = getattr(cfg, "chemistry", None)

    # -----------------------------
    # OCV + overpotential سلولی
    # -----------------------------
    def compute_overpotential_cell(self, state: PhysicsState):
        """
        η_cell = V_cell - V_eq
        V_eq = U_cathode(SOC_c) - U_anode(SOC_a)
        """
        if self.chemistry is not None:
            U_an = self.chemistry.U_anode(state.soc_anode)
            U_ca = self.chemistry.U_cathode(state.soc_cathode)
        else:
            U_an = self.cfg.U_anode(state.soc_anode)
            U_ca = self.cfg.U_cathode(state.soc_cathode)

        V_eq = U_ca - U_an
        eta_cell = state.cell_voltage_V - V_eq

        state.equilibrium_voltage_V = V_eq
        state.overpotential_cell_V = eta_cell

        # برای سازگاری با نسخه قبلی:
        state.overpotential_anode_V = -0.5 * eta_cell
        state.overpotential_cathode_V = 0.5 * eta_cell

        return eta_cell, V_eq

    # -----------------------------
    # Butler–Volmer خام
    # -----------------------------
    def butler_volmer_raw(self, j, eta, T_K):
        F = self.cfg.F
        R = self.cfg.R_gas
        alpha = 0.5

        frt = F / (R * T_K)
        return j * (np.exp(alpha * frt * eta) - np.exp(-(1 - alpha) * frt * eta))

    # -----------------------------
    # flux مؤثر (نسخه جدید)
    # -----------------------------
    def compute_flux_bv(self, state: PhysicsState, eta_cell: float):
        j = state.current_density_A_m2
        T_K = state.temperature_K
        j_bv = self.butler_volmer_raw(j, eta_cell, T_K)
        return j_bv

    # -----------------------------
    # flux ساده (نسخه قبلی)
    # -----------------------------
    def compute_flux_simple(self, state: PhysicsState):
        return state.current_density_A_m2

    # -----------------------------
    # گرما – نسخه قبلی (برناردی ساده)
    # -----------------------------
    def compute_heat_simple(self, state: PhysicsState):
        eta_an = state.overpotential_anode_V
        eta_ca = state.overpotential_cathode_V
        return state.current_density_A_m2 * (eta_an + eta_ca)

    # -----------------------------
    # گرما – نسخه جدید (J * (V_cell - V_eq))
    # -----------------------------
    def compute_heat_bernardi(self, state: PhysicsState, V_eq: float):
        j = state.current_density_A_m2
        V_cell = state.cell_voltage_V
        return j * (V_cell - V_eq)
