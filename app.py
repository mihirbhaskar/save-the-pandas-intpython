"""
File: app.py
Description: Main file for the front-end of the Dash application
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
import os
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import tkinter
from tkinter import *
from tkinter import ttk
from numpy import longcomplex
import csv
import tkinter.messagebox
import json
import requests

app = dash.Dash(__name__)
app.title = 'Steel City Services'

# =============================================================================
# Reading data
# =============================================================================

path = 'MainFrame.csv'

df = pd.read_csv(path, index_col=0)
# This gets the time of the most recent content modification -> when the data is first loaded into the app
lastmt = os.stat(path).st_mtime

# Pulling column names from df to serve as options to populate the dropdown
tags = ['CLOTHING', 'FOOD', 'HOUSEHOLD GOODS', 'HOUSING', 'TRAINING AND OTHER SERVICES']

# =============================================================================
# Defining functions to create the appropriate HTML Divs (i.e. sections of the UI)
# =============================================================================

def description_card():
    """
    Returns
    -------
    A Div containing dashboard title & descriptions
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Steel City Services"),
            html.H3("Find and contribute support options near you"),
            html.Div(
                id="intro",
                children='''Use the search options below to find locations near you providing support, or
                            let us know about an initiative we may have missed.''',
                ),
            ],
        )

def generate_control_card():
    """

    Returns
    -------
    A Div containing the user-defined options for searching and adding new info

    """
    return html.Div(
        id="control-card",
        children=[
            # Entering address
            html.P("Enter your address and click submit"),
            dcc.Input(id='user-address', value='', type='text'),
            html.Button('Submit', id='submit-user-address', n_clicks = 0),
            html.Br(),
            html.Br(),
            # Entering distance
            html.P("Enter your max travel distance in miles"),
            dcc.Input(id='max-travel-dist', value=10, type='number'),
            html.Br(),
            html.Br(),
            # Selecting categories
            html.P("Select relevant categories"),
            dcc.Dropdown(
            id='asset-type',
            options=[{'label': i, 'value': i} for i in tags],
            value=[i for i in tags],
            multi=True
            ),
            html.Br(),
            # Button to update data
            html.P("Know a place we don't? Click to add info"),
            html.Button('Submit your own data', id='submit-data'),
            html.Div(id='output-container-button'),
            
            # Interval with which data gets updated
            dcc.Interval(id='data-update-interval', interval=1000, n_intervals=0),
            html.P(id='placeholder')
            
            
            ]
        
        )
    

# =============================================================================
# Defining layout of the app
# =============================================================================

app.layout = html.Div([
    
    # Left column
    html.Div(id="left-column",
             className="four columns",
             children=[description_card(), generate_control_card()]
        ),
    
    # Right column
    html.Div(
        id="right-column",
        className="eight columns",
        children=[
            # Output table
            html.Div(id='output-table'), 
            ],
        ),
    ],
)
    

# =============================================================================
# Callback for the dataset to be updated when the .csv is modified (by data entry)
# =============================================================================

# Data update callback
@app.callback(Output('placeholder', 'children'), 
              [Input('data-update-interval', 'n_intervals')]
)
def dataset_update_trigger(n):
    
    # Reading in the data fresh if there was an update, and update last modified time
    global lastmt # lastmt and df have to be defined as global variables in order to hold outside of this function
                  # and be relevant for the next callback, which filters/uses the dataset
    global df
    if os.stat(path).st_mtime > lastmt:
        lastmt = os.stat(path).st_mtime
        df = pd.read_csv(path)
        return ""
    return ""

# =============================================================================
# Callback for the filtered set of results to be created and displayed
# =============================================================================

@app.callback(
    Output(component_id='output-table', component_property='children'),
   [Input('submit-user-address', 'n_clicks')],
   [State('user-address', 'value')],
   Input('max-travel-dist', 'value'),
   Input('asset-type', 'value'),
)
def search_output_div(n_clicks, user_address, max_travel_dist, asset_type):
    # First output value, before user has submitted anything - show blank
    if n_clicks == 0:
        return ''
    
    else:
        # Translate input address into lat-longs 
        user_coords = getAddressCoords(input_address = user_address, api_key = google_apikey)
        
        # Check if address was translated properly - if yes, it should return a tuple
        if type(user_coords) == list:
    
            # =============================================================================
            # Filtering the data according to parameters            
            # =============================================================================
            
            # Filter the data frame with observations that fall within max distance limit, using a user-defined program
            fdata = filterNearby(point = user_coords[0], data = df, max_dist = max_travel_dist)
            
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
            fdata['SUPPORT PROVIDED'] = ''
    
            for i in tags: # Note: tags is defined at the top of the script, as the list of service categories
                fdata.loc[fdata[i] == 1, 'SUPPORT PROVIDED'] += i + ',' # Concat on the service name (column name) if it's value is 1
            fdata['SUPPORT PROVIDED'] = fdata['SUPPORT PROVIDED'].str[:-1] # Strip the last comma 
            
            # Round the distance in miles column to 2 decimal places
            fdata['DISTANCE IN MILES'] = fdata['DISTANCE IN MILES'].round(2)
            

            # To-do: Make the vicinity a 'link' display that when users click gives them directions
            # Link format to follow: https://www.google.com/maps/dir/?api=1&origin=760+West+Genesee+Street+Syracuse+NY+13204&destination=314+Avery+Avenue+Syracuse+NY+13204
            # How to do it in code: https://github.com/plotly/dash-table/issues/222#issuecomment-585179610
            
            # Select the appropriate columns to display
            fdata = fdata[['NAME', 'SUPPORT PROVIDED', 'VICINITY', 'DISTANCE IN MILES', 'WEBSITE', 'NOTES']]
                                    
            # Convert the dataframe into Dash's DataTable for display in the app
            tmpdta = fdata.to_dict('rows')
            tmpcols = [{"name": i, "id": i,} for i in (fdata.columns)]
            
            # Return a well-formatted dash table
            return dash_table.DataTable(data = tmpdta, columns = tmpcols,
                                        fixed_rows={'headers': True},
                                        #fill_width=False,
                                        # Need to play around with this code
                                         style_cell_conditional=[
                                             {'if': {'column_id': 'DISTANCE IN MILES'},
                                              'width':'80px'}],
                                        #     {'if': {'column_id': 'support provided'},
                                        #      'width': '20%'},
                                        #     {'if': {'column_id': 'vicinity'},
                                        #      'width':'30%'},
                                        #     {'if': {'column_id': 'distance in miles'},
                                        #      'width': '10%'},
                                        #     ],
                                        style_data={'whiteSpace':'normal',
                                                    'height': 'auto',
                                                    'lineHeight':'15px'},
                                        style_cell={'textAlign': 'left',
                                                    'height': 'auto',
                                                    'minWidth': '80px',
                                                    'width': '180px',
                                                    'maxWidth': '180px',
                                                    'whiteSpace': 'normal'},
                                        style_header={'fontWeight':'bold'})
            
        # If address failed, return the string error message
        else:
            return "Invalid address" ''
        

