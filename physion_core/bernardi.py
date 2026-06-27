# physion_core/bernardi.py
import numpy as np


class BernardiHeatModel:
    """
    Heat generation model (Bernardi-style):

    Q_dot = I * (V - U_eq) - T * (dU_eq/dT) * I
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.A_cell = getattr(cfg, "A_cell", 1.0)  # m^2

    def heat_generation(self, j, V, V_eq, T_K, soc_anode, soc_cathode):
        """
        Compute total heat generation [W].

        j: current density [A/m^2]
        V: cell voltage [V]
        V_eq: equilibrium voltage [V]
        T_K: temperature [K]
        soc_anode, soc_cathode: SOCs for dUeq/dT
        """
        I = j * self.A_cell

        dUeq_dT_fun = getattr(self.cfg, "dUeq_dT", None)
        if callable(dUeq_dT_fun):
            dUeq_dT = float(dUeq_dT_fun(soc_anode, soc_cathode))
        else:
            dUeq_dT = 0.0

        Q_irrev = I * (V - V_eq)
        Q_rev = -T_K * dUeq_dT * I
        return Q_irrev + Q_rev
