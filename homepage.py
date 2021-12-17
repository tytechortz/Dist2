import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html



body = dbc.Container([
    html.Div([
        html.H2('Home')
    ],
    className='row'
    ),
    dbc.Button("Open App", color="primary", href="/dist2"),
])

def Homepage():
    layout = html.Div([
    body
    ])
    return layout