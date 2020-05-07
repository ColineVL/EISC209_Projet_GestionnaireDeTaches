from django import forms
from .models import *


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
