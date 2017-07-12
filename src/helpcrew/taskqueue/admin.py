from django.contrib import admin\

from .models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ('added', 'finished', 'msg_to', 'is_finished')
    ordering = ('is_finished', 'added')
    exclude = ()
    readonly_fields = ()


admin.site.register(Email, EmailAdmin)
