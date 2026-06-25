import os
import matplotlib.pyplot as plt
from physion_core.cycle_engine import run_simulation


def main():
    # 1) پارامترهای شبیه‌سازی (می‌توانی تغییر بدهی)
    params = {
        "n_cycles": 1,
        "t_half_cycle": 100,
        "dt_min": 0.1,
    }

    # 2) اجرای شبیه‌سازی
    result = run_simulation(params)

    t = result["t"]
    V = result["V"]
    T = result["T"]
    R = result["R_total"]
    sei = result["sei_avg"]
    cs_a = result["cs_anode"]
    cs_c = result["cs_cathode"]

    # 3) ساخت پوشهٔ ذخیره‌سازی نمودارها
    os.makedirs("plots", exist_ok=True)

    # -------------------------------
    # 4) رسم نمودارهای اصلی
    # -------------------------------

    # Voltage
    plt.figure()
    plt.plot(t, V)
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Voltage vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_voltage.png", dpi=300)

    # Temperature
    plt.figure()
    plt.plot(t, T)
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_temperature.png", dpi=300)

    # Total Resistance
    plt.figure()
    plt.plot(t, R)
    plt.xlabel("Time [s]")
    plt.ylabel("Total Resistance [Ohm]")
    plt.title("Resistance vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_resistance.png", dpi=300)

    # SEI
    plt.figure()
    plt.plot(t, sei)
    plt.xlabel("Time [s]")
    plt.ylabel("SEI (avg)")
    plt.title("SEI Growth vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_sei.png", dpi=300)

    # Surface concentration (anode)
    plt.figure()
    plt.plot(t, cs_a)
    plt.xlabel("Time [s]")
    plt.ylabel("Surface Concentration (Anode)")
    plt.title("Anode Surface Concentration vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_cs_anode.png", dpi=300)

    # Surface concentration (cathode)
    plt.figure()
    plt.plot(t, cs_c)
    plt.xlabel("Time [s]")
    plt.ylabel("Surface Concentration (Cathode)")
    plt.title("Cathode Surface Concentration vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_cs_cathode.png", dpi=300)

    # -------------------------------
    # 5) محاسبهٔ کمیت‌های کمکی برای ریسک دندریت و CCD
    # -------------------------------

    # تخمین سادهٔ overpotential: η ≈ V + I*R
    # چون I_app در مدل ثابت است، اینجا نرمال‌سازی شده با 1.0 در نظر می‌گیریم
    eta = [V[i] + R[i] for i in range(len(V))]

    # حداکثر غلظت سطحی آند برای نرمال‌سازی
    cs_max = max(cs_a) if max(cs_a) != 0 else 1.0

    # -------------------------------
    # 6) نمودار ریسک دندریت (واقعی‌تر)
    # Risk ~ f(η, cs_a)
    # -------------------------------
    dendrite_risk = [
        (abs(eta[i]) / (abs(eta[i]) + 1e-9)) * (1.0 - cs_a[i] / cs_max)
        for i in range(len(t))
    ]

    plt.figure()
    plt.plot(t, dendrite_risk, color="red")
    plt.xlabel("Time [s]")
    plt.ylabel("Dendrite Risk Index (normalized)")
    plt.title("Dendrite Risk vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_dendrite_risk.png", dpi=300)

    # -------------------------------
    # 7) نمودار CCD (واقعی‌تر)
    # CCD ~ 1/R * (cs_a/cs_max) * 1/|η|
    # -------------------------------
    ccd = [
        (1.0 / R[i] if R[i] != 0 else 0.0)
        * (cs_a[i] / cs_max)
        * (1.0 / (abs(eta[i]) + 1e-9))
        for i in range(len(t))
    ]

    plt.figure()
    plt.plot(t, ccd, color="purple")
    plt.xlabel("Time [s]")
    plt.ylabel("CCD (normalized)")
    plt.title("Critical Current Density vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_ccd.png", dpi=300)

    print("All plots saved successfully in 'plots' folder.")


if __name__ == "__main__":
    main()
