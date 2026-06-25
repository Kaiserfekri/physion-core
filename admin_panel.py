import streamlit as st
import sqlite3

DB_FILE = "physion.db"

def get_jobs():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, status, created_at, finished_at FROM jobs")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_result(job_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT result, metrics FROM job_results WHERE job_id = ?", (job_id,))
    row = cur.fetchone()
    conn.close()
    return row

st.title("Physion V20 Admin Panel")

jobs = get_jobs()
for job in jobs:
    st.write(f"Job {job[0]} - Status: {job[1]} - Created: {job[2]} - Finished: {job[3]}")
    if st.button(f"View Result {job[0]}"):
        result = get_result(job[0])
        if result:
            st.json({"result": result[0], "metrics": result[1]})
        else:
            st.write("No result found")
