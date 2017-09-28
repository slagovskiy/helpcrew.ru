from django.contrib import admin

from .models import Crew, CrewUsers, CrewService, ServicePrice, TaskPriority, CrewEvent
from .models import TaskFiles, CrewTask, TaskEvent


class CrewAdmin(admin.ModelAdmin):
    list_display = ('name', 'added')
    ordering = ('name',)
    exclude = ()
    readonly_fields = ()


class CrewUsersAdmin(admin.ModelAdmin):
    list_display = ('crew', 'user', 'type')
    ordering = ('crew', 'user')
    exclude = ()
    readonly_fields = ()


class CrewServiceAdmin(admin.ModelAdmin):
    list_display = ('crew', 'name', 'deleted')
    ordering = ('crew', 'name')
    exclude = ()
    readonly_fields = ()


class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ('service', 'start_date', 'cost')
    ordering = ('service', 'start_date')
    exclude = ()
    readonly_fields = ()


class TaskPriorityAdmin(admin.ModelAdmin):
    list_display = ('crew', 'name', 'time_factor', 'cost_factor', 'default', 'deleted')
    ordering = ('crew', 'name')
    exclude = ()
    readonly_fields = ()


class CrewEventAdmin(admin.ModelAdmin):
    list_display = ('crew', 'date', 'user', 'message')
    ordering = ('date',)
    exclude = ()
    readonly_fields = ()


class TaskFilesAdmin(admin.ModelAdmin):
    list_display = ('task', 'file')
    ordering = ('task',)
    exclude = ()
    readonly_fields = ()


class CrewTaskAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'crew')
    ordering = ('-date_in',)
    exclude = ()
    readonly_fields = ()


class TaskEventAdmin(admin.ModelAdmin):
    list_display = ('task', 'message')
    ordering = ('-date',)
    exclude = ()
    readonly_fields = ()


admin.site.register(CrewUsers, CrewUsersAdmin)
admin.site.register(CrewService, CrewServiceAdmin)
admin.site.register(ServicePrice, ServicePriceAdmin)
admin.site.register(TaskPriority, TaskPriorityAdmin)
admin.site.register(CrewEvent, CrewEventAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(TaskFiles, TaskFilesAdmin)
admin.site.register(CrewTask, CrewTaskAdmin)
admin.site.register(TaskEvent, TaskEventAdmin)
