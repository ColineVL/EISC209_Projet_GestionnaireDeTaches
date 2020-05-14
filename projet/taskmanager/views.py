# Inportation dans Django
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Importation de fichiers du projet
from .forms import TaskForm, NewEntryForm, ExportForm, ProjectForm
from .models import *
from .export import *
from .filters import TaskFilter

# Importations extérieures
from zipfile import ZipFile
import shutil
from datetime import datetime


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


# Pas une view, pour obtenir le pluriel
def plural(nb):
    if nb > 1:
        return 's'
    else:
        return ''


# Vue gérant l'accueil
@login_required
def accueil(request):
    # On récupère les projets de l'utilisateur, ainsi que leur nombre
    list_projects = request.user.project_set.all()
    nb_projects = len(list_projects)

    # On récupère la liste des tâches des projets de l'utilisateur
    list_all_tasks = Task.objects.none()
    for project in list_projects:
        list_all_tasks = list_all_tasks.union(project.task_set.all())

    # On récupère la liste des tâches assignées à l'utilisateur, ainsi que leur nombre
    list_tasks = request.user.task_set.all()
    nb_tasks = len(list_tasks)

    # On récupère la liste des tâches assignées à l'utilisateur et non terminée, ainsi que leur nombre
    list_tasks_unfinished = list_tasks.exclude(status__name="Terminée")
    nb_tasks_unfinished = len(list_tasks_unfinished)

    # On récupère la tâche assignée à l'utilisateur et non terminée, qui a le plus grand taux d'avancement
    list_tasks_unfinished = list_tasks_unfinished.order_by("-progress")
    try:
        task_most_progress = list_tasks_unfinished[0]
    except IndexError:
        task_most_progress = None

    # On récupère le nombre de tâches terminées
    nb_tasks_done = nb_tasks - nb_tasks_unfinished

    # Date quand l'utilisateur s'est connecté pour la dernière fois
    date_last_connection = LastLogin.objects.get(user=request.user).previous

    # On récupère les entrées apparues depuis la dernière fois qu'il s'est connecté
    list_entries_last_connection = Journal.objects.none()
    for task in list_all_tasks:
        list_entries_last_connection = list_entries_last_connection.union(
            task.journal_set.filter(date__gt=date_last_connection).exclude(author=request.user))

    # On récupère leur nombre
    nb_all_entries_last_connection = len(list_entries_last_connection)

    # On récupère les entrées apparues dans les tâches assignées à l'utilisateur
    # depuis la dernière fois qu'il s'est connecté
    list_entries_last_connection = Journal.objects.none()
    for task in list_tasks:
        list_entries_last_connection = list_entries_last_connection.union(
            task.journal_set.filter(date__gt=date_last_connection).exclude(author=request.user))

    # On récupère leur nombre
    nb_entries_last_connection = len(list_entries_last_connection)

    # Utilisé pour bien accorder dans la template
    plural_entry = ''
    plural_entry_bis = 'a'
    if nb_all_entries_last_connection > 1:
        plural_entry = 's'
        plural_entry_bis = 'ont'

    plural_project = plural(nb_projects)
    plural_task = plural(nb_tasks)
    plural_task_un = plural(nb_tasks_unfinished)
    plural_task_done = plural(nb_tasks_done)

    # On prépare le graphe des entrées par statut
    dico = {
        "Nouvelle": 0,
        "En cours": 0,
        "En attente": 0,
        "Terminée": 0,
    }
    for task in list_tasks:
        # On ajoute 1 à la catégorie correspondante
        dico[task.status.name] += 1

    return render(request, 'taskmanager/accueil.html', locals())


# Cette vue est appelée juste après que l'utilisateur se soit connecté
# Elle permet de stocker la dernière fois où l'utilisateur s'est connecté
@login_required
def record_date(request):
    # get_or_create renvoie un tuple de longueur 2 avec l'objet et un booléen indiquant
    # si l'objet est nouveau ou non
    ll_object = LastLogin.objects.get_or_create(user=request.user)[0]

    # On vérifie d'abord que le champ n'est pas None
    if ll_object.current:
        # Dans ce cas, on vérifie que le champ last_login de User est plus récent
        # que le champ current de LastLogin
        if request.user.last_login > ll_object.current:
            ll_object.previous = ll_object.current
            ll_object.current = request.user.last_login

    else:
        # Dans ce cas, on remplit les deux champs de la même façon
        ll_object.current = request.user.last_login
        ll_object.previous = request.user.last_login

    ll_object.save()

    return redirect('accueil', permanent=True)


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

    # On prépare le graphe (spiderweb)
    list_dicts = []
    for pro in list_projects:
        dict_project = {
            "name": pro.name,
            "nb": len(Journal.objects.filter(task__project=pro))
        }
        list_dicts.append(dict_project)
    return render(request, 'taskmanager/projects.html', locals())


