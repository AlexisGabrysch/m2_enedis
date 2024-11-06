# Description: This file contains the DashApp class which is used to create a Dash app with multiple tabs.
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

class DashApp:
    def __init__(self, DataFrame):
        # Initialize the API and get the dataframe
     
        # Initialize the Dash app
        self.app = dash.Dash(__name__)
        self.app.title = 'ENEDIS'
        self.server = self.app.server

        self.df = DataFrame
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Contexte', children=[
                    html.Div([
                        html.H1('Contexte'),
                        html.P('This project is created to demonstrate the use of Dash with multiple tabs.')
                    ])
                ]),
                dcc.Tab(label='Data', children=[
                    html.Div([
                        html.H1('Data'),
                        html.Table([
                            html.Thead(
                                html.Tr([html.Th(col) for col in self.df.columns])
                            ),
                            html.Tbody([
                                html.Tr([
                                    html.Td(self.df.iloc[i][col]) for col in self.df.columns
                                ]) for i in range(min(len(self.df), 5))
                            ])
                        ])
                    ])
                ]),
                dcc.Tab(label='Graph', children=[
                    html.Div([
                        html.H1('Graph'),
                        dcc.Graph(
                            id='histogram',
                            figure=px.histogram(self.df, x='Période_construction' , title='Histogram of Période_construction')
                        )
                    ])
                ])
            ])
        ])

    def run(self):
        port = int(os.environ.get('PORT', 8050))
        self.app.run_server(debug=False, host='0.0.0.0', port=port)