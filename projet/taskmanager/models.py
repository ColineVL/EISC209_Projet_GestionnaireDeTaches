from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Modèle Project
class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


# Modèle Status
class Status(models.Model):
    name = models.CharField(max_length=200)
    # Ce champ est utilisé pour l'apparence des statuts avec Bootstrap4
    badge_color = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Status"
        # Cette ligne sert à ne pas avoir "statuss" dans l'administration


# Modèle Task
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(blank=True, max_length=400)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name


# Modele Journal
class Journal(models.Model):
    date = models.DateTimeField()
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.entry


# Ce modèle est utilisé pour enregistrer la dernière fois que l'utilisateur s'est connecté
class LastLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    current = models.DateTimeField(null=True)
    previous = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username
