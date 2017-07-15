from sc2replaynotifier import ReplayHandler

from .trainingassistantreplayhandler import TrainingAssistantReplayHandler as _TrainingAssistantReplayHandler
from .replayanalyser import analyse_replay as _analyse_replay
from .replayanalysisrenderer import ReplayAnalysisRenderer as _ReplayAnalysisRenderer


def create_training_assistant_replay_handler(host: str) -> ReplayHandler:
    renderer = _ReplayAnalysisRenderer(host)
    return _TrainingAssistantReplayHandler(_analyse_replay, renderer.render_replay_analysis)