from allure import epic, feature
from pytest import mark

from clusters import Clusters
from services import Services


@epic(Clusters.GOALS_AND_ESTIMATE)
@mark.cluster_goals_and_estimate
class ClusterGoalsAndEstimate:
    """Разметка для сервисов кластера "Цели и Оценка" """
    pass


@mark.app_goals
@mark.api
@feature(Services.APP_GOALS)
class GoalsAPI(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_goals" """
    pass


@mark.app_web_goals
@mark.web
@feature(Services.APP_WEB_GOALS)
class GoalsWeb(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_web_goals" """
    pass


@mark.app_rtfvalues
@mark.api
@feature(Services.APP_RTFVALUES)
class RTFValuesAPI(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_rtfvalues" """
    pass


@mark.app_web_rtfvalues
@mark.web
@feature(Services.APP_WEB_RTFVALUES)
class RTFValuesWeb(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_web_rtfvalues" """
    pass


@mark.app_perfreview
@mark.api
@feature(Services.APP_PERFREVIEW)
class PerfreviewAPI(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_perfreview" """
    pass


@mark.app_web_perfreview
@mark.web
@feature(Services.APP_WEB_PERFREVIEW)
class PerfreviewWeb(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_web_perfreview" """
    pass


@mark.app_web_perfreview_admin
@mark.web
@feature(Services.APP_WEB_PERFREVIEW_ADMIN)
class PerfreviewWebAdmin(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_web_perfreview_admin" """
    pass


@mark.app_cloud_serviceorder
@mark.api
@feature(Services.APP_CLOUD_SERVICEORDER)
class ServiceOrderAPI(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_cloud_serviceorder" """
    pass


@mark.app_web_cloud_serviceorder
@mark.web
@feature(Services.APP_WEB_CLOUD_SERVICEORDER)
class ServiceOrderWeb(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_web_cloud_serviceorder" """
    pass


@mark.app_cloud_absences
@mark.api
@feature(Services.APP_CLOUD_ABSENCES)
class AbsencesAPI(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_cloud_absences" """
    pass


@mark.app_web_cloud_absences
@mark.web
@feature(Services.APP_WEB_CLOUD_ABSENCES)
class AbsencesWeb(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_web_cloud_absences" """
    pass


@mark.app_cloud_hr_journal
@mark.api
@feature(Services.APP_CLOUD_HR_JOURNAL)
class HRJournalAPI(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_cloud_hr_journal" """
    pass


@mark.app_cloud_payslip
@mark.api
@feature(Services.APP_CLOUD_PAYSLIP)
class PayslipAPI(ClusterGoalsAndEstimate):
    """Разметка для сервиса "app_cloud_payslip" """
    pass
