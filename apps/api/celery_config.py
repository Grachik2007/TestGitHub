import os
from datetime import timedelta
from celery.schedules import crontab

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
timezone = "Europe/Moscow"  # MSK timezone
enable_utc = True

task_track_started = True
task_time_limit = 60 * 60  # 1 hour
task_soft_time_limit = 55 * 60  # 55 minutes

broker_connection_retry_on_startup = True
broker_connection_retry = True
broker_connection_max_retries = 10

result_expires = 86400  # 24 hours

# Celery Beat Schedule
beat_schedule = {
    # Daily sync at 00:00 MSK
    "wonderfulbed-daily-sync": {
        "task": "tasks.wonderfulbed_sync.sync_wonderfulbed_daily",
        "schedule": crontab(hour=0, minute=0),  # Every day at 00:00
        "options": {
            "expires": 3600,  # Task expires after 1 hour if not picked up
        },
    },
    # Check sync status every hour
    "check-sync-status": {
        "task": "tasks.wonderfulbed_sync.check_sync_status",
        "schedule": crontab(minute=0),  # Every hour
    },
}
