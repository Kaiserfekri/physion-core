import numpy as np
from physion_core.fullcell.physics_state import PhysicsState


class MechanicalModel:
    """
    Linear elastic + chemo-thermal expansion model.
    نسخهٔ ترکیبی:
    - پارامترها از cfg.mechanical یا chemistry
    - سازگار با اسکلت قبلی compute_stress(state)
    """

    def __init__(self, cfg_or_chemistry):
        self.src = cfg_or_chemistry

        self.E_modulus = getattr(self.src, "E_modulus", 0.0)
        self.alpha_vol = getattr(self.src, "alpha_vol", 0.0)
        self.beta_soc = getattr(self.src, "beta_soc", 0.0)
        self.swelling_coeff = getattr(self.src, "swelling_coeff", 0.0)

    def stress(self, soc, T_K):
        delta_T = T_K - 298.15
        return self.E_modulus * (self.alpha_vol * delta_T + self.beta_soc * soc)

    def swelling(self, soc):
        return self.swelling_coeff * soc

    # نسخهٔ قبلی:
    def compute_stress(self, state: PhysicsState):
        return self.stress(state.soc_anode, state.temperature_K)
