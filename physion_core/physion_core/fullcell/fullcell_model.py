from physion_core.fullcell.physics_state import PhysicsState


class ReactionModel:
    def __init__(self, chemistry):
        self.chemistry = chemistry

    def compute_flux(self, state: PhysicsState):
        # فعلاً جریان را همان ورودی می‌گیریم
        return state.current_density_A_m2

    def compute_heat(self, state: PhysicsState):
        # استفاده از شیمی برای محاسبه OCV
        U_an = self.chemistry.U_anode(state.soc_anode, state.temperature_K)
        U_ca = self.chemistry.U_cathode(state.soc_cathode, state.temperature_K)

        # اورپتانسیل واقعی
        eta_an = state.overpotential_anode_V + (U_an - U_ca)
        eta_ca = state.overpotential_cathode_V + (U_ca - U_an)

        # مدل ساده برناردی
        return state.current_density_A_m2 * (eta_an + eta_ca)


class MechanicalModel:
    def __init__(self, chemistry):
        self.chemistry = chemistry

    def compute_stress(self, state: PhysicsState):
        # فعلاً اسکلت
        return 0.0


class DegradationModel:
    def __init__(self, chemistry):
        self.chemistry = chemistry

    def update(self, state: PhysicsState, dt: float):
        # فعلاً اسکلت
        pass


class FullCellModel:
    def __init__(self, cfg):
        self.cfg = cfg
        self.chemistry = cfg.chemistry
        self.state = PhysicsState()

        # ماژول‌های فیزیکی
        self.reaction = ReactionModel(self.chemistry)
        self.mechanics = MechanicalModel(self.chemistry)
        self.degradation = DegradationModel(self.chemistry)

    def step(self, dt: float, current_density_A_m2: float):
        # زمان
        self.state.time_s += dt

        # جریان
        self.state.current_density_A_m2 = current_density_A_m2

        # واکنش
        j = self.reaction.compute_flux(self.state)
        self.state.reaction_rate_A_m2 = j

        # گرما
        q_dot = self.reaction.compute_heat(self.state)
        self.state.heat_source_W_m3 = q_dot

        # تنش
        self.state.stress_Pa = self.mechanics.compute_stress(self.state)

        # تخریب
        self.degradation.update(self.state, dt)

    def summary(self):
        return {
            "chemistry": type(self.chemistry).__name__,
            "capacity_anode": self.chemistry.capacity_anode(),
            "capacity_cathode": self.chemistry.capacity_cathode(),
            "time_s": self.state.time_s,
            "current_density_A_m2": self.state.current_density_A_m2,
            "heat_source_W_m3": self.state.heat_source_W_m3,
        }
