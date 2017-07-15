from typing import List

import techlabreactor
from sc2reader.objects import Player
from sc2reader.resources import Replay

from .replayanalysis import ReplayAnalysis, PlayerPerformance, PerformanceMetric


def _inject_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    achieved_value = techlabreactor.get_inject_pops_for_player(player, replay)
    ideal_value = 17
    rating = achieved_value / ideal_value

    return PerformanceMetric(
        "'Spawn Larvae' ability completed count",
        "The number of times the Queen's 'Spawn Larvae' ability completed during this game phase.",
        achieved_value,
        ideal_value,
        rating)


def _get_early_game_performance_metrics_for_player(player: Player, replay: Replay) -> List[PerformanceMetric]:
    return [
        _inject_performance(player, replay)
    ]


def _analyse_player_performance(player: Player, replay: Replay) -> PlayerPerformance:
    if replay.length >= 7 * 60:
        early_game_performance_metrics = _get_early_game_performance_metrics_for_player(player, replay)
    else:
        early_game_performance_metrics = []

    return PlayerPerformance(
        "{} ({})".format(player.name, player.play_race),
        early_game_performance_metrics)


def analyse_replay(replay: Replay) -> ReplayAnalysis:

    replay_hash = replay.filehash
    player_performances = [
        _analyse_player_performance(player, replay)
        for player
        in replay.players
        if player.play_race == "Zerg"]

    return ReplayAnalysis(replay_hash, player_performances)

