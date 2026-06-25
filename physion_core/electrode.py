import numpy as np

class ElectrodeSPM:
    """
    Single Particle Model (SPM) electrode
    Clean version for Physion Web Engine + SOC + j_lim
    """

    def __init__(self, cfg, is_anode=True):
        self.cfg = cfg
        self.is_anode = is_anode

        # Particle radius
        self.R = cfg.R_particle_anode if is_anode else cfg.R_particle_cathode

        # Diffusion coefficient
        self.D0 = cfg.D0_anode if is_anode else cfg.D0_cathode

        # Reaction rate
        self.j0 = cfg.j0_anode if is_anode else cfg.j0_cathode

        # Porosity
        self.eps = cfg.eps_anode if is_anode else cfg.eps_cathode

        # Initial concentration profile
        self.cs = np.ones(20) * (cfg.cs0_cathode if not is_anode else 1000.0)

        # Spatial grid inside particle
        self.N = len(self.cs)
        self.r = np.linspace(0, self.R, self.N)
        self.dr = self.r[1] - self.r[0]

        # ===== NEW: SOC state =====
        self.soc = 1.0 if is_anode else 0.0

    def D_eff(self):
        """Temperature‑corrected diffusion coefficient"""
        return self.cfg.D0_eff(self.D0)

    def j0_eff(self):
        """Temperature‑corrected reaction rate"""
        return self.cfg.j0_eff(self.j0)

    def surface_concentration(self):
        """Return concentration at particle surface"""
        return self.cs[-1]

    # ===== NEW: j_lim =====
    def j_lim(self):
        """
        Limiting current density based on diffusion limit:
        j_lim ≈ D_eff * cs_surface / R
        """
        cs_surf = self.surface_concentration()
        D = self.D_eff()
        return D * cs_surf / (self.R + 1e-12)

    def update_diffusion(self, j, dt):
        """
        Explicit diffusion update inside particle
        """
        D = self.D_eff()
        cs_new = self.cs.copy()

        for i in range(1, self.N - 1):
            cs_new[i] = (
                self.cs[i]
                + D * dt / self.dr**2
                * (self.cs[i+1] - 2*self.cs[i] + self.cs[i-1])
            )

        # Boundary: flux at surface from applied current
        cs_new[-1] -= j * dt / (self.cfg.F * self.eps)

        self.cs = cs_new

        # ===== NEW: SOC update =====
        sign = -1.0 if self.is_anode else 1.0
        soc_change = sign * j * dt * self.cfg.soc_scale
        self.soc += soc_change
        self.soc = max(0.0, min(1.0, self.soc))

    def overpotential(self, j):
        """
        Butler‑Volmer simplified overpotential
        """
        j0 = self.j0_eff()
        if abs(j) < 1e-12:
            return 0.0
        return (self.cfg.R_gas * self.cfg.T_cell / self.cfg.F) * np.arcsinh(j / (2*j0))

    def get_state(self):
        return {
            "r": self.r.tolist(),
            "cs": self.cs.tolist(),
            "surface_cs": float(self.surface_concentration()),
            "soc": float(self.soc),
            "j_lim": float(self.j_lim()),
        }
