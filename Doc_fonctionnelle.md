<h1 style="text-align: center;">Documentation Fonctionnelle</h1>

<div style="text-align: justify;">
Cette documentation a pour but d'expliquer les différents composants de l'application.</div>

# Table des matières
1. [Page Contexte](#Contexte)
2. [Page Stats](#Statistique) -- Ajouter sous onglets
3. [Page Visualisations](#Visualisations)
3.1 [Page Graphiques](#Graphiques)
3.2 [Page Cartographie](#Cartographie)
4. [Page Prédiction](#Prédiction)

 Ajouter le rachraissement des données via l'api + Réentraînement du modèle dans la bonne page

# 1. Contexte

<div style="text-align: justify;">Cette première page correspond à la page d'accueil de notre application. Comme son nom l'indique, elle contextualise le projet en expliquant les objectifs de l'application ainsi que les différentes pages disponibles sur l'application.</div>

# 2. Statistiques
<div style="text-align: justify;">Cette deuxième page présente les indicateurs de performances que nous avons définis permettant ainsi de familiariser l'utilisateur avec les données. Dans cet onglet, un tableau les présentant est disponible.</div>

<div style="text-align: justify;">La possibilité d'explorer les données via un volet de filtre rend l'interface dynamique pour l'utilisateur et permet une meilleure exploitation et exploration du jeu de données.</div>

# 3. Visualisations
<div style="text-align: justify;">Cet onglet est un peu particulier puisqu'il se subdivise en deux pages différentes : l'analyse graphique et la cartographie.</div>

## 3.1. Graphiques
<div style="text-align: justify;">Cette partie permet d'obtenir différents types de visualisation en fonction des variables sélectionnées via le volet dédié. Selon le type des colonnes choisies, les graphiques proposés ne sont pas les mêmes. Il est possible d'ajouter plus d'informations en déterminant une variable spécifique pour les couleurs.</div>

<div style="display: flex; margin-left: 50px;">
    <div style="margin-right: 100px;">
        <u>En Bivarié</u> :
        <ul>
            <li>Nuage de point (Scatter plot)</li>
            <li>Courbe (Line chart)</li>
            <li>Diagramme en bar (bar chart)</li>
        </ul>
    </div>
    <div>
        <u>En Univarié</u> :
        <ul>
            <li>Boîte à moustache (Box plot)</li>
            <li>Histogramme (Hist)</li>
        </ul>
    </div>
</div>

<div style="text-align: justify;">En faisant ça, l'utilisateur visualise les informations qui l'intéressent en choisissant le graphique le plus parlant.Chaque graphique peut être téléchargé au format png en cliquant sur le bouton éponyme.
</div>


## 3.2. Cartographie
<div style="text-align: justify;">Cet ongle présente une carte interactive des différentes étiquettes DPE du Rhône. Il est possible de zoomer pour avoir plus de détail sur une zone en particulier.</div>

# 4. Prédictions
<div style="text-align: justify;">Cette page prends la forme d'un formulaire et permet de prédire sa consommation énergétique annuelle et son DPE. Pour ce faire, rien de plus simple, il suffit de répondre aux X questions posées de cet onglet.</div>