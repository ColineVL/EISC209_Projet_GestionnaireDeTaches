from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects, name='accueil'),
    path('projects', views.projects, name='projects'),
    path('project/<int:id_project>', views.project, name='project'),
    path('task/<int:id_task>', views.task, name='task'),
    path('newtask/<int:id_project>', views.newtask, name='newtask'),
    path('edittask/<int:id_task>', views.edittask, name='edittask'),

    #TODO enlever ça, c'est un test
    path('test', views.test, name="test"),
    path('json', views.json, name='json_example'),
    path('test_HC', views.chart_data, name="chart_data")
]
