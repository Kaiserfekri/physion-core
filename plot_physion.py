import os
import matplotlib.pyplot as plt
from physion_core.cycle_engine import run_simulation


def main():
    # Simulation parameters
    params = {
        "n_cycles": 1,
        "t_half_cycle": 100,
        "dt_min": 0.1,
    }

    # Run simulation
    result = run_simulation(params)

    t = result["t"]
    V = result["V"]
    T = result["T"]
    R = result["R_total"]
    sei = result["sei_avg"]
    cs_a = result["cs_anode"]
    cs_c = result["cs_cathode"]
    eta_a = result["eta_anode"]
    eta_c = result["eta_cathode"]
    j_lim_a = result["j_lim_anode"]      # NEW
    j_lim_c = result["j_lim_cathode"]    # NEW

    # Create output folder
    os.makedirs("plots", exist_ok=True)

    # -------------------------------
    # 1) Voltage
    # -------------------------------
    plt.figure()
    plt.plot(t, V)
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Voltage vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_voltage.png", dpi=300)

    # -------------------------------
    # 2) Temperature
    # -------------------------------
    plt.figure()
    plt.plot(t, T)
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_temperature.png", dpi=300)

    # -------------------------------
    # 3) Total Resistance
    # -------------------------------
    plt.figure()
    plt.plot(t, R)
    plt.xlabel("Time [s]")
    plt.ylabel("Total Resistance [Ohm]")
    plt.title("Resistance vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_resistance.png", dpi=300)

    # -------------------------------
    # 4) SEI Growth
    # -------------------------------
    plt.figure()
    plt.plot(t, sei)
    plt.xlabel("Time [s]")
    plt.ylabel("SEI (avg)")
    plt.title("SEI Growth vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_sei.png", dpi=300)

    # -------------------------------
    # 5) Surface Concentration (Anode)
    # -------------------------------
    plt.figure()
    plt.plot(t, cs_a)
    plt.xlabel("Time [s]")
    plt.ylabel("Surface Concentration (Anode)")
    plt.title("Anode Surface Concentration vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_cs_anode.png", dpi=300)

    # -------------------------------
    # 6) Surface Concentration (Cathode)
    # -------------------------------
    plt.figure()
    plt.plot(t, cs_c)
    plt.xlabel("Time [s]")
    plt.ylabel("Surface Concentration (Cathode)")
    plt.title("Cathode Surface Concentration vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_cs_cathode.png", dpi=300)

    # ============================================================
    # 7) DENDRITE RISK — MIT‑REAL MODEL
    # ============================================================

    # η_total = η_cathode - η_anode
    eta_total = [eta_c[i] - eta_a[i] for i in range(len(t))]

    # cs_max واقعی از مدل
    cs_max = max(cs_a) if max(cs_a) != 0 else 1.0

    # η_crit از کانفیگ (اگر نبود، مقدار پیش‌فرض)
    try:
        from physion_core.config import CellConfig
        eta_crit = CellConfig().eta_crit
    except:
        eta_crit = 0.05  # fallback

    # MIT‑Real dendrite risk:
    # Risk = (|η_anode| / η_crit) * (cs_a / cs_max)
    dendrite_risk = [
        (abs(eta_a[i]) / (eta_crit + 1e-12)) * (cs_a[i] / (cs_max + 1e-12))
        for i in range(len(t))
    ]

    plt.figure()
    plt.plot(t, dendrite_risk, color="red")
    plt.xlabel("Time [s]")
    plt.ylabel("Dendrite Risk Index")
    plt.title("Dendrite Risk (|η|/η_crit × cs/cs_max)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_dendrite_risk.png", dpi=300)

    # ============================================================
    # 8) CCD — REAL PHYSICS (j_lim / |η|)
    # ============================================================

    ccd = [
        j_lim_a[i] / (abs(eta_total[i]) + 1e-12)
        for i in range(len(t))
    ]

    plt.figure()
    plt.plot(t, ccd, color="purple")
    plt.xlabel("Time [s]")
    plt.ylabel("CCD (A/m^2)")
    plt.title("Critical Current Density vs Time (Using j_lim and η)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_ccd.png", dpi=300)

    print("All plots saved successfully in 'plots' folder.")


if __name__ == "__main__":
    main()
