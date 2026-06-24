from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import uuid

app = FastAPI(
    title="Physion V20 Web Simulation Engine",
    version="1.0.0"
)

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

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

