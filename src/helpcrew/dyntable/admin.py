from django.contrib import admin
from .models import Table, Field


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted')
    ordering = ('name',)
    exclude = ()
    readonly_fields = ()


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'order', 'deleted')
    ordering = ('order',)
    exclude = ()
    readonly_fields = ()


admin.site.register(Table, TableAdmin)
admin.site.register(Field, FieldAdmin)
