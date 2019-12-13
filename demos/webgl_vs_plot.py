import numpy as np

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

import webglviewer
from phi.viz.dash.webgl_util import default_sky


APP = dash.Dash(__name__)
APP.config.suppress_callback_exceptions = True

APP.layout = html.Div([
    html.Button('2D/3D', id='button'),
    html.Div(id='display'),
    dcc.Interval(id='interval', interval=1000)
])

DIM = [50, 50, 50]

WEBGL = webglviewer.Webglviewer(
    id='viewer',
    sky=default_sky(),
    material_type="LIQUID",
    representation_type="SDF"
)


@APP.callback(Output('display', 'children'), [Input('button', 'n_clicks')])
def switch_display(n):
    if n is None:
        return []
    print(n)
    if n % 2 == 0:
        return dcc.Graph(id='graph')
    else:
        return WEBGL


@APP.callback(Output('viewer', 'data'), [Input('interval', 'n_intervals')])
def display_output(n_intervals):
    if n_intervals is None:
        n_intervals = 0
    n_intervals = n_intervals % 5
    arr = np.ones((DIM[0], DIM[1], DIM[2]), dtype="float32")
    arr[n_intervals:n_intervals + int(DIM[0]*0.3), n_intervals:n_intervals + int(DIM[0]*0.3), n_intervals:n_intervals + int(DIM[0]*0.3)] = -1
    return arr


APP.run_server(debug=True, port=8051)
