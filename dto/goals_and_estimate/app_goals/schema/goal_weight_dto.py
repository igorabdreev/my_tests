import datetime

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto
from dto.goals_and_estimate.app_goals.schema.goal_enum import Period


class GoalWeightResponse(GoalsDto):
    """ Описание веса цели """
    goalId: StrictInt
    uuid: StrictStr
    Q1: StrictFloat
    Q2: StrictFloat
    Q3: StrictFloat
    Q4: StrictFloat
    Y: StrictFloat


class GoalWeightRequest(GoalsDto):
    """ Описание веса цели """
    Q1: StrictFloat
    Q2: StrictFloat
    Q3: StrictFloat
    Q4: StrictFloat
    Y: StrictFloat


class GoalWeightShortResponseV2(GoalWeightRequest):
    """ Сокращенное описание веса целей """
    pass


class GoalWeightsRebalance(GoalWeightRequest):
    """ Ребалансировка целей """
    goalId: StrictInt
    goalWeightId: StrictInt


class GoalWeightsRebalanceResponse(GoalWeightsRebalance):
    """ Цель с ребелансировкой """
    title: StrictStr
    startDate: datetime.date
    endDate: datetime.date
    yearGoal: StrictBool
    periodStart: Period
    periodEnd: Period


class GoalWeightsRebalanceRequest(GoalsDto):
    """ Запрос на ребалансировку цели """
    goalWeightsRebalance: list[GoalWeightsRebalance]


class DistributionStatusWeightResponse(GoalWeightRequest):
    """ Распределение статуса весов """
    pass