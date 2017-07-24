from typing import Callable

from sc2reader.resources import Replay
from sc2replaynotifier import ReplayHandler


def _is_empty_analysis(replay_analysis: dict) -> bool:
    if not replay_analysis.items():
        return True

    all_metrics = []

    for player_performance in replay_analysis.get("players", []):
        all_metrics.extend(player_performance.get("earlyGamePerformanceMetrics", []))

    return not bool(all_metrics)


class TrainingAssistantReplayHandler(ReplayHandler):

    def __init__(
            self,
            replay_analyser,
            replay_analysis_uploader,
            url_opener: Callable[[str], None],
            logger: Callable[[str], None]):
        self.analyse_replay = replay_analyser
        self.upload_replay_analysis = replay_analysis_uploader
        self.open_url = url_opener
        self.log = logger

    async def handle_replay(self, replay: Replay):
        self.log("New replay detected, analysing...")

        replay_analysis = await self.analyse_replay(replay)

        self.log("Replay analysis complete.")

        if _is_empty_analysis(replay_analysis):
            self.log("Analysis results were empty.")
            return

        self.log("Uploading replay analysis...")

        result = await self.upload_replay_analysis(replay_analysis)
        url = result.get("url", "")

        if not url:
            self.log("Replay analysis upload failed.")

        self.log("Replay analysis upload complete, opening analysis.")

        self.open_url(url)
