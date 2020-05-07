from django import forms
from .models import Task, Project


# Form à partir de Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)
        # Quand l'utilisateur crée une tache ou la modifie, il ne doit pas changer le projet associé.

    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if priority < 0:
            raise forms.ValidationError("La priorité doit être un entier positif !")
        return priority
    # L'utilisateur ne pourra pas entrer de priorité négative


# Form pour entrer une nouvelle information complémentaire dans un journal
class NewEntryForm(forms.Form):
    entry = forms.CharField(max_length=200)


# Form pour créer un nouveau projet, à partir de Project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

