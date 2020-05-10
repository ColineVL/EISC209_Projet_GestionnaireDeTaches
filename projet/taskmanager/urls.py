from django.urls import path

from . import views

# TO DO: commenter les path
urlpatterns = [
    #Accueil
    path('', views.accueil, name='accueil'),

    # Projets
    path('projects', views.projects, name='projects'),
    path('project/<int:id_project>', views.project, name='project'),
    path('newproject', views.newproject, name='newproject'),
    path('editproject/<int:id_project>', views.editproject, name='editproject'),

    # Tâches
    path('task/<int:id_task>', views.task, name='task'),
    path('newtask/<int:id_project>', views.newtask, name='newtask'),
    path('edittask/<int:id_task>', views.edittask, name='edittask'),
    path('usertasks/all', views.usertasks_all, name='usertasks_all'),
    path('usertasks/done', views.usertasks_done, name='usertasks_done'),

    # Membres
    path('members/allprojects', views.membersallprojects, name="membersallprojects"),
    path('members/<int:id_project>', views.membersbyproject, name='membersbyproject'),

    # URL vers la page d'activité, pour voir les dernières entrées de journal par tâche
    path('activity/allprojects', views.activity_all, name="activity_all"),
    # Même URL que la précédente, mais trié pour un seul projet
    path('activity/<int:id_project>', views.activity_per_project, name="activity_per_project"),
  
    # Exportation de données
    path('export_data',views.export_data, name="export_data")

]
