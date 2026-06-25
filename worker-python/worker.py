import json
import redis
from datetime import datetime

from physion_core.cycle_engine import run_simulation
from database import SessionLocal, SimulationResult, Job, JobResult

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

print("Worker (ORM version) started... waiting for jobs")

while True:
    job = redis_client.blpop("physion-jobs")
    _, job_json = job

    job_data = json.loads(job_json)
    job_id = job_data["job_id"]
    input_data = job_data["input_data"]

    print(f"Running job {job_id}")

    session = SessionLocal()
    try:
        # ایجاد یا به‌روزرسانی Job
        job_obj = session.query(Job).filter(Job.id == job_id).first()
        if not job_obj:
            job_obj = Job(
                id=job_id,
                status="running",
                created_at=datetime.utcnow(),
                finished_at=None,
            )
            session.add(job_obj)
        else:
            job_obj.status = "running"
            job_obj.finished_at = None

        session.commit()

        # اجرای شبیه‌سازی
        result = run_simulation(input_data)

        # ذخیرهٔ نتیجه
        job_result = JobResult(
            job_id=job_id,
            result=json.dumps(result),
            metrics=json.dumps(result.get("metrics", {})),
            created_at=datetime.utcnow()
        )
        session.add(job_result)

        # به‌روزرسانی وضعیت Job
        job_obj.status = "done"
        job_obj.finished_at = datetime.utcnow()
        session.commit()

        print(f"Job {job_id} done")

        # به‌روزرسانی SimulationResult مرتبط
        sim = session.query(SimulationResult).filter(
            SimulationResult.job_id == job_id
        ).first()

        if sim:
            sim.steps = len(result["t"])
            sim.avg_voltage = float(sum(result["V"]) / len(result["V"]))
            sim.max_temperature = max(result["T"])
            session.commit()

    except Exception as e:
        print(f"Job {job_id} failed:", str(e))
        job_obj = session.query(Job).filter(Job.id == job_id).first()
        if job_obj:
            job_obj.status = "failed"
            job_obj.finished_at = datetime.utcnow()
            session.commit()
    finally:
        session.close()
