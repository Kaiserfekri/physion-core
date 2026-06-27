class PhysicsState:
    """
    وضعیت فیزیکی لحظه‌ای سلول.
    نام متغیرها واحد را در خود دارند تا باگ واحدی کمتر شود.
    """

    def __init__(self):
        self.time_s = 0.0
        self.current_density_A_m2 = 0.0
        self.temperature_K = 298.15

        # حالت الکترودها
        self.soc_anode = 0.5
        self.soc_cathode = 0.5

        # الکترولیت
        self.electrolyte_conc_mol_m3 = 1000.0

        # اورپتانسیل‌ها
        self.overpotential_anode_V = 0.0
        self.overpotential_cathode_V = 0.0

        # خروجی‌های مدل
        self.heat_source_W_m3 = 0.0
        self.stress_Pa = 0.0
        self.reaction_rate_A_m2 = 0.0

        # تخریب
        self.degradation_state = {}