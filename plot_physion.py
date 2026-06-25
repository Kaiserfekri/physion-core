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
    # 7) DENDRITE RISK — REAL DATA (NO GUESSING)
    # ============================================================

    # η_total = η_cathode - η_anode
    eta_total = [eta_c[i] - eta_a[i] for i in range(len(t))]

    # Normalize cs
    cs_max = max(cs_a) if max(cs_a) != 0 else 1.0

    dendrite_risk = [
        abs(eta_total[i]) * (1 - cs_a[i] / cs_max)
        for i in range(len(t))
    ]

    plt.figure()
    plt.plot(t, dendrite_risk, color="red")
    plt.xlabel("Time [s]")
    plt.ylabel("Dendrite Risk (normalized)")
    plt.title("Dendrite Risk vs Time (Using Real η and cs)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_dendrite_risk.png", dpi=300)

    # ============================================================
    # 8) CCD — REAL DATA (NO GUESSING)
    # ============================================================

    # CCD ∝ (1/R_total) * (cs_a/cs_max) * (1/|η_total|)
    ccd = [
        (1.0 / R[i] if R[i] != 0 else 0.0)
        * (cs_a[i] / cs_max)
        * (1.0 / (abs(eta_total[i]) + 1e-12))
        for i in range(len(t))
    ]

    plt.figure()
    plt.plot(t, ccd, color="purple")
    plt.xlabel("Time [s]")
    plt.ylabel("CCD (normalized)")
    plt.title("Critical Current Density vs Time (Using Real η and R)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_ccd.png", dpi=300)

    print("All plots saved successfully in 'plots' folder.")


if __name__ == "__main__":
    main()
