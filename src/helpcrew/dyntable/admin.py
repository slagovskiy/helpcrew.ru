from django.contrib import admin
from .models import Table, Field, Index, Record


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


class IndexAdmin(admin.ModelAdmin):
    list_display = ('num', 'table', 'deleted')
    ordering = ('table','num')
    exclude = ()
    readonly_fields = ()


class RecordAdmin(admin.ModelAdmin):
    list_display = ('index', 'field', 'value')
    ordering = ('index', 'field')
    exclude = ()
    readonly_fields = ()


admin.site.register(Table, TableAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Record, RecordAdmin)
