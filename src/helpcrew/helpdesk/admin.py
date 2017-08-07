from django.contrib import admin

from .models import Crew, CrewUsers, CrewService


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


admin.site.register(CrewUsers, CrewUsersAdmin)
admin.site.register(CrewService, CrewServiceAdmin)
admin.site.register(Crew, CrewAdmin)
