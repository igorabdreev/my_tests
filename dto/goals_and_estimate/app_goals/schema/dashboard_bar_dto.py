from pydantic import StrictBool, StrictFloat, StrictInt

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto


class DashboardProgressInfo(GoalsDto):
    """ Данные о прогрессе """
    enableWeight: StrictFloat
    disableWeight: StrictFloat


class DashboardGoalsInfo(GoalsDto):
    """ Данные о прогрессе цели """
    countAll: StrictInt
    countRisk: StrictInt
    countExpired: StrictInt
    countCompleted: StrictInt
    countInProgress: StrictInt


class DashboardBarKeyResultsInfo(GoalsDto):
    """ Данные о ключевых результатах """
    countAll: StrictInt
    countCompleted: StrictInt


class DashboardBarMetaResponse(GoalsDto):
    """ Отображение аналитики """
    visibleAnalytics: StrictBool


class DashboardBarResponse(GoalsDto):
    """ Данные о прогрессе """
    progress: DashboardProgressInfo
    goals: DashboardGoalsInfo
    keyResults: DashboardBarKeyResultsInfo
    meta: DashboardBarMetaResponse