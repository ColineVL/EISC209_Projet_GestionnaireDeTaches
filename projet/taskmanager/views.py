from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Project


# Create your views here.


@login_required
def accueil(request):
    return render(request, 'taskmanager/accueil.html')


@login_required
def projects(request):
    liste_projets = request.user.project_set.all()
    return render(request, 'taskmanager/projects.html', locals())
