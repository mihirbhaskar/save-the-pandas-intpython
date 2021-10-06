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
import getLocationWebsite


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
    
    results = getGM.getMapData('KEY',
                               '40.440600,-79.995900', keyword, '50000')
    data = results[0]
    data['category'] = categories[catIndex]
    nextToken = results[1]
        
    # Next, we run the query again on up to two nextToken calls. 
    # Google's API only produces 60 results on nearby search, with 20 in each
    # initial API call. So we check to see whether there is a nextToken for each
    if nextToken is not None:
        time.sleep(2) # Need to introduce this so that API call ready for token
        results2 = getGM.getMapData('KEY',
                               '40.440600,-79.995900', keyword, '50000', 
                               nextToken)
        data2 = results2[0]
        data2['category'] = categories[catIndex]
        nextToken = results2[1]
        
        if nextToken is not None:
            time.sleep(2)
            results3 = getGM.getMapData('KEY',
                               '40.440600,-79.995900', keyword, '50000', 
                               nextToken)
            data3 = results3[0]
            data3['category'] = categories[catIndex]
            nextToken = results3[1]
       
    try:
        MainFrame = MainFrame.append([data, data2, data3], ignore_index = True)
    except:
        try:
            MainFrame = MainFrame.append([data, data2], ignore_index = True)
        except:
            MainFrame = MainFrame.append([data], ignore_index = True)
    
    # Tick up the index for 'categories' to get the category for the next keyword.        
    catIndex += 1

   
# Retain Pittsburgh addresses
MainFrame = MainFrame[MainFrame['vicinity'].str.contains('Pittsburgh')]
# Drop results with a price level listed (Gets rid of most of the restaurants)
MainFrame = MainFrame.drop(MainFrame.loc[MainFrame['price_level']>=1].index)
# Drop price level, if it exists
MainFrame = MainFrame.loc[:,MainFrame.columns.isin(['latitude','longitude',
            'vicinity','name','place_id','category',])]
# Add a dummy column for use in pivot table
MainFrame['Value'] = int(1)
# Reshape the mainframe
MainFrame = MainFrame.pivot_table(
        index=['name', 'place_id', 'latitude', 'longitude', 'vicinity'], 
         columns='category', 
         values='Value').reset_index()
MainFrame.index.name = MainFrame.columns.name = None
# Add 'Notes' to make compatible with other data.
MainFrame['Notes']=''
# 'URL' column will be added using Google Maps API "Place Details" in a separate file.
# That file will also drop 'place_id' for union compatibility.

websites = []
for i in MainFrame['place_id'][0:5]:
    website = getLocationWebsite('KEY','ChIJff4dv1DxNIgRRrImDNjSHLE','website')
    websites.append(website[1])
    
getLocationWebsite('KEY', 'ChIJff4dv1DxNIgRRrImDNjSHLE', "website")
    
print(websites)

# Write to CSV
MainFrame.to_csv('MainFrame.csv')
