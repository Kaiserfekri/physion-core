import json
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
from physion_core.cycle_engine import run_simulation


# Redis
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


# DB connection factory
def get_db():
    return psycopg2.connect(
        host="postgres",
        database="physion",
        user="physion_user",
        password="your_password"
    )


print("Worker started... waiting for jobs")


while True:
    # Blocking wait for job
    job = redis_client.blpop("physion-jobs")
    _, job_json = job

    job_data = json.loads(job_json)
    job_id = job_data["job_id"]
    input_data = job_data["input_data"]

    print(f"Running job {job_id}")

    try:
        # Run simulation
        result = run_simulation(input_data)

        # Save result
        db = get_db()
        cur = db.cursor()

        cur.execute("""
            INSERT INTO job_results (job_id, result, metrics)
            VALUES (%s, %s, %s)
        """, (
            job_id,
            json.dumps(result),
            json.dumps(result.get("metrics", {}))
        ))

        cur.execute("""
            UPDATE jobs
            SET status='done', finished_at=NOW()
            WHERE id=%s
        """, (job_id,))

        db.commit()
        db.close()

        print(f"Job {job_id} done")

    except Exception as e:
        db = get_db()
        cur = db.cursor()

        cur.execute("""
            UPDATE jobs
            SET status='failed', finished_at=NOW()
            WHERE id=%s
        """, (job_id,))

        db.commit()
        db.close()

        print(f"Job {job_id} failed:", str(e))
