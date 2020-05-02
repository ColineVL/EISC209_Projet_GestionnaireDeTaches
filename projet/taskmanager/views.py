from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, NewEntryForm
from .models import Project, Task, Journal


@login_required
def projects(request):
    list_projects = request.user.project_set.all()
    for pr in list_projects:
        pr.nbMembers = len(pr.members.all())
        pr.nbTasks = len(pr.task_set.all())
    return render(request, 'taskmanager/projects.html', locals())


@login_required
def project(request, id_project):
    project_to_display = get_object_or_404(Project, id=id_project)
    list_tasks = Task.objects.filter(project__id=id_project)
    return render(request, 'taskmanager/project.html', locals())


@login_required
def task(request, id_task):
    task_to_display = get_object_or_404(Task, id=id_task)
    list_journal = Journal.objects.filter(task=task_to_display)
    form = NewEntryForm(request.POST or None)
    if form.is_valid():
        entry = form.cleaned_data['entry']
        journal = Journal(task=task_to_display)
        journal.date = datetime.now()
        journal.entry = entry
        journal.author = request.user
        journal.save()
        form = NewEntryForm()
    return render(request, "taskmanager/task.html", locals())


@login_required
def newtask(request, id_project):
    project_related = get_object_or_404(Project, id=id_project)
    list_members = project_related.members.all()
    form = TaskForm(request.POST or None)
    method = "New"
    if form.is_valid():
        task_formed = form.save(commit=False)
        task_formed.project = project_related
        task_formed.save()
        print("ici") #TODO
        return redirect('task', id_task=task_formed.id)
    return render(request, 'taskmanager/modifytask.html', locals())


@login_required
def edittask(request, id_task):
    task_formed = get_object_or_404(Task, id=id_task)
    project_related = task_formed.project
    list_members = project_related.members.all()
    form = TaskForm(request.POST or None, instance=task_formed)
    method = "Edit"
    if form.is_valid():
        form.save()
        return redirect(task, id_task=task_formed.id)
    return render(request, 'taskmanager/modifytask.html', locals())
