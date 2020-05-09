from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, NewEntryForm, ExportForm
from .models import *
from .resources import *
from django.http import HttpResponse
from zipfile import ZipFile
import shutil
from .export import *

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

@login_required
def export_data(request):
    """
    This views allows the exportation of data to a specified format.
    It is able to handle five different formats 'csv','xls','json','html' and 'yaml'.
    The function construct the asked file, add them to a zip file and then destroy the temporary files
    :param request:
    :return:
    """
    form = ExportForm(request.POST or None,user=request.user)

    if form.is_valid():
        file_type = form.cleaned_data['file_type']
        archive_name = form.cleaned_data['archive_name']
        bool_project = form.cleaned_data['bool_project']
        bool_task = form.cleaned_data['bool_task']
        bool_status = form.cleaned_data['bool_status']
        bool_journal = form.cleaned_data['bool_Journal']
        one_dir_by_project = form.cleaned_data['one_dir_by_project']
        ordered_journal_by_task = form.cleaned_data['ordered_journal_by_task']
        all_projects = form.cleaned_data['all_projects']

        # here we get the table of the project file
        project_set = request.user.project_set.all()
        if  not all_projects:
            projects_name = form.cleaned_data['project']
            project_set = project_set.filter(name__in=projects_name)

        # we create the http response and we link a zip file to it
        response = HttpResponse('content_type=application/zip')
        zipObj = ZipFile(response, 'w')

        # depending on the entry we create the different files an directory and add them to the zip file
        if bool_project:
            create_file(file_type,'projects.'+file_type,project_set, ProjectRessource(),zipObj)
        if bool_status:
            create_file(file_type,'status.'+file_type,Status.objects.all(), StatusResource(),zipObj)
        if bool_task or bool_journal:
            if one_dir_by_project:
                for project in project_set:
                    os.mkdir(project.name)
                    if bool_task:
                        create_file(file_type,project.name+'/task.'+file_type, Task.objects.filter(project=project), TaskResource(),zipObj)
                    if bool_journal:
                        if ordered_journal_by_task:
                            set = Journal.objects.filter(task__in=Task.objects.filter(project=project)).order_by('task')
                        else:
                            set = Journal.objects.filter(task__in=Task.objects.filter(project=project)).order_by('date')
                        create_file(file_type, project.name+'/journal.'+file_type, set,JournalResource(),zipObj)
                    shutil.rmtree(project.name) # we remove the tempory directories
            else:
                if bool_task:
                    create_file(file_type,'task.'+file_type, Task.objects.filter(project__in=project_set),TaskResource(),zipObj)
                if bool_journal:
                    create_file(file_type,'journal.'+file_type, Journal.objects.filter(task__in=Task.objects.filter(project__in=project_set)),JournalResource(),zipObj)

        response['Content-Disposition'] = 'attachment; filename="' + archive_name + '.zip"'
        return response

    return render(request, 'taskmanager/export_data.html', locals())