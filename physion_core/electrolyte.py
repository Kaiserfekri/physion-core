import numpy as np

class Electrolyte1DModel:
    """
    1D electrolyte model for Physion Web Engine
    ساده‌شده از TZIM/V20:
      - C_e(z) diffusion + migration
      - phi(z) potential
      - j_BV(z) local current density
      - E(z) = -dphi/dz
      - DGI و CCD قابل محاسبه
    """

    def __init__(self, cfg):
        self.cfg = cfg

        # Grid
        self.N = cfg.N_tzim
        self.L = cfg.L_tzim
        self.z = np.linspace(0, self.L, self.N)
        self.dz = self.z[1] - self.z[0]

        # State
        self.C = np.ones(self.N) * cfg.C_e0      # electrolyte concentration
        self.phi = np.zeros(self.N)             # potential
        self.j_BV = np.zeros(self.N)            # local BV current density
        self.E = np.zeros(self.N)               # electric field

        # Time tracking برای Sand و DGI
        self.t_elapsed = 0.0

    def _update_electric_field(self):
        """
        E(z) = -dphi/dz (central differences)
        """
        phi = self.phi
        E = np.zeros_like(phi)
        E[1:-1] = -(phi[2:] - phi[:-2]) / (2 * self.dz)
        E[0] = -(phi[1] - phi[0]) / self.dz
        E[-1] = -(phi[-1] - phi[-2]) / self.dz
        self.E = E

    def step(self, j_app: float, dt: float, V_app: float):
        """
        یک گام ساده:
          - diffusion روی C
          - حل خیلی ساده روی phi (gradient خطی)
          - محاسبه j_BV(z) با BV محلی
        این نسخه سبک است و فقط برای نزدیک شدن به V20 طراحی شده،
        نه برای حل کامل PDE مثل TZIMSolver.
        """
        self.t_elapsed += dt

        cfg = self.cfg
        D_e = cfg.D_e
        C = self.C.copy()

        # Diffusion ساده روی C_e(z)
        C_new = C.copy()
        for i in range(1, self.N - 1):
            C_new[i] = (
                C[i]
                + D_e * dt / self.dz**2
                * (C[i+1] - 2*C[i] + C[i-1])
            )

        # مرزها را نزدیک مقدار اولیه نگه می‌داریم
        C_new[0] = cfg.C_e0
        C_new[-1] = cfg.C_e0 * 0.8

        self.C = C_new

        # پتانسیل را به‌صورت خطی بین 0 و V_app فرض می‌کنیم
        self.phi = np.linspace(0.0, V_app, self.N)

        # میدان الکتریکی
        self._update_electric_field()

        # BV محلی
        frt = cfg.F / (cfg.R_gas * cfg.T_cell)
        j0_eff = cfg.j0_eff(cfg.j0_anode)

        eta = V_app - self.phi - cfg.U_anode
        self.j_BV = j0_eff * (
            np.exp(0.5 * frt * eta) - np.exp(-cfg.alpha_a * frt * eta)
        )

    def hotspot(self):
        """
        بیشینهٔ داخلی |j_BV|
        """
        j_abs = np.abs(self.j_BV[1:-1])
        if len(j_abs) == 0:
            return 0.0, 0.0
        idx = int(np.argmax(j_abs)) + 1
        return float(self.z[idx] * 1e6), float(self.j_BV[idx])

    def DGI_profile(self):
        """
        DGI(z) = |j_BV(z)| / j_Sand(t)
        """
        j_crit = self.cfg.j_sand(self.t_elapsed)
        return np.abs(self.j_BV) / (j_crit + 1e-12)

    def CCD(self):
        """
        Critical current density via Sand's equation
        """
        return self.cfg.j_sand(self.t_elapsed)

    def get_state(self):
        return {
            "z": self.z.tolist(),
            "C_e": self.C.tolist(),
            "phi": self.phi.tolist(),
            "j_BV": self.j_BV.tolist(),
            "E": self.E.tolist(),
        }
