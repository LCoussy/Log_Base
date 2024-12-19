# Projet Log Base

Ce projet permet d'analyser des logs de requêtes SQL bloquées et perdues, de générer des tableaux et des statistiques à partir de ces logs. 
Il fournit également une interface utilisateur graphique pour ouvrir des fichiers ou des dossiers et afficher les résultats dans une table.

## Fonctionnalités

- **Analyse des requêtes bloquées**
- **Interface utilisateur**
- **Génération de tableaux**
- **Génération de statistiques**
  
## Structure du projet
```
├── batchOpen.py # Gestion des fichiers dans les dossiers 

├── data_handler.py # Module pour la gestion des données des logs 

├── MainApp.py # Application Kivy 

├── main.py # Application principale 

├── DragAndDrop.py # Interface de glisser-déposer 

├── DisplayArray.py # Affichage des résultats dans un tableau 

├── DisplayLogTree.py # Interface pour explorer et sélectionner des fichiers logs

├── parser.py # Fonctions d'analyse des logs

├── requirements.txt # Liste des dépendances 

├── README.md # Ce fichier 

├── Display.py # fichiers principal pour l'affichage des données et la navigation dans les fichiers

├── DisplayStat.py #

├── FilterFiles.py # Organisation des fichiers en hiérarchie basée sur leurs dates de modification

├── GetContentLog.py # Gestion de la mise en cache et du traitement des fichiers log avec Pickle

├── GraphAverageDailyBlock.py # Affichage des graphique des blocages moyens par jour

├── GraphBlockPerTables.py # Graphique des blocages par table

├── GraphDailyBlock.py # Graphique des blocages quotidiens

├── GraphScreen.py # Affichage d'images de graphiques 

├── HandleSwitch.py # Commutation entre les écrans avec des boutons dans Kivy.

└── processing.py # Valide et traite un dossier avec gestion d'erreur.

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
   Vous pouvez récuperer les dépendances nécessaires en allant sur Build -> Artifacts, et télécharger la derniere version sortie


## Utilisation
Lancez l'application Kivy en exécutant le fichier principal main.py :

```py
python main.py
```

### Interface Utilisateur
Glisser-déposer ou bouton pour charger des fichiers/dossiers logs
Vous pouvez charger un fichier ou un dossier contenant des logs SQL à analyser via l'interface graphique.

Exploration des fichiers


### Changement entre les vues
Vous pouvez basculer entre les vues de "Requêtes bloquées", "Requêtes perdues" et les "Statistiques" via les boutons en bas.


Si vous souhaitez changer de dossier de logs, relancez l'application.

