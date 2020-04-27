from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('projects', views.projects, name='projects'),
    path('project/<int:id>', views.project, name='project')


]
