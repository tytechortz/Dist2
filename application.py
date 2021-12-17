import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from pandas.io.json import json_normalize
import pandas as pd
import requests
from homepage import Homepage
from dist2 import dist2_App

# from usgs_sites import USGS_06710247

app = dash.Dash(name=__name__, 
                title="District 2 Data Dashboard",
                assets_folder="static",
                assets_url_path="static")

application = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content'),
    dcc.Interval(
            id='interval-component',
            interval=500*1000, # in milliseconds
            n_intervals=0
        ),
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dist2':
        return dist2_App()
    else:
        return Homepage()



# url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=01646500&parameterCd=00060,00065&siteStatus=all'

englewood_url = 'https://waterservices.usgs.gov/nwis/iv/?format=rdb&indent=on&sites=06711565&parameterCd=00060&siteStatus=all'

union_url = 'https://waterservices.usgs.gov/nwis/iv/?format=rdb&indent=on&sites=06710247&parameterCd=00060&siteStatus=all'





@app.callback(
    [Output('ew-data-raw', 'data'),
    Output('un-data-raw', 'data')],
    Input('interval-component', 'n_intervals'))
def get_dist2_data(n):
    pd.set_option('display.max_columns', None)

    print(n)
    print('SUP')
    ew = pd.read_csv(englewood_url, sep='\t', comment='#')
    un = pd.read_csv(union_url, sep='\t', comment='#')
    
    ew.drop(ew.columns[[1,3,-1]], axis=1, inplace=True)
    un.drop(un.columns[[1,3,-1]], axis=1, inplace=True)
    ew = ew.set_index('datetime')
    un = un.set_index('datetime')
    # print(ew)
    # print(un)
    
    # englewood = ew.iloc[-1,[2,1]]
    # union = un.iloc[-1,[2,1]]
    # print(englewood)
    # print(union)
    
    return ew.to_json(), un.to_json()


@app.callback(
    Output('usgs-data-layout', 'children'),
    Input('ew-data-raw', 'data'))
def get_usgs_data_outlet(data):
    ew = pd.read_json(data)
    print(ew)
    print(type(ew))

    return html.Div([
        html.Div([
            html.H2('USGS Stations')
        ],
            className='row'
        ),
        html.Div([
            html.H6('Englewood Discharge = {}'.format(ew.iloc[-1,-1]))
        ],
            className='row'
        ),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)