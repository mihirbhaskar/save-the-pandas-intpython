# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 18:15:49 2021

Filename: cleanWebScrapeTags

@author: Michaela Marincic (mmarinci)
"""

import pandas as pd
from getLocationWebsite import getLocationWebsite as getLW

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
newScrape['Website'] = ''


newScrape.to_csv('FoodSites_FINAL.csv')


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
    newScrape['place_id'] = getAddressCoords(address,'AIzaSyC5S1GFZDB7rwVTQJ5w327Ev5wLilfdMgo')[1]

urlList = []
for place in newScrape['place_id']:
    urlList.append(getLW('AIzaSyC5S1GFZDB7rwVTQJ5w327Ev5wLilfdMgo',place,'website'))

print(urlList)
newScrape['Website'] = urlList
print(newScrape['Website'])


















