from .physics_state import PhysicsState

class ReactionModel:
    def __init__(self, chemistry):
        self.chemistry = chemistry

    def compute_flux(self, state: PhysicsState):
        return state.current_density_A_m2

    def compute_heat(self, state: PhysicsState):
        return state.current_density_A_m2 * (
            state.overpotential_anode_V + state.overpotential_cathode_V
        )

class MechanicalModel:
    def __init__(self, chemistry):
        self.chemistry = chemistry

    def compute_stress(self, state: PhysicsState):
        return 0.0

class DegradationModel:
    def __init__(self, chemistry):
        self.chemistry = chemistry

    def update(self, state: PhysicsState, dt: float):
        pass

class FullCellModel:
    def __init__(self, cfg):
        self.cfg = cfg
        self.chemistry = cfg.chemistry
        self.state = PhysicsState()

        self.reaction = ReactionModel(self.chemistry)
        self.mechanics = MechanicalModel(self.chemistry)
        self.degradation = DegradationModel(self.chemistry)

    def step(self, dt: float, current_density_A_m2: float):
        self.state.time_s += dt
        self.state.current_density_A_m2 = current_density_A_m2

        j = self.reaction.compute_flux(self.state)
        self.state.reaction_rate_A_m2 = j

        q_dot = self.reaction.compute_heat(self.state)
        self.state.heat_source_W_m3 = q_dot

        self.state.stress_Pa = self.mechanics.compute_stress(self.state)
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
