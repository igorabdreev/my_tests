import datetime
from typing import Any, Optional

from pydantic import Field, StrictBool, StrictInt, StrictStr

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto
from dto.goals_and_estimate.app_goals.schema.goal_dto import (
    AssigneeResponse,
    FireStateResponseV2,
    GoalAssigneesResponseV2,
    GoalFileResponse,
    GoalFireResponse,
    MetaInfoBoardResponse,
    MetaInfoPanelResponseV2,
    PermissionGoal,
    PersonResponse,
    ProgressSummary
)
from dto.goals_and_estimate.app_goals.schema.goal_enum import (
    ApproveStatus,
    FireState,
    GoalType,
    Period,
    PermissionStatus,
    Visibility
)
from dto.goals_and_estimate.app_goals.schema.goal_kr_dto import (
    AbstractKeyResultResponseDto,
    GoalKRPeriodResponseV2,
    GoalKRResponse
)
from dto.goals_and_estimate.app_goals.schema.goal_weight_dto import GoalWeightResponse, GoalWeightShortResponseV2


class GoalResponseV2(GoalsDto):
    """ Цель версии 2 """
    id: StrictInt
    title: StrictStr
    description: StrictStr
    assignees: GoalAssigneesResponseV2
    startDate: datetime.date
    endDate: datetime.date
    periodStart: Period
    periodEnd: Period
    yearGoal: StrictBool
    visibility: Visibility
    keyResults: GoalKRPeriodResponseV2
    progress: ProgressSummary
    fire: FireStateResponseV2
    isRiskState: StrictBool
    riskComment: StrictStr
    isFreeze: StrictBool
    type: GoalType
    approveStatus: ApproveStatus
    files: list[GoalFileResponse]


class GoalWithoutReferences(GoalsDto):
    """ Модель описания цели без связей """
    id: Optional[StrictInt] = Field(description='id цели', default=None)
    title: StrictStr = Field(description='Название цели')
    description: StrictStr = Field(description='Описание цели')
    endDate: datetime.date = Field(description='Дата окончания')
    periodStart: Period = Field(description='Периоды цели')
    periodEnd: Period = Field(description='Периоды цели')
    visibility: Visibility = Field(description='Видимая/невидимая')
    progress: StrictInt = Field(description='Прогресс цели')


class GoalWithoutRelatives(GoalWithoutReferences):
    """ Модель описания цели без родственных """
    reporter: AssigneeResponse = Field(description='От кого цель')
    responsible: AssigneeResponse = Field(description='Ответственный')
    assignees: list[AssigneeResponse] = Field(description='Назначенные')
    keyResults: list[AbstractKeyResultResponseDto] = Field(description='Ключевой результат цели')


class GoalFullAloneResponse(GoalWithoutRelatives):
    """ Модель описания цели """
    startDate: datetime.date = Field(description='Дата начала')
    yearGoal: datetime.date = Field(description='Цель на год')
    childrenGoals: list[GoalWithoutRelatives] = Field(description='Дочерние цели')
    parentGoal: Optional[GoalWithoutRelatives] = Field(description='Вышестоящая цель')
    fireState: FireState = Field(description='')
    isRiskState: StrictBool = Field(description='Цель под риском')
    riskComment: StrictStr = Field(description='Комментарий цели под риском')
    isFreeze: StrictBool = Field(description='Заморозка цели')
    type: GoalType = Field(description='Тип цели')
    files: Optional[list[GoalFireResponse]] = Field(description='Файлы цели')
    weight: GoalWeightResponse = Field(description='Вес цели')
    keyResults: GoalKRResponse = Field(description='Ключевой результат цели')


class GoalFullResponse(GoalFullAloneResponse):
    """ Развернутое описание цели """
    features: dict


class GoalAcceptanceResponse(GoalsDto):
    """ Подтверждение назначения цели """
    goal: GoalWithoutReferences
    assignee: AssigneeResponse
    requestAuthor: PersonResponse


class KitPersonInviteResponse(GoalsDto):
    """ Обертка над подтверждениями назначения цели """
    data: list[GoalAcceptanceResponse]


class GoalFullBaseResponse(GoalsDto):
    """ Полная информация о цели """
    id: Optional[StrictInt]
    title: StrictStr
    description: StrictStr
    reporter: AssigneeResponse
    responsible: AssigneeResponse
    assignees: list[AssigneeResponse]
    startDate: datetime.date
    endDate: datetime.date
    periodStart: Period
    periodEnd: Period
    yearGoal: StrictBool
    visibility: Visibility
    keyResults: GoalKRResponse
    progress: StrictInt
    fireState: FireState
    isRiskState: StrictBool
    riskComment: StrictStr
    isFromManager: StrictBool
    isFreeze: StrictBool
    type: GoalType
    files: list[GoalFileResponse]
    weight: GoalWeightResponse
    features: dict[Any, StrictBool]


class GoalsWithMetaDataResponse(GoalsDto):
    """ Цели с метаданными """
    data: list[GoalFullBaseResponse]
    meta: MetaInfoBoardResponse
    person: PersonResponse


class GoalInfoShortResponseV2(GoalsDto):
    """ Сокращенная информация о цели версия 2 """
    goal: GoalResponseV2
    weight: GoalWeightShortResponseV2
    permissionGoal: PermissionGoal


class GoalInfoResponseV2(GoalsDto):
    """ Данные о цели версия 2 """
    goal: GoalResponseV2
    weight: GoalWeightShortResponseV2
    features: dict
    permissionGoal: PermissionGoal


class GoalPanelResponseV2(GoalsDto):
    """ Данные по цели для панели """
    data: list[GoalInfoResponseV2]
    meta: MetaInfoPanelResponseV2
    person: PersonResponse


class KRStatisticsInGoalNodeAreaResponse(GoalsDto):
    """ Статистика ключевых результатов """
    countAllKR: StrictInt
    countKRByPeriod: StrictInt


class GoalForTreePanelResponse(GoalsDto):
    """ Цель для дерева целей """
    id: StrictInt
    title: StrictStr
    description: StrictStr
    startDate: datetime.date
    endDate: datetime.date
    periodStart: Period
    periodEnd: Period
    yearGoal: StrictBool
    visibility: Visibility
    keyResults: KRStatisticsInGoalNodeAreaResponse
    isRiskState: StrictBool
    isFreeze: StrictBool
    type: GoalType
    isFutureCycle: StrictBool


class GoalsForTreePanelResponse(GoalsDto):
    """ Список целей для дерева целей """
    goals: list[GoalForTreePanelResponse]


class SocialInteractionPeopleResponse(GoalsDto):
    """ Запрос на новую связь цели """
    persons: list[PersonResponse]


class PermissionAreaResponse(GoalsDto):
    """ Разрешение для области """
    status: PermissionStatus


class GoalNodeAreaResponse(GoalsDto):
    """ Узел области целей """
    isPresent: StrictBool
    isVisible: StrictBool


class LinkAreaResponse(GoalsDto):
    """ Область связей """
    parentGoal: GoalNodeAreaResponse
    goal: GoalNodeAreaResponse
    childrenGoals: list[GoalNodeAreaResponse]

