from django.apps import AppConfig


class ToolboxConfig(AppConfig):
    name = 'helpcrew.toolbox'

    def ready(self):
        from .models import Global
        Global.add_not_exist('user-crew-limit', '3')    # ограничение на количество команд у пользователя
        Global.add_not_exist('crew-user-limit', '10')   # ограничение на пользователей в команде
        Global.add_not_exist('start-task', '15')        # начало работ по новой заявке
        Global.add_not_exist('incident-time-one', '2')  # время на решение инцидента до оповещения диспетчера
        Global.add_not_exist('incident-time-two', '6')  # время на решение инцидента до оповещения администратора
        Global.add_not_exist('request-time-one', '24')  # время на решение заявки до оповещения диспетчера
        Global.add_not_exist('request-time-two', '72')  # время на решение заявки до оповещения администратора
