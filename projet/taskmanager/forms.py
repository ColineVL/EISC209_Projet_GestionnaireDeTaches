from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class InfoForm(forms.ModelForm):
    text = forms.CharField(max_length=200)

