from pydantic import StrictInt, StrictStr

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto


class StatisticsBoardWidgetResponseV2(GoalsDto):
    """ Виджет статистики """
    countPeopleAll: StrictInt
    countPeopleUseGoals: StrictInt
    countGoalsAll: StrictInt
    countGoalsCompleted: StrictInt
    countGoalsRisk: StrictInt
    countGoalsFire: StrictInt


class StatisticsBoardTableRowPersonResponseV2(GoalsDto):
    """ Ячейка персона для ряда таблицы статистики """
    uuid: StrictStr
    firstName: StrictStr
    lastName: StrictStr
    middleName: StrictStr
    positionFullName: StrictStr
    photoUrl: StrictStr
    fullName: StrictStr


class StatisticsBoardTableRowProgressResponseV2(GoalsDto):
    """ Ячейка прогресса для ряда таблицы статистики """
    progressWithDisableWeight: StrictInt
    progressWithEnableWeight: StrictInt


class StatisticsBoardTableRowGoalsResponseV2(GoalsDto):
    """ Ячейка цели для ряда таблицы статистики """
    countGoalsAll: StrictInt
    countGoalsCompleted: StrictInt
    countGoalsRisk: StrictInt
    countGoalsFire: StrictInt


class StatisticsBoardTableRowResponseV2(GoalsDto):
    """ Ряд таблицы статистики """
    person: StatisticsBoardTableRowPersonResponseV2
    progress: StatisticsBoardTableRowProgressResponseV2
    goals: StatisticsBoardTableRowGoalsResponseV2


class StatisticsBoardTableResponseV2(GoalsDto):
    """ Таблица статистики """
    data: list[StatisticsBoardTableRowResponseV2]


class PageInfoResponse(GoalsDto):
    """ Информация о странице """
    pageNumber: StrictInt
    pageSize: StrictInt
    countPage: StrictInt
    countAll: StrictInt


class StatisticsBoardDirectTableResponseV2(GoalsDto):
    """ Таблица статистики прямого подчинения """
    table: StatisticsBoardTableResponseV2
    page: PageInfoResponse


class StatisticsBoardTeamTableResponseV2(GoalsDto):
    """ Таблица статистики команды """
    table: StatisticsBoardTableResponseV2
    page: PageInfoResponse


class StatisticsBoardStructureTableResponseV2(GoalsDto):
    """ Таблица статистики структуры """
    table: StatisticsBoardTableResponseV2
    page: PageInfoResponse