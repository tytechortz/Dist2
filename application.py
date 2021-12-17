import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from homepage import Homepage

app = dash.Dash(name=__name__, 
                title="Environmental Data Dashboard",
                assets_folder="static",
                assets_url_path="static")

application = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content'),
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/stuff':
        return dt_App()
    else:
        return Homepage()


if __name__ == '__main__':
    app.run_server(debug=True)