from django.apps import AppConfig


class ToolboxConfig(AppConfig):
    name = 'toolbox'

    def ready(self):
        from toolbox.models import Global
        Global.add_not_exist('user-crew-limit', '3')
        Global.add_not_exist('crew-user-limit', '10')
