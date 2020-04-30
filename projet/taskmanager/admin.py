from django.contrib import admin
from .models import Project, Task, Status, Journal

# On enregistre nos modèles dans l'administration
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Journal)
admin.site.register(Status)

