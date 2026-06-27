from .parameter_set import ParameterSet
from . import functions as f

def _map_params(raw: dict) -> ParameterSet:
    """
    raw: دیکشنری خوانده‌شده از JSON.
    این تابع نام توابع را به خود تابع در functions.py نگاشت می‌کند.
    """
    return ParameterSet({
        "U_anode": getattr(f, raw["U_anode"]),
        "U_cathode": getattr(f, raw["U_cathode"]),
        "dU_anode_dT": getattr(f, raw["dU_anode_dT"]),
        "dU_cathode_dT": getattr(f, raw["dU_cathode_dT"]),
        "capacity_anode": raw["capacity_anode"],
        "capacity_cathode": raw["capacity_cathode"],
        "D_anode": getattr(f, raw["D_anode"]),
        "D_cathode": getattr(f, raw["D_cathode"]),
        "kinetics_anode": raw["kinetics_anode"],
        "kinetics_cathode": raw["kinetics_cathode"],
        "electrolyte": raw["electrolyte"],
        "mechanical": raw["mechanical"],
        "degradation": raw["degradation"],
    })


def load_lfp_graphite_params(path: str) -> ParameterSet:
    raw_ps = ParameterSet.from_json(path)
    return _map_params(raw_ps.data)


def load_nmc_graphite_params(path: str) -> ParameterSet:
    raw_ps = ParameterSet.from_json(path)
    return _map_params(raw_ps.data)


def load_lco_graphite_params(path: str) -> ParameterSet:
    raw_ps = ParameterSet.from_json(path)
    return _map_params(raw_ps.data)


def load_nca_graphite_params(path: str) -> ParameterSet:
    raw_ps = ParameterSet.from_json(path)
    return _map_params(raw_ps.data)
