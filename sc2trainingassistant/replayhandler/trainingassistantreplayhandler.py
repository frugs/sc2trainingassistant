from typing import Callable

from sc2reader.resources import Replay
from sc2replaynotifier import ReplayHandler

from .replayanalysis import ReplayAnalysis


def _is_non_empty_analysis(replay_analysis: ReplayAnalysis):
    all_metrics = []

    for player_performance in replay_analysis.player_performances:
        all_metrics.append(player_performance.early_game_performance_metrics)

    return bool(all_metrics)


class TrainingAssistantReplayHandler(ReplayHandler):

    def __init__(
            self,
            replay_analyser: Callable[[Replay], ReplayAnalysis],
            replay_analysis_renderer):
        self.analyse_replay = replay_analyser
        self.render_replay_analysis = replay_analysis_renderer

    async def handle_replay(self, replay: Replay):
        replay_analysis = self.analyse_replay(replay)

        if not _is_non_empty_analysis(replay_analysis):
            await self.render_replay_analysis(replay_analysis)