from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'projects', 'tasks', 'date', 'done', 'clients', 'entreprise', 'tech_stack')
    list_filter = ('done', 'date', 'entreprise')
    search_fields = ('tasks', 'projects', 'clients', 'entreprise')
    ordering = ('-date',)