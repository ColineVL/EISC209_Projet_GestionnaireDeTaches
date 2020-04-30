from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, NewEntryForm
from .models import Project, Task, Journal


@login_required
def projects(request):
    liste_projets = request.user.project_set.all()
    for pr in liste_projets:
        pr.nbMembers = len(pr.members.all())
        pr.nbTasks = len(pr.task_set.all())
    return render(request, 'taskmanager/projects.html', locals())


@login_required
def project(request, id):
    projet = get_object_or_404(Project, id=id)
    liste_taches = Task.objects.filter(project__id=id)
    return render(request, 'taskmanager/project.html', locals())


@login_required
def task(request, id):
    task = get_object_or_404(Task, id=id)
    liste_journal = Journal.objects.filter(task=task)

    form = NewEntryForm(request.POST or None)
    if form.is_valid():
        entry = form.cleaned_data['entry']
        journal = Journal(task=task)
        journal.date = datetime.now()
        journal.entry = entry
        journal.author = request.user
        journal.save()
        form = NewEntryForm()
    return render(request, 'taskmanager/task.html', locals())


@login_required
def newtask(request, idProjet):
    projet = get_object_or_404(Project, id=idProjet)
    list_members = projet.members.all()
    form = TaskForm(request.POST or None)
    method = "New"
    if form.is_valid():
        tache = form.save(commit=False)
        tache.project = projet
        tache.save()
        return redirect('task', id=tache.id)
    return render(request, 'taskmanager/modifytask.html', locals())


@login_required
def edittask(request, idTask):
    tache = get_object_or_404(Task, id=idTask)
    projet = tache.project
    list_members = projet.members.all()
    form = TaskForm(request.POST or None, instance=tache)
    method = "Edit"
    if form.is_valid():
        form.save()
        return redirect(task, id=tache.id)
    return render(request, 'taskmanager/modifytask.html', locals())


def test(request):
    ok = "no"
    form = TestForm(request.POST or None)
    if form.is_valid():
        form.save()
        ok = "yes"
    return render(request, 'taskmanager/test.html', locals())

