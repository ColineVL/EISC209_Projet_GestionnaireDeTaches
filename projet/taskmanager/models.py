from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# Modele Project
class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    def __str__(self):
        return self.name
