"""
File: createGoogleDF.py

Desc: This file creates a dataframe via results from getGoogleMaps.py


"""
import getGoogleMaps as getMaps

nearHolden = getMaps.getMapData('INSERT KEY HERE',
           '40.454470,-79.931210',
           'free',
           '80000')