import django_filters
from django_filters.widgets import RangeWidget

from .models import Task, User, Status
from django.db import models
from django import forms


class TaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Nom',
                                     widget=forms.TextInput(attrs={'title': 'Nom',
                                                                   'placeholder': "Ecrire entierement ou partiellement la tache..."}))

    assignee = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all(), field_name='assignee',
                                                        label='Assignée à')

    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gt', label='A faire après:',
                                           widget=forms.DateInput(attrs={'type': 'date',
                                                                         'title': 'Date de début',
                                                                         'placeholder': "..."}))

    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='lt', label='A terminer avant:',
                                         widget=forms.DateInput(attrs={'type': 'date',
                                                                       'title': 'Date de fin',

                                                                       'placeholder': "..."}))

    status = django_filters.ModelMultipleChoiceFilter(queryset=Status.objects.all(), field_name='status',
                                                      label='Statut')
    # TODO : borner la valeur de la priorité

    priority = django_filters.LookupChoiceFilter(field_name='priority',
                                                 lookup_choices=[('exact', 'égal à'), ('gte', 'Plus grande ou égal à'),
                                                                 ('lte', 'Plus petite ou égal à')],
                                                 field_class=forms.IntegerField,
                                                 label='Priorité',
                                                 )

    progress = django_filters.LookupChoiceFilter(field_name='progress',
                                                 lookup_choices=[('exact', 'égal à'), ('gte', 'Plus grande ou égal à'),
                                                                 ('lte', 'Plus petite ou égal à')],
                                                 field_class=forms.IntegerField,
                                                 label='progrès',
                                                 )
    #TESTTEST
    # class Meta:
    #   model = Task
    # fields = ['name']
    """    class Meta:
        model = Task
        fields = ['name','assignee', 'start_date']


        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'label': 'nom de la tache',
                    'lookup_expr': 'icontains',
                    'widget': forms.TextInput(attrs={'title':'Nom', 'placeholder': "Ecrire entierement ou partiellement la tache..."})
                },
            },

            models.DateField: {
                'filter_class' : django_filters.DateFilter,
                'extra': lambda f: {

                    'label': 'Date de debut',
                    'lookup_expr': 'year__gte',
                    'widget': forms.SelectDateWidget()
                }
            }
        }
"""
