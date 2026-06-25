from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import redis
import json
import uuid

from database import SessionLocal, SimulationResult, User, Job, JobResult
from jose import jwt, JWTError
from auth_main import router as auth_router


app = FastAPI(
    title="Physion V20 Web Simulation Engine",
    version="1.0.0"
)

SECRET_KEY = "CHANGE_THIS_TO_A_SECURE_KEY"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app.include_router(auth_router)


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
    user = session.query(User).filter(User.email == email).first()
    session.close()

    if user is None:
        raise credentials_exception

    return user


def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# ==========================
# REDIS
# ==========================
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


# ==========================
# INPUT MODEL
# ==========================
class SimulationInput(BaseModel):
    C_rate: float = 1.0
    n_cycles: int = 1
    T_cell: float = 298.15


# ==========================
# SIMULATE
# ==========================
@app.post("/simulate")
def simulate(input: SimulationInput, current_user = Depends(get_current_user)):
    job_id = str(uuid.uuid4())

    job_data = {
        "job_id": job_id,
        "input_data": input.dict()
    }

    # ارسال job به صف Redis
    redis_client.rpush("physion-jobs", json.dumps(job_data))

    session = SessionLocal()

    # ایجاد رکورد Job
    job_obj = Job(
        id=job_id,
        status="queued",
    )
    session.add(job_obj)

    # ایجاد SimulationResult
    sim = SimulationResult(
        name=f"job_{job_id}",
        steps=0,
        avg_voltage=0.0,
        max_temperature=0.0,
        user_id=current_user.id,
        job_id=job_id
    )
    session.add(sim)

    session.commit()
    session.close()

    return {
        "status": "queued",
        "job_id": job_id
    }


# ==========================
# RESULT
# ==========================
@app.get("/result/{job_id}")
def get_result(job_id: str, current_user = Depends(get_current_user)):
    session = SessionLocal()

    job = session.query(Job).filter(Job.id == job_id).first()
    if not job:
        session.close()
        return {"error": "job_id not found"}

    if job.status != "done":
        status = job.status
        session.close()
        return {"job_id": job_id, "status": status}

    job_result = session.query(JobResult).filter(
        JobResult.job_id == job_id
    ).order_by(JobResult.id.desc()).first()

    session.close()

    if not job_result:
        return {"error": "result not found"}

    result_json = json.loads(job_result.result)
    metrics_json = json.loads(job_result.metrics)

    return {
        "job_id": job_id,
        "status": "done",
        "result": result_json,
        "metrics": metrics_json
    }


# ==========================
# ADMIN LIST
# ==========================
@app.get("/admin/simulations")
def admin_list_simulations(current_user = Depends(require_admin)):
    session = SessionLocal()
    sims = session.query(SimulationResult).all()
    session.close()

    return [
        {
            "id": s.id,
            "name": s.name,
            "steps": s.steps,
            "avg_voltage": s.avg_voltage,
            "max_temperature": s.max_temperature,
            "user_id": s.user_id,
            "job_id": s.job_id
        }
        for s in sims
    ]


# ==========================
# USER LIST
# ==========================
@app.get("/my/simulations")
def my_simulations(current_user = Depends(get_current_user)):
    session = SessionLocal()
    sims = session.query(SimulationResult).filter(
        SimulationResult.user_id == current_user.id
    ).all()
    session.close()

    return [
        {
            "id": s.id,
            "name": s.name,
            "steps": s.steps,
            "avg_voltage": s.avg_voltage,
            "max_temperature": s.max_temperature,
            "job_id": s.job_id
        }
        for s in sims
    ]

