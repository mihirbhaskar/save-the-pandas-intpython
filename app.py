"""
File: app.py
Description: Contains the front-end of the Dash application
Author: Mihir Bhaskar

Usage instructions:
    1. Install all the relevant libraries if this is your first time running the app. 
       Do this by opening 'Anaconda Prompt', and installing the following:
        
        (a) Install Dash and its components by typing the commands shown here https://stackoverflow.com/questions/49613878/python-install-dash-with-conda
        (b) Install dash table by typing 'conda install -c conda-forge dash-table'
        (c) Install geopy by typing 'conda install -c conda-forge geopy'
    
    2. Enter your Google API key at the start (line 23 of this script) for the geo-coding to work
    3. Run this script, and open the http://(...) link that is displayed in the console with 'Dash is running on ...'
       in your browser
       
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================

google_apikey = ''

# Programs defined in this repo:
from getAddressCoords import getAddressCoords
from filterNearby import filterNearby

# Other libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

app = dash.Dash(__name__)

# =============================================================================
# Reading data
# =============================================================================

df = pd.read_csv('pittCity_final.csv')

tags = df['Tag1'].unique() # Pulling tags from the database to populate the dropdown


# =============================================================================
# Layout section
# =============================================================================

app.layout = html.Div([
    
    # App title
    html.H1('Community Support Search'),
    
    # Address entry, display geocoded lat-long
    html.Div([
        html.Label("Enter your current address:"),
        dcc.Input(id='user-address', value='', type='text')
        ]),
    
    html.Button('Submit', id='submit-user-address', n_clicks = 0),
    
    html.Div([
        html.Label("Enter the maximum distance you want to travel, in miles:"),
        dcc.Input(id='max-travel-dist', value=10, type='number')
        ]),
    
    # Select relevant categories
    html.Div([
        html.Label("Select categories: "),
        dcc.Dropdown(
            id='asset-type',
            options=[{'label': i, 'value': i} for i in tags],
            value=[i for i in tags],
            multi=True
            )
        ]),
    
    # Display appropriately filtered table
    html.Div(id='output-table')
])

# =============================================================================
# Callbacks section
# =============================================================================

@app.callback(
    Output(component_id='output-table', component_property='children'),
   [Input('submit-user-address', 'n_clicks')],
   [State('user-address', 'value')],
   Input('max-travel-dist', 'value'),
   Input('asset-type', 'value')
)
def update_output_div(n_clicks, user_address, max_travel_dist, asset_type):
    # First output value, before user has submitted anything - show blank
    if n_clicks == 0:
        return ''
    
    else:
        # Translate input address into lat-longs 
        user_coords = getAddressCoords(input_address = user_address, api_key = google_apikey)
        
        # Check if address was translated properly - if yes, it should return a tuple
        if type(user_coords) == tuple:
            
            # Filter the data frame with observations that fall within max distance limit
            filtered_data = filterNearby(point = user_coords, data = df, max_dist = max_travel_dist)
            
            # Now filter this data with only the categories the user selected
            filtered_data = filtered_data[filtered_data['Tag1'].isin(asset_type)]
            
            # Finally, select the appropriate columns to display
            filtered_data = filtered_data[['name', 'street', 'zip', 'distance', 'type', 'Tag1', 'Tag2', 'Notes', 'Website']]
            
            # Convert the dataframe into Dash's DataTable for display in the app
            tmpdta = filtered_data.to_dict('rows')
            tmpcols = [{"name": i, "id": i,} for i in (filtered_data.columns)]
            
            return dash_table.DataTable(data = tmpdta, columns = tmpcols)
            
        # If address failed, return the string error message
        else:
            return "Invalid address"
    
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)

