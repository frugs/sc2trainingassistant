import aiohttp.web

from .app import ReplayAnalysisService as _Service


def start_replay_analysis_service(host: str, port: int):
    service = _Service()

    aiohttp.web.run_app(service, host=host, port=port)