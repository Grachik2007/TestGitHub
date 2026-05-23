from celery import Celery

app = Celery('ai_agents')
app.config_from_object('celery_config')
