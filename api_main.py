from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import redis
import json
import uuid
import sqlite3

# NEW: SQLAlchemy imports
from database import SessionLocal, SimulationResult, User

# NEW: JWT imports
from jose import jwt, JWTError

# NEW: include auth router
from auth_main import router as auth_router


app = FastAPI(
    title="Physion V20 Web Simulation Engine",
    version="1.0.0"
)

# ==========================
# AUTH CONFIG
# ==========================
SECRET_KEY = "CHANGE_THIS_TO_A_SECURE_KEY"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# include auth endpoints
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


# ⭐⭐ NEW — تابع چک ادمین ⭐⭐
def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# ==========================
# REDIS + SQLITE
# ==========================
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

DB_FILE = "physion.db"

def get_db():
    return sqlite3.connect(DB_FILE)


class SimulationInput(BaseModel):
    C_rate: float = 1.0
    n_cycles: int = 1
    T_cell: float = 298.15


# ==========================
# SIMULATE (Protected)
# ==========================
@app.post("/simulate")
def simulate(input: SimulationInput, current_user = Depends(get_current_user)):
    job_id = str(uuid.uuid4())

    job_data = {
        "job_id": job_id,
        "input_data": input.dict()
    }

    # Push job to Redis queue
    redis_client.rpush("physion-jobs", json.dumps(job_data))

    # Save simulation request in SQLAlchemy DB
    session = SessionLocal()
    sim = SimulationResult(
        name=f"job_{job_id}",
        steps=0,
        avg_voltage=0.0,
        max_temperature=0.0,
        user_id=current_user.id   # اتصال شبیه‌سازی به کاربر
    )
    session.add(sim)
    session.commit()
    session.close()

    return {
        "status": "queued",
        "job_id": job_id
    }


# ==========================
# RESULT (Protected)
# ==========================
@app.get("/result/{job_id}")
def get_result(job_id: str, current_user = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    # Check job status
    cur.execute("SELECT status FROM jobs WHERE id = ?", (job_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return {"error": "job_id not found"}

    status = row[0]

    if status != "done":
        conn.close()
        return {"job_id": job_id, "status": status}

    # Fetch result
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


# ==========================
# ⭐⭐ NEW — اندپوینت مخصوص ادمین ⭐⭐
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
            "user_id": s.user_id
        }
        for s in sims
    ]