@login_required
def project(request, id_project):
    # On récupère le projet demandé
    project_to_display = get_object_or_404(Project, id=id_project)
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if request.user not in project_to_display.members.all():
        return redirect('accueil')
    # On récupère la liste des tâches du projet
    list_tasks = Task.objects.filter(project__id=id_project)

    # On crée le filtre pour les taches
    filter = TaskFilter(request.GET, queryset=list_tasks)

    # On prépare le diagramme de Gantt
    list_dicts = []
    for task_to_display in filter.qs:
        # On ajoute à la liste un dictionnaire regroupant les infos de la tâche
        dict_task = {
            "name": task_to_display.name,
            "start": [task_to_display.start_date.year, task_to_display.start_date.month,
                      task_to_display.start_date.day],
            "end": [task_to_display.due_date.year, task_to_display.due_date.month, task_to_display.due_date.day],
            "progress": task_to_display.progress / 100
        }
        list_dicts.append(dict_task)
    return render(request, 'taskmanager/project.html', locals())


@login_required
def newproject(request):
    # On crée un formulaire pour créer un nouveau projet
    form = ProjectForm(request.POST or None)
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "Nouveau"
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
    if request.user not in list_members:
        return redirect('accueil')
    # On crée un form pour modifier le projet demandé
    form = ProjectForm(request.POST or None, instance=project_formed)
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "Modifier"
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
    # Trie des entrées dans l'ordre décroissant des dates
    list_journal = list_journal.order_by('-date')
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if request.user not in task_to_display.project.members.all():
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
    if request.user not in list_members:
        return redirect('accueil')
    # On crée un formulaire pour créer une nouvelle tâche
    form = TaskForm(request.POST or None)
    form.fields['assignee'].queryset = project_related.members
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "Nouvelle"
    if form.is_valid():
        task_formed = form.save(commit=False)
        # On attribue automatiquement le projet
        task_formed.project = project_related
        # Si le status est "terminée", alors l'avancement est mis à 100%
        if task_formed.status.name == "Terminée":
            task_formed.progress = 100
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
    if request.user not in list_members:
        return redirect('accueil')
    # On crée un form pour modifier la tâche demandée
    form = TaskForm(request.POST or None, instance=task_formed)
    form.fields['assignee'].queryset = task_formed.project.members
    # On crée une variable qui sera utilisée dans le template pour personnaliser le titre
    method = "Modifier"
    if form.is_valid():
        form.save()
        # Si le status est "terminée", alors l'avancement est mis à 100%
        if task_formed.status.name == "Terminée":
            task_formed.progress = 100
            task_formed.save()
        # On redirige vers la tâche modifiée
        return redirect(task, id_task=id_task)
    return render(request, 'taskmanager/modifytask.html', locals())


@login_required
def usertasks_all(request):
    # On récupère les tâches assignées à l'utilisateur
    list_tasks = request.user.task_set.all()
    #On crèe le filtre pour trier et filtrer les taches affichées
    filter = TaskFilter(request.GET, queryset=list_tasks)
    # Cette variable est utilisée pour changer le titre de la template
    title = "Toutes mes tâches"

    return render(request, "taskmanager/usertasks.html", locals())


@login_required
def usertasks_unfinished(request):
    # On récupère les tâches assignées à l'utilisateur non terminées
    list_tasks = request.user.task_set.exclude(status__name="Terminée")
    # On crèe le filtre pour trier et filtrer les taches affichées
    filter = TaskFilter(request.GET, queryset=list_tasks)
    # Cette variable est utilisée pour changer le titre de la template
    title = "Mes tâches non terminées"
    return render(request, "taskmanager/usertasks.html", locals())


