import datetime
from typing import Any

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto
from dto.goals_and_estimate.app_goals.schema.goal_dto import (
    AssigneeResponse,
    GoalsWithMetaDataParamsResponse,
    PersonResponse
)
from dto.goals_and_estimate.app_goals.schema.goal_enum import FireState, GoalType, Period, Visibility
from dto.goals_and_estimate.app_goals.schema.goal_kr_dto import GoalKRResponse
from dto.goals_and_estimate.app_goals.schema.goal_weight_dto import GoalWeightResponse


class WidgetServiceProfileGoalAndWeightResponseV2(GoalsDto):
    """ Виджет для сервиса профайл """
    id: StrictInt
    title: StrictStr
    description: StrictStr
    reporter: AssigneeResponse
    responsible: AssigneeResponse
    assignees: list[AssigneeResponse]
    endDate: datetime.date
    startDate: datetime.date
    periodStart: Period
    periodEnd: Period
    yearGoal: StrictBool
    visibility: Visibility
    keyResults: GoalKRResponse
    progress: StrictInt
    fireState: FireState
    isRiskState: StrictBool
    riskComment: StrictStr
    isFreeze: StrictBool
    type: GoalType
    weight: GoalWeightResponse


class MetaInfoWidgetResponse(GoalsDto):
    """ Виджет метаданных """
    goalYears: list[StrictInt]
    params: GoalsWithMetaDataParamsResponse


class WidgetServiceProfileFinalResponseV2(GoalsDto):
    """ Виджет для сервиса профайл версия 2 """
    data: list[WidgetServiceProfileGoalAndWeightResponseV2]
    meta: MetaInfoWidgetResponse
    person: PersonResponse
    onPlus: StrictBool


class WidgetGoalShortResponseV3(WidgetServiceProfileGoalAndWeightResponseV2):
    """ Виджет сокращенной информации по целям """
    pass


class WidgetInfoBlockProgressV3(GoalsDto):
    """ Виджет прогресса """
    enableWeight: StrictFloat
    disableWeight: StrictFloat


class WidgetInfoBlockKeyResultV3(GoalsDto):
    """ Виджет ключевого результата """
    countAll: StrictInt
    countCompleted: StrictInt


class WidgetInfoBlockGoalsV3(GoalsDto):
    """ Виджет инфо-блока """
    countAll: StrictInt
    countRisk: StrictInt
    countExpired: StrictInt
    countCompleted: StrictInt
    countInProgress: StrictInt


class WidgetInfoBlockStatisticsResponseV3(GoalsDto):
    """ Виджет для инфо-блока статистики """
    progress: WidgetInfoBlockProgressV3
    keyResults: WidgetInfoBlockKeyResultV3
    goals: WidgetInfoBlockGoalsV3

class VisibleAnalitics(WidgetInfoBlockStatisticsResponseV3):
    """Видимость аналитики"""
    visibleAnalytics: StrictBool

class GoalDashboardBar(WidgetInfoBlockStatisticsResponseV3):
    """ Дашборд на главной """


class WidgetInfoBlockResponseV3(GoalsDto):
    """ Виджет инфо-блока ответа """
    goals: list[WidgetGoalShortResponseV3]
    statistics: WidgetInfoBlockStatisticsResponseV3


class WidgetIntegrationEstimatePesponseV3(WidgetServiceProfileFinalResponseV2):
    """ Виджет для сервиса интеграции """
    data: dict[Any, WidgetInfoBlockResponseV3]