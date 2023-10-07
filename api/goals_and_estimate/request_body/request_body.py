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
    def json_create_goal_with_kpi(startDate, endDate):

        json_create_goal_with_kpi = {
            'assignees': [],
            'description': '',
            'startDate': startDate,
            'endDate': endDate,
            'keyResults': [{"id": "-1",
                            "type": "KPI",
                            "title": get_random_string(),
                            "description": "",
                            "targetValue": 1000,
                            "valueMin": 800,
                            "valueMax": 1200,
                            "progressMin": 85,
                            "progressMax": 120,
                            "metric": "штук",
                            "status": "DONE",
                            "startDate": "2023-10-06T06:14:28.732Z",
                            "endDate": "2023-12-31"}],
            'periodEnd': 'Q1',
            'periodStart': 'Q4',
            'reporterId': self.user_uuid,
            'title': get_random_string(),
            'type': 'STANDARD',
            'visibility': 'VISIBLE',
            'weight': {'Q1': 5, 'Q2': 5, 'Q3': 5, 'Q4': 5, 'Y': 5},
            'yearGoal': True,
            'fileIds': []
        }
        return json_create_goal_with_kpi