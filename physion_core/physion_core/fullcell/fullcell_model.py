from physion_core.fullcell.physics_state import PhysicsState


class ReactionModel:
    def __init__(self, chemistry):
        self.chemistry = chemistry

    def compute_flux(self, state: PhysicsState):
        # فعلاً جریان را همان ورودی می‌گیریم
        return state.current_density_A_m2

    def compute_heat(self, state: PhysicsState):
        # اینجا فقط از اورپتانسیل‌های ذخیره‌شده در state استفاده می‌کنیم
        # بدون دوباره شمردن اختلاف OCV بین آند و کاتد
        eta_an = state.overpotential_anode_V
        eta_ca = state.overpotential_cathode_V

        # مدل ساده برناردی: q = J * (η_an + η_ca)
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

    def _update_soc(self, dt: float):
        """
        به‌روزرسانی سادهٔ SOC بر اساس جریان.
        این یک مدل مینیمال است و واحدها را ایده‌آل فرض می‌کند.
        """
        J = self.state.current_density_A_m2  # A/m^2

        # ظرفیت‌ها (فرضی، بر حسب Ah/kg یا مشابه) از شیمی
        cap_an = self.chemistry.capacity_anode()
        cap_ca = self.chemistry.capacity_cathode()

        if cap_an > 0:
            # آند: شارژ شدن با جریان منفی، دشارژ با جریان مثبت (علامت ساده)
            d_soc_an = - J * dt / (3600.0 * cap_an)
            self.state.soc_anode += d_soc_an

        if cap_ca > 0:
            # کاتد: برعکس آند
            d_soc_ca = J * dt / (3600.0 * cap_ca)
            self.state.soc_cathode += d_soc_ca

        # می‌توانی بعداً clamp هم اضافه کنی، فعلاً فقط دینامیک را اضافه کردیم

    def step(self, dt: float, current_density_A_m2: float):
        # زمان
        self.state.time_s += dt

        # جریان
        self.state.current_density_A_m2 = current_density_A_m2

        # به‌روزرسانی SOC (دینامیک ساده)
        self._update_soc(dt)

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

