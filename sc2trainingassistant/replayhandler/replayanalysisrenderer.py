import json
import webbrowser

import aiohttp

from .replayanalysis import ReplayAnalysis

ADD_REPLAY_ANALYSIS_ENDPOINT = "/add/"
ERROR_ENDPOINT = "/error/"


class ReplayAnalysisRenderer:

    def __init__(self, host: str):
        self.add_replay_analysis_endpoint = host + ADD_REPLAY_ANALYSIS_ENDPOINT
        self.error_endpoint = host + ERROR_ENDPOINT

    async def render_replay_analysis(self, replay_analysis: ReplayAnalysis):
        data = {
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
                        } for performance_metric in player_performance.early_game_performance_metrics]
                } for player_performance in replay_analysis.player_performances]
        }

        async with aiohttp.ClientSession() as session:
            async with session.put(self.add_replay_analysis_endpoint + replay_analysis.hash, json=data) as resp:
                content = await resp.json()

        url = content.get("url", self.error_endpoint)

        webbrowser.open_new_tab(url)




