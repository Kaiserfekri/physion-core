import json
import redis
import threading
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from physion_core.cycle_engine import run_simulation
from database import SessionLocal, SimulationResult, Job, JobResult, OutboxJob

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

MAX_RETRIES = 3
LOCK_TTL = 60
WORKER_ID = "worker-1"
JOB_STALE_SECONDS = 300  # 5 دقیقه

print("Worker (Production-Safe + Atomic + Fault Recovery + Outbox) started...")


def heartbeat_loop():
    import time
    while True:
        try:
            redis_client.set(
                f"worker:{WORKER_ID}:heartbeat",
                datetime.utcnow().isoformat(),
                ex=LOCK_TTL
            )
        except Exception:
            pass
        time.sleep(10)


threading.Thread(target=heartbeat_loop, daemon=True).start()


def process_outbox_once():
    """یک outbox job پردازش نشده را به صف Redis می‌فرستد."""
    session = SessionLocal()
    try:
        with session.begin():
            outbox = session.execute(
                select(OutboxJob).where(OutboxJob.processed == False)
            ).scalar_one_or_none()

            if not outbox:
                return

            redis_client.rpush("physion-jobs", outbox.payload)
            outbox.processed = True
    finally:
        session.close()


while True:
    # قبل از هر job، یک outbox را sync کن
    process_outbox_once()

    job = redis_client.blpop("physion-jobs")
    _, job_json = job

    job_data = json.loads(job_json)
    job_id = job_data["job_id"]
    input_data = job_data["input_data"]

    lock_key = f"job_lock:{job_id}"

    got_lock = redis_client.set(lock_key, WORKER_ID, nx=True, ex=LOCK_TTL)
    if not got_lock:
        continue

    print(f"Running job {job_id}")

    session = SessionLocal()
    try:
        with session.begin():
            job_obj = session.execute(
                select(Job).where(Job.id == job_id).with_for_update()
            ).scalar_one_or_none()

            if not job_obj:
                redis_client.delete(lock_key)
                continue

            # Idempotency: اگر قبلاً نتیجه ثبت شده و job completed است، skip
            existing_result_id = session.execute(
                select(JobResult.id).where(JobResult.job_id == job_id)
            ).scalar_one_or_none()

            if job_obj.state == "completed" and existing_result_id is not None:
                print(f"Job {job_id} already completed, skipping")
                redis_client.delete(lock_key)
                continue

            # Recovery: اگر job در حالت running/locked و stale است
            if job_obj.state in ["running", "locked"]:
                if job_obj.last_heartbeat and \
                   (datetime.utcnow() - job_obj.last_heartbeat) > timedelta(seconds=JOB_STALE_SECONDS):
                    job_obj.state = "retrying"
                    job_obj.next_run_at = datetime.utcnow()

            if job_obj.state in ["completed", "dead"]:
                redis_client.delete(lock_key)
                continue

            if job_obj.next_run_at and datetime.utcnow() < job_obj.next_run_at:
                redis_client.rpush("physion-jobs", json.dumps(job_data))
                redis_client.delete(lock_key)
                continue

            job_obj.state = "running"
            job_obj.status = "running"
            job_obj.last_heartbeat = datetime.utcnow()

            # اجرای شبیه‌سازی
            result = run_simulation(input_data)

            V = result.get("V", [])
            T = result.get("T", [])
            t = result.get("t", [])

            avg_voltage = float(sum(V) / len(V)) if len(V) > 0 else 0.0
            max_temperature = max(T) if len(T) > 0 else 0.0
            steps = len(t)

            job_result = JobResult(
                job_id=job_id,
                result=json.dumps(result),
                metrics=json.dumps(result.get("metrics", {})),
                created_at=datetime.utcnow()
            )
            try:
                session.add(job_result)
            except IntegrityError:
                # اگر به خاطر unique constraint خطا داد، یعنی قبلاً نتیجه ثبت شده
                session.rollback()

            sim = session.execute(
                select(SimulationResult).where(SimulationResult.job_id == job_id).with_for_update()
            ).scalar_one_or_none()

            if sim:
                sim.steps = steps
                sim.avg_voltage = avg_voltage
                sim.max_temperature = max_temperature

            job_obj.state = "completed"
            job_obj.status = "done"
            job_obj.finished_at = datetime.utcnow()
            job_obj.next_run_at = None
            job_obj.last_heartbeat = datetime.utcnow()

        print(f"Job {job_id} completed")

    except Exception as e:
        print(f"Job {job_id} failed:", str(e))

        with session.begin():
            job_obj = session.execute(
                select(Job).where(Job.id == job_id).with_for_update()
            ).scalar_one_or_none()

            if job_obj:
                job_obj.attempts += 1
                job_obj.last_error = str(e)

                if job_obj.attempts < MAX_RETRIES:
                    delay = 2 ** (job_obj.attempts - 1)
                    job_obj.state = "retrying"
                    job_obj.status = "failed"
                    job_obj.next_run_at = datetime.utcnow() + timedelta(seconds=delay)
                    job_obj.last_heartbeat = datetime.utcnow()

                    redis_client.rpush("physion-jobs", json.dumps(job_data))
                    print(f"Retrying job {job_id} after {delay}s")
                else:
                    job_obj.state = "dead"
                    job_obj.status = "failed"
                    job_obj.finished_at = datetime.utcnow()
                    job_obj.next_run_at = None
                    job_obj.last_heartbeat = datetime.utcnow()

                    redis_client.rpush("physion-dead-jobs", json.dumps(job_data))
                    print(f"Job {job_id} moved to DEAD LETTER QUEUE")

    finally:
        redis_client.delete(lock_key)
        session.close()
