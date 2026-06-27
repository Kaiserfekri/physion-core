from .parameter_set import ParameterSet
from .registry import FUNCTION_REGISTRY

REQUIRED_KEYS = {
    "U_anode",
    "U_cathode",
    "dU_anode_dT",
    "dU_cathode_dT",
    "capacity_anode",
    "capacity_cathode",
    "D_anode",
    "D_cathode",
    "kinetics_anode",
    "kinetics_cathode",
    "electrolyte",
    "mechanical",
    "degradation",
}

def _get_func(name: str):
    try:
        return FUNCTION_REGISTRY[name]
    except KeyError:
        raise ValueError(f"Unknown function name in JSON: {name}")

def _map_params(raw: dict) -> ParameterSet:
    missing = REQUIRED_KEYS - set(raw.keys())
    if missing:
        raise ValueError(f"Missing keys in JSON: {missing}")

    return ParameterSet({
        "U_anode": _get_func(raw["U_anode"]),
        "U_cathode": _get_func(raw["U_cathode"]),
        "dU_anode_dT": _get_func(raw["dU_anode_dT"]),
        "dU_cathode_dT": _get_func(raw["dU_cathode_dT"]),
        "capacity_anode": raw["capacity_anode"],
        "capacity_cathode": raw["capacity_cathode"],
        "D_anode": _get_func(raw["D_anode"]),
        "D_cathode": _get_func(raw["D_cathode"]),
        "kinetics_anode": raw["kinetics_anode"],
        "kinetics_cathode": raw["kinetics_cathode"],
        "electrolyte": raw["electrolyte"],
        "mechanical": raw["mechanical"],
        "degradation": raw["degradation"],
    })

def load_params(path: str) -> ParameterSet:
    raw_ps = ParameterSet.from_json(path)
    return _map_params(raw_ps.data)
