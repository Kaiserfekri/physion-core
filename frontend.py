import streamlit as st
import requests

st.title("Physion V20 Simulation")

# ورودی‌ها
C_rate = st.number_input("C-rate", 0.1, 5.0, 1.0)
n_cycles = st.number_input("Cycles", 1, 100, 1)
T_cell = st.number_input("Temperature (K)", 250.0, 400.0, 298.15)

if st.button("Run Simulation"):
    payload = {"C_rate": C_rate, "n_cycles": n_cycles, "T_cell": T_cell}
    r = requests.post("http://localhost:8000/simulate", json=payload)
    st.json(r.json())

    if "job_id" in r.json():
        job_id = r.json()["job_id"]
        st.write(f"Job ID: {job_id}")
        result = requests.get(f"http://localhost:8000/result/{job_id}")
        st.json(result.json())
