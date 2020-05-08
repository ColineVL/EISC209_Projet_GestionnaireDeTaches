from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, NewEntryForm
from .models import Project, Task, Journal

# TODO test
import json


@login_required
def projects(request):
    # On récupère la liste des projets
    list_projects = request.user.project_set.all()
    # Pour chaque projet, on note le nombre de membres et le nombre de tâches
    for pr in list_projects:
        pr.nbMembers = len(pr.members.all())
        pr.nbTasks = len(pr.task_set.all())
    return render(request, 'taskmanager/projects.html', locals())


@login_required
def project(request, id_project):
    # On récupère le projet demandé
    project_to_display = get_object_or_404(Project, id=id_project)
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if not request.user in project_to_display.members.all():
        return redirect('accueil')
    # On récupère la liste des tâches du projet
    list_tasks = Task.objects.filter(project__id=id_project)
    # On prépare le diagramme de Gantt
    # Pour chaque tâche, on stocke la date de début et la date de fin
    names = []
    starts = []
    ends = []
    for task_to_display in list_tasks:
        print(task_to_display.name)
        names.append(task_to_display.name)
        start = task_to_display.start_date
        end = task_to_display.due_date
        starts.append([start.year, start.month, start.day])
        ends.append([end.year, end.month, end.day])
    return render(request, 'taskmanager/project.html', locals())





@login_required
def task(request, id_task):
    # On récupère la tâche demandée et la liste des entrées du journal
    task_to_display = get_object_or_404(Task, id=id_task)
    list_journal = Journal.objects.filter(task=task_to_display)
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if not request.user in task_to_display.project.members.all():
        return redirect('accueil')
    # On crée un fom pour ajouter une entrée au journal
    form = NewEntryForm(request.POST or None)
    if form.is_valid():
        entry = form.cleaned_data['entry']
        journal = Journal(task=task_to_display)
        journal.entry = entry
        # On remplit les autres attributs du journal
        journal.date = datetime.now()
        journal.author = request.user
        # On l'enregistre
        journal.save()
        # On efface l'entrée de l'utilisateur
        form = NewEntryForm()
    return render(request, "taskmanager/task.html", locals())


@login_required
def newtask(request, id_project):
    # On récupère le projet parent et la liste des membres
    project_related = get_object_or_404(Project, id=id_project)
    list_members = project_related.members.all()
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if not request.user in list_members:
        return redirect('accueil')
    # On crée un formulaire pour créer une nouvelle tâche
    form = TaskForm(request.POST or None)
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "New"
    if form.is_valid():
        task_formed = form.save(commit=False)
        task_formed.project = project_related
        task_formed.save()
        # On redirige vers la tâche nouvellement créée
        return redirect('task', id_task=task_formed.id)
    return render(request, 'taskmanager/modifytask.html', locals())


@login_required
def edittask(request, id_task):
    # On récupère la tâche à modifier, le projet parent et la liste des membres
    task_formed = get_object_or_404(Task, id=id_task)
    project_related = task_formed.project
    list_members = project_related.members.all()
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if not request.user in list_members:
        return redirect('accueil')
    # On crée un form pour modifier la tâche demandée
    form = TaskForm(request.POST or None, instance=task_formed)
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "Edit"
    if form.is_valid():
        form.save()
        # On redirige vers la tâche modifiée
        return redirect(task, id_task=id_task)
    return render(request, 'taskmanager/modifytask.html', locals())


# TODO ceci est un test
def test(request):
    project_to_display = get_object_or_404(Project, id=1)
    # On récupère la liste des tâches du projet
    list_tasks = Task.objects.filter(project__id=1)
    return render(request, 'taskmanager/test.html')


def json(request):
    return render(request, 'json_example.html')


def chart_data(request):
    dataset = Task.objects \
        .values('assignee') \
        .annotate(value=Count('assignee'))

    data = Task.objects.values('assignee', 'id')
    lista = [{'as': i['assignee'], 'id': i['id']} for i in data]
    resp = json.dumps(lista, cls=DjangoJSONEncoder)
    return HttpResponse(resp)

    # chart = {
    #     'chart': {'type': 'pie'},
    #     'title': {'text': 'Tasks by user'},
    #     'series': [{
    #         'name': 'tasks',
    #         'data': Task.objects.values('assignee','id')
    #     }]
    # }
    #
    # return JsonResponse(chart)
