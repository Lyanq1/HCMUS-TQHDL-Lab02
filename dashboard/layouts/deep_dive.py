from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

def create_deepdive_layout(df):
    categories = df['category'].unique().tolist()

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Deep Dive Analysis"),
                html.P("Filter and explore specific segments", className="text-muted")
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.Label("Select Category:"),
                dcc.Dropdown(
                    id='category-filter',
                    options=[{'label': cat, 'value': cat} for cat in categories],
                    value=categories[0]
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='deepdive-chart')
            ], width=12),
        ])
    ], fluid=True)
