class PhysicsState:
    """
    State container for Physion V30 – Hybrid
    """

    def __init__(self):
        # زمان
        self.time_s = 0.0

        # دما
        self.temperature_K = 298.15

        # جریان
        self.current_density_A_m2 = 0.0

        # SOC کلی (مینیمال + SPM)
        self.soc_anode = 1.0
        self.soc_cathode = 0.0

        # ولتاژ
        self.cell_voltage_V = 3.7
        self.equilibrium_voltage_V = 3.7
        self.overpotential_cell_V = 0.0

        # اورپتانسیل‌های جداگانه (برای سازگاری با نسخه قبلی)
        self.overpotential_anode_V = 0.0
        self.overpotential_cathode_V = 0.0

        # خروجی‌های واکنش
        self.reaction_rate_A_m2 = 0.0

        # گرما
        self.heat_source_W_m3 = 0.0

        # تنش
        self.stress_Pa = 0.0

        # تخریب / SEI
        self.sei_avg = 0.0
