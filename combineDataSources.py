"""
File: combineDataSources.py

Desc: This file takes the results of createDF.py, CleaningPittCity.py,
and CleanWebScrapeTags.py, which take results from the Google API, a CSV provided by
the city of Pittsburgh, and data yielded from web scraping.

Output: pandas dataframe Combined_Dataset.csv

Author: Michaela Marincic (mmarinci)
"""

# Read in the three CSV files with data from the three sources (API, CSV, Web).
def createMainFrame():
    import pandas as pd
    apiData = pd.read_csv('APIData.csv', index_col=0)
    csvData = pd.read_csv('pittCity_REALfinal.csv')
    scrapedData = pd.read_csv('FoodSites_FINAL.csv', index_col=0)

# Make all column names uppercase for compatibility.
    for col in apiData.columns:
        apiData.rename(columns=str.upper, inplace=True)
    for col in csvData.columns:
        csvData.rename(columns=str.upper, inplace=True)
    for col in scrapedData.columns:
        scrapedData.rename(columns=str.upper, inplace=True)

# Rearrange and rename columns to all match. 
    cols = scrapedData.columns.tolist()
    ordered = [cols[0]] + cols[2:4] + [cols[1]] + cols[4:]
    scrapedData = scrapedData[ordered]

    csvData.rename(columns={'HOUSEHOLD':'HOUSEHOLD GOODS'}, inplace=True)
    scrapedData.rename(columns={'HOUSEHOLD':'HOUSEHOLD GOODS','LAT':'LATITUDE',
                    'LONG':'LONGITUDE'}, inplace=True)

# Concatenate data sources into single file.
    MainFrame_FINAL = apiData.append([csvData, scrapedData], ignore_index=True)
    MainFrame_FINAL.to_csv('MainFrame.csv')

if __name__ == '__main__':
    createMainFrame()