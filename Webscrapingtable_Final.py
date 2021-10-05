# Webscraping free after-school meals table 

# Description: Code to scrape the after-school feeding data from the website below
# https://pittsburghpa.gov/citiparks/after-school-feeding-program
# for additional sites to add to our searchable database. Leverage the 
# lat/long function to match lat/longs for addresses. 

# Final output: CSV w/ free meal sites, findFood(url) function 


#############################################################################

import requests
from bs4 import BeautifulSoup 
import pandas as pd 
import json 


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


# now, let's clean up the data to get rid of funky html formatting: 
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

foodsites.reset_index(drop=True, inplace=True) # reindex bc we dropped Paulson site


# we need lat/long - copying function from mihir's code 
def getAddressCoords(input_address, api_key):
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=' 
           + input_address + '&key=' + api_key)
    
    response = requests.get(url)
    result = json.loads(response.text)
    
    # Check these error codes again - there may be more
    if result['status'] not in ['INVALID_REQUEST', 'ZERO_RESULTS']:
                
        lat = result['results'][0]['geometry']['location']['lat']
        long = result['results'][0]['geometry']['location']['lng']

        return (lat, long) 
    
    # Flagging if there was an error
    else:
        return "Invalid address"


# get coords using API key and function defined above 
coords = []
for each in foodsites["Vicinity"]: 
    coord = getAddressCoords(each, "Enter your API key here")  
    coords.append(coord)
  
    
# save each item of each tuple into lat and long lists
lat = []
long = []
for each in coords: 
    lat1 = each[0]
    lat.append(lat1)
    long1 = each[1]
    long.append(long1)
    

# add lat and long cols to dF
foodsites["lat"] = lat 
foodsites["long"] = long 

# all of these sites are food; add the tag in: 
foodTag = list(1 for x in (range(7)))


# add the tag cols in for all possible cols (only food)
foodsites["Clothing"] = ""
foodsites["Food"] = foodTag
foodsites["Household"] = ""
foodsites["Housing"] = ""
foodsites["Training and other services"] = ""

print(foodsites)

# output this to CSV to collate w/ CSVs containing other site data: 
foodsites.to_csv("FoodSites_tableScrape.csv", index=False)

