import aiohttp.web

from .app import ReplayUploaderApplication as _App


def start_webapp(
        host: str,
        port: int,
        analyse_replay_endpoint: str,
        add_replay_analysis_endpoint: str,
        show_replay_analysis_endpoint: str):

    webapp = _App(analyse_replay_endpoint, add_replay_analysis_endpoint, show_replay_analysis_endpoint)

    aiohttp.web.run_app(webapp, host=host, port=port)