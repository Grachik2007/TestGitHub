import os
from datetime import timedelta

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
timezone = "UTC"
enable_utc = True

task_track_started = True
task_time_limit = 30 * 60
task_soft_time_limit = 25 * 60

broker_connection_retry_on_startup = True
broker_connection_retry = True
broker_connection_max_retries = 10

result_expires = 3600

beat_schedule = {
    "check-health": {
        "task": "tasks.health_check",
        "schedule": timedelta(minutes=5),
    },
}
