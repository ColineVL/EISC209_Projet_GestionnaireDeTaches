import django_filters

from .models import User, Status
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

    # TODO : borner la valeur du progrès

    progress = django_filters.LookupChoiceFilter(field_name='progress',
                                                 lookup_choices=[('exact', 'égal à'), ('gte', 'Plus grande ou égal à'),
                                                                 ('lte', 'Plus petite ou égal à')],
                                                 field_class=forms.IntegerField,
                                                 label='progrès',
                                                 )


class TaskOrdering(django_filters.FilterSet):
    CHOICES = (
        ('priority ascending', 'Prioritè plus haute'),
        ('priority descending', 'Prioritè plus basse'),
        ('progress ascending', 'Progrès plus haut'),
        ('progress descending', 'Progrès plus bas'),
        ('due_date closer', 'Date de fin plus proche'),
        ('due_date further', 'Date de fin plus loine')
    )

    task_ordering = django_filters.ChoiceFilter(label='Trier par :', choices=CHOICES, method='filter_by_order')

    def filter_by_order(selfself, queryset, name, value):
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