@login_required
def usertasks_done(request):
    # Dans l'argument, mettre le statut qui correspond à une tâche terminé
    list_tasks = request.user.task_set.filter(status__name="Terminée")
    # On crèe le filtre pour trier et filtrer les taches affichées
    filter = TaskFilter(request.GET, queryset=list_tasks)
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
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if request.user not in project_to_display.members.all():
        return redirect('accueil')
    # On récupère tous les membres du projet
    list_members = project_to_display.members.all()

    # On prépare le graphe : pour chaque membre, on stocke le nombre de ses tâches
    list_dicts = []
    for mem in list_members:
        dict_member = {
            "name": mem.username,
            "nb": len(mem.task_set.filter(project=project_to_display))
        }
        list_dicts.append(dict_member)
    return render(request, 'taskmanager/membersbyproject.html', locals())


# Pas une vue
# Cette fonction permet de récupérer la liste des entries à partir d'une liste de tâches
def get_list_entries(list_tasks, request):
    # On récupère les paramètres GET affiche et notmyentries
    # affiche sert à afficher un nombre précis d'entrées
    # notmyentries sert à afficher ou non les entrées de l'utilisateur connecté
    try:
        affiche = request.GET['affiche' or None]
    except:
        # Par défaut, affiche vaut 20
        affiche = 20

    try:
        notmyentries = request.GET['notmyentries' or None]
    except:
        # Par défaut, notmyentries vaut off
        notmyentries = "off"

    # On prend l'entier correspondant à afficher
    affiche = int(affiche)

    # On récupère toutes les entrées de journal dont l'auteur n'est pas l'utilisateur, dans le cas où notmyentries
    # vaut on
    if notmyentries == "on":
        list_entries = Journal.objects.none()
        for task in list_tasks:
            list_entries = list_entries.union(task.journal_set.exclude(author=request.user))
        # Qu'on trie par date décroissante
        list_entries = list_entries.order_by('-date')

    # Dans le cas contraire, on récupère toutes les entrées de journal
    else:
        list_entries = Journal.objects.none()
        for task in list_tasks:
            list_entries = list_entries.union(task.journal_set.all())
        # Qu'on trie par date décroissante
        list_entries = list_entries.order_by('-date')

    # Enfin, on slash la liste des entrées, si affiche ne vaut pas -1
    if affiche > 0:
        list_entries = list_entries[:affiche]
    return list_entries, affiche, notmyentries


# Cette vue permet d'afficher les dernières activités de tous les projets où participe l'utilisateur
@login_required
def activity_all(request):
    # On récupère tous les projets de l'utilisateur
    list_projects = request.user.project_set.all()

    # On récupère les tâches correspondantes
    list_tasks = Task.objects.none()

    for project in list_projects:
        list_tasks = list_tasks.union(project.task_set.all())

    (list_entries, affiche, notmyentries) = get_list_entries(list_tasks, request)
    #Filtre pour le journal
    #journal_filter = JournalFilter(request.GET, queryset = list_entries)
    # Ce dictionnaire est utilisé dans la template pour spécifier les choix du paramètre affiche
    dict_choices = {
        "20": 20,
        "100": 100,
        "Toutes": -1
    }

    # On récupère la dernière fois qu'un utilisateur s'est connecté
    last_login = LastLogin.objects.get(user=request.user).previous

    return render(request, 'taskmanager/activity-all.html', locals())


# Cette vue permet d'afficher les dernières activités d'un projet où participe l'utilisateur
@login_required
def activity_per_project(request, id_project):
    # On récupère le projet correspondant
    projet = get_object_or_404(Project, id=id_project)
    # Si l'utilisateur n'est pas dans le projet, on le redirige vers sa page d'accueil
    if request.user not in projet.members.all():
        return redirect('accueil')

    # On récupère les tâches
    list_tasks = projet.task_set.all()

    (list_entries, affiche, notmyentries) = get_list_entries(list_tasks, request)

    # Ce dictionnaire est utilisé dans la template pour spécifier les choix du paramètre affiche
    dict_choices = {
        "20": 20,
        "100": 100,
        "Toutes": -1
    }

    # On récupère la dernière fois qu'un utilisateur s'est connecté
    last_login = LastLogin.objects.get(user=request.user).previous

    return render(request, 'taskmanager/activity-per-project.html', locals())


