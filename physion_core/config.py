import json
import hashlib
import numpy as np

class CellConfig:
    def __init__(self):
        self.cell_type   = "Li-Metal"
        self.model_type  = "SPM"

        # Geometry
        self.L_anode     = 50.0e-6
        self.L_sep       = 25.0e-6
        self.L_cathode   = 80.0e-6
        self.A_electrode = 1.0e-4
        self.mass_cell   = 5.0e-3

        # TZIM
        self.N_tzim  = 200
        self.L_tzim  = 8.0e-6
        self.z_b1    = 2.5e-6
        self.z_b2    = 5.0e-6
        self.E1      = 0.75e9
        self.E2      = 1.25e9
        self.E3      = 2.00e9

        # Electrolyte
        self.C_e0    = 1000.0
        self.D_e     = 2.0e-10
        self.kappa_e = 0.5
        self.t_plus  = 0.363

        # Anode
        self.D0_anode  = 1.20e-10
        self.j0_anode  = 2.5e-2
        self.alpha_a   = 0.5
        self.R_particle_anode   = 5.0e-6
        self.eps_anode = 0.3
        # قبلاً U_anode ثابت بود، الان به‌عنوان مقدار مرجع نگه می‌داریم
        self.U_anode_ref   = 0.01

        # Cathode
        self.D0_cathode  = 1.0e-14
        self.j0_cathode  = 1.5e-2
        self.alpha_c_cat = 0.5
        self.R_particle_cathode = 3.0e-6
        self.eps_cathode = 0.3
        self.cs_max      = 51410.0
        self.cs0_cathode = 25000.0

        # SEI
        self.rho_sei   = 1700.0
        self.M_sei     = 0.07399
        self.x_Li_sei  = 2.0
        self.V_sei_mol = 2.5e-5
        self.Omega_Li  = 1.3e-5
        self.kappa_sei = 1.0e-4

        # Thermal
        self.T_ref     = 298.15
        self.T_cell    = 298.15
        self.T_amb     = 298.15
        self.Ea_j0     = 30000.0
        self.Ea_D0     = 20000.0
        self.Cp_cell   = 800.0
        self.h_conv    = 10.0
        self.dH_SEI    = -250000.0

        # Constants
        self.R_gas = 8.314
        self.F     = 96485.0

        # Sand
        self.sand_safety = 1.0

        # Protocol
        self.protocol     = "CC-CV"
        self.V_charge     = 4.2
        self.V_discharge  = 2.8
        self.I_1C         = 1.0e-3
        self.C_rate       = 1.0
        self.V_cv_cutoff  = 4.19
        self.I_cv_cutoff  = 1.0e-4
        self.n_cycles     = 100
        self.t_half_cycle = 3600.0
        self.Q_initial    = 3.0
        self.capacity_cutoff = 0.80

        # Solver
        self.bdf2_lte_tol = 1.0e-4
        self.dt_min       = 0.1
        self.dt_max       = 300.0
        self.newton_tol   = 1e-8
        self.max_newton   = 12
        self.snapshot_every = 1
        self.live_plot_every = 1

        # ===== اضافه‌شده برای SOC و OCV =====

        # مقیاس ساده برای آپدیت SOC (بعداً می‌توانیم فیزیکی‌ترش کنیم)
        self.soc_scale = 1e-5

        # پارامترهای OCV ساده (می‌توانی بعداً با جدول واقعی جایگزین کنی)
        self.U_anode_min = 0.0      # ولتاژ تعادلی آند در SOC=1
        self.U_anode_max = 0.20     # در SOC=0 (مثال)

        self.U_cathode_min = 3.80   # در SOC=0
        self.U_cathode_max = 4.30   # در SOC=1

        # ===== اضافه‌شده برای ریسک دندریت =====
        self.eta_crit = 0.05  # V - آستانهٔ نمونه برای شروع ناپایداری دندریت

    # ===== توابع موجود قبلی =====

    def j0_eff(self, j0r):
        return j0r*np.exp(-self.Ea_j0/self.R_gas*(1/self.T_cell-1/self.T_ref))

    # ===== توابع جدید برای MIT‑Real پایه =====

    # جریان اعمالی (فعلاً ثابت؛ بعداً می‌توانی پروتکل واقعی بزاری)
    def I_app(self):
        # می‌توانی این را به C-rate و ظرفیت وصل کنی
        return self.I_1C * self.C_rate

    # OCV آند به‌عنوان تابعی از SOC
    def U_anode(self, soc_a: float) -> float:
        soc_a = max(0.0, min(1.0, soc_a))
        return self.U_anode_min + (1.0 - soc_a) * (self.U_anode_max - self.U_anode_min)

    # OCV کاتد به‌عنوان تابعی از SOC
    def U_cathode(self, soc_c: float) -> float:
        soc_c = max(0.0, min(1.0, soc_c))
        return self.U_cathode_min + soc_c * (self.U_cathode_max - self.U_cathode_min)
