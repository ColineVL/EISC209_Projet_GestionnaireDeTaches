from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Project, Task, Journal


# Create your views here.


@login_required
def accueil(request):
    return render(request, 'taskmanager/accueil.html')


@login_required
def projects(request):
    liste_projets = request.user.project_set.all()
    return render(request, 'taskmanager/projects.html', locals())


@login_required
def project(request, id):
    projet = Project.objects.get(id=id)
    liste_taches = Task.objects.filter(project__id = id)
    return render(request, 'taskmanager/project.html', locals())


@login_required
def task(request, id):
    task = Task.objects.get(id=id)

    liste_journal = Journal.objects.filter(task=task)
    return render(request, 'taskmanager/task.html', locals())