@login_required
def histogram(request):
    # On récupère tous les projets de l'utilisateur
    list_projects = request.user.project_set.all()

    # On récupère les tâches correspondantes
    list_tasks = Task.objects.none()
    for project in list_projects:
        list_tasks = list_tasks.union(project.task_set.all())

    # On récupère toutes les entrées
    list_entries = Journal.objects.filter(task__project__in=list_projects)

    # Qu'on trie par date croissante
    list_entries = list_entries.order_by('date')

    # On récupère seulement les dates des entrées
    list_dates = []
    for entry in list_entries:
        list_dates.append([entry.date.year, entry.date.month, entry.date.day, entry.date.hour, entry.date.minute])

    return render(request, 'taskmanager/histogram.html', locals())


@login_required
def export_data(request):
    """
    This view is used for the exportation of data
    """
    # we take the information of the form
    form = ExportForm(request.POST or None, user=request.user)

    if form.is_valid():
        file_type = form.cleaned_data['file_type']  # the type of the files we want to product
        archive_name = form.cleaned_data['archive_name']  # the name of the achive we want to produce
        bool_project = form.cleaned_data['bool_project']  # do we want the projects data
        bool_task = form.cleaned_data['bool_task']  # do we want the task data
        bool_status = form.cleaned_data['bool_status']  # do we want the status data
        bool_journal = form.cleaned_data['bool_Journal']  # do we want the journal data
        one_dir_by_project = form.cleaned_data['one_dir_by_project']  # do we want one directory by project
        ordered_journal_by_task = form.cleaned_data['ordered_journal_by_task']  # do we want journal grouped by task
        all_projects = form.cleaned_data['all_projects']  # do we want all projects

        project_set = request.user.project_set.all()
        if not all_projects:
            # if all_projects is false, we take the different projets we want
            projects_name = form.cleaned_data['project']
            project_set = project_set.filter(name__in=projects_name)

        response = HttpResponse('content_type=application/zip')
        zipObj = ZipFile(response, 'w')  # we create a zip object that we link to the http response

        # we create the different files that we want
        if bool_project:
            create_file(file_type, 'projects.' + file_type, project_set,
                        ['name', 'members'], zipObj)
        if bool_status:
            create_file(file_type, 'status.' + file_type, Status.objects.all(),
                        ['name'], zipObj)
        if bool_task or bool_journal:
            if one_dir_by_project:
                for project in project_set:
                    os.mkdir(project.name)  # this is to create a directory for a project
                    if bool_task:
                        create_file(file_type, project.name + '/task.' + file_type,
                                    Task.objects.filter(project=project),
                                    ['project', 'name', 'description', 'assignee', 'start_date', 'due_date', 'priority',
                                     'status', 'progress'], zipObj)
                    if bool_journal:
                        if ordered_journal_by_task:
                            set = Journal.objects.filter(task__in=Task.objects.filter(project=project)).order_by('task')
                        else:
                            set = Journal.objects.filter(task__in=Task.objects.filter(project=project)).order_by('date')
                        create_file(file_type, project.name + '/journal.' + file_type, set,
                                    ['date', 'entry', 'author', 'task'], zipObj)
                    shutil.rmtree(
                        project.name)  # once all the project have been added to the zip file, w destroy the temporary directory of the project
            else:
                if bool_task:
                    create_file(file_type, 'task.' + file_type, Task.objects.filter(project__in=project_set),
                                ['project', 'name', 'description', 'assignee', 'start_date', 'due_date', 'priority',
                                 'status', 'progress'], zipObj)
                if bool_journal:
                    create_file(file_type, 'journal.' + file_type,
                                Journal.objects.filter(task__in=Task.objects.filter(project__in=project_set)),
                                ['date', 'entry', 'author', 'task'], zipObj)

        response['Content-Disposition'] = 'attachment; filename="' + archive_name + '.zip"'
        return response

    return render(request, 'taskmanager/export_data.html', locals())


# Pas de login required
def newuser(request):
    if request.method == 'POST':
        # On crée le form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            # On crée l'utilisateur
            user = authenticate(username=username, password=password)
            # On crée l'objet "dernière fois que l'utilisateur s'est connecté"
            log = LastLogin(user=user, current=datetime.now(), previous=datetime.now())
            log.save()
            # On le connecte
            login(request, user)
            # On le redirige
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'registration/newuser.html', locals())
