from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)


class NewEntryForm(forms.Form):
    entry = forms.CharField(max_length=200)

    from django import forms


class TestForm(forms.Form):
    FRUIT_CHOICES = [
        ('orange', 'Oranges'),
        ('cantaloupe', 'Cantaloupes'),
        ('mango', 'Mangoes'),
        ('honeydew', 'Honeydews'),
    ]
    favorite_fruit = forms.CharField(label='What is your favorite fruit?',
                                     widget=forms.Select(choices=FRUIT_CHOICES))
