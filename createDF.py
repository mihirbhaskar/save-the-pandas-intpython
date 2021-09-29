"""
File: createDF.py

Desc: This file uses the getMapData function to call the google API and
search our keywords within a 50000 meter radius, covering well beyond the 
entire area of Pittsburgh. Then, the file removes suspected restaurants and stores
and drops duplicate results from respective keyword searches. The cleaned dataframe
gets saved to a database to enable a self-join for matching records with 
different category tags.

Originating code written as importSearchKeywords.py

Output: pandas dataframe MainFrame, written to .csv
"""
import getGoogleMaps as getGM
import pandas as pd
import time
import sqlite3

with open('Keywords.csv', 'r') as f:
    keywords = []
    categories = []
    for line in f:
        line = line.split(',')
        keywords.append(line[1])
        categories.append(line[0])

MainFrame = pd.DataFrame()
catIndex = 1
for keyword in keywords[1:]:
    
    results = getGM.getMapData('AIzaSyDaj75GIsIPy8duB2O3T_-2tBz9qSgQABk',
                               '40.440600,-79.995900', keyword, '50000')
    data = results[0]
    data['category'] = categories[catIndex]
    nextToken = results[1]
        
    # Next, we run the query again on up to two nextToken calls. 
    # Google's API only produces 60 results on nearby search, with 20 in each
    # initial API call. So we check to see whether there is a nextToken for each
    if nextToken is not None:
        time.sleep(2) # Need to introduce this so that API call ready for token
        results2 = getGM.getMapData('AIzaSyDaj75GIsIPy8duB2O3T_-2tBz9qSgQABk',
                               '40.440600,-79.995900', keyword, '50000', 
                               nextToken)
        data2 = results2[0]
        data2['category'] = categories[catIndex]
        nextToken = results2[1]
        
        if nextToken is not None:
            time.sleep(2)
            results3 = getGM.getMapData('AIzaSyDaj75GIsIPy8duB2O3T_-2tBz9qSgQABk',
                               '40.440600,-79.995900', keyword, '50000', 
                               nextToken)
            data3 = results3[0]
            data3['category'] = categories[catIndex]
            nextToken = results3[1]
    
    try:
        MainFrame = MainFrame.append([data, data2, data3])
    except:
        try:
            MainFrame = MainFrame.append([data, data2])
        except:
            MainFrame = MainFrame.append([data])
    
    # Tick up the index for 'categories' to get the category for the next keyword.        
    catIndex += 1
            
        
# Must remove cols with unsupported type list or dict
MainFrame = MainFrame.drop('types', 1)
MainFrame = MainFrame.drop('photos', 1)

# Retain Pittsburgh addresses
MainFrame = MainFrame[MainFrame['vicinity'].str.contains('Pittsburgh')]

# Drop duplicated results
MainFrame = MainFrame.drop_duplicates()

# Drop results with a price level listed (Gets rid of most of the restaurants)

# Store MainFrame as database table.
# REMOVE PRICE LABEL ONCE CODE IS DONE.
# DEAL WITH PERIODS IN COLUMN NAMES.
for col in MainFrame.columns:
    print(col)
    
connection = sqlite3.connect('MainFrame.db')
cursor = connection.cursor()
query = """CREATE TABLE IF NOT EXISTS MainFrame (
business_status VARCHAR2(20),
icon VARCHAR2(150),
icon_background_color VARCHAR2(10),
icon_mask_base_uri VARCHAR2(150),
name VARCHAR2(150) PRIMARY KEY,
place_id VARCHAR2(50),
rating NUMBER(4),
reference VARCHAR2(50),
scope VARCHAR2(10),
user_ratings_total NUMBER(3),
vicinity VARCHAR2(50),
geometry.location.lat NUMBER(10),
geometry.location.lng NUMBER(10),
geometry.viewport.northeast.lat NUMBER(10),
geometry.viewport.northeast.lng NUMBER(10),
geometry.viewport.southwest.lat NUMBER(10),
geometry.viewport.southwest.lng NUMBER(10),
opening_hours.open_now VARCHAR2(5),
plus_code.compound_code VARCHAR2(50),
plus_code.global_code VARCHAR2(50),
category VARCHAR2(15),
price_level NUMBER(1),
permanently_closed VARCHAR2(5));"""

cursor.execute(query)
connection.close()

    
print(MainFrame)
MainFrame.to_csv('MainFrame.csv')
