"""
File: app.py
Description: Contains the front-end of the Dash application
Authors: Mihir Bhaskar, Anna (Qi)

Usage instructions:
    1. Install Dash and its components by opening 'Anaconda Prompt' and typing commands
        shown at this link: https://stackoverflow.com/questions/49613878/python-install-dash-with-conda
    2. Enter your Google API key at the start for the geo-coding to work
"""

google_apikey = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'

import json
import requests
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
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=' 
           + input_value + '&key=' + google_apikey)
    response = requests.get(url)
    
    if n_clicks == 0:
        return ''
    
    else:
        # Need to check this bit of code
        # Based on if response status code was successful, returns lat-long or says invalid address
        if response.status_code == 200:
            
            result = json.loads(response.text)
            
            lat = result['results'][0]['geometry']['location']['lat']
            long = result['results'][0]['geometry']['location']['lng']
    
            return 'Latitude: {:.2f}, Longitude: {:.2f}'.format(lat, long)   
        
        # Flagging if there was an error
        else:
            return "Invalid address"
    
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)

