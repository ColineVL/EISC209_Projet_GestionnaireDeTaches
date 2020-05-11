from django import forms
from .models import *


# Form à partir de Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)
        # Quand l'utilisateur crée une tache ou la modifie, il ne doit pas changer le projet associé.

    def clean_progress(self):
        progress = self.cleaned_data['progress']
        if progress > 100:
            raise forms.ValidationError("Le taux d'avancement ne peut supérieur à 100%")
            # TODO plutôt une barre entre 0 et 100 et un bouton à déplacer ?
        return progress
    # On spécifie que le taux d'avancement doit rester entre 0 et 100

    # TODO vérifier que les dates sont start < end


# Form pour entrer une nouvelle information complémentaire dans un journal
class NewEntryForm(forms.Form):
    entry = forms.CharField(max_length=200)


# Form pour créer un nouveau projet, à partir de Project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class ExportForm(forms.Form):
    """
    This form is used to export datas contained in the model
    """
    archive_name = forms.CharField(max_length=100)
    choice_types = [
        ('csv','csv'),
        ('html','html'),
        ('xlsx','xlsx'),
        ('json','json'),
        ('yaml','yaml'),
    ]
    file_type = forms.ChoiceField(choices = choice_types,label='type de fichier')
    bool_project = forms.BooleanField(initial=True,required=False, label='table projet')
    bool_task = forms.BooleanField(initial=True,required=False, label='table tâche')
    bool_status = forms.BooleanField(initial=False,required=False, label='table statut')
    bool_Journal = forms.BooleanField(initial=True,required=False, label='table journal')
    one_dir_by_project = forms.BooleanField(initial=True, required=False, label='un répertoire par projet')
    ordered_journal_by_task = forms.BooleanField(initial=True, required=False, label='grouper le journal par tâche')
    all_projects = forms.BooleanField(initial=True, required=False, label='sélectionner tous les projets')

    def clean(self):
        """
        Thanks to this function, the field project is only needed if the case all_project is not select
        :return:
        """
        all_project = self.cleaned_data['all_projects']
        if not all_project:
            if not self.cleaned_data['project']:
                # if not all project are needed and there is nothing in project, we raise an error in the field project
                msg = forms.ValidationError('Merci de sélectionner au moins un projet')
                self.add_error('project', msg)
        else:
            # in the other case project is an empty field
            self.cleaned_data['project']=''

        return self.cleaned_data


    def __init__(self,*args,**kwargs):
        # in the project field, only the project of the user must appear, so we redifine the init function
        user = kwargs.pop('user')
        super().__init__(*args,**kwargs)
        self.fields['project'] = forms.MultipleChoiceField(choices=[(proj.name, proj.name) for proj in user.project_set.all()],
                                                           required=False,
                                                           help_text="Requis uniquement si 'sélectionner tous les projets' est décoché")
        # the help text allows to help the user and appear in muted in the form
