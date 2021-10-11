"""
File: createDF.py

Desc: This file uses the getMapData function to call the google API and
search our keywords within a 50000 meter radius of the center of Pittsburgh, 
covering well beyond the entire area of Pittsburgh. Then, the file removes 
suspected restaurants and storesand drops duplicate results from respective 
keyword searches. Then, the file uses the getLocationWebsite function to attach
website information to the places which have a website.

Finally, the file outputs a .csv file that contains all of the Google API data
that we need.

Inputs: Google Places API key
Output: pandas dataframe MainFrame, written to .csv
"""
import getGoogleMaps as getGM
import pandas as pd
import time
import getLocationWebsite as getLW

def createGoogleDF(apiKey):
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
    
        results = getGM.getMapData(apiKey,
                               '40.440600,-79.995900', keyword, '50000')
        data = results[0]
        data['category'] = categories[catIndex]
        nextToken = results[1]
        
        # Next, we run the query again on up to two nextToken calls. 
        # Google's API only produces 60 results on nearby search, with 20 in each
        # initial API call. So we check to see whether there is a nextToken for each
        if nextToken is not None:
            time.sleep(2) # Need to introduce this so that API call ready for token
            results2 = getGM.getMapData(apiKey,
                               '40.440600,-79.995900', keyword, '50000', 
                               nextToken)
            data2 = results2[0]
            data2['category'] = categories[catIndex]
            nextToken = results2[1]
        
            if nextToken is not None:
                time.sleep(2)
                results3 = getGM.getMapData(apiKey,
                               '40.440600,-79.995900', keyword, '50000', 
                               nextToken)
                data3 = results3[0]
                data3['category'] = categories[catIndex]
                nextToken = results3[1]
                
       # This portion of the code appends data to data2 and data3, if both 
       # exist, to data2 if data3 does not exist, and to nothing if neither
       # exist. The variable data should always exist.
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

    # 'URL' column will be added using Google Maps API "Place Details"
    websites = {'place_id':[], 'website':[]}
    for i in MainFrame['place_id']:
        result = getLW.getLocationWebsite(apiKey,
                                       i,'website')
    
        if not result.empty:
            websites['place_id'].append(i)
            websites['website'].append(result.at[0,'website'])
    websitedf = pd.DataFrame.from_dict(websites)

    MainFrame = MainFrame.join(websitedf.set_index('place_id'), on='place_id')
    MainFrame.drop(columns = 'place_id', inplace = True)

    # Write to CSV
    MainFrame.to_csv('APIData.csv')

if __name__ == '__main__':
    apikey = input('Enter your Google Places API Key: ')
    try:
        createGoogleDF(apikey)
    except:
        print('Try again! Error.')
        apikey = input('Enter your Google Places API Key: ')
        