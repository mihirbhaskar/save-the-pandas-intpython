# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 22:16:46 2021

@author: Michaela Marincic (mmarinci)

File: getLocationWebsite.py

Desc: The function getLocationWebsite takes a Google Maps place_id as a parameter
(along with the field 'website' and an API key) and returns the website for
the specified location using the "Place Details" API in Google Maps.

Output: A dataframe with the website for a given location (place_id).
"""

import requests
import json
import pandas as pd

def getLocationWebsite(key, ID, fields):
    params = {'key' : key,
              'place_id' : ID,
              'fields' : fields}
    url = 'https://maps.googleapis.com/maps/api/place/details/json?'
    response = requests.get(url,params)
    result = json.loads(response.text)
    df = pd.json_normalize(result['result'])
    return df


print(getLocationWebsite('KEY', 'ChIJff4dv1DxNIgRRrImDNjSHLE', 'website'))
