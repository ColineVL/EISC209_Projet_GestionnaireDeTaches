from django.contrib.auth.models import User
from django.db import models


# Modèle Project
class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


# Modèle Status
class Status(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Status"
        # Cette ligne sert à ne pas avoir "statuss" dans l'administration


# Modèle Task
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

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
