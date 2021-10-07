# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 18:15:49 2021

Filename: cleanWebScrapeTags

Author: Michaela Marincic (mmarinci)

Desc: Take the data scraped from an afterschool food program and clean the columns
to match the two other csv data files to prepare for merging.

Output: A csv file with columns:
Name
Vicinity
lat
long
Clothing
Food
Household
Housing
Training and other services
Notes
website
"""

import pandas as 
import requests
import json
import getLocationWebsite as getLW

oldScrape = pd.read_csv('FoodSites_tableScrape.csv')

tagNames = ['Clothing','Food','Household','Housing','Training and other services']
tagIndex = 0
for col in oldScrape.columns[-5:]:
    oldScrape.rename(columns = {col:tagNames[tagIndex]}, inplace=True)
    tagIndex += 1
    
oldScrape['Food'] = 1

for tag in tagNames:
    if tag != 'Food':
        oldScrape[tag] = 0
newScrape = oldScrape.copy()
newScrape['Notes'] = ''




import requests
import json

def getAddressCoords(input_address, api_key):
    params = {'key' : api_key,
              'address' : input_address}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(url, params)
    result = json.loads(response.text)
    
    # Check these error codes again - there may be more
    if result['status'] not in ['INVALID_REQUEST', 'ZERO_RESULTS']:
                
        lat = result['results'][0]['geometry']['location']['lat']
        long = result['results'][0]['geometry']['location']['lng']
        place_id = result['results'][0]['place_id']

        return [(lat, long), place_id]
    
    # Flagging if there was an error
    else:
        return "Invalid address"
    
for address in newScrape['Vicinity']:
    newScrape['place_id'] = getAddressCoords(address,'KEY')[1]

websites = {'place_id':[], 'website':[]}
for i in newScrape['place_id']:
   result = getLW.getLocationWebsite('KEY',
                                     i,'website')
   if not result.empty:
       websites['place_id'].append(i)
       websites['website'].append(result.at[0,'website'])
   else:
       websites['place_id'].append(i)
       websites['website'].append('')       

websitedf = pd.DataFrame.from_dict(websites)

newScrape = newScrape.join(websitedf.set_index('place_id'), on='place_id')
newScrape.drop(columns = 'place_id', inplace = True)


newScrape.to_csv('FoodSites_FINAL.csv')


















