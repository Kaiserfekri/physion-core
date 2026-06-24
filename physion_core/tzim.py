import numpy as np

class TZIMModel:
    """
    Transient Zone Interphase Mechanics (TZIM)
    Clean version for Physion Web Engine
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.N = cfg.N_tzim
        self.L = cfg.L_tzim

        # Spatial grid
        self.z = np.linspace(0, self.L, self.N)
        self.dz = self.z[1] - self.z[0]

        # Mechanical modulus profile
        self.E = self._build_modulus_profile()

        # Initial SEI thickness distribution
        self.sei = np.zeros(self.N)

    def _build_modulus_profile(self):
        """
        Three‑zone modulus profile:
        E1 → E2 → E3
        """
        E = np.zeros(self.N)

        z1 = self.cfg.z_b1
        z2 = self.cfg.z_b2

        for i, zi in enumerate(self.z):
            if zi < z1:
                E[i] = self.cfg.E1
            elif zi < z2:
                E[i] = self.cfg.E2
            else:
                E[i] = self.cfg.E3

        return E

    def update_sei(self, j, dt):
        """
        Simple SEI growth model:
        d(sei)/dt = kappa_sei * |j|
        """
        growth = self.cfg.kappa_sei * abs(j) * dt
        self.sei += growth

    def stress(self):
        """
        Compute stress = E * strain
        Here strain is approximated from SEI gradient
        """
        grad = np.gradient(self.sei, self.dz)
        return self.E * grad

    def get_state(self):
        return {
            "z": self.z.tolist(),
            "sei": self.sei.tolist(),
            "E": self.E.tolist(),
        }
