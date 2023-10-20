from enum import auto

from dto.goals_and_estimate.app_goals.schema.generic import AutoStrEnum


class Status(AutoStrEnum):
    """ Перечисление видов статусов"""
    REQUESTED = auto()
    REJECTED = auto()
    RESPONSIBLE = auto()
    ACCEPTED = auto()
    AUTHOR = auto()


class KeyResultStatus(AutoStrEnum):
    CREATED = auto()
    DONE = auto()


class FreezeStatus(AutoStrEnum):
    ON = auto()
    OFF = auto()


class KeyResultMetricStatus(AutoStrEnum):
    CREATED = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    OVERFULFILLED = auto()
    DELETED = auto()


class ApproveStatus(AutoStrEnum):
    NOT_AGREED = auto()
    REVIEW = auto()
    APPROVE = auto()
    REJECTED = auto()
    INVALIDATED = auto()


class KeyResultType(AutoStrEnum):
    """ Тип ключевого результата """
    BINARY = auto()
    METRIC = auto()
    EVOLUTION = auto()


class Period(AutoStrEnum):
    """ Перечисление видов периодов у цели"""
    Q1 = auto()
    Q2 = auto()
    Q3 = auto()
    Q4 = auto()
    Y = auto()
    ALL = auto()


class Visibility(AutoStrEnum):
    """ Перечисление типов видимости цели"""
    VISIBLE = auto()
    INVISIBLE = auto()


class FireState(AutoStrEnum):
    """ Установка состояния """
    FIRE = auto()
    FIRE_CALENDAR = auto()
    NOT_FIRE = auto()


class GoalType(AutoStrEnum):
    """" Типы видов цели """
    STANDARD = auto()
    EVOLUTION = auto()
    TEAM = auto()
    KPI = auto()


class ReporterStatus(AutoStrEnum):
    """ Статус от кого цель """
    YOU = auto()
    MANAGER = auto()
    COLLEAGUE = auto()
    ADMIN = auto()


class GoalEventType(AutoStrEnum):
    """ Тип операции с целью """
    CREATE_GOAL = auto()
    ADD_DESCRIPTION_GOAL = auto()
    CHANGE_TITLE_GOAL = auto()
    CHANGE_DESCRIPTION_GOAL = auto()
    CHANGE_DATE_GOAL = auto()
    COMPLETE_GOAL = auto()
    DELETE_GOAL = auto()
    CHANGE_KR_EXPIRY_DATE = auto()
    CREATE_KR_BINARY = auto()
    ADD_DESCRIPTION_KR_BINARY = auto()
    CHANGE_TITLE_KR_BINARY = auto()
    CHANGE_DESCRIPTION_KR_BINARY = auto()
    DELETE_KR_BINARY = auto()
    COMPLETE_KR_BINARY = auto()
    RETURN_TO_WORK_KR_BINARY = auto()
    CREATE_KR_METRIC = auto()
    ADD_DESCRIPTION_KR_METRIC = auto()
    CHANGE_TITLE_KR_METRIC = auto()
    CHANGE_DESCRIPTION_KR_METRIC = auto()
    DELETE_KR_METRIC = auto()
    INCREASE_METRIC_KR_METRIC = auto()
    DECREASE_METRIC_KR_METRIC = auto()
    COMPLETE_METRIC_KR_METRIC = auto()
    CREATE_KR_EVOLUTION = auto()
    DELETE_KR_EVOLUTION = auto()
    COMPLETE_KR_EVOLUTION = auto()
    RETURN_TO_WORK_KR_EVOLUTION = auto()
    ACCEPT_GOAL_ASSIGNEE = auto()
    LEAVE_GOAL_ASSIGNEE = auto()
    DELETE_ASSIGNEE = auto()
    APPROVE_PROCESS_BY_MANAGER = auto()
    APPROVE_PROCESS = auto()
    REJECTED_PROCESS = auto()
    INVALIDATED_PROCESS = auto()
    ADD_FILE = auto()
    DELETE_FILE = auto()


class CatalogItemType(AutoStrEnum):
    """ Тип единицы каталога """
    BOOK = auto()
    AUDIO = auto()
    PAPER = auto()
    VIDEO = auto()
    UGC = auto()
    MATERIAL = auto()
    ONLINE = auto()
    ONSITE = auto()
    PROGRAM = auto()
    PLAYLIST = auto()
    PLB_track = auto()
    PLB_compilation = auto()
    SURVEY = auto()


class PermissionStatus(AutoStrEnum):
    """ Статус разрешений """
    CREATE_LINK = auto()
    ONLY_SEE = auto()
    FORBIDDEN = auto()


class InitiatorType(AutoStrEnum):
    """ Дочерняя или родительская цель """
    PARENT = auto()
    CHILD = auto()


class Layer(AutoStrEnum):
    """ Слой """
    FOS = auto()
    OSHS = auto()
    SBERGILE = auto()
    CUSTOM = auto()
    OSHS_DEPARTMENT_ONLY = auto()


class ViewMode(AutoStrEnum):
    """ Вид """
    STANDARD = auto()
    ONLY_AUTHOR = auto()
    ONLY_RESPONSIBLE = auto()
    RESPONSIBLE = auto()