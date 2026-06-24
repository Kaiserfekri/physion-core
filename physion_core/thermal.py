import numpy as np

class ThermalModel:
    """
    Simple thermal model for Physion Web Engine
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.T = cfg.T_cell

    def heat_generation(self, j, eta, sei_rate):
        """
        Total heat = Joule + Reaction + SEI formation
        """
        Q_joule = abs(j) * eta * self.cfg.F
        Q_reaction = j * self.cfg.dH_SEI
        Q_sei = sei_rate * self.cfg.dH_SEI
        return Q_joule + Q_reaction + Q_sei

    def update(self, j, eta, sei_rate, dt):
        """
        dT/dt = (Q_gen - hA(T - Tamb)) / (m Cp)
        """
        Q_gen = self.heat_generation(j, eta, sei_rate)
        Q_loss = self.cfg.h_conv * (self.T - self.cfg.T_amb)

        dTdt = (Q_gen - Q_loss) / (self.cfg.mass_cell * self.cfg.Cp_cell)
        self.T += dTdt * dt

    def get_state(self):
        return {
            "T": float(self.T)
        }
