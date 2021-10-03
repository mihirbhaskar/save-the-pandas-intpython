"""
File: getGoogleMaps.py

Desc: This file accesses the Google Maps Nearby Search API for 
key- AIzaSyC2yikJt6UgbHwuD9MuOvZliOFYdn34VbU. It outputs a pandas dataframe
containing nearby places found according to an input keyword, radius, and 
location.

For more on nearby search see:
https://developers.google.com/maps/documentation/places/web-service/search-nearby

Output: A pandas dataframe holding information including-
business_status
icon
icon_background_color
icon_mask_base_uri
name
place_id
rating
reference
scope
types
user_ratings_total
vicinity
geometry.location.lat
geometry.location.lng
geometry.viewport.northeast.lat
geometry.viewport.northeast.lng
geometry.viewport.southwest.lat
geometry.viewport.southwest.lng
plus_code.compound_code
plus_code.global_code
opening_hours.open_now
"""
import json
import requests
import pandas as pd

def getMapData(key, location, keyword, radius, next_page_token = None):
    params = {
        'key' : key,
        'location' : location,
        'keyword' : keyword,
        'radius' : radius,
        'pagetoken' : next_page_token
        }
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    # If there is no next page token provided, delete that key-value pair
    if next_page_token is None:
        del params['pagetoken']
    # Call the Google API
    response = requests.get(url,params)
    result = json.loads(response.text)
    df = pd.json_normalize(result['results'])
    # Separate the address from the city, first add commas to strings without
    # them so that we can use str.split()
    df = df.loc[:,df.columns.isin(['geometry.location.lat','geometry.location.lng',
            'vicinity','name','place_id','price_level',])]
    # Rename to make everything simpler
    df = df.rename(columns={"geometry.location.lat": "latitude", 
                       "geometry.location.lng": "longitude"})
    # Finally, return the next page token for the next page, if there is one
    try:
        next_page_tk = result['next_page_token']
        return [df,next_page_tk]
    except:
        # Return the output data frame and the next page token in a list
        return [df,None]



    
    