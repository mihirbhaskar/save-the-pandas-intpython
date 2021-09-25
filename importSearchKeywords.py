# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 17:36:26 2021

@author: Michaela Marincic
"""


with open('C:/Users/mmari/Downloads/KeywordsForEachCategory.csv', 'r') as f:
    keywords = []
    for line in f:
        line = line.split(',')
        keywords.append(line[1])

print(keywords[1:])

import getGoogleMaps as getGM

MainFrame = getGM.getMapData('AIzaSyCnFdidklQ6-Z8FYYJ0oAcIfrZRkJV6XrY','40.454470,-79.931210', 
                   keywords[1], '2000')
for keyword in keywords[2:]:
    results = getGM.getMapData('AIzaSyCnFdidklQ6-Z8FYYJ0oAcIfrZRkJV6XrY','40.454470,-79.931210', keyword, '2000')
    MainFrame.append(results)
    
print(MainFrame)
