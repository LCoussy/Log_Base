# Projet Log Base  

Ce projet permet d'analyser des logs de requêtes SQL bloquées et perdues, de générer des tableaux et des statistiques à partir de ces logs.  
Il fournit une interface utilisateur graphique pour ouvrir des fichiers et afficher les résultats dans une table ou des graphiques.  

## Fonctionnalités  

- **Analyse des requêtes bloquées et perdues**  
- **Génération de tableaux**  
- **Génération de Graphiques statistiques** 

## Structure du projet  

```
├── batchOpen.py # Gestion des fichiers dans les dossiers  

├── data_handler.py # Module pour la gestion des données des logs  

├── MainApp.py # Application Kivy  

├── main.py # Application principale  

├── DragAndDrop.py # Interface de glisser-déposer  

├── DisplayArray.py # Affichage des résultats dans un tableau  

├── DateRangeSelector.py # Fenêtre pour entrer et valider une période de dates (dd/mm/yy) avec bouton de validation  

├── DisplayEncadrement.py # Interface pour sélectionner la date comprenant les boutons "<", ">", "moins" et "plus"  

├── parser.py # Fonctions d'analyse des logs  

├── requirements.txt # Liste des dépendances  

├── README.md # Ce fichier  

├── Display.py # Fichier principal pour l'affichage des données et la navigation dans les fichiers  

├── DisplayStat.py # Affichage des statistiques  

├── FilterFiles.py # Organisation des fichiers en hiérarchie basée sur leurs dates de modification  

├── GetContentLog.py # Gestion de la mise en cache et du traitement des fichiers logs avec Pickle  

├── GraphAverageDailyBlock.py # Affichage du graphique des blocages moyens par jour  

├── GraphBlockPerTables.py # Graphique des blocages par table  

├── GraphDailyBlock.py # Graphique des blocages quotidiens  

├── GraphScreen.py # Affichage d'images de graphiques  

├── HandleSwitch.py # Commutation entre les écrans avec des boutons dans Kivy  

└── processing.py # Validation et traitement d'un dossier avec gestion des erreurs  
```

## Installation (2 possibilités)  

1. **Cloner le dépôt :**  
##### Avec HTTPS  
```bash
git clone https://forge.iut-larochelle.fr/log_base/ihm_kivy.git
```  
##### Avec SSH  
```bash
git clone git@forge.iut-larochelle.fr:log_base/ihm_kivy.git
```  

2. **Télécharger l'archive :**  
##### Rendez-vous à l'adresse suivante et cliquez sur "Code" -> "zip" ou "tar"  
```
https://forge.iut-larochelle.fr/log_base/ihm_kivy
```

## Installation des dépendances  

Copiez le dossier `venv_project` que vous avez reçu sur teams dans le même répertoire que les fichiers du projet. Le chemin devrait ressembler à ceci :  

```
votre_dossier_de_projet/
├── venv_project/
├── batchOpen.py
├── data_handler.py
├── MainApp.py
├── main.py
├── ...
└── README.md
```

## Exécution de l'application  

1. **Naviguez vers le dossier du projet**  
   Utilisez la commande `cd` pour changer de répertoire vers le dossier du projet :  
   ```bash
   cd chemin/vers/votre_dossier_de_projet
   ```

2. **Exécutez le fichier principal**  
   Exécutez le script principal pour lancer l'application :  
   ```bash
   python main.py
   ```

## Utilisation de l'application  

1. **Charger des fichiers ou dossiers de logs**  
   Utilisez la fonction de glisser-déposer prévue dans l'interface pour charger vos fichiers, puis sélectionnez la date de début et de fin de la période sélectionnée.  
   Si la deuxième date est vide, seule la semaine de départ sera utilisée.  

2. **Explorer les fichiers**  
   Vous pourrez naviguer entre les différentes vues pour analyser les **Requêtes bloquées**, les **Requêtes perdues** et consulter les **Statistiques** via les **boutons** situés en bas de l'interface graphique.  

3. **Changement de période**  
   Si vous souhaitez changer la période, vous pouvez utiliser les boutons `<` et `>` pour changer de semaine, ainsi que les boutons `+` et `-` pour ajouter ou soustraire une période.  
   Vous pouvez également modifier la date de la période comme lorsque vous lancez l'application.  

4. **Changer de dossier de logs**  
   Si vous souhaitez changer le dossier contenant les logs, vous devrez relancer l'application.  

---