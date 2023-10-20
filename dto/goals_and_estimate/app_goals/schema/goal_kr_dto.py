import datetime
from typing import Optional

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto
from dto.goals_and_estimate.app_goals.schema.goal_dto import PersonResponse
from dto.goals_and_estimate.app_goals.schema.goal_enum import (
    CatalogItemType,
    FireState,
    KeyResultMetricStatus,
    KeyResultStatus,
    KeyResultType
)


class PermissionKR(GoalsDto):
    """ Разрешение на редактирование ключевого результата """
    canEditKR: StrictBool


class AbstractKeyResultResponseDto(GoalsDto):
    """ Модель ответа базового ключевого результата """
    id: StrictInt
    title: StrictStr
    description: StrictStr
    createDate: Optional[StrictStr] = None
    progress: StrictInt
    type: KeyResultType
    reporter: PersonResponse
    startDate: datetime.date
    endDate: datetime.date
    fireState: FireState
    isFreeze: StrictBool


class AbstractKeyResultResponseV2(AbstractKeyResultResponseDto):
    """ Базовый ключевой результат версии 2 """
    permissionKR: PermissionKR


class GoalKRResponse(GoalsDto):
    """ Модель ответа ключевого результата цели """
    countAllKR: StrictInt
    countKRByPeriod: StrictInt
    keyResultInProgress: list[AbstractKeyResultResponseDto]
    keyResultCompleted: list[AbstractKeyResultResponseDto]


class GoalKRPeriodResponseV2(GoalsDto):
    """ Период ключевого результата """
    countAllKR: StrictInt
    countKRByPeriod: StrictInt
    keyResults: list[AbstractKeyResultResponseV2]


class AbstractKRRequest(GoalsDto):
    """ Модель запроса базового ключевого результата """
    type: KeyResultType
    endDate: datetime.date
    status: KeyResultStatus


class KeyResultBinaryRequest(AbstractKRRequest):
    """ Модель бинарного ключевого результата """
    title: StrictStr
    description: StrictStr


class KeyResultMetricRequest(KeyResultBinaryRequest):
    """ Модель метрического ключевого результата """
    status: KeyResultMetricStatus
    startProgress: StrictFloat
    targetProgress: StrictFloat
    metric: StrictStr


class KeyResultEvolutionRequest(AbstractKRRequest):
    """ Модель ключевого результата развития """
    materialId: StrictStr


class KeyResultBinaryEditProgressRequest(GoalsDto):
    """ Модель редактирования бинарного ключевого результата """
    status: KeyResultStatus


class KeyResultMetricEditProgressRequest(GoalsDto):
    """ Модель редактирования метрического ключевого результата """
    currentProgress: StrictFloat


class KeyResultEvolutionResponse(GoalsDto):
    """ Модель ответа ключевого результата развития """
    id: StrictInt
    title: StrictStr
    description: StrictStr
    reporter: PersonResponse
    type: KeyResultType
    materialId: StrictStr
    status: KeyResultStatus
    duration: StrictInt
    durationStr: StrictStr
    materialType: CatalogItemType
    progress: StrictInt
    startDate: datetime.date
    endDate: datetime.date
    fireState: FireState
    isFreeze: StrictBool