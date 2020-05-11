# GestionnaireDeTaches
Projet de groupe AWNG, cours de 2A. Mai-juin 2020.

## Installation
Clonez le répertoire sur votre ordinateur.
```
git clone https://github.com/ColineVL/GestionnaireDeTaches.git
```
Dans PyCharm, ouvrez le dossier. Dans le terminal, installez les modules nécessaires. 
```
pip install django-bootstrap4
pip install django-import-export
```
Placez-vous dans le dossier *projet*, et lancez les migrations.
```
python manage.py migrate
```
Lancez la commande pour démarrer le serveur.
```
python manage.py runserver
```
Le serveur est alors accessible dans n'importe quel navigateur, à l'adresse : http://localhost:8000/

Pour avoir un bon fonctionnement des statuts des tâches, votre base de données doit avoir un élément <i>status</i> dont le nom est :
```
Terminée
```

## Authors
Coline van Leeuwen <br>
Martin Delage <br>
Alexis Vandewalle <br>
Nicola Imperatore
