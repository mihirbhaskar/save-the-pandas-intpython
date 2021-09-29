"""
File: app.py
Description: Contains the front-end of the Dash application
Author: Mihir Bhaskar

Usage instructions:
    1. Install Dash and its components by opening 'Anaconda Prompt' and typing commands
        shown at this link: https://stackoverflow.com/questions/49613878/python-install-dash-with-conda
    2. Enter your Google API key at the start for the geo-coding to work
"""

google_apikey = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'

from getAddressCoords import getAddressCoords # program defined in this repo
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

app = dash.Dash(__name__)

# =============================================================================
# Layout section
# =============================================================================

app.layout = html.Div([
    
    # App title
    html.H1('Community Support Search'),
    
    # Address entry, display geocoded lat-long
    html.Div([
        "Enter your current address: ",
        dcc.Input(id='user-address', value='', type='text')
        ]),
    
    html.Button('Submit', id='submit-user-address', n_clicks = 0),
    
    html.Br(), # adds a line break
    html.Div(id='geocoded-user-address'),
    
])

# =============================================================================
# Callbacks section
# =============================================================================

@app.callback(
    Output(component_id='geocoded-user-address', component_property='children'),
   [Input('submit-user-address', 'n_clicks')],
   [State('user-address', 'value')] 
)
def update_output_div(n_clicks, input_value):
    # First output value, before user has submitted anything - show blank
    if n_clicks == 0:
        return ''
    
    # Return the output from the getAddressCoords function
    else:
        return getAddressCoords(input_address = input_value, api_key = google_apikey)
    
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)

