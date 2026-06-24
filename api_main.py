from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import uuid
import sqlite3

app = FastAPI(
    title="Physion V20 Web Simulation Engine",
    version="1.0.0"
)

# Redis connection
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# SQLite DB file
DB_FILE = "physion.db"

def get_db():
    return sqlite3.connect(DB_FILE)


class SimulationInput(BaseModel):
    C_rate: float = 1.0
    n_cycles: int = 1
    T_cell: float = 298.15


@app.post("/simulate")
def simulate(input: SimulationInput):
    job_id = str(uuid.uuid4())

    job_data = {
        "job_id": job_id,
        "input_data": input.dict()
    }

    redis_client.rpush("physion-jobs", json.dumps(job_data))

    return {
        "status": "queued",
        "job_id": job_id
    }


# ⭐⭐ اندپوینت نتیجه — بیرون از simulate ⭐⭐
@app.get("/result/{job_id}")
def get_result(job_id: str):
    conn = get_db()
    cur = conn.cursor()

    # Check job status
    cur.execute("SELECT status FROM jobs WHERE id = ?", (job_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return {"error": "job_id not found"}

    status = row[0]

    # If still running or failed
    if status != "done":
        conn.close()
        return {"job_id": job_id, "status": status}

    # If done → fetch result
    cur.execute("""
        SELECT result, metrics
        FROM job_results
        WHERE job_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (job_id,))

    result_row = cur.fetchone()
    conn.close()

    if not result_row:
        return {"error": "result not found"}

    result_json = json.loads(result_row[0])
    metrics_json = json.loads(result_row[1])

    return {
        "job_id": job_id,
        "status": "done",
        "result": result_json,
        "metrics": metrics_json
    }

