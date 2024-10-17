# Projet Log Base

Ce projet permet d'analyser des logs de requêtes SQL bloquées et de générer des tableaux à partir de ces logs. 
Il fournit également une interface utilisateur graphique pour ouvrir des fichiers ou des dossiers et afficher les résultats dans une table.

## Fonctionnalités

- **Analyse des requêtes bloquées**
- **Interface utilisateur**
- **Génération de tableaux**
  
## Structure du projet
```

├── batchOpen.py # Gestion des fichiers dans les dossiers 

├── data_handler.py # Module pour la gestion des données des logs 

├── MainApp.py # Application Kivy 

├── main.py # Application principale 

├── DragAndDrop.py # Interface de glisser-déposer 

├── DisplayArray.py # Affichage des résultats dans un tableau 

├── DisplayLogs.py # Affichage de navigation dans les fichiers

├── parser.py # Fonctions d'analyse des logs

├── requirements.txt # Liste des dépendances 

└── README.md # Ce fichier 
```


## Installation, 2 possibilités

1. **Cloner le dépôt:** 
#####  avec https
```bash
git clone https://forge.iut-larochelle.fr/log_base/ihm_kivy.git
```
#####  avec ssh
```bash
git clone git@forge.iut-larochelle.fr:log_base/ihm_kivy.git
```

2. **Télécharger l'archive:** 
##### rendez vous à l'adresse suivante, et cliquer sur Code -> zip ou tar
```
https://forge.iut-larochelle.fr/log_base/ihm_kivy
```

Installer les dépendances :

   Ce projet utilise Kivy pour l'interface utilisateur et d'autres modules pour la manipulation des données.
   Les dépendances nécessaires sont spécifiées dans le fichier requirements.txt.
   Vous pouvez les installer en exécutant :

```bash
pip install -r requirements.txt
```

## Utilisation


Lancer l'application Kivy en exécutant le fichier main.py :

```bash
python main.py
```

Utilisez l'interface de glisser-déposer ou le bouton pour charger un fichier ou un dossier contenant des logs à analyser. Les résultats seront affichés dans le tableau situé a droite.

En effectuant un [Ctrl]+[clic], vous ouvrirez toute la hiérarchie des fichiers sélectionnés, tandis qu'un simple [clic] ouvrira le dernier fichier de la hiérarchie.

Si vous voulez changer de dossier de logs, vous devez relancer l'application.



