import logging
from .fullcell import FullCellModel
from .config import CellConfig

# ===== اضافه‌شده برای مرحله ۲ (Logging) =====
logger = logging.getLogger("cycle_engine")


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
        logger.info("CycleEngine: Simulation run started.")
        result = self.model.run()
        logger.info("CycleEngine: Simulation run finished.")
        return result


def run_simulation(params: dict):
    """
    External API function used by FastAPI
    """
    logger.info("run_simulation called with params: %s", params)

    cfg = CellConfig()

    # Override parameters from API input
    for k, v in params.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)
            logger.debug("Config override: %s = %s", k, v)

    engine = CycleEngine(cfg)
    result = engine.run()

    logger.info("run_simulation completed. Steps: %d", len(result["t"]))
    return result
