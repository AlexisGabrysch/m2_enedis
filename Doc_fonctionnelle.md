<h1 style="text-align: center;">Documentation Fonctionnelle</h1>

<div style="text-align: justify;">
Cette documentation a pour but d'expliquer les différents composants de l'application.</div>

# Table des matières
1. [Contexte](#Contexte)
2. [Stats](#Stats)
2.1 [Aperçu des données](#Aperçu_Données)
2.2 [KPI](#KPI)
3. [Graphs](#Graphs)
3.1 [Graphique](#Graphique)
3.2 [Cartographie](#Cartographie)
4. [Prédiction](#Prédiction)

# 1. Contexte

<div style="text-align: justify;">Cette première page correspond à la page d'accueil de notre application. Comme son nom l'indique, elle contextualise le projet en expliquant les objectifs de l'application ainsi que les différentes pages disponibles. Il est possible de rafraîchir les données via l'API.</div>

# 2. Stats
<div style="text-align: justify;">Cet onglet se subdivise en deux pages différentes.</div>

## 2.1 Aperçu des données
<div style="text-align: justify;"> Dans cet onglet, on peut visualiser les données sous forme de tableau et l'exporter en csv via un bouton.

## 2.2 KPI
Cette deuxième page présente les indicateurs de performances que nous avons définis permettant ainsi de familiariser l'utilisateur avec les données.</div>

<div style="text-align: justify;">La possibilité d'explorer les données via un volet de filtre rend l'interface dynamique pour l'utilisateur et permet une meilleure exploitation et exploration du jeu de données.</div>

# 3. Graphs

## 3.1. Graphique
<div style="text-align: justify;">Cette partie permet d'obtenir différents types de visualisation en fonction des variables sélectionnées via le volet dédié. Selon le type des colonnes choisies, les graphiques proposés ne sont pas les mêmes. Il est possible d'ajouter plus d'informations en déterminant une variable spécifique pour les couleurs.</div>

<div style="display: flex; margin-left: 50px;">
    <div style="margin-right: 100px;">
        <u>Graphique en bivarié</u> :
        <ul>
            <li>Nuage de point (Scatter plot)</li>
            <li>Courbe (Line chart)</li>
            <li>Diagramme en bar (bar chart)</li>
        </ul>
    </div>
    <div>
        <u>Graphique en univarié</u> :
        <ul>
            <li>Boîte à moustache (Box plot)</li>
            <li>Histogramme (Hist)</li>
        </ul>
    </div>
</div>

<div style="text-align: justify;">En faisant ça, l'utilisateur visualise les informations qui l'intéressent en choisissant le graphique le plus parlant. Il est possible d'ajouter autant de graphique que l'on souhaite et ainsi de personnaliser son tableau de bord. Chaque graphique peut être téléchargé au format png en cliquant sur le bouton éponyme.
</div>


## 3.2. Cartographie
<div style="text-align: justify;">Cet ongle présente une carte interactive de la répartition des différentes étiquettes DPE du Rhône. Il est possible de zoomer pour avoir plus de détail sur une zone en particulier.</div>

# 4. Prédictions
<div style="text-align: justify;">Cette page prends la forme d'un formulaire et permet de prédire sa consommation énergétique annuelle et son DPE. Pour ce faire, rien de plus simple, il suffit de répondre aux questions posées.</div>