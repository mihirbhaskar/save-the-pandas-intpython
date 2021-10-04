"""
File: combineDataSources.py
Desc: This file takes the results of createDF.py, CleaningPittCity.py,
and INSERTNAME.py, which take results from the Google API, a CSV provided by
the city of Pittsburgh, and data yielded from web scraping.
Output: pandas dataframe AllData.csv
"""
import pandas as pd
APIdata = pd.read_csv('MainFrame.csv')
CSVdata = pd.read_csv('pittCity_REALfinal.csv')

