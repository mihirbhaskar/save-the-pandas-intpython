"""
File: getGoogleMaps.py
Author: Jameson Carter

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

def getMapData(key, location, keyword, radius):
    params = {
        'key':key,
        'keyword':keyword,
        'location':location,
        'radius':radius
        }
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    
    response = requests.get(url,params)
    result = json.loads(response.text)
    df = pd.json_normalize(result['results'])
    return df

# The below function call pulls results for the 'food bank' term
# within 2000 meters of 5729 Holden Street
'''
nearHolden = getMapData('AIzaSyC2yikJt6UgbHwuD9MuOvZliOFYdn34VbU',
           '40.454470,-79.931210',
           'food bank',
           '2000')
'''

    
    