import numpy as np
from scipy.interpolate import CubicSpline

_user_ocv_data = {
    "lfp": {"soc": None, "U": None, "spline": None},
    "nmc": {"soc": None, "U": None, "spline": None},
    "lco": {"soc": None, "U": None, "spline": None},
    "nca": {"soc": None, "U": None, "spline": None},
}

def _clamp_soc(soc):
    return float(np.clip(float(soc), 0.0, 1.0))

# -----------------------------
# ست‌کردن دادهٔ کاربر
# -----------------------------

def set_user_ocv_lfp(soc_array, U_array):
    soc = np.array(soc_array, dtype=float)
    U = np.array(U_array, dtype=float)
    _user_ocv_data["lfp"]["soc"] = soc
    _user_ocv_data["lfp"]["U"] = U
    _user_ocv_data["lfp"]["spline"] = CubicSpline(soc, U)

def set_user_ocv_nmc(soc_array, U_array):
    soc = np.array(soc_array, dtype=float)
    U = np.array(U_array, dtype=float)
    _user_ocv_data["nmc"]["soc"] = soc
    _user_ocv_data["nmc"]["U"] = U
    _user_ocv_data["nmc"]["spline"] = CubicSpline(soc, U)

def set_user_ocv_lco(soc_array, U_array):
    soc = np.array(soc_array, dtype=float)
    U = np.array(U_array, dtype=float)
    _user_ocv_data["lco"]["soc"] = soc
    _user_ocv_data["lco"]["U"] = U
    _user_ocv_data["lco"]["spline"] = CubicSpline(soc, U)

def set_user_ocv_nca(soc_array, U_array):
    soc = np.array(soc_array, dtype=float)
    U = np.array(U_array, dtype=float)
    _user_ocv_data["nca"]["soc"] = soc
    _user_ocv_data["nca"]["U"] = U
    _user_ocv_data["nca"]["spline"] = CubicSpline(soc, U)

# -----------------------------
# Graphite (Anode)
# -----------------------------

def U_anode_graphite(soc, T_K):
    soc = _clamp_soc(soc)
    U = 0.1 + 0.9 * soc
    U += 0.0 * (T_K - 298.15)
    return U

def dU_anode_dT_graphite(soc):
    return 0.0

def D_anode_graphite(soc, T_K):
    return 1e-14

# -----------------------------
# LFP – سه سطح
# -----------------------------

def U_cathode_lfp_simple(soc, T_K):
    soc = _clamp_soc(soc)
    U = 3.2 + 0.4 * soc
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_lfp_user(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["lfp"]
    if data["soc"] is None:
        return U_cathode_lfp_simple(soc, T_K)
    U = float(np.interp(soc, data["soc"], data["U"]))
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_lfp_industrial(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["lfp"]
    if data["spline"] is None:
        return U_cathode_lfp_user(soc, T_K)
    U = float(data["spline"](soc))
    U += 0.0 * (T_K - 298.15)
    return U

def dU_cathode_dT_lfp(soc):
    return 0.0

def D_cathode_lfp(soc, T_K):
    return 5e-14

# -----------------------------
# NMC – سه سطح
# -----------------------------

def U_cathode_nmc_simple(soc, T_K):
    soc = _clamp_soc(soc)
    U = 3.6 + 0.5 * soc
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_nmc_user(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["nmc"]
    if data["soc"] is None:
        return U_cathode_nmc_simple(soc, T_K)
    U = float(np.interp(soc, data["soc"], data["U"]))
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_nmc_industrial(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["nmc"]
    if data["spline"] is None:
        return U_cathode_nmc_user(soc, T_K)
    U = float(data["spline"](soc))
    U += 0.0 * (T_K - 298.15)
    return U

def dU_cathode_dT_nmc(soc):
    return 0.0

def D_cathode_nmc(soc, T_K):
    return 5e-14

# -----------------------------
# LCO – سه سطح
# -----------------------------

def U_cathode_lco_simple(soc, T_K):
    soc = _clamp_soc(soc)
    U = 3.7 + 0.4 * soc
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_lco_user(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["lco"]
    if data["soc"] is None:
        return U_cathode_lco_simple(soc, T_K)
    U = float(np.interp(soc, data["soc"], data["U"]))
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_lco_industrial(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["lco"]
    if data["spline"] is None:
        return U_cathode_lco_user(soc, T_K)
    U = float(data["spline"](soc))
    U += 0.0 * (T_K - 298.15)
    return U

def dU_cathode_dT_lco(soc):
    return 0.0

def D_cathode_lco(soc, T_K):
    return 4e-14

# -----------------------------
# NCA – سه سطح
# -----------------------------

def U_cathode_nca_simple(soc, T_K):
    soc = _clamp_soc(soc)
    U = 3.8 + 0.5 * soc
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_nca_user(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["nca"]
    if data["soc"] is None:
        return U_cathode_nca_simple(soc, T_K)
    U = float(np.interp(soc, data["soc"], data["U"]))
    U += 0.0 * (T_K - 298.15)
    return U

def U_cathode_nca_industrial(soc, T_K):
    soc = _clamp_soc(soc)
    data = _user_ocv_data["nca"]
    if data["spline"] is None:
        return U_cathode_nca_user(soc, T_K)
    U = float(data["spline"](soc))
    U += 0.0 * (T_K - 298.15)
    return U

def dU_cathode_dT_nca(soc):
    return 0.0

def D_cathode_nca(soc, T_K):
    return 6e-14
