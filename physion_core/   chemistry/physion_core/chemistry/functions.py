import numpy as np
from scipy.interpolate import CubicSpline

# -----------------------------
# Graphite (Anode) – اسکلت
# -----------------------------
def U_anode_graphite(soc, T_K):
    # فعلاً اسکلت، بعداً می‌توانی پرش کنی
    return 0.1 + 0.9 * float(soc)

def dU_anode_dT_graphite(soc):
    # مشتق دما – فعلاً ثابت کوچک
    return 0.0

def D_anode_graphite(soc, T_K):
    # ضریب انتشار ساده
    return 1e-14


# -----------------------------
# ذخیرهٔ دادهٔ کاربر برای LFP
# -----------------------------
_user_ocv_data_lfp = {
    "soc": None,
    "U": None,
    "spline": None,
}


def set_user_ocv_lfp(soc_array, U_array):
    """
    این تابع را وقتی کاربر OCV لFP را آپلود کرد صدا می‌کنی.
    ورودی‌ها:
        soc_array: لیست یا آرایهٔ SOC (بین 0 و 1)
        U_array: لیست یا آرایهٔ ولتاژ [V]
    """
    soc = np.array(soc_array, dtype=float)
    U = np.array(U_array, dtype=float)

    _user_ocv_data_lfp["soc"] = soc
    _user_ocv_data_lfp["U"] = U
    _user_ocv_data_lfp["spline"] = CubicSpline(soc, U)


# -----------------------------
# LFP – سطح ساده (Simple Mode)
# -----------------------------
def U_cathode_lfp_simple(soc, T_K):
    """
    OCV سادهٔ لFP:
    بین 3.2 تا 3.6 ولت، خطی با SOC.
    فقط برای تست و اجرای بدون دادهٔ واقعی.
    """
    soc = float(soc)
    return 3.2 + 0.4 * soc


def dU_cathode_dT_lfp(soc):
    """
    مشتق OCV نسبت به دما – فعلاً تقریب ساده.
    """
    return 0.0


def D_cathode_lfp(soc, T_K):
    """
    ضریب انتشار ساده برای لFP.
    """
    return 5e-14


# -----------------------------
# LFP – سطح پیشرفته (User Upload Mode)
# -----------------------------
def U_cathode_lfp_user(soc, T_K):
    """
    OCV مبتنی بر دادهٔ کاربر (جدول SOC–U).
    اگر دادهٔ کاربر موجود نباشد، به سطح ساده برمی‌گردد.
    """
    soc = float(soc)
    data_soc = _user_ocv_data_lfp["soc"]
    data_U = _user_ocv_data_lfp["U"]

    if data_soc is None or data_U is None:
        # fallback
        return U_cathode_lfp_simple(soc, T_K)

    return float(np.interp(soc, data_soc, data_U))


# -----------------------------
# LFP – سطح صنعتی/پژوهشی (Industrial Mode)
# -----------------------------
def U_cathode_lfp_industrial(soc, T_K):
    """
    OCV مبتنی بر CubicSpline روی دادهٔ کاربر.
    اگر spline موجود نباشد، به سطح user یا ساده برمی‌گردد.
    """
    soc = float(soc)
    spline = _user_ocv_data_lfp["spline"]

    if spline is None:
        return U_cathode_lfp_user(soc, T_K)

    return float(spline(soc))


# -----------------------------
# اسکلت NMC / LCO / NCA – فقط برای کامل بودن فایل
# بعداً می‌توانی مشابه LFP برای آن‌ها هم سه سطح بسازی.
# -----------------------------
def U_cathode_nmc(soc, T_K):
    return 3.6 + 0.5 * float(soc)

def dU_cathode_dT_nmc(soc):
    return 0.0

def D_cathode_nmc(soc, T_K):
    return 5e-14


def U_cathode_lco(soc, T_K):
    return 3.7 + 0.4 * float(soc)

def dU_cathode_dT_lco(soc):
    return 0.0

def D_cathode_lco(soc, T_K):
    return 4e-14


def U_cathode_nca(soc, T_K):
    return 3.8 + 0.5 * float(soc)

def dU_cathode_dT_nca(soc):
    return 0.0

def D_cathode_nca(soc, T_K):
    return 6e-14
