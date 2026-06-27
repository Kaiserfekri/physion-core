import numpy as np


class ElectrodeSPM:
    """
    Single Particle Model (SPM)
    Diffusion + SOC + j_lim
    """

    def __init__(self, cfg, is_anode=True):
        self.cfg = cfg
        self.is_anode = is_anode

        # شعاع ذره
        self.R = cfg.R_particle_anode if is_anode else cfg.R_particle_cathode

        # ضریب نفوذ
        self.D0 = cfg.D0_anode if is_anode else cfg.D0_cathode

        # نرخ واکنش پایه
        self.j0_base = cfg.j0_anode if is_anode else cfg.j0_cathode

        # تخلخل
        self.eps = cfg.eps_anode if is_anode else cfg.eps_cathode

        # پروفایل اولیه غلظت
        self.cs = np.ones(20) * (cfg.cs0_cathode if not is_anode else 1000.0)

        # شبکه شعاعی
        self.N = len(self.cs)
        self.r = np.linspace(0, self.R, self.N)
        self.dr = self.r[1] - self.r[0]

        # SOC داخلی
        self.soc = 1.0 if is_anode else 0.0

    def D_eff(self):
        if hasattr(self.cfg, "D0_eff"):
            return self.cfg.D0_eff(self.D0)
        return self.D0

    def surface_concentration(self):
        return self.cs[-1]

    def j_lim(self):
        cs_surf = self.surface_concentration()
        D = self.D_eff()
        return D * cs_surf / (self.R + 1e-12)

    def update_diffusion(self, j, dt):
        D = self.D_eff()
        cs_new = self.cs.copy()

        for i in range(1, self.N - 1):
            cs_new[i] = (
                self.cs[i]
                + D * dt / self.dr**2
                * (self.cs[i+1] - 2 * self.cs[i] + self.cs[i-1])
            )

        cs_new[-1] -= j * dt / (self.cfg.F * self.eps)
        self.cs = cs_new

        sign = -1.0 if self.is_anode else 1.0
        soc_change = sign * j * dt * getattr(self.cfg, "soc_scale", 1e-5)
        self.soc += soc_change
        self.soc = max(0.0, min(1.0, self.soc))

    def get_state(self):
        return {
            "r": self.r.tolist(),
            "cs": self.cs.tolist(),
            "surface_cs": float(self.surface_concentration()),
            "soc": float(self.soc),
            "j_lim": float(self.j_lim()),
        }
