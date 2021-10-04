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

google_apikey = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'

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
from tkinter import *
from numpy import longcomplex
import csv
import tkinter.messagebox

app = dash.Dash(__name__)

# =============================================================================
# Reading data
# =============================================================================

df = pd.read_csv('MainFrame.csv', index_col=0)

# Pulling column names from df to serve as options to populate the dropdown
tags = ['Clothing', 'Food', 'Household Goods', 'Housing', 'Training and other services']

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
    
    # Display appropriately filtered and formatted table (# table is formatted in the callback section below)
    # The style tag here centres the output
    html.Div(id='output-table'), # style={'width':'80%', 'margin': '0 auto'}) - play with this code
    
    # Button to update data
    html.Button('Click to submit your own data', id='submit-data'),
    html.Div(id='output-container-button')

    ])

# =============================================================================
# Callback for the main user search and filtering section
# =============================================================================

@app.callback(
    Output(component_id='output-table', component_property='children'),
   [Input('submit-user-address', 'n_clicks')],
   [State('user-address', 'value')],
   Input('max-travel-dist', 'value'),
   Input('asset-type', 'value')
)
def search_output_div(n_clicks, user_address, max_travel_dist, asset_type):
    # First output value, before user has submitted anything - show blank
    if n_clicks == 0:
        return ''
    
    else:
        # Translate input address into lat-longs 
        user_coords = getAddressCoords(input_address = user_address, api_key = google_apikey)
        
        # Check if address was translated properly - if yes, it should return a tuple
        if type(user_coords) == tuple:
            
            # =============================================================================
            # Filtering the data according to parameters            
            # =============================================================================
            
            # Filter the data frame with observations that fall within max distance limit, using a user-defined program
            fdata = filterNearby(point = user_coords, data = df, max_dist = max_travel_dist)
            
            # Now filter this data with only the categories the user selected
            
            # First step: create a flag variable that takes 1 if any of the relevant categories have '1' 
            fdata['Keep'] = 0
            
            # Asset_type is a list of categories that users have selected
            for i in asset_type:
                fdata.loc[fdata[i] == 1, 'Keep'] = 1
                
            # Keep the appropriate rows
            fdata = fdata[fdata['Keep'] == 1]
            
            # =============================================================================
            # Format the data for presenting it in the front-end table            
            # =============================================================================
            
            # Combine the information in dummy columns to one column with comma-separated services provided
            fdata['support provided'] = ''
    
            for i in tags: # Note: tags is defined at the top of the script, as the list of service categories
                fdata.loc[fdata[i] == 1, 'support provided'] += i + ',' # Concat on the service name (column name) if it's value is 1
            fdata['support provided'] = fdata['support provided'].str[:-1] # Strip the last comma 
            
            # Round the distance in miles column to 2 decimal places
            fdata['distance in miles'] = fdata['distance in miles'].round(2)
            
            # Select the appropriate columns to display
            fdata = fdata[['name', 'support provided', 'vicinity', 'distance in miles']]
                                    
            # Convert the dataframe into Dash's DataTable for display in the app
            tmpdta = fdata.to_dict('rows')
            tmpcols = [{"name": i, "id": i,} for i in (fdata.columns)]
            
            # Return a well-formatted dash table
            return dash_table.DataTable(data = tmpdta, columns = tmpcols,
                                        fixed_rows={'headers': True},
                                        fill_width=False,
                                        
                                        
                                        # Need to play around with this code
                                        # style_cell_conditional=[
                                        #     {'if': {'column_id': 'name'},
                                        #      'width':'40%'},
                                        #     {'if': {'column_id': 'support provided'},
                                        #      'width': '20%'},
                                        #     {'if': {'column_id': 'vicinity'},
                                        #      'width':'30%'},
                                        #     {'if': {'column_id': 'distance in miles'},
                                        #      'width': '10%'},
                                        #     ],

                                        style_data={'height': 'auto'})
            
        # If address failed, return the string error message
        else:
            return "Invalid address" ''
        

# =============================================================================
# Callback for the data entry section
# =============================================================================
@app.callback(
    Output(component_id='output-container-button', component_property='children'),
    Input('submit-data', 'n_clicks')
)
def data_entry_div(n_clicks):
    
    if n_clicks is not None:

        root=Tk()
        root.title('Upload UI')  #title
        #root.geometry('500x300') window大小
        
        Label(root,text='Name:').grid(row=0,column=0)
        Label(root,text='Type:').grid(row=0,column=2)
        Label(root,text='Tag1:').grid(row=0,column=4)
        Label(root,text='Tag2:').grid(row=0,column=6)
        Label(root,text='Latitute:').grid(row=1,column=0)
        Label(root,text='Longitude:').grid(row=1,column=2)
        Label(root,text='Address Number:').grid(row=1,column=4)
        Label(root,text='Street:').grid(row=1,column=6)
        Label(root,text='Zipcode:').grid(row=2,column=0)
        Label(root,text='Website:').grid(row=2,column=2)
        Label(root,text='Note:').grid(row=2,column=4)
        
        e1=Entry(root)
        e1.grid(row=0,column=1,padx=7,pady=5) #name
        e2=Entry(root)
        e2.grid(row=0,column=3,padx=7,pady=5) #type
        e3=Entry(root)
        e3.grid(row=0,column=5,padx=7,pady=5) #tag1
        e4=Entry(root)
        e4.grid(row=0,column=7,padx=7,pady=5) #tag2
        e5=Entry(root)
        e5.grid(row=2,column=1,padx=7,pady=5) #zipcode
        e6=Entry(root)
        e6.grid(row=2,column=3,padx=10,pady=5)#website
        e7=Entry(root)
        e7.grid(row=1,column=1,padx=7,pady=5) #latitute
        e8=Entry(root)
        e8.grid(row=1,column=3,padx=7,pady=5) #longtitude
        e9=Entry(root)
        e9.grid(row=1,column=5,padx=7,pady=5) #adds num
        e10=Entry(root)
        e10.grid(row=1,column=7,padx=7,pady=5)#street
        e11=Entry(root)
        e11.grid(row=2,column=5,padx=7,pady=5)#note
        
        def yes_or_no():
            a=tkinter.messagebox.askokcancel('Upload data','Do you want upload this data?')
            if a:
                upload_val()
        
        def upload_val():
            name=e1.get()
            type=e2.get()
            tag1=e3.get()
            tag2=e4.get()
            zip=e5.get()
            website=e6.get()
            lat=e7.get()
            long=e8.get()
            adds=e9.get()
            street=e10.get()
            note=e11.get()
        
            # write into file
            #df=pd.DataFrame({'name':str(name),'type':str(type),'tag1':str(tag1),'tag2':str(tag2),'zipcode':str(zip),'website':str(website),'latitute':str(lat),
            #'longtitute':str(long),'address_number':str(adds),'street':str(street),'note':str(note)})
            #df.to_csv('pittCity_final.csv',mode='a')
            place=[name,lat,long,adds,street,zip,type,tag1,tag2,note,website]
            with open('pittCity_final.csv','a') as file:
                writer=csv.writer(file)
                writer.writerow(place)
        
            b=tkinter.messagebox.showinfo('Result','Uploaded Successfully')
        
        Button(root,text='Upload',width=10,command=yes_or_no).grid(row=3,column=0,sticky=E,padx=10,pady=5)
        Button(root,text='Exit',width=10,command=root.quit).grid(row=3,column=4,sticky=E,padx=10,pady=5)
        
        root.mainloop()

        return "Data entry successfull"
    
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)

