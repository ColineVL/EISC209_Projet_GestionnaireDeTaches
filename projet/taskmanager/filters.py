#Necessary
import django_filters
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404

from .models import User, Status, Project, Task

class TaskFilter(django_filters.FilterSet):
    """
        This class creates an object filter for filtering a task model for its fields
        :param django_filters.FIlterSet: Django library needed for the filter to work
    """

    #Nom de la tache. Si l'utilisateur cherche des lettre de la tache
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Nom',
                                     widget=forms.TextInput(attrs={'title': 'Nom de la tâche',
                                                                   'placeholder': "Écrire entièrement ou partiellement le nom de la tâche..."}))

    # TODO(Nicola): borner la choix de field assignée aux utilisateurs du projet
    #Assignée field, lorsque un utilisateur est selectionné
    assignee = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all(), field_name='assignee',
                                                        label='Assignée à')

    #Date de debut. On cherche les date après (gt) la date selectionnée
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gt', label='À faire après',
                                           widget=forms.DateInput(attrs={'type': 'date',
                                                                         'title': 'Date de début',
                                                                         'placeholder': "..."}))

    #Date de debut. On cherche les date avant (lt) la date selectionnée
    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='lt', label='À terminer avant',
                                         widget=forms.DateInput(attrs={'type': 'date',
                                                                       'title': 'Date de fin',

                                                                       'placeholder': "..."}))
    #Liason pour le statut de la tache
    status = django_filters.ModelMultipleChoiceFilter(queryset=Status.objects.all(), field_name='status',
                                                      label='Statut')

    #La priorité peut etre cherché de plusieures façons: exacte, superieur, inferieur à un certain nombre
    priority = django_filters.LookupChoiceFilter(field_name='priority',
                                                 lookup_choices=[('exact', 'Égale à'), ('gte', 'Supérieure ou égale à'),
                                                                 ('lte', 'Inférieure ou égale à')],
                                                 field_class=forms.IntegerField,
                                                 label='Priorité',
                                                 validators=[MinValueValidator(1), MaxValueValidator(10)],
                                                 widget=forms.TextInput(attrs={'min': 1, 'max': 10, 'type': 'number'})
                                                 )

    #Le progrès peut etre cherché de plusieures façons: exacte, superieur, inferieur à un certain nombre
    progress = django_filters.LookupChoiceFilter(field_name='progress',
                                                 lookup_choices=[('exact', 'Égal à'), ('gte', 'Supérieur ou égal à'),
                                                                 ('lte', 'Inférieur ou égal à')],
                                                 field_class=forms.IntegerField,
                                                 label='Progrès',
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                 widget=forms.TextInput(attrs={'min': 0, 'max': 100, 'type': 'number'})
                                                 )
    #Les choix servent pour diversifier le type de tri
    CHOICES = (
        ('priority descending', 'Priorité haute'),
        ('priority ascending', 'Priorité basse'),
        ('progress descending', 'Progrès élevé'),
        ('progress ascending', 'Progrès bas'),
        ('due_date closer', 'Date de fin proche'),
        ('due_date further', 'Date de fin lointaine')
    )

    #Le tri est atteint par un ChoiceFilter avec une methode definie dessous
    task_ordering = django_filters.ChoiceFilter(label='Trier par', choices=CHOICES, method='filter_by_order')


    def filter_by_order(selfself, queryset, name, value):
        """
           This function defines the way the queryset is gonna be sorted by specifying an expression linked to the fields expressed in CHOICES
           :param selfself: the funciton itself
           :param queryset: the queryset to sort
           :param name :
           :param value: the link with the fields in CHOICES
        """
        if value == 'priority ascending':
            expression = 'priority'
        elif value == 'priority descending':
            expression = '-priority'
        elif value == 'progress ascending':
            expression = 'progress'
        elif value == 'progress descending':
            expression = '-progress'
        elif value == 'due_date closer':
            expression = 'due_date'
        elif value == 'due_date further':
            expression = '-due_date'
        else:
            value == 'priority'
        return queryset.order_by(expression)


