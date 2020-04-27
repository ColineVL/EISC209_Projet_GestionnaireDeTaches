from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import TaskForm, NewEntryForm
from .models import Project, Task, Journal


# Create your views here.

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
    add = False
    task = Task.objects.get(id=id)
    liste_journal = Journal.objects.filter(task=task)

    form = NewEntryForm(request.POST or None)
    if form.is_valid():
        text = form.cleaned_data['text']
        journal = Journal(task=task)
        journal.date = datetime.now()
        journal.entry = text
        journal.author = request.user
        journal.save()

    return render(request, 'taskmanager/task.html', locals())


@login_required
def newtask(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        tache = form.save()
        return redirect(task, id = tache.id)
    # TODO attention il te crée une nouvelle tache à chaque fois !
    return render(request, 'taskmanager/newtask.html', locals())


@login_required
def edittask(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(instance=task)
    return render(request, 'taskmanager/newtask.html', locals())

#TODO Et si quelqu'un écrit l'URL tout seul et en écrit un faux ? Créer une page 404.

def test(request):
    return render(request, 'taskmanager/test.html')