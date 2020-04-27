from django.contrib import admin
from .models import Project, Task, Status, Journal

# Register your models here.

admin.site.register(Project)
admin.site.register(Task)

#TODO dans l'admin ils mettent les noms de modele au pluriel, donc on lit statuss. Comment changer ça ?
admin.site.register(Status)

admin.site.register(Journal)