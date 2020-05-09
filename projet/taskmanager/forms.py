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

        return progress
    # On spécifie que le taux d'avancement doit rester entre 0 et 100


# Form pour entrer une nouvelle information complémentaire dans un journal
class NewEntryForm(forms.Form):
    entry = forms.CharField(max_length=200)


# Form pour créer un nouveau projet, à partir de Project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class ExportForm(forms.Form):
    archive_name = forms.CharField(max_length=100)
    choice_types = [
        ('csv','csv'),
        ('html','html'),
        ('xls','xls'),
        ('json','json'),
        ('yaml','yaml'),
    ]
    file_type = forms.ChoiceField(choices = choice_types)
    bool_project = forms.BooleanField(initial=True,required=False, label='project table')
    bool_task = forms.BooleanField(initial=True,required=False, label='task table')
    bool_status = forms.BooleanField(initial=False,required=False, label='status table')
    bool_Journal = forms.BooleanField(initial=True,required=False, label='journal table')
    one_dir_by_project = forms.BooleanField(initial=True, required=False, label='one directory by project')
    ordered_journal_by_task = forms.BooleanField(initial=True, required=False, label='group journal by task')
    all_projects = forms.BooleanField(initial=True, required=False, label='select all projects')

    def clean(self):
        all_project = self.cleaned_data['all_projects']
        if not all_project:
            if not self.cleaned_data['project']:
                msg = forms.ValidationError('Please select at least one project')
                self.add_error('project', msg)
        else:
            self.cleaned_data['project']=''

        return self.cleaned_data


    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super().__init__(*args,**kwargs)
        self.fields['project'] = forms.MultipleChoiceField(choices=[(proj.name, proj.name) for proj in user.project_set.all()],
                                                           required=False,
                                                           help_text="Only require if all projects is deselect")
