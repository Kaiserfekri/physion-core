import math

from physion_core.config import CellConfig
from physion_core.cycle_engine import run_simulation


def test_config_basic():
    cfg = CellConfig()
    assert cfg.cell_type == "Li-Metal"
    assert cfg.model_type == "SPM"
    assert cfg.cs_max > 0
    assert cfg.I_1C > 0


def test_one_short_simulation_runs():
    params = {
        "n_cycles": 1,
        "t_half_cycle": 10,
        "dt_min": 1.0,
    }

    result = run_simulation(params)

    # باید حداقل چند نقطه زمانی داشته باشیم
    assert len(result["t"]) > 0
    assert len(result["V"]) == len(result["t"])
    assert len(result["eta_anode"]) == len(result["t"])

    # ولتاژ نباید NaN باشد
    assert not any(math.isnan(v) for v in result["V"])
