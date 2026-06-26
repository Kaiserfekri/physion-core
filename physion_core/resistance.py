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

    def electrolyte_resistance(self, C_e_surface: float | None = None):
        """
        R_e = L_sep / (kappa_e_eff * A)
        kappa_e_eff ∝ C_e_surface / C_e0
        اگر C_e_surface داده نشود، همان kappa_e ثابت استفاده می‌شود.
        """
        kappa = self.cfg.kappa_e
        if C_e_surface is not None and hasattr(self.cfg, "C_e0"):
            kappa = kappa * max(C_e_surface, 1e-12) / max(self.cfg.C_e0, 1e-12)
        return self.cfg.L_sep / (kappa * self.cfg.A_electrode)

    def ohmic_resistance(self):
        """
        Simple constant ohmic resistance
        """
        return 0.01  # 10 mΩ

    def total(self, C_e_surface: float | None = None):
        """
        Total internal resistance
        با در نظر گرفتن وابستگی R_electrolyte به C_e_surface.
        """
        R_e = self.electrolyte_resistance(C_e_surface)
        return self.ohmic_resistance() + self.R_sei + R_e

    def get_state(self, C_e_surface: float | None = None):
        return {
            "R_sei": float(self.R_sei),
            "R_electrolyte": float(self.electrolyte_resistance(C_e_surface)),
            "R_total": float(self.total(C_e_surface))
        }
