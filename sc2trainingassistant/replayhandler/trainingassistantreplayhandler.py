from typing import Callable

from sc2reader.resources import Replay
from sc2replaynotifier import ReplayHandler

from .replayanalysis import ReplayAnalysis


class TrainingAssistantReplayHandler(ReplayHandler):

    def __init__(
            self,
            replay_analyser: Callable[[Replay], ReplayAnalysis],
            replay_analysis_renderer):
        self.analyse_replay = replay_analyser
        self.render_replay_analysis = replay_analysis_renderer

    async def handle_replay(self, replay: Replay):
        replay_analysis = self.analyse_replay(replay)
        await self.render_replay_analysis(replay_analysis)