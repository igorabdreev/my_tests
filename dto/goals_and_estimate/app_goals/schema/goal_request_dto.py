import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import StrictBool, StrictInt, StrictStr

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto
from dto.goals_and_estimate.app_goals.schema.goal_enum import GoalType, InitiatorType, Period, Visibility
from dto.goals_and_estimate.app_goals.schema.goal_kr_dto import (
    KeyResultBinaryRequest,
    KeyResultEvolutionRequest,
    KeyResultMetricRequest
)
from dto.goals_and_estimate.app_goals.schema.goal_weight_dto import GoalWeightRequest


class CreateGoalForOtherRequestV1(GoalsDto):
    """ Создать цель для другого """
    title: StrictStr
    description: StrictStr
    startDate: datetime.date
    endDate: datetime.date
    periodStart: Period
    periodEnd: Period
    yearGoal: StrictBool
    visibility: Visibility
    keyResults: list[Union[KeyResultBinaryRequest, KeyResultEvolutionRequest, KeyResultMetricRequest]]
    fileIds: list[StrictInt]


class CreateGoalRequestV1(GoalsDto):
    """ Описание создания цели """
    reporterId: UUID
    title: StrictStr
    description: StrictStr
    assignees: list[StrictStr]
    startDate: datetime.date
    endDate: datetime.date
    periodStart: Period
    periodEnd: Period
    visibility: Visibility
    keyResults: list[Union[KeyResultBinaryRequest, KeyResultEvolutionRequest, KeyResultMetricRequest]]
    weight: Optional[GoalWeightRequest] = None
    yearGoal: StrictBool
    type: GoalType
    fileIds: Optional[list[StrictInt]] = None


class AbstractGoalEditRequest(GoalsDto):
    """ Базовая модель редактирования цели """
    title: StrictStr
    description: StrictStr
    visibility: Visibility
    isRiskState: StrictBool
    riskComment: StrictStr


class GoalEditRequestV1(AbstractGoalEditRequest):
    """ Базовая модель редактирования цели версии 1 """
    weight: GoalWeightRequest


class GoalEditRequestV2(AbstractGoalEditRequest):
    """ Модель редактирования цели версии 2 """
    startDate: datetime.date
    endDate: datetime.date
    periodStart: Period
    periodEnd: Period
    isYearGoal: StrictBool


class NewGoalLinkRequest(GoalsDto):
    """ Запрос на новую связь цели """
    parentGoalId: StrictInt
    childGoalId: StrictInt
    initiatorType: InitiatorType
    targetLinkPersonId: UUID


class DeleteGoalLinkRequest(GoalsDto):
    """ Запрос на удаление связи цели """
    parentGoalId: StrictInt
    childGoalId: StrictInt
    initiatorType: InitiatorType