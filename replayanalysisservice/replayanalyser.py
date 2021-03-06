from math import log
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

    thirty_five_worker_timing = techlabreactor.worker_count_timing(35, player, replay)
    if thirty_five_worker_timing > 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken to build 35 workers",
            "Time taken since the start of the game to build 35 workers (equivalent to optimal saturation of 2 mineral "
            "lines and a single gas geyser).",
            _seconds_to_time_string(thirty_five_worker_timing),
            _seconds_to_time_string(235),
            5 - (4 * thirty_five_worker_timing / 235)))

    two_base_saturation_timing = techlabreactor.two_base_saturation_timing(player, replay)
    if two_base_saturation_timing > 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken to build 44 workers",
            "Time taken since the start of the game to build 44 workers (equivalent to optimal saturation of 2 bases).",
            _seconds_to_time_string(two_base_saturation_timing),
            _seconds_to_time_string(280),
            5 - (4 * two_base_saturation_timing / 280)))

    three_base_saturation_timing = techlabreactor.three_base_saturation_timing(player, replay)
    if three_base_saturation_timing > 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken to build 66 workers",
            "Time taken since the start of the game to build 66 workers (equivalent to optimal saturation of 3 bases).",
            _seconds_to_time_string(three_base_saturation_timing),
            _seconds_to_time_string(390),
            5 - (4 * three_base_saturation_timing / 390)))

    return performance_metrics


def _worker_supply_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    if replay.length.seconds < 270:
        return []

    performance_metrics = []

    worker_supply = techlabreactor.worker_supply_at(270, player, replay)
    if worker_supply > 0:
        performance_metrics.append(PerformanceMetric(
            "Worker supply at 4:30",
            "The amount of supply used by workers (active as well as currently in production) at the 4:30 mark.",
            str(worker_supply),
            str(42),
            ((worker_supply - 42) / 14) + 1))

    return performance_metrics


def _upgrade_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    first_upgrade_started_timing = techlabreactor.first_upgrade_started_timing(player, replay)

    if first_upgrade_started_timing > 0:
        return [
            PerformanceMetric(
                "Time taken before first upgrade",
                "Time elapsed from the start of the game before starting the first unit upgrade. A unit "
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

    fourth_expansion_timing = techlabreactor.fourth_expansion_timing(player, replay)
    if fourth_expansion_timing >= 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken before securing fourth",
            "Time elapsed from the start of the game before commencing construction of an expansion at the fourth "
            "expansion position.",
            _seconds_to_time_string(fourth_expansion_timing),
            _seconds_to_time_string(390),
            (-1 * fourth_expansion_timing + 390 + 52) / 52))

    return performance_metrics


def _creep_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    performance_metrics = []

    creep_tumours = techlabreactor.creep_tumours_built_before_second(420, player, replay)
    if creep_tumours >= 0:
        target = 20
        rating = 0 if creep_tumours <= 10 else (log(creep_tumours - 10) / 3) + 0.68

        performance_metrics.append(PerformanceMetric(
            "Number of Creep Tumours built",
            "The number of Creep Tumours that were started during this game phase.",
            str(creep_tumours),
            str(target),
            rating))

    return performance_metrics


def _tier_upgrade_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    if not player.play_race == "Zerg":
        return []

    performance_metrics = []

    lair_timing = techlabreactor.lair_started_timing(player, replay)
    if lair_timing >= 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken before starting Lair",
            "Time elapsed from the start of the game before commencing upgrading of a Hatchery into a Lair.",
            _seconds_to_time_string(lair_timing),
            _seconds_to_time_string(360),
            (-1 * lair_timing + 360 + 110) / 110))

    return performance_metrics


def _gas_income_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    if not player.play_race == "Zerg":
        return []

    performance_metrics = []

    timing = techlabreactor.second_gas_timing(player, replay)
    if timing >= 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken before securing 2nd gas geyser",
            "Time elapsed from the start of the game before commencing construction of the second Extractor, "
            "Assimilator, or Refinery on a Vespene Geyser.",
            _seconds_to_time_string(timing),
            _seconds_to_time_string(300),
            (-1 * timing + 300 + 52) / 52))

    return performance_metrics


def _safety_spore_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    if not player.play_race == "Zerg":
        return []

    performance_metrics = []

    timing = techlabreactor.safety_spores_timing(player, replay)
    if timing >= 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken before starting safety Spore Crawlers",
            "Time elapsed from the start of the game before commencing construction of Spore Crawlers for safety "
            "against cloaked, burrowed, or flying units.",
            _seconds_to_time_string(timing),
            _seconds_to_time_string(270),
            (-1 * timing + 270 + 52) / 52))

    return performance_metrics


def _overlord_speed_performance(player: Player, replay: Replay) -> List[PerformanceMetric]:
    if not player.play_race == "Zerg":
        return []

    performance_metrics = []

    timing = techlabreactor.overlord_speed_research_started_timing(player, replay)
    if timing >= 0:
        performance_metrics.append(PerformanceMetric(
            "Time taken before researching Overlord speed",
            "Time elapsed from the start of the game before commencing research of the Pneumatized Carapace research.",
            _seconds_to_time_string(timing),
            _seconds_to_time_string(380),
            (-1 * timing + 380 + 52) / 52))

    return performance_metrics


def _get_early_game_performance_metrics_for_player(player: Player, replay: Replay) -> List[PerformanceMetric]:
    performance_metrics = []

    performance_metrics.extend(_inject_performance(player, replay))
    performance_metrics.extend(_worker_saturation_performance(player, replay))
    performance_metrics.extend(_worker_supply_performance(player, replay))
    performance_metrics.extend(_upgrade_performance(player, replay))
    performance_metrics.extend(_expansion_performance(player, replay))
    performance_metrics.extend(_creep_performance(player, replay))
    performance_metrics.extend(_tier_upgrade_performance(player, replay))
    performance_metrics.extend(_gas_income_performance(player, replay))
    performance_metrics.extend(_safety_spore_performance(player, replay))
    performance_metrics.extend(_overlord_speed_performance(player, replay))

    return performance_metrics


def _analyse_player_performance(player: Player, replay: Replay) -> PlayerPerformance:
    early_game_performance_metrics = _get_early_game_performance_metrics_for_player(player, replay)

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

