from django.contrib import admin
from django.utils.text import Truncator

from .models import Project, Task, Status, Journal


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'nbMembers')
    ordering = ('name',)
    search_fields = ('name',)

    def nbMembers(self, project):
        return len(project.members.all())

    nbMembers.short_description = "Number of members"


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'project', 'assignee', 'start_date', 'due_date', 'priority', 'status')
    list_filter = ('project', 'assignee', 'status')
    ordering = ('name', 'project', 'priority')
    search_fields = ('name', 'project', 'assignee')

    def apercu_contenu(self, task):
        raise Truncator(task.description).chars(40, truncate='...')

    apercu_contenu.short_description = 'Description'


class JournalAdmin(admin.ModelAdmin):
    list_display = ('entry', 'author', 'task', 'date')
    list_filter = ('author', 'task')
    date_hierarchy = 'date'
    ordering = ('author', 'task', 'date')
    search_fields = ('entry', 'author', 'task')


# On enregistre nos modèles dans l'administration
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Status)
