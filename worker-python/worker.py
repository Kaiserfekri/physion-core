import json
import redis
import threading
import uuid
from datetime import datetime, timedelta

from sqlalchemy import select

from physion_core.cycle_engine import run_simulation
from database import SessionLocal, SimulationResult, Job, JobResult, OutboxJob


redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# ==========================
# CONFIG
# ==========================
MAX_RETRIES = 3
LOCK_TTL = 60
JOB_STALE_SECONDS = 300

STREAM_KEY = "physion-jobs-stream"
DEAD_STREAM = "physion-dead-jobs-stream"
GROUP_NAME = "physion-workers"

WORKER_ID = f"worker-{uuid.uuid4()}"

print(f"Worker started with ID: {WORKER_ID}")


# ==========================
# STREAM GROUP
# ==========================
def ensure_stream_group():
    try:
        redis_client.xgroup_create(STREAM_KEY, GROUP_NAME, id="0-0", mkstream=True)
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            pass


ensure_stream_group()


# ==========================
# HEARTBEAT THREAD (WORKER)
# ==========================
def heartbeat_loop():
    import time
    while True:
        redis_client.set(
            f"worker:{WORKER_ID}:heartbeat",
            datetime.utcnow().isoformat(),
            ex=LOCK_TTL
        )
        time.sleep(10)


threading.Thread(target=heartbeat_loop, daemon=True).start()


# ==========================
# HEARTBEAT THREAD (JOB)
# ==========================
def job_heartbeat(job_id: str, stop_event: threading.Event):
    import time
    while not stop_event.is_set():
        session = SessionLocal()
        try:
            with session.begin():
                job_obj = session.execute(
                    select(Job).where(Job.id == job_id).with_for_update()
                ).scalar_one_or_none()
                if job_obj:
                    job_obj.last_heartbeat = datetime.utcnow()
        finally:
            session.close()
        time.sleep(10)


# ==========================
# OUTBOX SYNC (Batch)
# ==========================
def process_outbox_once():
    session = SessionLocal()
    try:
        with session.begin():
            outboxes = session.execute(
                select(OutboxJob).where(OutboxJob.processed == False).limit(100)
            ).scalars().all()

            if not outboxes:
                return

            for outbox in outboxes:
                redis_client.xadd(
                    STREAM_KEY,
                    {"payload": outbox.payload},
                    id="*"
                )
                outbox.processed = True
    finally:
        session.close()


# ==========================
# PENDING RECOVERY (XAUTOCLAIM)
# ==========================
def claim_pending_once():
    # پیام‌های Pending که بیش از 60 ثانیه idle بوده‌اند را Claim می‌کنیم
    try:
        res = redis_client.xautoclaim(
            STREAM_KEY,
            GROUP_NAME,
            WORKER_ID,
            min_idle_time=60000,
            start_id="0-0",
            count=1
        )
    except redis.exceptions.ResponseError:
        return None

    # res = (new_start_id, [(msg_id, fields), ...])
    if not res or len(res) < 2:
        return None

    messages = res[1]
    if not messages:
        return None

    msg_id, fields = messages[0]
    return (msg_id, fields)


# ==========================
# MAIN LOOP
# ==========================
while True:
    process_outbox_once()

    # اول سعی می‌کنیم Pending را Claim کنیم
    claimed = claim_pending_once()
    if claimed:
        msg_id, fields = claimed
    else:
        resp = redis_client.xreadgroup(
            GROUP_NAME,
            WORKER_ID,
            {STREAM_KEY: ">"},
            count=1,
            block=5000
        )

        if not resp:
            continue

        stream, messages = resp[0]
        msg_id, fields = messages[0]

    payload = fields.get("payload")
    if not payload:
        redis_client.xack(STREAM_KEY, GROUP_NAME, msg_id)
        continue

    job_data = json.loads(payload)
    job_id = job_data["job_id"]
    input_data = job_data["input_data"]

    lock_key = f"job_lock:{job_id}"
    got_lock = redis_client.set(lock_key, WORKER_ID, nx=True, ex=LOCK_TTL)
    if not got_lock:
        # پیام Pending می‌ماند و بعداً توسط Worker دیگر Claim می‌شود
        continue

    print(f"Running job {job_id} (msg {msg_id})")

    # شروع heartbeat مخصوص این job
    stop_event = threading.Event()
    threading.Thread(target=job_heartbeat, args=(job_id, stop_event), daemon=True).start()

    session = SessionLocal()
    try:
        with session.begin():
            job_obj = session.execute(
                select(Job).where(Job.id == job_id).with_for_update()
            ).scalar_one_or_none()

            if not job_obj:
                redis_client.xack(STREAM_KEY, GROUP_NAME, msg_id)
                redis_client.delete(lock_key)
                stop_event.set()
                continue

            existing_result = session.execute(
                select(JobResult.id).where(JobResult.job_id == job_id)
            ).scalar_one_or_none()

            if job_obj.state == "completed" and existing_result:
                redis_client.xack(STREAM_KEY, GROUP_NAME, msg_id)
                redis_client.delete(lock_key)
                stop_event.set()
                continue

            if job_obj.state in ["running", "locked"]:
                if job_obj.last_heartbeat and \
                   (datetime.utcnow() - job_obj.last_heartbeat) > timedelta(seconds=JOB_STALE_SECONDS):
                    job_obj.state = "retrying"
                    job_obj.next_run_at = datetime.utcnow()

            if job_obj.state in ["completed", "dead"]:
                redis_client.xack(STREAM_KEY, GROUP_NAME, msg_id)
                redis_client.delete(lock_key)
                stop_event.set()
                continue

            if job_obj.next_run_at and datetime.utcnow() < job_obj.next_run_at:
                # پیام Pending می‌ماند؛ بعداً دوباره Claim می‌شود
                redis_client.delete(lock_key)
                stop_event.set()
                continue

            job_obj.state = "running"
            job_obj.status = "running"
            job_obj.last_heartbeat = datetime.utcnow()

            # اجرای شبیه‌سازی (طولانی ممکن است، heartbeat جداگانه داریم)
            result = run_simulation(input_data)

            V = result.get("V", [])
            T = result.get("T", [])
            t = result.get("t", [])

            avg_voltage = float(sum(V) / len(V)) if len(V) else 0.0
            max_temperature = max(T) if len(T) else 0.0
            steps = len(t)

            # Idempotency: چون قبلاً چک کردیم، نیازی به try/except نیست
            if not existing_result:
                job_result = JobResult(
                    job_id=job_id,
                    result=json.dumps(result),
                    metrics=json.dumps(result.get("metrics", {})),
                    created_at=datetime.utcnow()
                )
                session.add(job_result)

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

        redis_client.xack(STREAM_KEY, GROUP_NAME, msg_id)
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
                    # پیام Pending می‌ماند؛ بعداً با XAUTOCLAIM دوباره گرفته می‌شود
                    print(f"Retry scheduled for job {job_id} after {delay}s")
                else:
                    job_obj.state = "dead"
                    job_obj.status = "failed"
                    job_obj.finished_at = datetime.utcnow()
                    job_obj.next_run_at = None
                    job_obj.last_heartbeat = datetime.utcnow()

                    redis_client.xack(STREAM_KEY, GROUP_NAME, msg_id)
                    redis_client.xadd(
                        DEAD_STREAM,
                        {"payload": payload, "error": str(e)},
                        id="*"
                    )
                    print(f"Job {job_id} moved to DEAD LETTER STREAM")

    finally:
        stop_event.set()
        redis_client.delete(lock_key)
        session.close()
