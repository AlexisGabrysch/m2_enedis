
from dash import dcc, html
from dash.dependencies import Input, Output, State , MATCH, ALL
# Ajouter l'importation de plotly.express
from pyproj import Transformer
from model import Model
from api import API  # Added import of API class
import dash
import pandas as pd
import plotly.express as px
import dash_table
import os
import  uuid
import plotly.io as pio  # Add import for Plotly
import io
import plotly.graph_objects as go
import json


class DashApp:
    def __init__(self):
        # Initialiser l'application Dash
        self.app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
        self.app.title = 'ENEDIS'
        self.server = self.app.server
        
        self.new_data = None    
        self.nl = 0
        self.df = API().get_data()
        self.setup_layout()
        self.setup_callbacks()
        self.convert_coordinates()

    def convert_coordinates(self):
            # Initialisation du transformateur de Lambert-93 (EPSG:2154) vers WGS84 (EPSG:4326)
        transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)

        # Coordonnées en Lambert-93
        y_coords = self.df["Coordonnée_cartographique_X_(BAN)"].values
        x_coords = self.df["Coordonnée_cartographique_Y_(BAN)"].values

        # Conversion des coordonnées en latitude et longitude
        lat_lon_coords = [transformer.transform(y, x) for x, y in zip(x_coords, y_coords)]
        self.df["Coordonnée_cartographique_X_(BAN)"] = [coord[0] for coord in lat_lon_coords]
        self.df["Coordonnée_cartographique_Y_(BAN)"] = [coord[1] for coord in lat_lon_coords]
        print("fin de la conversion")

    def setup_layout(self):
        self.app.layout = html.Div([
                    dcc.Tabs(
                        id="tabs",value='contexte',
                        children=[
                            dcc.Tab(label='Contexte' , value='contexte', className='tab', selected_className='selected-tab'),
                            dcc.Tab(label='Statistiques',value='stats', className='tab', selected_className='selected-tab'),
                                
                            dcc.Tab(label='Visualisations',value='graph', className='tab', selected_className='selected-tab'),
                            dcc.Tab(label='Prédictions',value='prediction', className='tab', selected_className='selected-tab')
                    
                        ]), html.Div(id='tabs-content')
                    ],
                    style={
                        'width': '80%',
                        'margin': '0 auto'
                    }
                )
        

    def render_stats(self):
              return html.Div([  dcc.Tabs(id='stats-subtabs', value='data_sub' , children=[
                                    dcc.Tab(label='Aperçu des Données', value='data_sub', className='subtab_stats', selected_className='selected-tab'),
                                        
                                    dcc.Tab(label='KPI' , value='kpi_sub', className='subtab_stats', selected_className='selected-tab'),
                                        
                                    ]),
                                
                            html.Div(id='stats-content')
                        ])
    

    def render_table_stats(self):
        return html.Div([
                            dash_table.DataTable(
                                id='data-table',
                                columns=[{"name": i, "id": i} for i in self.df.columns],
                                data=self.df.head(100).to_dict('records'),
                                page_size=10,
                                filter_action='native',
                                sort_action='native',
                                fixed_rows={'headers': True},
                                style_table={'overflowX': 'auto'},
                                style_cell={  # Update styles for cells
                                    'width':'100px',  # Set max-width to prevent overflow
                                    'whiteSpace': 'nowrap',
                                    'padding': '2px',          # Reduced padding
                                    'fontSize': '12px',        # Decreased font size
                                    'textAlign': 'center',
                                    'lineHeight': '1',          # Added line height
                                    'border': 'none'  # Remove cell borders
                                },
                                style_header={
                                    'backgroundColor': '#f0f0f0',
                                    'fontWeight': 'bold',
                                    'fontSize': '12px',        # Decreased header font size
                                    'textAlign': 'center',
                                    'lineHeight': '1',          # Added line height
                                    'border': 'none'  # Remove header borders
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': '#fafafa'
                                    }
                                ],
                            ),
                            html.Button("Téléchargement CSV", id="download-button", n_clicks=0, className='download-button'),  # Added download button
                            dcc.Download(id="download-dataframe-csv")  # Added Download component
                        ], className='box')
                    
        


    def render_kpi(self):

        return html.Div([
                            html.H1('Statistiques Avancées'),
                            html.P('Voici quelques indicateurs clés pour mieux comprendre les données.'),
                            html.H3('Filtres' , style={'textAlign': 'center'}), 
                            html.Div(
                                className='filtre-container',
                                style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                                children=[
                                    html.Div(
                                        style={'display': 'flex', 'flexDirection': 'row', 'gap': '20px'},
                                        children=[
                                            html.Div(
                                                className='option-box dropdown-item',
                                                style={'flex': '1', 'maxWidth': '500px'},
                                                children=[
                                                    html.Label("Communes", className='dropdown-label' , style={'textAlign': 'center'}),
                                                    dcc.Dropdown(
                                                        id='commune_filtre',
                                                        options=[{'label': commune, 'value': commune} for commune in self.df['Nom__commune_(BAN)'].value_counts().index],
                                                        multi=True,
                                                        placeholder='Choisissez une ou plusieurs communes'
                                                    ), 
                                                ]
                                            ),
                                            html.Div(
                                                className='option-box dropdown-item',
                                                style={'flex': '1', 'maxWidth': '500px'},
                                                children=[
                                                    html.Label("Période de construction", className='dropdown-label' , style={'textAlign': 'center'}),
                                                    dcc.Dropdown(
                                                        id='periode-filtre',
                                                        options=[{'label': periode, 'value': periode} for periode in self.df['Période_construction'].unique()],
                                                        multi=True,
                                                        placeholder='Choisissez une ou plusieurs périodes de construction'
                                                    ), 
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div( style={'display': 'flex', 'flexDirection': 'row', 'gap': '20px' , 'justifyContent': 'center'},
                                             children=[
                                    html.Div(
                                        className='option-box dropdown-item',
                                        style={'textAlign': 'center' , 'width': '100%'},
                                        children=[
                                            html.Label("Etiquette DPE", className='dropdown-label'),
                                            dcc.Checklist(
                                                id='etiquette_dpe_filtre',
                                                options=[{'label': etiquette, 'value': etiquette} for etiquette in sorted(self.df['Etiquette_DPE'].unique())],
                                                value=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                                                inline=True,  
                                                inputStyle={'margin-right': '10px'}
                                            ), 
                                        ]
                                    )
                                             ]
                                    ),
                                    html.Div(id='filtre-container', style={'display': 'flex','flexDirection': 'row','justifyContent': 'center','alignItems': 'center','width': '100%','textAlign': 'center'})
                                ]
                            ), 
                            html.Div(id='kpi-container', style={
                                'display': 'grid',
                                'gridTemplateColumns': '1fr 1fr',
                                'gap': '20px',
                                'justifyItems': 'center',
                                'alignItems': 'center'
                            })             
                        ], className='box')



    def render_graph_visual(self):
        return html.Div(
                className='box',
                children=[
                    html.H1("Dashboard dynamique - ENEDIS"),
                    html.P("Selectionnez les variables que vous voulez visualiser et le type de chart souhaité."),
                    html.P("Vous pouvez ajouter plusieurs graphiques en cliquant sur le bouton 'Ajouter le graphique'."),
                    html.P("Pour supprimer un graphique, cliquez sur le bouton 'Suppprimer' en bas du graphique."),
                    html.I("La selection de une seule variable est favorable pour des performances optimales."),
                    html.I("On peut réaliser des graphiques de type scatter, line, bar, histogram, box et pie selon les variables choisies."),
                    html.Div(
                    html.I("Le téléchargement des graphiques est possible uniquement en local avec la version 0.1.0.post1 de kaleido" , style={"color": "red"}),
                    ),
                    html.Div([
                        html.Div([
                            html.Label("Selectionne la variable X"),
                            dcc.Dropdown(
                                id='dropdown-x',
                                options=[{'label': col, 'value': col} for col in self.df.columns],
                                value='Variable1'
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
                        html.Div([
                            html.Label("Selectionne la variable Y"),
                            dcc.Dropdown(
                                id='dropdown-y',
                                options=[{'label': col, 'value': col} for col in self.df.columns],
                                value=None
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
                    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                    html.Div([
                        html.Div([
                            html.Label("Selectionne la variable de couleur (Optional)"),
                            dcc.Dropdown(
                                id='dropdown-color',
                                options=[{'label': col, 'value': col} for col in self.df.columns],
                                value=None
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
                        html.Div([
                            html.Label("Selectionne le type de graphique"),
                            dcc.Dropdown(
                                id='dropdown-chart-type',
                                options=[
                                    {'label': 'Scatter', 'value': 'scatter'},
                                    {'label': 'Line', 'value': 'line'},
                                    {'label': 'Bar', 'value': 'bar'},
                                    {'label': 'Histogram', 'value': 'histogram'},
                                    {'label': 'Box', 'value': 'box'},
                                    {'label': 'Pie', 'value': 'pie'},
                                ],
                                value='scatter',
                                placeholder='Select a chart type'
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
                    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
                    html.Button("Ajouter le graphique", id="add-graph-button", n_clicks=0, style={'margin-top': '20px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
                    dcc.Store(id='graphs-store', data=[]),

                    html.Div(
                        id='graph-container',
                        style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px', 'width': '100%'}
                    ),
                    dcc.Download(id="download-plot")
                ]
            )
        
    def render_graph(self):

        return html.Div([

                dcc.Tabs(id="graph-subtabs", value='graphique_sub',  children=[
                        dcc.Tab(label='Graphique' , className='subtab_visu', selected_className='selected-tab' , value='graphique_sub'),

                                        
    
                        dcc.Tab(label='Cartographie' ,  className='subtab_visu', selected_className='selected-tab' , value='cartographie_sub')
                                    ]),
                                
                html.Div(id='graph-content')
                ])
    

    def render_contexte(self):
        return html.Div(children=[
                                html.Div(
                                    className='box',
                                    children=[
                                        html.Div(
                                            className='contexte-section',
                                            children=[
                                                html.H2(
                                                    "Analyse de la consommation énergétique et des étiquettes DPE dans le Rhône",
                                                    style={'textAlign': 'center'}
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className='contexte-section',
                                            children=[
                                                html.H2("Objectifs du projet"),
                                                html.P([
                                                    "La transition écologique est aujourd'hui au cœur des enjeux de société. "
                                                    "Chez GreenTechn, notre ambition est de contribuer activement à ce changement en associant notre expertise technologique aux défis environnementaux. "
                                                    "Pour cela, cette application, conçue pour analyser la consommation énergétique des logements dans le Rhône et les classer selon leur Diagnostic de Performance Énergétique (DPE). "
                                                    "Cette démarche vise à fournir des insights concrets pour soutenir la transition vers des bâtiments plus performants et respectueux de l’environnement. "
                                                    "Ainsi que de prédire la consommation et le DPE des logements. "
                                                    "Les données de ce projet proviennent de l'API de l'",
                                                    html.A("ADEME", href="https://data.ademe.fr/datasets/dpe-v2-logements-existants/api-doc"), "."
                                                ]),
                                            ]
                                        ),
                                        html.Div(
                                            className='contexte-section',
                                            children=[
                                                html.H2("Structure de l'application"),
                                                html.P([
                                                    "L'application se découpe en 4 onglets:"
                                                ]),
                                                html.Ul([
                                                    html.Li("Contexte : "),
                                                    html.Li("Statistiques : "),
                                                    html.Li("Visualisations : visualisation des données"),
                                                    html.Li("Prédiction de la consommation et du DPE de votre logement ")
                                                ]),
                                            ]
                                        ),
                                        html.Div(
                                            className='contexte-section',
                                            children=[
                                                html.H2("Explication DPE"),
                                                html.P(
                                                    "Le Diagnostic de Performance Énergétique (DPE) est un document qui évalue la consommation d'énergie et l'impact environnemental d'un bâtiment ou d'un logement. Il se présente comme cela :"
                                                ),
                                                html.Img(
                                                    src="assets/dpe_contexte.png",
                                                    style={'display': 'block', 'margin': '20px auto', 'max-width': '80%'}
                                                ),
                                                html.P(
                                                    "Le DPE attribue une étiquette énergétique allant de A à G, A étant la meilleure note et G la moins bonne. Cette étiquette est calculée en fonction de la consommation d'énergie du logement et de son impact sur l'environnement."
                                                ),
                                                html.P(
                                                    "Le DPE est un outil essentiel pour informer les propriétaires et les locataires sur la performance énergétique d'un logement. Il permet de sensibiliser les occupants à leur consommation d'énergie et de les encourager à adopter des comportements plus éco-responsables."
                                                ),
                                            ]
                                        ),
                                        
                                        html.Div(
                                            className='box',
                                            children=[
                                                html.H2("Rafraîchissement des données"),
                                                html.P("Cliquez sur le bouton ci-dessous pour rafraîchir les données. Cette opération peut prendre quelques minutes. De plus, les données de l'API sont mises à jour tous les mois seulement."),
                                                html.Div([
                                                    html.Div(id='last-refresh-date', style={'margin-bottom': '10px', 'fontWeight': 'bold'}),
                                                    html.Button('Rafraîchir', id='refresh-button', n_clicks=0),
                                                    dcc.Loading(
                                                        id="loading-refresh",
                                                        type="default",
                                                        children=html.Div(id='refresh-status')
                                                    )
                                                ])]),
                                                # Nouveau compartiment pour réentraîner les données
                                        html.Div(
                                                    className='box',
                                                    children=[
                                                        html.H2("Réentrainement des données"),
                                                        html.P("Cliquez sur le bouton ci-dessous pour réentraîner le modèle avec les dernières données."),
                                                        html.Button('Réentraîner', id='retrain-button', n_clicks=0, className='retrain-button'),
                                                        dcc.Loading(
                                                            id="loading-retrain",
                                                            type="default",
                                                            children=html.Div(id='retrain-status')
                                                        )
                                                        
                                                    ]
                                                    
                                                ),html.Div(
                                            className='contexte-section',
                                            children=[
                                                html.H2("Contributeurs"),
                                                html.P("Les contributeurs de ce projet sont : "),
                                                       html.B("Alexis GABRYSCH, Lucile PERBET et Joël SOLLARI."),
                                            ]
                                        ),
                                                
                                    ])])
                                   
    
    def render_cartographie(self):
    

        fig = px.scatter_mapbox(

            self.df.sample(20000),
            lat="Coordonnée_cartographique_Y_(BAN)",
            lon="Coordonnée_cartographique_X_(BAN)",
            color="Etiquette_DPE",
            size_max=10,
            color_discrete_map={
                'A': '#479E72',
                'B': '#6BAE5E',
                'C': '#ADCA7D',
                'D': '#F3E84F',
                'E': '#E7B741',
                'F': '#DE8647',
                'G': '#C6362C'
            },
            category_orders={
                "Etiquette_DPE": ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            },
            hover_data={
                'Etiquette_DPE': True,
                "Type_bâtiment": True,
                "Conso_5_usages_é_finale": True,
                "Coordonnée_cartographique_X_(BAN)": False,
                "Coordonnée_cartographique_Y_(BAN)": False
            },
            zoom=10,
        )
       
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=10,
            mapbox_center={"lat": 45.75, "lon": 4.85},
            mapbox_bounds={"west": -5, "east": 9, "south": 41, "north": 51},  # Limites de la France métropolitaine
            margin={"r": 0, "l": 0, "b": 0},
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        return html.Div(
            className='box',
            children=[
                html.H3('Carte interactive du DPE dans le Rhones', className='map-title'),  
                html.P('Survolez les points pour plus d\'informations. Cliquez sur les étiquettes pour les afficher ou les masquer. Zoomez (bouton en haut à gauche) et déplacez vous sur la carte pour explorer les données.'), 
                html.I('Les points sont échantillonnés pour des raisons de performance.' , style={"font-size": "10px"}),
                dcc.Graph(figure=fig)
            ],
            style={
                'width': '80%',
                'margin': '10 auto'
            }
        )

    def render_prediction_page_dpe(self):
        return html.Div(
            className='box',  # Main container box
            children=[
                html.Div(
                    className='form-container',
                    children=[
                        html.Div(
                            id='general-info-section',
                            className='form-section active',
                            children=[
                                html.H3('Informations générales sur le logement'),
                                html.Div(
                                    id='building-images',
                                    children=[
                                        dcc.RadioItems(
                                            id='building-type',
                                            options=[
                                                {
                                                    'label': html.Div([
                                                        html.Img(src='assets/images/maison.png', className='building-image'),
                                                        html.Div('Maison', className='image-label')
                                                    ], className='building-type-image'),
                                                    'value': 'Maison'
                                                },
                                                {
                                                    'label': html.Div([
                                                        html.Img(src='assets/images/appartement.png', className='building-image'),
                                                        html.Div('Appartement', className='image-label')
                                                    ]),
                                                    'value': 'Appartement'
                                                },
                                                {
                                                    'label': html.Div([
                                                        html.Img(src='assets/images/immeuble.png', className='building-image'),
                                                        html.Div('Immeuble', className='image-label')
                                                    ]), 
                                                    'value': 'Immeuble'
                                                }
                                            ],
                                            value='Maison',
                                            inline=True,
                                            className='building-type-radioitems'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Période de construction'),
                                        dcc.Dropdown(
                                            id='periode-construction',
                                            options=[
                                                {'label': 'Avant 1950', 'value': 'Avant 1950'},
                                                {'label': '1950-1970', 'value': '1950-1970'},
                                                {'label': '1970-1990', 'value': '1970-1990'},
                                                {'label': '1990-2010', 'value': '1990-2010'},
                                                {'label': 'Après 2010', 'value': 'Après 2010'}
                                            ],
                                            placeholder='Période de construction'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Hauteur sous plafond (m)'),
                                        dcc.Input(
                                            id='hauteur-sous-plafond',
                                            type='number',
                                            placeholder='Hauteur sous plafond'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Nombre de niveaux du logement'),
                                        dcc.Input(
                                            id='nombre-niveau-logement',
                                            type='number',
                                            placeholder='Nombre de niveaux du logement'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Surface habitable du logement (m²)'),
                                        dcc.Input(
                                            id='surface-habitable-logement',
                                            type='number',
                                            placeholder='Surface habitable du logement'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Numéro d\'étage de l\'appartement'),
                                        dcc.Input(
                                            id='numero-etage-appartement',
                                            type='number',
                                            placeholder='Numéro d\'étage de l\'appartement'
                                        )
                                    ]
                                ),
                                html.Div(id='general-info-error', className='error-message'),
                                html.Button('Suivant', id='next-to-isolation', n_clicks=0, className='next-button')
                            ]
                        ),
                        html.Div(
                            id='isolation-info-section',
                            className='form-section hidden',
                            children=[
                                html.H2('Informations sur l\'isolation du logement'),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Qualité de l\'isolation du plancher bas'),
                                        dcc.Dropdown(
                                            id='qualite-isolation-plancher-bas',
                                            options=[
                                                {'label': 'Très mauvaise', 'value': 'Très mauvaise'},
                                                {'label': 'Mauvaise', 'value': 'Mauvaise'},
                                                {'label': 'Moyenne', 'value': 'Moyenne'},
                                                {'label': 'Bonne', 'value': 'Bonne'},
                                                {'label': 'Très bonne', 'value': 'Très bonne'}
                                            ],
                                            placeholder='Qualité de l\'isolation du plancher bas'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Type de toiture'),
                                        dcc.Dropdown(
                                            id='type-toiture',
                                            options=[
                                                {'label': 'Comble aménagé', 'value': 'comble_aménagé'},
                                                {'label': 'Combles perdus', 'value': 'comble_perdu'},
                                                {'label': 'Terrasses', 'value': 'terrasse'}
                                            ],
                                            placeholder='Type de toiture'
                                        )
                                    ]
                                ),
                                html.Div(id='isolation-info-error', className='error-message'),
                                html.Button('Précédent', id='prev-to-general', n_clicks=0, className='prev-button'),
                                html.Button('Suivant', id='next-to-equipment', n_clicks=0, className='next-button')
                            ]
                        ),
                        html.Div(
                            id='equipment-info-section',
                            className='form-section hidden',
                            children=[
                                html.H2('Informations sur les équipements du logement'),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Type d\'énergie principale pour le chauffage'),
                                        dcc.Dropdown(
                                            id='type-energie-principale-chauffage',
                                            options=[
                                                {'label': 'Électricité', 'value': 'Électricité'},
                                                {'label': 'Gaz', 'value': 'Gaz'},
                                                {'label': 'Fioul', 'value': 'Fioul'},
                                                {'label': 'Bois', 'value': 'Bois'},
                                            ],
                                            placeholder='Type d\'énergie principale pour le chauffage'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Type d\'énergie principale pour l\'ECS'),
                                        dcc.Dropdown(
                                            id='type-energie-principale-ecs',
                                            options=[
                                                {'label': 'Électricité', 'value': 'Électricité'},
                                                {'label': 'Gaz', 'value': 'Gaz'},
                                                {'label': 'Fioul', 'value': 'Fioul'},
                                                {'label': 'Bois', 'value': 'Bois'},
                                            ],
                                            placeholder='Type d\'énergie principale pour l\'ECS'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Y a-t-il la climatisation ?'),
                                        dcc.Dropdown(
                                            id='climatisation',
                                            options=[
                                                {'label': 'Oui', 'value': 1},
                                                {'label': 'Non', 'value': 0}
                                            ],
                                            placeholder='Y a-t-il la climatisation ?'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='form-group',
                                    children=[
                                        html.Label('Consommation de chauffage finale (kWh)'),
                                        dcc.Input(
                                            id='conso-chauffage-finale',
                                            type='number',
                                            placeholder='Consommation de chauffage finale'
                                        )
                                    ]
                                ),
                                html.Button('Précédent', id='prev-to-isolation', n_clicks=0, className='prev-button'),
                                html.Button('Predict', id='predict-button', n_clicks=0, className='predict-button')
                            ]
                        ),
                        html.Div(id='prediction-output')
                    ]
                )
            ],
            style={
                'width': '80%',
                'margin': '10 auto'
            }
        )

    def setup_callbacks(self):

        @self.app.callback(
            Output('tabs-content', 'children'),
            [Input('tabs', 'value')]
        )
        def render_tab_content(tab):
            if tab == 'contexte':
                return self.render_contexte()
            elif tab == 'stats':
                return self.render_stats()
            elif tab == 'graph':
                return self.render_graph()
            elif tab == 'prediction':
                return self.render_prediction_page_dpe()

            
        @self.app.callback(
            Output('graph-content', 'children'),
            [Input('graph-subtabs', 'value')]
        )
        def render_graph_content(tab):
            if tab == 'graphique_sub':
                return self.render_graph_visual()
            elif tab == 'cartographie_sub':
                return self.render_cartographie()

        @self.app.callback(
            Output('stats-content', 'children'),
            [Input('stats-subtabs', 'value')]
        )
        def render_stats_content(tab):
            if tab == 'data_sub':
                return self.render_table_stats()
            elif tab == 'kpi_sub':
                return self.render_kpi()
            
            


        @self.app.callback(
            Output("download-dataframe-csv", "data"),
            Input("download-button", "n_clicks"),
            prevent_initial_call=True,
        )
        def download_csv(n_clicks):
            return dcc.send_file("assets/enedis_69.csv")

        @self.app.callback(
            Output('general-info-section', 'className'),
            Output('isolation-info-section', 'className'),
            Output('equipment-info-section', 'className'),
            Input('next-to-isolation', 'n_clicks'),
            Input('prev-to-general', 'n_clicks'),
            Input('next-to-equipment', 'n_clicks'),
            Input('prev-to-isolation', 'n_clicks'),
            State('general-info-section', 'className'),
            State('isolation-info-section', 'className'),
            State('equipment-info-section', 'className')
        )
        def navigate_sections(next_to_isolation, prev_to_general, next_to_equipment, prev_to_isolation,
                              general_info_class, isolation_info_class, equipment_info_class):
            ctx = dash.callback_context
            if not ctx.triggered:
                return general_info_class, isolation_info_class, equipment_info_class

            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'next-to-isolation' and 'active' in general_info_class:
                return 'form-section hidden', 'form-section active', 'form-section hidden'
            elif button_id == 'prev-to-general' and 'active' in isolation_info_class:
                return 'form-section active', 'form-section hidden', 'form-section hidden'
            elif button_id == 'next-to-equipment' and 'active' in isolation_info_class:
                return 'form-section hidden', 'form-section hidden', 'form-section active'
            elif button_id == 'prev-to-isolation' and 'active' in equipment_info_class:
                return 'form-section hidden', 'form-section active', 'form-section hidden'

            return general_info_class, isolation_info_class, equipment_info_class

        @self.app.callback(
            Output('prediction-output', 'children'),
            [Input('predict-button', 'n_clicks')],
            [State('building-type', 'value'),
             State('periode-construction', 'value'),
             State('hauteur-sous-plafond', 'value'),
             State('nombre-niveau-logement', 'value'),
             State('surface-habitable-logement', 'value'),
             State('numero-etage-appartement', 'value'),
             State('qualite-isolation-plancher-bas', 'value'),
             State('type-toiture', 'value'),
             State('type-energie-principale-chauffage', 'value'),
             State('type-energie-principale-ecs', 'value'),
             State('climatisation', 'value'),
             State('conso-chauffage-finale', 'value')]
        )
        def predict(n_clicks, building_type, periode_construction, hauteur_sous_plafond, nombre_niveau_logement,
                    surface_habitable_logement, numero_etage_appartement, qualite_isolation_plancher_bas,
                    type_toiture, type_energie_principale_chauffage, type_energie_principale_ecs, climatisation,
                    conso_chauffage_finale):
            if n_clicks > 0:
                fields = [building_type, periode_construction, hauteur_sous_plafond, nombre_niveau_logement, surface_habitable_logement,
                          numero_etage_appartement, qualite_isolation_plancher_bas, type_toiture,
                          type_energie_principale_chauffage, type_energie_principale_ecs, climatisation, conso_chauffage_finale]

                if any(field is None or field == '' for field in fields):
                    return html.Div('Please fill in all the fields')
                # Create a DataFrame from the input values
                input_data = pd.DataFrame({
                    'Type_bâtiment': [building_type],
                    'Période_construction': [periode_construction],
                    'Hauteur_sous_plafond': [hauteur_sous_plafond],
                    'Nombre_niveau_logement': [nombre_niveau_logement],
                    'Surface_habitable_logement': [surface_habitable_logement],
                    'N°_étage_appartement': [numero_etage_appartement],
                    'Qualité_isolation_plancher_bas': [qualite_isolation_plancher_bas],
                    'Type_isolation_plancher_haut': [type_toiture],
                    'Type_énergie_principale_chauffage': [type_energie_principale_chauffage],
                    'Type_énergie_principale_ECS': [type_energie_principale_ecs],
                    'Climatisation': [climatisation],
                    'Conso_chauffage_é_finale': [conso_chauffage_finale]
                })

                # Specify the columns to be converted to dummy variables
                categorical_columns = ['Type_bâtiment', 'Période_construction', 'Qualité_isolation_plancher_bas', 'Type_isolation_plancher_haut', 'Type_énergie_principale_chauffage', 'Type_énergie_principale_ECS', 'Climatisation']

                # Make a prediction using the model
                model = Model()
                predictions_conso, predictions_etiquette = model.prediction(input_data, categorical_columns)

                # Display the prediction result
                return html.Div([
                    html.H4('Résultat de la prédiction'),
                    html.P(f'La prédiction de la consommation est: {predictions_conso[0]} kWh/an'),
                    html.P(f'L\'étiquette DPE prédite est: {predictions_etiquette[0]}')
                ])
            return ''

        @self.app.callback(
            [Output('refresh-status', 'children'),
             Output('refresh-button', 'children'),
             Output('refresh-button', 'disabled'),
             Output('last-refresh-date', 'children')],  # Added Output for last refresh date
            [Input('refresh-button', 'n_clicks')]
        )
        def refresh_data(n_clicks):
            if n_clicks > 0:
                try:
                    # Disable the button during processing
                    disabled = True
                    status_message = 'En cours de traitement...'

                    # Fetch and save data
                    api = API()
                    df, nl = api.refresher()
                    self.nl += nl
                    if df is not None:
                        print(df)
                        self.df = df
                        
                        # Extract the latest date_reception_dpe
                        if 'Date_réception_DPE' in self.df.columns:
                            latest_date = self.df['Date_réception_DPE'].dropna().sort_values(ascending=False).iloc[0]
                            latest_date_str = f'Dernier rafraîchissement : {latest_date}'
                            self.new_data = True
                    else:
                        latest_date = self.df['Date_réception_DPE'].dropna().sort_values(ascending=False).iloc[0]
                        latest_date_str = f'Dernier rafraîchissement : {latest_date}'
                        self.new_data = None

                    # Update status and button label after processing
                    status_message = f'Données rafraîchies . Nombres de lignes ajoutées : {nl}'
                    button_label = 'Rafraîchi'
                    disabled = False
                    return status_message, button_label, disabled, latest_date_str
                    
            
                except Exception as e:
                    # Handle potential errors
                    status_message = f'Erreur : {str(e)}'
                    button_label = 'Rafraîchir'
                    disabled = False
                    latest_date_str = 'Dernier rafraîchissement : erreur'
                    return status_message, button_label, disabled, latest_date_str

            # Initialize last refresh date on first load
            if 'Date_réception_DPE' in self.df.columns:
                latest_date = self.df['Date_réception_DPE'].dropna().sort_values(ascending=False).iloc[0]
                latest_date_str = f'Dernier rafraîchissement : {latest_date}'
            else:
                latest_date_str = 'Dernier rafraîchissement : inconnu'
            return '', 'Rafraîchir', False, latest_date_str

        @self.app.callback(
            Output('kpi-container', 'children'),
            [Input('commune_filtre', 'value'),
             Input('etiquette_dpe_filtre', 'value'),
             Input('periode-filtre', 'value')]
        )
        def update_kpi_display(communes_select, etiquettes_select, periode_select):
            # Filtrer les données en fonction des communes sélectionnées
            filtered_df = self.df
            if communes_select:
                filtered_df = self.df[self.df['Nom__commune_(BAN)'].isin(communes_select)]

            if etiquettes_select:
                filtered_df = filtered_df[filtered_df['Etiquette_DPE'].isin(etiquettes_select)]
            
            if periode_select:
                filtered_df = filtered_df[self.df['Période_construction'].isin(periode_select)]
            
            # Check if the filtered DataFrame is empty
            if filtered_df.empty:
                return [
                    html.Div([
                        html.H4("Nombre de communes"),
                        html.P("0")
                    ], style={'padding': '20px', 'backgroundColor': '#e7f2f8', 'margin': '10px'}),
                    
                    html.Div([
                        html.H4("Nombre de logements"),
                        html.P("0")
                    ], style={'padding': '20px', 'backgroundColor': '#f9f0d8', 'margin': '10px'}),
                    
                    html.Div([
                        html.H4("Consommation électrique moyenne par an"),
                        html.P("0 kWh/an")
                    ], style={'padding': '20px', 'backgroundColor': '#dff0d8', 'margin': '10px'}),

                    html.Div([
                        html.H4("Type de chauffage le plus courant"),
                        html.P("N/A")
                    ], style={'padding': '20px', 'backgroundColor': '#dff0d8', 'margin': '10px'}),
                ]

            # Calcul des KPI en fonction des données filtrées
            nb_communes = filtered_df['Nom__commune_(BAN)'].nunique()  # Nombre de communes sélectionnées
            nb_logements = len(filtered_df)  # Nombre de logements
            conso = filtered_df['Conso_5_usages_é_finale'].mean()  # Consommation moyenne
            mode_heating_series = filtered_df['Type_énergie_principale_chauffage'].mode()
            mode_heating = mode_heating_series.iloc[0] if not mode_heating_series.empty else "N/A"  # Type de chauffage le plus courant


            # Affichage des KPIs avec les valeurs filtrées
            return [
                html.Div([
                    html.H4("Nombre de communes"),
                    html.P(f"{nb_communes}")
                ], style={'padding': '20px', 'backgroundColor': '#e7f2f8', 'margin': '10px'}),
                
                html.Div([
                    html.H4("Nombre de logements"),
                    html.P(f"{nb_logements}")
                ], style={'padding': '20px', 'backgroundColor': '#f9f0d8', 'margin': '10px'}),
                
                html.Div([
                    html.H4("Consommation électrique moyenne par an"),
                    html.P(f"{conso:.2f} kWh/an")
                ], style={'padding': '20px', 'backgroundColor': '#dff0d8', 'margin': '10px'}),

                html.Div([
                    html.H4("Type de chauffage le plus courant"),  # Updated label
                    html.P(f"{mode_heating}")
                ], style={'padding': '20px', 'backgroundColor': '#dff0d8', 'margin': '10px'}),
            ]



        @self.app.callback(
            Output('type-energie-principale-chauffage', 'options'),
            [Input('commune_filtre', 'value'),
             Input('periode-filtre', 'value')]
        )
        def update_heating_type_options(communes, periods):
            filtered_df = self.df
            if communes:
                filtered_df = filtered_df[filtered_df['Nom__commune_(BAN)'].isin(communes)]
            if periods:
                filtered_df = filtered_df[filtered_df['Période_construction'].isin(periods)]
            heating_types = filtered_df['Type_énergie_principale_chauffage'].dropna().unique()
            options = [{'label': ht, 'value': ht} for ht in sorted(heating_types)]
            return options
        

######################## Graphs Callbacks ########################
                
        # Callback to dynamically update chart-type options based on variable selections
        @self.app.callback(
            Output('dropdown-chart-type', 'options'),
            Input('dropdown-x', 'value'),
            Input('dropdown-y', 'value')
        )
        def update_chart_options(x_var, y_var):
            options = []

            # If only one of x_var or y_var is selected (but not both), show univariate options
            if (x_var and not y_var) or (y_var and not x_var):
                options = [
                    {'label': 'Histogram', 'value': 'histogram'},
                    {'label': 'Box Plot', 'value': 'box'}
                ]
            
            # If both x_var and y_var are selected, show bivariate options
            elif x_var and y_var:
                options = [
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'}
                ]

            return options

        # Unified callback to handle adding and removing graphs
        @self.app.callback(
            Output('graphs-store', 'data'),
            Input('add-graph-button', 'n_clicks'),
            Input({'type': 'remove-button', 'index': ALL}, 'n_clicks'),
            State('dropdown-x', 'value'),
            State('dropdown-y', 'value'),
            State('dropdown-color', 'value'),
            State('dropdown-chart-type', 'value'),
            State('graphs-store', 'data')
        )
        def update_graphs_store(add_clicks, remove_clicks, x_var, y_var, color_var, chart_type, graphs_data):
            ctx = dash.callback_context

            # Check if the add button was clicked
            if ctx.triggered and ctx.triggered[0]['prop_id'] == 'add-graph-button.n_clicks' and add_clicks > 0:
                # Generate a unique ID for each new graph
                graph_id = str(uuid.uuid4())

                # Create the figure based on chart type
                fig = None  # Start with an empty variable
                if x_var and y_var:
                    title = f"{x_var} vs {y_var}"
                elif x_var:
                    title = f"{x_var}"
                elif y_var:
                    title = f"{y_var}"
                if color_var is not None:
                    title = title + f" by {color_var}"
                
                # Handle the different chart types based on selections
                if chart_type == 'scatter' and x_var and y_var:
                    fig = px.scatter(self.df, x=x_var, y=y_var, color=color_var,
                                    title=f"Scatter Plot of " + title)
                elif chart_type == 'line' and x_var and y_var:
                    fig = px.line(self.df, x=x_var, y=y_var, color=color_var,
                                title=f"Line Chart of " + title)
                elif chart_type == 'bar' and x_var and y_var:
                    fig = px.bar(self.df, x=x_var, y=y_var, color=color_var,
                                title=f"Bar Chart of " + title)
                elif chart_type == 'histogram' and x_var and not y_var:
                    fig = px.histogram(self.df, x=x_var, color=color_var,
                                    title=f"Histogram of " + title)
                elif chart_type == 'box' and x_var and not y_var:
                    fig = px.box(self.df, y=x_var, color=color_var,
                                title=f"Box Plot of " + title)
                elif chart_type == 'histogram' and not x_var and y_var:
                    fig = px.histogram(self.df, x=y_var, color=color_var,
                                    title=f"Histogram of {y_var}")
                elif chart_type == 'box' and not x_var and y_var:
                    fig = px.box(self.df, y=y_var, color=color_var,
                                title=f"Box Plot of {y_var}")

                # Avoid UnboundLocalError by ensuring 'fig' is always defined
                if fig:
                    # Center the title for each graph type
                    fig.update_layout(title={'x': 0.5})

                    # Append the new graph's figure along with its ID to the list in the store
                    graphs_data.append({'id': graph_id, 'figure': fig.to_dict(), 'type': chart_type})

            # Check if a remove button was clicked
            elif ctx.triggered and 'remove-button' in ctx.triggered[0]['prop_id']:
                # Extract the ID of the clicked remove button
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                button_id_dict = eval(button_id)  # Convert string back to dict
                graph_id_to_remove = button_id_dict['index']

                # Filter out the graph with the matching ID
                graphs_data = [graph for graph in graphs_data if graph['id'] != graph_id_to_remove]
            
            


            # Return the updated list of graphs
            return graphs_data

        # Callback to render all graphs stored in graphs-store
        @self.app.callback(
            Output('graph-container', 'children'),
            Input('graphs-store', 'data')
        )
        def display_graphs(graphs_data):
            # Render each graph with a "Remove" button
            return [
            html.Div(
                [
                dcc.Graph(figure=fig_dict['figure'], id=fig_dict['id'], style={'width': '100%', 'height': '300px'}, responsive=True),
                html.Button("Supprimer", id={'type': 'remove-button', 'index': fig_dict['id']}, n_clicks=0),
                html.Button("Télécharger", id={'type': 'download-button-graph', 'index': fig_dict['id']}, n_clicks=0),
                dcc.Download(id={'type': 'download-dataframe-png-graph', 'index': fig_dict['id']})
                ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'padding': '10px',
                'border': '1px solid #ccc',
                'margin': '10px',
                'width': '100%',
                }
            ) for fig_dict in graphs_data
            ]

        @self.app.callback(
            Output('download-plot', 'data'),
            Input({'type': 'download-button-graph', 'index': ALL}, 'n_clicks'),
            State('graphs-store', 'data'),
            prevent_initial_call=True,
        )
        def download_graph(n_clicks, graphs_data):
            
            if not any(n_clicks):
                return  # Avoid triggering if no button is actually clicked

            # Find the specific button with an incremented n_clicks
            for i, n_clicks in enumerate(n_clicks):
                if n_clicks:
                    # Retrieve the graph id and data for the clicked button
                    graph_id = graphs_data[i]['id']
                    fig_data = graphs_data[i]['figure']
                    
                    # Convert figure JSON data to a Plotly figure
                    fig = pio.from_json(json.dumps(fig_data))
                    img_bytes = fig.to_image(format="png")

                    # Trigger file download
                    return dcc.send_bytes(img_bytes, filename=f"{graph_id}_plot.png")
            return

        # réentrainement des données
        @self.app.callback(
            [Output('retrain-status', 'children'),
             Output('retrain-button', 'children'),
             Output('retrain-button', 'disabled')],
            [Input('retrain-button', 'n_clicks')]
        )
        
        def retrain_model(n_clicks):
            
            if n_clicks > 0:
                try:
                    # Disable the button during processing
                    disabled = True
                    status_message = 'En cours de traitement...'
                    if self.nl == 0:
                        status_message = 'Erreur : aucune nouvelle donnée à traiter'
                        button_label = 'Réentraîner'
                        disabled = False
                        return status_message, button_label, disabled
                    # Réentrainement du modèle
                    model = Model()
                    model.fine_tuning(self.df)
                    self.convert_coordinates()
                    
                    # Update status and button label after processing
                    status_message = 'Modèle réentrainé'
                    button_label = 'Réentraîné'
                    disabled = False
                    return status_message, button_label, disabled
                except Exception as e:
                    # Handle potential errors
                    status_message = f'Erreur : {str(e)}'
                    button_label = 'Réentraîner'
                    disabled = False
                    return status_message, button_label, disabled

            return '', 'Réentraîner', False

        
    def run(self):
        port = int(os.environ.get('PORT', 8050))
        self.app.run_server(debug=False, host='0.0.0.0', port=port)
