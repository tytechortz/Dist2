import dash
from dash import html
from dash import dcc

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

def get_ice_header():

    header = html.Div([
        html.Div([
            html.H3('District 2', style={'text-align': 'center'}),
        ],
            className='row'
        ),
    ])

    return header


def get_nav_bar():
    navbar = html.Div([
        html.Div([
            html.Div([], className='col-2'),
            html.Div([
                dcc.Link(
                    html.H6(children='Home'),
                    href='/homepage'
                )
            ],
                className='col-2',
                style={'text-align': 'center'}
            ),
            html.Div([], className = 'col-2')
        ],
            className = 'row',
            style = {'background-color' : 'dark-green',
                    'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
        ),
    ])

    return navbar

def get_emptyrow(h='15px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow

def dist2_App():
    return html.Div([
        get_nav_bar(),
        get_emptyrow(),
        html.Div(id='usgs-data-layout'),
        dcc.Store(id='ew-data-raw'),
        dcc.Store(id='un-data-raw'),
        dcc.Store(id='cc-data-raw'),
        dcc.Store(id='fl-data-raw')
    ])

app.layout = dist2_App