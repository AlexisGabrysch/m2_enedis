# M2_enedis

Le projet M2 Enedis est une application de data science visant à prédire la performance énergétique (DPE) des logements ainsi que leur consommation énergétique dans le département du Rhône. 

Cette application, permet d'explorer les données de performance énergétique grâce à des visualisations interactives, et offre des prédictions basées sur des données extraites de l'API de l'[ADEME]( https://data.ademe.fr/datasets/dpe-v2-logements-existants/api-doc). 

L'application a été entièrement réalisée en Python, en utilisant Dash pour la création de l'interface utilisateur.

## Table des matières
- [Auteurs](#auteurs)
- [Méthodologie](#méthodologie)
- [Structure de l'application](#structure-de-lapplication)
- [Structure du code](#strcuture-du-code)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [TUTO](#tuto)

## Auteurs

Le projet, `m2_enedis`, a été développé par:

- Alexis GABRYSCH
- Joël SOLLARI
- Lucile PERBET

## Méthodologie

Notre approche consiste à utiliser un seul modèle de régression pour prédire à la fois l'étiquette DPE et la consommation énergétique des logements. Cette méthode permet de simplifier la maintenance du modèle en concentrant les efforts d’optimisation sur une unique architecture, tout en exploitant la corrélation entre le DPE et la consommation énergétique pour améliorer les prédictions.

Nous sommes parties sur Random Forest Regressor pour obtenir des bonnes performances pour les prédictions.

## Structure de l'application
- **Contexte** : Cette page vous présente les objectifs de l'application. Il est possible de rafraîchir les données via l'API.
- **Statistiques** : Dans cet onglet, on visualise les données sous forme de tableau avec la possibilité de le télécharger en CSV. Vous avez aussi une vue sur les différents KPI implémentés.
- **Visualisations** : Il est possible de créer ses propres graphiques pour analyser et comprendre les enjeux de la consommation énergétique. Une carte du Rhône est disponible pour visualiser la répartition des étiquettes DPE à travers le département.
- **Prédictions** : En saisissant les informations demandées, vous obtiendrez la prédiction de votre logement.

## Strcuture du code
Le code s'organise autour de 4 fichiers : 
`api.py` : Pour récupérer les données via l'API
`model.py` : Pour réaliser les prédictions
`UI.py` : Contient tous le code pour l'application dash
`main.py`: Lancer l'application dash

## Installation
1. Récupération du répertoire

```bash
git clone https://github.com/AlexisGabrysch/m2_enedis.git
```

2. Installations des librairies nécessaires
```bash
pip install -r requirements.txt
```

## Utilisation

L'application peut-être visualiser de deux manières différentes soit en ligne soit en locale.

Si vous préférez la version locale
- Exécutez le code suivant :

```bash
python main.py
```
- Ensuite, allez à l'adresse suivant : 
http://127.0.0.1:8050/

Si vous préférez la version en ligne
- Suivez ce lien : https://m2-enedis-fw9e.onrender.com/

## TUTO
Lien de la vidéo Youtube pour expliquer l'application: 
https://youtu.be/AmfYefkkPvM
