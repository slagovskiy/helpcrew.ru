from django.apps import AppConfig


class ToolboxConfig(AppConfig):
    name = 'helpcrew.toolbox'

    def ready(self):
        from .models import Global
        try:
            Global.add_not_exist('user_crew_limit', '3')    # ограничение на количество команд у пользователя
            Global.add_not_exist('crew_user_limit', '10')   # ограничение на пользователей в команде
            Global.add_not_exist('start_task', '15')        # начало работ по новой заявке
            Global.add_not_exist('incident_time_one', '2')  # время на решение инцидента до оповещения диспетчера
            Global.add_not_exist('incident_time_two', '6')  # время на решение инцидента до оповещения администратора
            Global.add_not_exist('request_time_one', '24')  # время на решение заявки до оповещения диспетчера
            Global.add_not_exist('request_time_two', '72')  # время на решение заявки до оповещения администратора
        except:
            pass
