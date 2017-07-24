import tempfile

import sc2reader
from aiohttp.web import Application, Request, Response, json_response
from sc2reader.resources import Replay

from .replayanalysis import ReplayAnalysis
from .replayanalyser import analyse_replay

CHUNK_SIZE = 1024


def safe_load_replay(replay_file) -> Replay:
    try:
        return sc2reader.load_replay(replay_file, level=4)
    except Exception:
        return None


def serialise_replay_analysis(replay_analysis: ReplayAnalysis) -> dict:
    return {
        "hash": replay_analysis.hash,
        "players": [
            {
                "playerName": player_performance.player_name,
                "earlyGamePerformanceMetrics": [
                    {
                        "metricName": performance_metric.metric_name,
                        "metricDescription": performance_metric.metric_description,
                        "achievedValue": performance_metric.achieved_value,
                        "idealValue": performance_metric.ideal_value,
                        "rating": performance_metric.rating
                    } for performance_metric in player_performance.early_game_performance_metrics
                ]
            } for player_performance in replay_analysis.player_performances
        ]
    }


class ReplayAnalysisService(Application):

    def __init__(self):
        Application.__init__(self)

        self.router.add_post("/submit", self.submit)

    async def submit(self, request: Request) -> Response:
        with tempfile.TemporaryFile() as replay_file:
            while True:
                chunk = await request.content.read(CHUNK_SIZE)
                if not chunk:
                    break

                replay_file.write(chunk)

            replay_file.seek(0)

            try:
                replay = sc2reader.load_replay(replay_file)
            except Exception as e:
                return Response(body="Invalid Replay\n" + str(e), status=402)

        replay_analysis = await self.loop.run_in_executor(None, analyse_replay, replay)
        serialised_replay_analysis = await self.loop.run_in_executor(None, serialise_replay_analysis, replay_analysis)

        return json_response(data=serialised_replay_analysis)
