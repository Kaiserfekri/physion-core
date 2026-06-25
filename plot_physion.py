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
    # 4) رسم نمودارها
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

    print("All plots saved successfully in 'plots' folder.")


if __name__ == "__main__":
    main()
