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

url = 'https://waterservices.usgs.gov/nwis/iv/?format=rdb&indent=on&sites=06711565&parameterCd=00060&siteStatus=all'

# url = 'https://waterservices.usgs.gov/nwis/iv/?sites=06710247&parameterCd=00060&startDT=2021-12-16T05:20:25.901-07:00&endDT=2021-12-17T05:20:25.901-07:00&siteStatus=all&format=rdb'



@app.callback(
    Output('usgs-data-raw', 'data'),
    Input('interval-component', 'n_intervals'))
def get_dist2_data(n):
    pd.set_option('display.max_columns', None)

    print(n)
    print('SUP')
    df = pd.read_csv(url, sep='\t', comment='#')
    # usgs_data_raw = pd.read_csv(USGS_06710247)
    # print(df)
    df = df.set_index('datetime')
    print(df)
    discharge = df.iloc[-1,3]
    print(discharge)
    
    return df.to_json()



if __name__ == '__main__':
    app.run_server(debug=True)