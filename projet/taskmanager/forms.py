from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)


class NewEntryForm(forms.Form):
    entry = forms.CharField(max_length=200)
