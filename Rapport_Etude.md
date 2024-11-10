# Rapport d'étude

<div style="text-align: justify;">Dans ce rapport, nous allons expliqué les différentes étapes qui nous ont poussé à déterminer notre modèle.</div>

# Table des matières
1. [Choix des variables](#choix-des-variables)
2. [Pré-traitement](#Pre-traitement)
3. [Modèles testés]
4. Modèle Retenu
5. Optimisation du modèle
6. [KPI](#KPI) -- A modifier



# Choix des variables
<div style="text-align: justify;">La première étape avant de définir notre modèle a été de sélectionné des variables pertinentes. En effet, en requêtant toutes les données de l'API, 242 colonnes sont récupérés dont certaines. Nous avons fais le choix de réduire largement ce nombre de features pour obtenir un modèle plus rapide et moins lourd.</div>

Nos colonnes ont été sélectionné de manière arbitraire, nous avons pris en compte celle qui nous semblait utile.

Nos variables finales pour prédire l'étiquette DPE et la consommation énergétique sont Type_bâtiment,Période_construction,Surface_habitable_logement,Hauteur_sous-plafond,N°_étage_appartement,N°_département_(BAN),Nombre_niveau_logement,
Qualité_isolation_plancher_haut_toit_terrase,Qualité_isolation_plancher_haut_comble_aménagé,Qualité_isolation_plancher_haut_comble_perdu,Qualité_isolation_plancher_bas,Type_énergie_principale_chauffage,Type_énergie_principale_ECS,Type_énergie_climatisation,om__commune_(BAN),Code_INSEE_(BAN),Coordonnée_cartographique_X_(BAN),Coordonnée_cartographique_Y_(BAN),Conso_chauffage_é_finale,Conso_éclairage_é_finale,Conso_ECS_é_finale,Conso_refroidissement_é_finale,Conso_auxiliaires_é_finale,Coût_total_5_usages + Date réception DPE + _id + N°DPE

# Pré-traitement
## Variables catégorielles
<div style="text-align: justify;">Avant de pouvoir implémenter nos modèles, nous avons du effectuer un traitement de données. En effet, 10 features sont catégorielles et donc supportées directement dans un modèle de machine learning. La fonction *get_dummies* de la librairie Pandas permet de transformer les données en binaire. Cela a pour conséquence d'augmenter la quantité de variables. Nous en avons donc **XXXX** qui entre dans nos modèles.</div>

## Valeurs manquantes
<div style="text-align: justify;">Sur le jeu de données beaucoup des valeurs sont manquantes. Au vu de la grande quantité de lignes que nous avons, nous supprimons toutes les lignes possédant des vides.</div>

Mettre les différentes taille avant et après suppression des NA.

## Doublons
<div style="text-align: justify;">Avec l'API, nous récupérons des données en doubles qui sont supprimées.</div>

## Standardisation des données
Les données ont été standardisé comme les variables ne sont pas toutes à la même échelle. PAS SUR A DIRE : **La standardisation n'a pas eu d'impact significatif sur l'amélioration du modèle, nous démontrerons cela dans la partie suivante. Nous avons quand même fait le choix de le faire puisque cela assure que nos données soient plus facilement interprétable sur nos données**

# Modèles testés
<div style="text-align: justify;">Désormais, toutes nos variables sont prêtes pour lancer nos modèles et déterminer la prédiction de la consommation d'énergie et l'étiquette DPE.</div>

(préciser les différents modèles testés + métrique + interprétation) -- Tout réunir avec la partie suivante ??

# Modèle retenue
Nous avons donc choisi de partir sur un modèle prédisant nos deux variables cibles. PQ ? : **Cela économise en espace de n'avoir qu'un modèle plus tôt que deux** ???. Ainsi, notre choix s'est porté sur un Random Forest Regressor. Cependant, pour faire cela, il a fallu transformer la variable DPE en quantitative. Chaque lettre de l'étiquette est devenue un chiffre.
<p align="center">A = 1 |
B = 2 |
C = 3 |
D = 4 |
E = 5 |
F = 6 |
G = 7 </p>

Maintenant, toutes nos données sont prêtes pour je ne sais trop quoi.

# KPI
Quatre indicateurs clés de performances sont visibles dans l'application : 
- Nombre de logements
- Nombre de communes
- Consommation moyenne
- L'étiquette DPE la plus récurrente

<U>Nombre de logements</U> : Cet indicateur permet de mesurer la consommation énergétique dans le contexte du nombre d'habitations.

<U>Nombre de communes</U> : Cet indicateur permet de contextualiser la consommation énergétique sur un territoire plus large, en offrant une vue d'ensemble de la répartition géographique des consommations.

<U>Consommation moyenne</U> : La consommation moyenne par logement, commune ou période de constrcution est essentielle pour établir des comparaisons, identifier des anomalies ou des tendances.

<U>L'étiquette la plus récurrente</U> : Cet indicateur donne une idée de l'efficacité énergétique globale des logements dans une commune ou région choisie selon les filtres.