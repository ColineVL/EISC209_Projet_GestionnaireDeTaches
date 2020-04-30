from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects),
    path('projects', views.projects, name='projects'),
    path('project/<int:id>', views.project, name='project'),
    path('task/<int:id>', views.task, name='task'),
    path('newtask/<int:idProjet>', views.newtask, name='newtask'),
    path('edittask/<int:idTask>', views.edittask, name='edittask'),
]
