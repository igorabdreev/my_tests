import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto
from dto.goals_and_estimate.app_goals.schema.goal_enum import (
    CatalogItemType,
    FireState,
    FreezeStatus,
    GoalEventType,
    InitiatorType,
    KeyResultStatus,
    Layer, Period,
    ReporterStatus,
    Status
)


class AssigneeResponse(GoalsDto):
    """Модель описания назначенного"""
    uuid: UUID = Field(description='id пользователя')
    firstName: StrictStr = Field(description='имя пользователя')
    lastName: StrictStr = Field(description='фамилия пользователя')
    middleName: StrictStr = Field(description='отчество пользователя')
    fullName: StrictStr = Field(description='ФИО пользователя')
    positionShortName: StrictStr = Field(description='короткое описание должности')
    positionFullName: StrictStr = Field(description='полное описание должности')
    photoUrl: StrictStr = Field(description='URL на фото')
    gender: StrictStr = Field(description='пол')
    status: Status = Field(description='статус')
    comment: StrictStr = Field(description='комментарий')




class GoalAssigneesResponseV2(GoalsDto):
    """ Модель описания назначенного версии 2 """
    author: AssigneeResponse
    responsible: AssigneeResponse
    accepted: list[AssigneeResponse]
    requested: list[AssigneeResponse]
    rejected: list[AssigneeResponse]


class GoalsWithMetaDataParamsResponse(GoalsDto):
    """ Метаданные целей """
    countInvisibleGoals: StrictInt


class MetaInfoBoardResponse(GoalsDto):
    """ Данные о целях для таблицы """
    goalYears: list[StrictInt]
    features: dict
    params: GoalsWithMetaDataParamsResponse


class MetaInfoPanelResponseV2(MetaInfoBoardResponse):
    """ Данные о целях для панели """
    pass


class PersonResponse(GoalsDto):
    """ Модель описания персоны """
    uuid: UUID
    firstName: StrictStr
    lastName: StrictStr
    middleName: StrictStr
    fullName: StrictStr
    positionShortName: StrictStr
    positionFullName: StrictStr
    photoUrl: StrictStr
    gender: StrictStr


class GoalFireResponse(GoalsDto):
    """ Установка состояния """
    id: StrictInt
    name: StrictStr
    createDate: datetime.date
    author: PersonResponse
    isVisible: StrictBool
    availableStatus: StrictStr


class StatisticsProgressResponse(GoalsDto):
    """ Данные о прогрессе статистики """
    progress: StrictFloat


class PermissionGoal(GoalsDto):
    """ Разрешения на редактирование цели """
    canEditGoal: StrictBool
    canEditWeight: StrictBool
    canAcceptRequest: StrictBool


class GoalFileResponse(GoalsDto):
    """ Данные о файле """
    id: StrictInt
    name: StrictStr
    createDate: datetime.date
    author: PersonResponse
    isVisible: StrictBool
    availableStatus: StrictStr


class FireStateResponseV2(GoalsDto):
    """ Данные об установке состояния """
    state: FireState
    countFireCalendarKR: StrictInt
    countFireKR: StrictInt


class ProgressData(GoalsDto):
    """ Данные о прогрессе """
    progressWithDisableWeight: StrictFloat
    progressWithWeight: StrictFloat


class ProgressSummary(GoalsDto):
    """ Сведения о прогрессе """
    progress: StrictInt
    q1: ProgressData
    q2: ProgressData
    q3: ProgressData
    q4: ProgressData
    qYear: Optional[ProgressData] = None
    qyear: ProgressData


class GoalEventResponse(GoalsDto):
    """ События цели """
    eventType: GoalEventType
    reporter: PersonResponse
    reporterStatus: ReporterStatus
    goalId: StrictInt
    goalName: StrictStr
    createdDate: datetime.datetime


class CatalogItemResponse(GoalsDto):
    """ Элемент каталога """
    id: StrictStr
    title: StrictStr
    description: StrictStr
    type: CatalogItemType
    durationStr: StrictStr
    duration: StrictInt
    images: dict
    viewCount: StrictInt
    avgRating: StrictFloat


class CatalogSearchItem(CatalogItemResponse):
    """ Поиск каталога """
    pass


class InitializeProcessRequest(GoalsDto):
    """ Запрос инициализации процесса """
    mainApprover: UUID
    priorApprover: Optional[UUID] = None
    comment: Optional[StrictStr] = None


class CreateAssigneeRequest(GoalsDto):
    """ Выбрать назначенного """
    assignees: list[UUID]


class FavoritePersonWithOptionsResponse(GoalsDto):
    """ Запрос на избранных с опциями """
    person: PersonResponse
    onPlus: StrictBool


class FreezeRequest(GoalsDto):
    """ Заморозка целей """
    year: StrictInt
    periods: list[Period]
    personIds: list[UUID]
    departmentIds: list[UUID]
    status: FreezeStatus


class KeyResultEvolutionEditProgressRequest(GoalsDto):
    """ Редактирование ключевого результата развития """
    status: KeyResultStatus


class CatalogClientItemImageObjectResponse(GoalsDto):
    """ Каталог """
    resource: StrictStr
    url: StrictStr


class CatalogMaterialForGoal(GoalsDto):
    """ Материалы из каталога для целей """
    id: StrictStr
    title: StrictStr
    description: StrictStr
    type: CatalogItemType
    durationStr: StrictStr
    duration: StrictInt
    images: dict[Any, CatalogClientItemImageObjectResponse]
    viewCount: StrictInt
    avgRating: StrictFloat


class CatalogMaterialForGoalResponseV1(GoalsDto):
    """ Материалы из каталога для целей версии 1 """
    isConsistInGoal: StrictBool
    item: CatalogMaterialForGoal


class CatalogMaterialsSearchResultForGoalResponseV1(GoalsDto):
    """ Поиск материалов в каталоге """
    isSuccess: StrictBool
    materials: list[CatalogMaterialForGoalResponseV1]


class GoalLink(GoalsDto):
    """ Линк цели """
    parentGoalId: StrictInt
    childGoalId: StrictInt
    initiatorPersonId: StrictStr
    targetLinkPersonId: StrictStr
    initiatorType: InitiatorType
    isDeleted: StrictBool
    id: Optional[StrictInt] = None


class OrgTeamShortResponse(GoalsDto):
    """ Запрос на оргединицу """
    id: UUID
    name: StrictStr
    layer: Layer