# =============================================================================
# Callback for the data entry/input section
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
        Label(root,text='Vicinity:').grid(row=0,column=2)
        Label(root,text='Category:').grid(row=1,column=0)
        Label(root,text='Notes:').grid(row=2,column=0)
        Label(root,text='Website:').grid(row=2,column=2)
        
        e1=Entry(root)
        e1.grid(row=0,column=1,padx=7,pady=5) #name
        #comvalue=tkinter.StringVar()
        #e3=ttk.Combobox(root,textvariable=comvalue) #Category
        #e3.grid(row=0,column=5,padx=7,pady=5) #Place ID
        #e3['value']=('Clothing','Food','Household Goods','Housing','Training and other services')
        #e3.current(1)  #default setting->Food
        category = {0:'Clothing',1:'Food',2:'Household Goods',3:'Housing',4:'Training and other services'}
        dic1 = {}
        for i in range(len(category)):
            dic1[i] = BooleanVar()
            Checkbutton(root,text=category[i],variable=dic1[i]).grid(row=1,column=i+1)
        e4=Entry(root)
        e4.grid(row=2,column=1,padx=7,pady=5)#Notes
        e5=Entry(root)
        e5.grid(row=2,column=3,padx=7,pady=5)#Website   
        e6=Entry(root)
        e6.grid(row=0,column=3,padx=7,pady=5)#Vicinity
        e7=Entry(root)
        
        def required(): #name,vicinity
            r1=e1.get()
            r2=e6.get()
            flag=1
            if len(r1)==0:
                tkinter.messagebox.showwarning('Warning','Please enter the name!')
                flag=0
            if len(r2)==0:
                tkinter.messagebox.showwarning('Warning','Please enter the Vicinity!')
                flag=0
            if getAddressCoords(e6.get(), google_apikey) == 'Invalid address':
                tkinter.messagebox.showwarning('Warning','Please enter a valid address!')
                flag=0
            return flag
        
        def mutichoice():
            cats=[]
            for key,value in dic1.items():
                if value.get() == True:
                    cats.append(category[key])
            numb=len(cats)
            return cats,numb
        
        def yes_or_no():
            flag=required()
            if flag:
                a=tkinter.messagebox.askokcancel('Upload data','Do you want upload this data?')
                if a:
                    upload_val()
        #**************************            
        
        def upload_val():
            name=e1.get()
            notes=e4.get()
            website=e5.get()
            cat,numb=mutichoice()
            flag1=e7.get()
            flag2=e7.get()
            flag3=e7.get()
            flag4=e7.get()
            flag5=e7.get()
            for i in range(numb):
                if cat[i]=='Clothing':
                    flag1=1
                elif cat[i]=='Food':
                    flag2=1
                elif cat[i]=='Household Goods':
                    flag3=1
                elif cat[i]=='Housing':
                    flag4=1
                elif cat[i]=='Training and other services':
                    flag5=1
            #flag1,flag2,flag3,flag4,flag5=fill(flag1,flag2,flag3,flag4,flag5)
            lat= list(getAddressCoords(e6.get(), google_apikey)[0])[0]
            long=list(getAddressCoords(e6.get(), google_apikey)[0])[1]
            vin=e6.get()
        
            # write into file
            with open('MainFrame.csv','r', encoding="utf8") as file:
                count=len(file.readlines())-1
            placeall=[count,name,lat,long,vin,flag1,flag2,flag3,flag4,flag5,notes,website]
            with open('MainFrame.csv','a', encoding="utf8") as file:       
                writer=csv.writer(file)
                writer.writerow(placeall)
        
            b=tkinter.messagebox.showinfo('Result','Uploaded Successfully')
        
        Button(root,text='Upload',width=10,command=yes_or_no).grid(row=3,column=0,sticky=E,padx=10,pady=5)
        Button(root,text='Exit',width=10,command=root.quit).grid(row=3,column=3,sticky=E,padx=10,pady=5)
        
        root.mainloop()
        
        return "Data updated successfully"
    
    
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)

