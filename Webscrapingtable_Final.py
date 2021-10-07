""" Webscraping free after-school meals table 

    Description: Code to scrape the after-school feeding data from the website below
    https://pittsburghpa.gov/citiparks/after-school-feeding-program
    for additional sites to add to our searchable database. Leverage the 
    lat/long function to match lat/longs for addresses. 

    Final output: CSV w/ free meal site
    Additional output: findFood(url) function to scrape the site,
                        cleanFood(sites) function to beautify the output
                        and map tag terms, lat/longs, etc. to cleaned 
                        dataset generated 
                        
    Note: The scraping code initially worked such that we were able to generate 
    a CSV, which we read into our mainframe. After a few days, however, we began
    receiving an error message alerting us that we had exceeded max retries for
    this URL. Didn't pose an issue for our data collection purposes, as we'd 
    already scraped the table. 
"""

#############################################################################

import requests
from bs4 import BeautifulSoup 
import pandas as pd 
import json 
import getAddressCoords # need this function to add lat, longs to site addresses

# write a function to scrape the page 
def findFood(url): 
    
    page = requests.get(url)   
    soup = BeautifulSoup(page.content, 'html.parser') 
    major = soup.find(id="article")          # nesting into the articles
    categories =  major.find(class_="col-md-12")    # nesting a little further
    sites = categories.find("ul")       # gives us just the sites 
    individ = sites.find_all("li")     #  getting all of the lis
    locs = [s.get_text(strip=True) for  # strip gets rid of the
       s in individ]                     # xa0 terms in code 

    return locs 


# call the function on the after-school feeding site from CitiParks: 
sites = findFood("https://pittsburghpa.gov/citiparks/after-school-feeding-program")


# write a function to clean up the text and nget rid of funky html formatting: 
def cleanFood(sites): 
    locs2 = []
    for each in sites: 
        each = each.split("--")
        locs2.append(each) 
    
    # now that we have the cleaned data, put in DataFrame: 
    foodsites = pd.DataFrame(locs2, 
                             columns = ["Name", "Vicinity"])

    # the Paulson site is not currently operational
    # let's drop it; it's row 6 
    foodsites.drop(6, inplace=True) 
    
    # reset the index so that no terms skipped 
    foodsites.reset_index(drop=True, inplace=True) # reindex bc we dropped Paulson site
    
    
    # we need lat/long - use getAddressCords function form above
    """ NOTE: call getAddressCoords to get lat, longs of each site
       using API key and function defined above. 
       You need to ENTER YOUR API KEY for google maps geocoding as the 
       SECOND INPUT to the getAddressCoords function below 
    
    """ 
    coords = []
    for each in foodsites["Vicinity"]: 
        coord = getAddressCoords(each, "Enter API Key")  
        coords.append(coord)
        
    # save each item of each tuple into lat and long lists
    lat = []
    long = []
    place_ids = []
    for each in coords: 
        lat1 = each[0][0]
        lat.append(lat1)
        long1 = each[0][1]
        long.append(long1)
        place_id = each[1]
        place_ids.append(place_id)
        
    # add lat and long cols to dF
    foodsites["lat"] = lat 
    foodsites["long"] = long 
    
    # all of these sites are food; add the tag in: 
    foodTag = list(1 for x in (range(7)))
    
    # add the tag cols in for all possible cols (only food sites in this dataset) 
    foodsites["Clothing"] = 0
    foodsites["Food"] = foodTag
    foodsites["Household"] = 0
    foodsites["Housing"] = 0
    foodsites["Training and other services"] = 0
    foodsites['Notes']=''
    foodsites['place_id'] = place_ids
    
    # output this to CSV to collate w/ CSVs containing other site data: 
    foodsites.to_csv("FoodSites_tableScrape.csv", index=False)

