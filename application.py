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

comm_city_url = 'https://waterservices.usgs.gov/nwis/iv/?format=rdb&indent=on&sites=06714215&parameterCd=00060&siteStatus=all'

ft_lupton_url = 'https://waterservices.usgs.gov/nwis/iv/?format=rdb&indent=on&sites=06721000&parameterCd=00060&siteStatus=all'

d2_url = 'https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrystation/?format=csv&dateFormat=spaceSepToSeconds&fields=stationName%2CmeasDateTime%2CmeasValue&waterDistrict=2'





@app.callback(
    [Output('ew-data-raw', 'data'),
    Output('un-data-raw', 'data'),
    Output('cc-data-raw', 'data'),
    Output('fl-data-raw', 'data'),],
    Input('interval-component', 'n_intervals'))
def get_dist2_data(n):
    pd.set_option('display.max_columns', None)

    print(n)
    print('SUP')
    ew = pd.read_csv(englewood_url, sep='\t', comment='#')
    un = pd.read_csv(union_url, sep='\t', comment='#')
    cc = pd.read_csv(comm_city_url, sep='\t', comment='#')
    fl = pd.read_csv(ft_lupton_url, sep='\t', comment='#')
    d2 = pd.read_csv(d2_url, skiprows=[1])
    d2_header = d2.iloc[0]
    d2 = d2[1:]
    d2.columns = d2_header
    # d2 = d2.drop(d2.columns[[3]], axis=1)
    print(d2.columns)
    print(d2)
    d2.drop([nan])

    
    ew.drop(ew.columns[[1,3,-1]], axis=1, inplace=True)
    ew = ew[1:]
    un.drop(un.columns[[1,3,-1]], axis=1, inplace=True)
    un = un[1:]
    cc.drop(cc.columns[[1,3,-1]], axis=1, inplace=True)
    cc = cc[1:]
    fl.drop(fl.columns[[1,3,-1]], axis=1, inplace=True)
    fl = fl[1:]
    # ew = ew.set_index('datetime')
    # un = un.set_index('datetime')
    print(ew)
    # print(un)
    
    # englewood = ew.iloc[-1,[2,1]]
    # union = un.iloc[-1,[2,1]]
    # print(englewood)
    # print(union)
    
    return ew.to_json(), un.to_json(), cc.to_json(), fl.to_json()


@app.callback(
    Output('usgs-data-layout', 'children'),
    [Input('ew-data-raw', 'data'),
    Input('un-data-raw', 'data'),
    Input('cc-data-raw', 'data'),
    Input('fl-data-raw', 'data'),])
def get_usgs_data_outlet(ew_data, un_data, cc_data, fl_data):
    ew = pd.read_json(ew_data)
    un = pd.read_json(un_data)
    cc = pd.read_json(cc_data)
    fl = pd.read_json(fl_data)
    # print(ew)
    
    

    return html.Div([
        html.Div([
            html.H2('USGS Stations')
        ],
            className='row'
        ),
        html.Div([
            html.H6('Englewood Discharge = {} - {}'.format(ew.iloc[-1,-1], ew.datetime.iloc[-1]))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Union Discharge = {} - {}'.format(un.iloc[-1,-1], un.datetime.iloc[-1]))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Commerce City Discharge = {} - {}'.format(cc.iloc[-1,-1], cc.datetime.iloc[-1]))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Ft. Lupton Discharge = {} - {}'.format(fl.iloc[-1,-1], fl.datetime.iloc[-1]))
        ],
            className='row'
        ),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)