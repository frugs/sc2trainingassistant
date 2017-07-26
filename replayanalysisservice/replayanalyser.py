from typing import List

import techlabreactor
from sc2reader.objects import Player
from sc2reader.resources import Replay

from .replayanalysis import ReplayAnalysis, PlayerPerformance, PerformanceMetric


def _seconds_to_time_string(seconds) -> str:
    m, s = divmod(seconds, 60)
    return "{}:{:02d}".format(m, s)


def _inject_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    if not player.play_race == "Zerg":
        return []

    achieved_value = techlabreactor.get_inject_pops_for_player(player, replay)

    if achieved_value <= 0:
        return []

    ideal_value = 17
    rating = achieved_value / ideal_value

    return [PerformanceMetric(
        "'Spawn Larvae' ability completed count",
        "The number of times the Queen's 'Spawn Larvae' ability completed during this game phase.",
        achieved_value,
        ideal_value,
        rating)]


def _worker_saturation_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    performance_metrics = []

    two_base_saturation_timing = techlabreactor.two_base_saturation_timing(player, replay)
    if two_base_saturation_timing > 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken to saturate two bases (44 workers)",
            "Time taken since the start of the game to build 44 workers (equivalent to optimal saturation of 2 bases).",
            _seconds_to_time_string(two_base_saturation_timing),
            _seconds_to_time_string(280),
            5 - (4 * two_base_saturation_timing / 280)))

    three_base_saturation_timing = techlabreactor.three_base_saturation_timing(player, replay)
    if three_base_saturation_timing > 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken to saturate two bases (66 workers)",
            "Time taken since the start of the game to build 66 workers (equivalent to optimal saturation of 3 bases).",
            _seconds_to_time_string(three_base_saturation_timing),
            _seconds_to_time_string(390),
            5 - (4 * three_base_saturation_timing / 390)))

    return performance_metrics


def _upgrade_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    first_upgrade_started_timing = techlabreactor.first_upgrade_started_timing(player, replay)

    if first_upgrade_started_timing > 0:
        return [
            PerformanceMetric(
                "Time taken before first numerical upgrade",
                "Time elapsed from the start of the game before starting the first numerical upgrade. A numerical "
                "upgrade is an upgrade which effects the attack or defense values of multiple types of units, "
                "researched at an Evolution Chamber, Forge, or Engineering Bay.",
                _seconds_to_time_string(first_upgrade_started_timing),
                _seconds_to_time_string(330),
                5 - (4 * first_upgrade_started_timing / 330))
        ]
    else:
        return []


def _expansion_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    performance_metrics = []

    natural_expansion_timing = techlabreactor.natural_expansion_timing(player, replay)
    if natural_expansion_timing >= 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken before securing natural",
            "Time elapsed from the start of the game before commencing construction of an expansion at the natural "
            "expansion position.",
            _seconds_to_time_string(natural_expansion_timing),
            _seconds_to_time_string(56),
            2.5 - (1.5 * natural_expansion_timing / 56)))

    third_expansion_timing = techlabreactor.third_expansion_timing(player, replay)
    if third_expansion_timing >= 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken before securing third",
            "Time elapsed from the start of the game before commencing construction of an expansion at the third "
            "expansion position.",
            _seconds_to_time_string(third_expansion_timing),
            _seconds_to_time_string(210),
            2.5 - (1.5 * third_expansion_timing / 210)))

    return performance_metrics


def _get_early_game_performance_metrics_for_player(player: Player, replay: Replay) -> List[PerformanceMetric]:
    performance_metrics = []

    performance_metrics.extend(_inject_performance(player, replay))
    performance_metrics.extend(_worker_saturation_performance(player, replay))
    performance_metrics.extend(_upgrade_performance(player, replay))
    performance_metrics.extend(_expansion_performance(player, replay))

    return performance_metrics


def _analyse_player_performance(player: Player, replay: Replay) -> PlayerPerformance:
    if replay.length.seconds >= 7 * 60:
        early_game_performance_metrics = _get_early_game_performance_metrics_for_player(player, replay)
    else:
        early_game_performance_metrics = []

    return PlayerPerformance(
        "{} ({})".format(player.name, player.play_race),
        early_game_performance_metrics)


def analyse_replay(replay: Replay) -> ReplayAnalysis:

    replay_hash = replay.filehash
    replay_summary = techlabreactor.generate_replay_summary(replay)
    player_performances = [
        _analyse_player_performance(player, replay)
        for player
        in replay.players
        if player.play_race == "Zerg"]

    return ReplayAnalysis(replay_hash, replay_summary, player_performances)

