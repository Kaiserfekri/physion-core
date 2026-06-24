import numpy as np

class ResistanceModel:
    """
    Internal resistance model for Physion Web Engine
    """

    def __init__(self, cfg):
        self.cfg = cfg

        # Initial SEI resistance
        self.R_sei = 0.0

    def update_sei_resistance(self, sei_thickness):
        """
        R_sei = thickness / (kappa_sei)
        """
        if self.cfg.kappa_sei <= 0:
            self.R_sei = 0.0
        else:
            self.R_sei = sei_thickness / self.cfg.kappa_sei

    def electrolyte_resistance(self):
        """
        R_e = L_sep / (kappa_e * A)
        """
        return self.cfg.L_sep / (self.cfg.kappa_e * self.cfg.A_electrode)

    def ohmic_resistance(self):
        """
        Simple constant ohmic resistance
        """
        return 0.01  # 10 mΩ

    def total(self):
        """
        Total internal resistance
        """
        return self.ohmic_resistance() + self.R_sei + self.electrolyte_resistance()

    def get_state(self):
        return {
            "R_sei": float(self.R_sei),
            "R_electrolyte": float(self.electrolyte_resistance()),
            "R_total": float(self.total())
        }
