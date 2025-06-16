from django.contrib import admin
from manager.models import *

# Register your models here.

admin.site.site_header = "ON Track"
admin.site.site_title = "ONT"

class toDoTasksAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'startDate',
        'endDate',
        'priority',
    ]
    search_fields = [
        'title',
    ]
    list_filter = ['priority']


class onGoingTasksAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'startDate',
        'startedDate',
        'endDate',
        'priority',
        'statusOfBeginning',
    ]
    search_fields = [
        'title',
    ]
    list_filter = ['priority', 'statusOfBeginning']


class compTasksAdmin(admin.ModelAdmin):
    list_display = [                
        'title',
        'description',
        'priority',
        'startedDate',
        'deadLine',
        'completedDate',
        'statusOfCompletion',
    ]
    search_fields = [
        'title',
    ]
    list_filter = ['priority', 'statusOfCompletion']


admin.site.register(toDoTasks, toDoTasksAdmin)
admin.site.register(onGoingTasks, onGoingTasksAdmin)
admin.site.register(Completed, compTasksAdmin)

