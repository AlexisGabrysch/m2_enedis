# Rapport d'étude

<div style="text-align: justify;">Dans ce rapport, nous allons expliquer les différentes étapes qui nous ont poussés à déterminer notre modèle et présenter les KPIs.</div>

# Table des matières
1. [Choix des variables](#1-choix-des-variables)
2. [Pré-traitement](#2-pré-traitement)
2.1 [Création de variables](#21-création-de-variables)
2.2 [Doublons](#22-doublons)
2.3 [Valeurs manquantes](#23-valeurs-manquantes)
2.4 [Variables catégorielles](#24-variables-catégorielles)
2.5 [Standardisation des données](#25-standardisation-des-données)
3. [Modèles](#3-modèles)
3.1 [KNN](#31-knn)
3.2 [MLPClassifier](#32-mlpclassifier)
3.3 [XGBoost](#33-xgboost)
3.4 [Random Forest Regressor](#34-random-forest-regressor)
4. [KPI](#4-kpi)



# 1. Choix des variables
<div style="text-align: justify;">La première étape avant de définir notre modèle a été de sélectionner des variables pertinentes. En effet, en requêtant toutes les données de l'API, 242 colonnes sont récupérées. Nous avons fait le choix de réduire largement ce nombre de features pour ne garder uniquement celle impactante dans le modèle.</div>

Les colonnes que nous avons retenu ont été choisies sur plusieurs critères: 
- Le premier est la [méthode de 3CL](https://www.ecologie.gouv.fr/sites/default/files/documents/notice_DPE.pdf). C'est une méthode qui permet de calculer le DPE en fonction des caractéristiques du logements.

- Le second est que nous avons obervé d'autres simulateurs de DPE ce qui nous a permis d'avoir un aperçu de ce qui était important. 

Les variables qui ont été utiles pour la prédiction sont : 
Nos variables finales pour prédire l'étiquette DPE et la consommation énergétique sont 
- Type_bâtiment
- Période_construction
- Surface_habitable_logement
- Hauteur_sous-plafond
- N°_étage_appartement
- Nombre_niveau_logement
- Qualité_isolation_plancher_haut_toit_terrase
- Qualité_isolation_plancher_haut_comble_aménagé
- Qualité_isolation_plancher_haut_comble_perdu
- Qualité_isolation_plancher_bas
- Type_énergie_principale_chauffage
- Type_énergie_principale_ECS
- Type_énergie_climatisation
- Conso_chauffage_é_finale

Dans nos modèles, ces données sont également celles qui ont le plus d'impact.
# 2. Pré-traitement
## 2.1 Création de variables
Pour optimiser nos modèles, certaines variables ont été recodées pour en créer de nouvelles comme Qualité_isolation_plancher_haut qui prend les modalités de ces trois variables:
- Qualité_isolation_plancher_haut_toit_terrassse
- Qualité_isolation_plancher_haut_comble_aménagé
- Qualité_isolation_plancher_haut_comble_perdu

Il en va de même pour la climatisation qui été recodée. Si une valeur est présente dans Type_énergie_climatisation alors la variable prend 1 sinon 0.

## 2.2 Doublons
<div style="text-align: justify;">Sur notre jeu de données d'entrainement obtenu avec l'API, certaines lignes étaient en double. En conséquence, les doublons ont été supprimés</div>

## 2.3 Valeurs manquantes
<div style="text-align: justify;">Sur le jeu de données beaucoup des valeurs sont manquantes. Au vu de la grande quantité de lignes que nous avons, nous supprimons toutes les lignes possédant des vides.</div>

## 2.4 Variables catégorielles
<div style="text-align: justify;">
L'étape de traitement suivante a été d'encoder toutes les variables catégorielles pour qu'elles puissent entrer dans un modèle de régression grâce à un get_dummies.</div>

## 2.5 Standardisation des données
Les données ont été standardisées comme les variables ne sont pas toutes à la même échelle.

# 3. Modèles
<div style="text-align: justify;">Désormais, toutes nos variables sont prêtes pour lancer nos modèles et déterminer la prédiction de la consommation d'énergie et l'étiquette DPE.</div>

Nous avons testé plusieurs modèles avec toujours la même stratégie. Une séparation en train/test sur les données du Rhône puis une interprétation des métriques : 
- R² pour la consommation énergétique
- L'accuracy pour l'étiquette DPE.

## 3.1 KNN
Nous avons testé le KNN pour prédire uniquement l'étiquette DPE. Notre accuracy est de 0.57, donc 57% de nos étiquettes ont été prédites correctement, ce qui est peu. Pour améliorer ça nous sommes parties sur une autre approche.

## 3.2 MLPClassifier
Cet algorithme pour la classification des étiquettes DPE est encourageant puisque qu'il prédit à 0.82% les bonnes valeurs.

Nous avons fait le choix de tester des modèles de régression et ainsi tenter de prédire le DPE et la consommation énergétique avec un seul et unique modèle. Même si cette approche peut sembler contre-intuitive de prime abord, les deux variables étant corrélées, les modèles prédisant les deux ont de très bonnes performances.Le second avantage permet de ne manipuler qu'un seul modèle au lieu de deux. Pour que cela fonctionne la variable DPE a du être recodée en quantitatif. Chaque lettre de l'étiquette est devenue un chiffre.
<p align="center">A = 1 |
B = 2 |
C = 3 |
D = 4 |
E = 5 |
F = 6 |
G = 7 </p>

Le premier modèle de multioutput que nous avons mis en place est celui de XGBoost.

## 3.3 XGBoost 
Le XGBoost nous a permis d'entraîner un modèle sur la prédiction. L'accuracy était de 0.47 pour les étiquettes DPE et pour la consommation le R² était de 0.72 La prédiction n'est pas optimale surtout pour le DPE. A l'inverse pour le R², cela signifie que 72% de la consommation est expliquée par nos variables en entrée.


## 3.4 Random Forest Regressor
Ainsi, notre choix s'est porté sur un Random Forest Regressor. En effet, ces performances ne sont pas discutables comparées aux autres modèles décrit précedemment. En effet, l'accuracy pour les étiquettes DPE est de 0.87 et le R² est de 0.98. Cet algorithme est très performant pour prédire la consommation énergétique. L'accuracy obtenue est le meilleur comparé aux autres algorithmes. Ce sont pour ces raisons que notre modèle de prédcition est celui-ci.

# 4. KPI
Quatre indicateurs clés de performance sont visibles dans l'application : 
- Nombre de logements
- Nombre de communes
- Consommation moyenne
- Le type de chauffage le plus courant

<U>Nombre de logements</U> : Cet indicateur permet de contextualiser les données notamment sur le nombre de logement concerné.

<U>Nombre de communes</U> : Cet indicateur permet de donner un cadre géographique à l'utilisateur.

<U>Consommation moyenne</U> : La consommation moyenne par logement permet d'établir des comparaisons, identifier des anomalies ou des tendances.

<U>Le type de chauffage le plus courant</U> : Cet indicateur donne un aperçu du mode de chauffage le plus utilisé. Ce qui peut impacter grandement la consommation énergétique et donc le DPE.
