from django.urls import path

from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('projects', views.projects, name='projects')
]
