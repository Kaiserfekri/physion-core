# physion_core/mechanics.py
import numpy as np


class MechanicalModel:
    """
    Linear elastic + chemo-thermal expansion model.

    sigma = E * (alpha_vol * ΔT + beta_soc * SOC)
    swelling = swelling_coeff * SOC
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.E_modulus = getattr(cfg, "E_modulus", 0.0)      # Pa
        self.alpha_vol = getattr(cfg, "alpha_vol", 0.0)      # 1/K
        self.beta_soc = getattr(cfg, "beta_soc", 0.0)        # 1
        self.swelling_coeff = getattr(cfg, "swelling_coeff", 0.0)

    def stress(self, soc, T_K):
        delta_T = T_K - 298.15
        return self.E_modulus * (self.alpha_vol * delta_T + self.beta_soc * soc)

    def swelling(self, soc):
        return self.swelling_coeff * soc
