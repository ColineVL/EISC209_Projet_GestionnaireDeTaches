from import_export import resources
from .models import *
from import_export.fields import Field
# TODO on utilise encore import export ?

# This file contains classes wich allows model and queryset to be exported in several format

class ProjectRessource(resources.ModelResource):
    number_of_members = Field()

    class Meta:
        model = Project
        exclude = ('id',)

    # dehydrate_field allows to display a field as we want when we export datas
    def dehydrate_members(self, project):
        result = ''
        for member in project.members.all():
            result += member.username + ';'
        return result

    def dehydrate_number_of_members(self, project):
        return len(project.members.all())


class StatusResource(resources.ModelResource):
    class Meta:
        model = Status
        exclude = ('id',)


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        exclude = ('id',)

    def dehydrate_project(self, task):
        return task.project.name

    def dehydrate_status(self, task):
        return task.status.name

    def dehydrate_assignee(self, task):
        return task.assignee.username

    def dehydrate_progress(self, task):
        return task.progress.__str__() + '%'


class JournalResource(resources.ModelResource):
    class Meta:
        model = Journal
        exclude = ('id',)

    def dehydrate_author(self, journal):
        return journal.author.username

    def dehydrate_task(self, journal):
        return journal.task.name


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username')
