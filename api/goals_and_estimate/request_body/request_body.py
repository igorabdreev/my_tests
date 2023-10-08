from generators.randoms import get_random_string


class Request_body():

    @staticmethod
    def json_create_goal(current_year_start, current_year_end, user_uuid, periodStart='Q4', periodEnd='Q4',
                         yearGoal=False,
                         weight=None):
        """ Параметры для создания Бизнес цели без КР
        """
        if weight is None:
            weight = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0}
        json_create_goal = {
            'assignees': [],
            'description': '',
            'endDate': current_year_end,
            'keyResults': [],
            'periodEnd': periodEnd,
            'periodStart': periodStart,
            'reporterId': user_uuid,
            'startDate': current_year_start,
            'title': get_random_string(),
            'type': 'STANDARD',
            'visibility': 'VISIBLE',
            'weight': weight,
            'yearGoal': yearGoal,
            'fileIds': []
        }
        return json_create_goal

    @staticmethod
    def json_edit_goal(current_year_start, current_year_end, periodStart='Q1', periodEnd='Q4', isYearGoal=False,
                       weight=None):
        """ Параметры для редактирования Бизнес цели без КР
        """
        if weight is None:
            weight = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0}
        json_edit_goal = {
            "title": get_random_string(),
            "description": get_random_string(),
            "visibility": "VISIBLE",
            "isRiskState": True,
            "riskComment": get_random_string(),
            "startDate": current_year_start,
            "endDate": current_year_end,
            "periodStart": periodStart,
            "periodEnd": periodEnd,
            "isYearGoal": isYearGoal,
            'weight': weight
        }
        return json_edit_goal

    @staticmethod
    def json_create_goal_with_kpi(user_uuid, weight=None, startDate="2023-01-01", endDate="2023-12-31", periodEnd='Q1',
                                  periodStart='Q1', targetValue=1000, valueMin=800,
                                  valueMax=1200, progressMin=85, progressMax=120, yearGoal=True):
        """ Параметры для создания Бизнес цели KPI
        """
        if weight is None:
            weight = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0}
        json_create_goal_with_kpi = {
            'assignees': [],
            'description': '',
            'startDate': startDate,
            'endDate': endDate,
            'keyResults': [{"id": "-1",
                            "type": "KPI",
                            "title": get_random_string(),
                            "description": "",
                            "targetValue": targetValue,
                            "valueMin": valueMin,
                            "valueMax": valueMax,
                            "progressMin": progressMin,
                            "progressMax": progressMax,
                            "metric": "штук",
                            "status": "DONE",
                            "startDate": startDate,
                            "endDate": endDate}],
            'periodEnd': periodEnd,
            'periodStart': periodStart,
            'reporterId': user_uuid,
            'title': get_random_string(),
            'type': 'STANDARD',
            'visibility': 'VISIBLE',
            'weight': weight,
            'yearGoal': yearGoal,
            'fileIds': []
        }
        return json_create_goal_with_kpi

    @staticmethod
    def json_create_goal_with_kr(user_uuid, weight=None, yearGoal=True, startDate="2023-01-01", endDate="2023-12-31",
                                 startDate_kr="2023-01-01", endDate_kr="2023-12-31", periodEnd='Q1',
                                 periodStart='Q1'):
        """ Параметры для создания Бизнес цели с КР
        """
        if weight is None:
            weight = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0}
        json_create_goal_with_kr = {
            "title": get_random_string(),
            "type": "STANDARD",
            "description": get_random_string(),
            "periodStart": periodStart,
            "periodEnd": periodEnd,
            "startDate": startDate,
            "endDate": endDate,
            "yearGoal": yearGoal,
            "keyResults": [
                {"startDate": startDate_kr,
                 "title": get_random_string(),
                 "description": get_random_string(),
                 "endDate": endDate_kr,
                 "type": "BINARY",
                 "id": "1696782554679"}],
            "visibility": "VISIBLE",
            "fileIds": [],
            "assignees": [],
            "weight": weight,
            "reporterId": user_uuid}
        return json_create_goal_with_kr

    @staticmethod
    def json_create_kr_binary(endDate="2023-12-31"):
        json_create_kr_binary = {
            'description': get_random_string(),
            'endDate': endDate,
            'title': get_random_string(),
            'type': "BINARY"
        }
        return json_create_kr_binary

    @staticmethod
    def json_create_kr_metric(endDate="2023-12-31", metric="%", startProgress=0, targetProgress=100):
        json_create_kr_metric = {
            "title": get_random_string(),
            "description": get_random_string(),
            "endDate": endDate,
            "type": "METRIC",
            "metric": metric,
            "startProgress": startProgress,
            "targetProgress": targetProgress
        }
        return json_create_kr_metric
