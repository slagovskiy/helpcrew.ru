from django.contrib import admin

from .models import Global


class GlobalAdmin(admin.ModelAdmin):
    list_display = ('slug', 'value')
    ordering = ('slug',)
    exclude = ()
    readonly_fields = ()


admin.site.register(Global, GlobalAdmin)
