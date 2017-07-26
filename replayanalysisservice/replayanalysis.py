from typing import List, Union


class PerformanceMetric:

    def __init__(
            self,
            metric_name: str,
            metric_description: str,
            achieved_value: Union[int, float, str],
            ideal_value: Union[int, float, str],
            rating: float):

        self.metric_name = metric_name
        self.metric_description = metric_description
        self.achieved_value = achieved_value
        self.ideal_value = ideal_value
        self.rating = rating


class PlayerPerformance:

    def __init__(self, player_name: str, early_game_performance_metrics: List[PerformanceMetric]):
        self.player_name = player_name
        self.early_game_performance_metrics = early_game_performance_metrics


class ReplayAnalysis:

    def __init__(self, hash: str, summary: dict, player_performances: List[PlayerPerformance]):
        self.hash = hash
        self.summary = summary
        self.player_performances = player_performances

