# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 18:15:49 2021

Filename: cleanWebScrapeTags

Desc: Change column names in the web scraped data to match MainFrame. Data was scraped
from a Pittsburgh city afterschool food program that has since blocked us access when
we attempt to scrape it. The data is static, however, so we do not need to continue
scraping it in real time.

Output: A csv with the afterschool food program data scarped from the web. The csv
contains the following columns:
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
Website

@author: Michaela Marincic (mmarinci)
"""

import pandas as pd
from getLocationWebsite import getLocationWebsite as getLW

def cleanWebData(apiKey):

# Import the data that was scraped from the food program website while it was still
# allowing access.
    oldScrape = pd.read_csv('FoodSites_tableScrape.csv')

# Change the tag names to match the format used in MainFrame.
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


# Now get place_ids for each location using the Google Maps Geocode API.
# This will allow us to call the location's website using the Place Details API.
    from getAddressCoords import getAddressCoords as getAC
    
    for address in newScrape['Vicinity']:
        newScrape['place_id'] = getAC(address, apiKey)[1]

# Now that we have place_ids, we can query Place Details for any websites
# associated with these locations.
    websites = {'place_id':[], 'Website':[]}
    for i in newScrape['place_id']:
        result = getLW(apiKey, i,'website')
    
        if not result.empty:
            websites['place_id'].append(i)
            websites['Website'].append(result.at[0,'website'])
        else:
            websites['place_id'].append(i)
            websites['Website'].append('')
        
    websitedf = pd.DataFrame.from_dict(websites)
    newScrape = newScrape.join(websitedf.set_index('place_id'), on='place_id')
    newScrape.drop(columns = 'place_id', inplace=True)
    newScrape.drop_duplicates(inplace=True)

#Save the cleaned data to a csv.
    newScrape.to_csv('FoodSites_FINAL.csv')
    












