from typing import Optional
from uuid import UUID

from pydantic import StrictInt

from dto.goals_and_estimate.app_goals.schema.generic import GoalsDto
from dto.goals_and_estimate.app_goals.schema.goal_enum import Period, ViewMode


class TreePanelRequest(GoalsDto):
    """Модель описания назначенного"""
    personId: Optional[UUID] = None
    period: Period
    year: Optional[StrictInt] = None


class ImpersonateGoalsPanelRequest(GoalsDto):
    """ Панель целей """
    whomPersonId: UUID
    personId: Optional[UUID] = None
    period: Period
    year: StrictInt
    view: ViewMode


class GoalsPanelRequest(GoalsDto):
    """ Панель целей """
    personId: Optional[UUID] = None
    period: Period
    year: StrictInt
    view: ViewMode