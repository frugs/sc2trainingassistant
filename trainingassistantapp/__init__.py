import aiohttp.web

from .app import TrainingAssistantApplication as _TrainingAssistantApplication


def start_webapp(host: str, port: int, db_path):
    webapp = _TrainingAssistantApplication(db_path)

    aiohttp.web.run_app(webapp, host=host, port=port)