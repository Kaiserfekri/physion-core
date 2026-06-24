import json
import redis
import sqlite3
from physion_core.cycle_engine import run_simulation

# Redis connection
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# SQLite DB file
DB_FILE = "physion.db"

# Create tables if not exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            status TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            finished_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT,
            result TEXT,
            metrics TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# Insert or update job
def save_job_status(job_id, status):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO jobs (id, status, finished_at)
        VALUES (?, ?, CASE WHEN ?='done' THEN CURRENT_TIMESTAMP ELSE NULL END)
    """, (job_id, status, status))

    conn.commit()
    conn.close()

# Save simulation result
def save_result(job_id, result):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO job_results (job_id, result, metrics)
        VALUES (?, ?, ?)
    """, (
        job_id,
        json.dumps(result),
        json.dumps(result.get("metrics", {}))
    ))

    conn.commit()
    conn.close()


# Initialize DB
init_db()

print("Worker (SQLite version) started... waiting for jobs")

while True:
    job = redis_client.blpop("physion-jobs")
    _, job_json = job

    job_data = json.loads(job_json)
    job_id = job_data["job_id"]
    input_data = job_data["input_data"]

    print(f"Running job {job_id}")

    try:
        save_job_status(job_id, "running")

        result = run_simulation(input_data)

        save_result(job_id, result)
        save_job_status(job_id, "done")

        print(f"Job {job_id} done")

    except Exception as e:
        save_job_status(job_id, "failed")
        print(f"Job {job_id} failed:", str(e))
