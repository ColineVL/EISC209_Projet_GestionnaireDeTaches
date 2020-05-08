from django import forms
from .models import Task, Project


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

