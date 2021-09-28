"""
File: createDF.py

Desc: This file uses the getMapData function to call the google API and
search our keywords within a 50000 meter radius, covering well beyond the 
entire area of Pittsburgh. Then, the file removes suspected restaurants and stores
and drops duplicate results from respective keyword searches. 

Originating code written as importSearchKeywords.py

Output: pandas dataframe MainFrame, written to .csv
"""

import getGoogleMaps as getGM
import pandas as pd
import time

with open('Keywords.csv', 'r') as f:
    keywords = []
    for line in f:
        line = line.split(',')
        keywords.append(line[1])

MainFrame = pd.DataFrame()
for keyword in keywords[1:]:
    
    results = getGM.getMapData('AIzaSyDaj75GIsIPy8duB2O3T_-2tBz9qSgQABk',
                               '40.440600,-79.995900', keyword, '50000')
    data = results[0]
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
        nextToken = results2[1]
        
        if nextToken is not None:
            time.sleep(2)
            results3 = getGM.getMapData('AIzaSyDaj75GIsIPy8duB2O3T_-2tBz9qSgQABk',
                               '40.440600,-79.995900', keyword, '50000', 
                               nextToken)
            data3 = results3[0]
            nextToken = results3[1]
    
    try:
        MainFrame = MainFrame.append([data, data2, data3])
    except:
        try:
            MainFrame = MainFrame.append([data, data2])
        except:
            MainFrame = MainFrame.append([data])
        
# Must remove cols with unsupported type list or dict
MainFrame = MainFrame.drop('types', 1)
MainFrame = MainFrame.drop('photos', 1)

# Retain Pittsburgh addresses
MainFrame = MainFrame[MainFrame['vicinity'].str.contains('Pittsburgh')]

# Drop duplicated results
MainFrame = MainFrame.drop_duplicates()

# Drop results with a price level listed (Gets rid of most of the restaurants)

print(MainFrame)
MainFrame.to_csv('MainFrame.csv')