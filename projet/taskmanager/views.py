from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, NewEntryForm, ProjectForm
from .models import Project, Task, Journal


# Pas une view, c'est une fonction utile
def progress(project):
    # On récupère les tâches au sein du projet
    tasks = Task.objects.filter(project=project)

    # On calcule le taux d'avancement du projet
    # On considère que toutes les tâches ont le même poids
    nb_tasks = 0
    total_progress = 0
    for task in tasks:
        nb_tasks += 1
        total_progress += task.progress

    if nb_tasks == 0:
        return 0

    return total_progress / nb_tasks


@login_required
def projects(request):
    # On récupère la liste des projets
    list_projects = request.user.project_set.all()
    # Pour chaque projet, on note le nombre de membres et le nombre de tâches
    for pr in list_projects:
        pr.nbMembers = len(pr.members.all())
        pr.nbTasks = len(pr.task_set.all())

        # Taux d'avancement pour chaque projet (avec int on arrondit à l'entier)
        pr.progress = int(progress(pr))

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
    return render(request, 'taskmanager/project.html', locals())


@login_required
def newproject(request):
    # On crée un formulaire pour créer un nouveau projet
    form = ProjectForm(request.POST or None)
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "New"
    if form.is_valid():
        project_formed = form.save()
        # On redirige vers le projet nouvellement créé
        return redirect('project', id_project=project_formed.id)
    return render(request, 'taskmanager/modifyproject.html', locals())


@login_required
def editproject(request, id_project):
    # On récupère le projet à modifier
    project_formed = get_object_or_404(Project, id=id_project)
    list_members = project_formed.members.all()
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if not request.user in list_members:
        return redirect('accueil')
    # On crée un form pour modifier le projet demandé
    form = ProjectForm(request.POST or None, instance=project_formed)
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "Edit"
    if form.is_valid():
        form.save()
        # On redirige vers le projet modifié
        return redirect(project, id_project=id_project)
    return render(request, 'taskmanager/modifyproject.html', locals())


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


@login_required
def usertasks_all(request):
    list_tasks = request.user.task_set.all()
    return render(request, "taskmanager/usertasks-all.html", locals())


@login_required
def usertasks_done(request):
    # Dans l'argument, mettre le statut qui correspond à une tâche terminé
    list_tasks = request.user.task_set.filter(status__name="Terminée")
    return render(request, "taskmanager/usertasks-done.html", locals())


@login_required
def membersallprojects(request):
    # On récupère tous les projets de l'utilisateur
    list_projects = request.user.project_set.all()
    # On récupère tous les membres de chaque projet
    for pr in list_projects:
        pr.list_members = pr.members.all()
    return render(request, 'taskmanager/membersallprojects.html', locals())


@login_required
def membersbyproject(request, id_project):
    # On récupère le projet demandé
    project_to_display = get_object_or_404(Project, id=id_project)
    # On récupère tous les membres du projet
    list_members = project_to_display.members.all()
    return render(request, 'taskmanager/membersbyproject.html', locals())

@login_required
def activity_all(request):
    return render(request, 'taskmanager/activity-all.html', locals())

@login_required
def activity_per_project(request, id_project):
    return render(request, 'taskmanager/activity-per-project.html', locals())