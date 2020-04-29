from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, NewEntryForm
from .models import Project, Task, Journal


# Create your views here.

@login_required
def projects(request):
    liste_projets = request.user.project_set.all()
    return render(request, 'taskmanager/projects.html', locals())


@login_required
def project(request, id):
    projet = get_object_or_404(Project, id=id)
    liste_taches = Task.objects.filter(project__id = id)
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

    return render(request, 'taskmanager/task.html', locals())


@login_required
def newtask(request, idProjet):
    projet = get_object_or_404(Project, id=idProjet)
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.project = projet
        task.save()
        return redirect('task', id = task.id)
    return render(request, 'taskmanager/newtask.html', locals())


@login_required
def edittask(request, idTask):
    task = get_object_or_404(Task, id=idTask)
    form = TaskForm(instance=task)
    #form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        print("!!!!")
        form.save()
        return redirect(task, id=task.id)
    else:
        print("nooo")
        # TODO Apparemment le form n'est pas valide'
    return render(request, 'taskmanager/edittask.html', locals())


def test(request):
    return render(request, 'taskmanager/test.html')