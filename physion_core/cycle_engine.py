from .fullcell import FullCellModel
from .config import CellConfig


class CycleEngine:
    """
    High‑level simulation engine for Physion Web Engine
    """

    def __init__(self, cfg: CellConfig):
        self.cfg = cfg
        self.model = FullCellModel(cfg)

    def run(self):
        """
        Run the full simulation and return results
        """
        return self.model.run()


def run_simulation(params: dict):
    """
    External API function used by FastAPI
    """
    cfg = CellConfig()

    # Override parameters from API input
    for k, v in params.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)

    engine = CycleEngine(cfg)
    result = engine.run()
    return result
