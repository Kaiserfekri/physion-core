import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import redis
import json
import uuid

from sqlalchemy import select

from database import SessionLocal, SimulationResult, User, Job, JobResult, OutboxJob
from jose import jwt, JWTError
from auth_main import router as auth_router


app = FastAPI(
    title="Physion V20 Web Simulation Engine",
    version="1.0.0"
)

# ==========================
# SECURITY CONFIG
# ==========================
SECRET_KEY = os.getenv("PHYSION_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("PHYSION_SECRET_KEY is not set")

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app.include_router(auth_router)


# ==========================
# REDIS STREAM
# ==========================
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

STREAM_KEY = "physion-jobs-stream"


# ==========================
# AUTH HELPERS
# ==========================
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    session = SessionLocal()
    try:
        user = session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
    finally:
        session.close()

    if user is None:
        raise credentials_exception

    return user


def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# ==========================
# INPUT MODEL
# ==========================
class SimulationInput(BaseModel):
    C_rate: float = 1.0
    n_cycles: int = 1
    T_cell: float = 298.15


# ==========================
# SIMULATE (Atomic + Outbox)
# ==========================
@app.post("/simulate")
def simulate(input: SimulationInput, current_user = Depends(get_current_user)):
    job_id = str(uuid.uuid4())
    payload = json.dumps({
        "job_id": job_id,
        "input_data": input.dict()
    })

    session = SessionLocal()
    try:
        with session.begin():
            job_obj = Job(
                id=job_id,
                status="queued",
                state="queued",
                attempts=0,
                next_run_at=None,
                last_heartbeat=None
            )
            session.add(job_obj)

            sim = SimulationResult(
                name=f"job_{job_id}",
                steps=0,
                avg_voltage=0.0,
                max_temperature=0.0,
                user_id=current_user.id,
                job_id=job_id
            )
            session.add(sim)

            outbox = OutboxJob(
                job_id=job_id,
                payload=payload,
                processed=False
            )
            session.add(outbox)

    except Exception:
        session.close()
        raise HTTPException(status_code=500, detail="Failed to create job")
    finally:
        session.close()

    return {"status": "queued", "job_id": job_id}


# ==========================
# RESULT
# ==========================
@app.get("/result/{job_id}")
def get_result(job_id: str, current_user = Depends(get_current_user)):
    session = SessionLocal()

    try:
        job = session.execute(
            select(Job).where(Job.id == job_id)
        ).scalar_one_or_none()

        if not job:
            return {"error": "job_id not found"}

        if job.state in ["queued", "running", "retrying"]:
            return {"job_id": job_id, "status": job.state}

        if job.state == "dead":
            return {"job_id": job_id, "status": "dead", "error": job.last_error}

        job_result = session.execute(
            select(JobResult).where(JobResult.job_id == job_id).order_by(JobResult.id.desc())
        ).scalar_one_or_none()

        if not job_result:
            return {"error": "result not found"}

        return {
            "job_id": job_id,
            "status": "completed",
            "result": json.loads(job_result.result),
            "metrics": json.loads(job_result.metrics)
        }
    finally:
        session.close()
