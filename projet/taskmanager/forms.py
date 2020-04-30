from django import forms
from .models import Task


# Form à partir de Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)
        # Quand l'utilisateur crée une tache ou la modifie, il ne doit pas changer le projet associé.


# Form pour entrer une nouvelle information complémentaire dans un journal
class NewEntryForm(forms.Form):
    entry = forms.CharField(max_length=200)


# TODO enlever : c'est un test
class TestForm(forms.Form):
    FRUIT_CHOICES = [
        ('orange', 'Oranges'),
        ('cantaloupe', 'Cantaloupes'),
        ('mango', 'Mangoes'),
        ('honeydew', 'Honeydews'),
    ]
    favorite_fruit = forms.CharField(label='What is your favorite fruit?',
                                     widget=forms.Select(choices=FRUIT_CHOICES))
