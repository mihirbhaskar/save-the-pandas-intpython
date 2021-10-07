""" 
File: CleaningPittCity.py

Desc: Take the CSV of City of Pittsburgh facilities CSV/Excel file
from online. Clean this data, getting rid of sites that do not provide 
community service we are interested in. 
Generate a Pandas DataFrame that is exported to a final CSV, to be combined
with other CSV datas into the mainframe. 
 
Input: CSV file obtained from city of Pittsburgh at 
https://data.wprdc.org/dataset/city-of-pittsburgh-facilities/resource/fbb50b02-2879-47cd-abea-ae697ec05170

Output: CSV file of community sites that.    
"""

import pandas as pd 

def getPittDwnld(): 
    # import the pittCity data from the CSV/Excel file on GitHub: 
    pittCity = pd.read_excel("CSV to Clean - Pitt City Facils.xlsx", index_col=0)
    pd.set_option('display.max_columns', None)  # so that can see whole table 
    
    # gives us the types of facilities 
    pittCity.type.unique()
    # print(type_facil) 

    # things that will be useful for us: 
    # Senior 
    # Rec Center 
    # Community 
    
    # fill NaNs w/ Community, in case those rows are valuable but not coded 
    pittCity.fillna( {"type" : "Community"}, inplace=True ) 
    
    # select only the rows that are type Community, Senior, or Rec Center
    # select only those cols that are relevant and that we'll need to join w/ 
    # data from API, other searches 
    
    comm_only = pittCity.loc[pittCity["type"] == "Community"]  # 4 comm facil
    comm_only = comm_only[["name", "latitude", "longitude", "address_number", 
                          "street", "zip", "type"]]
    
    
    senior_only = pittCity.loc[pittCity["type"] == "Senior"] 
    senior_only = senior_only[["name", "latitude", "longitude", "address_number",
                          "street", "zip", "type"]]  # 16 senior facil
    
    recCtr_only = pittCity.loc[pittCity["type"] == "Rec Center"]
    recCtr_only = recCtr_only[["name", "latitude", "longitude", "address_number",
                          "street", "zip", "type"]] # 6 rec center facil
     
    # create an empty dF to put rows into: 
    pittSites = pd.DataFrame(columns=senior_only.columns) 
                           
    # now, glue the columns back together, w/ only the 
    # rows and col values we want 
    pittSites = pittSites.append(comm_only, ignore_index=True)
    pittSites = pittSites.append(senior_only, ignore_index=True)
    pittSites = pittSites.append(recCtr_only, ignore_index=True) 
    
    # get rid of decimals in address and zip code w/out messing us NaNs
    pittSites = pittSites.astype( {"address_number" : "Int64", # convert each to number val 
                                         "zip" : "Int64"})
    
    pittSites = pittSites.astype( {"address_number" : "str"})
    
    """
    # check each of the sites to see if they actually provide one of the following: 
    # food, housing, household goods, clothing, training and other services 
    
    # 0 - Hazelwood: food, training and other services
    # notes - YMCA food bank (first Sat of month), life skills programming for youth
    # website: https://www.spartancenter.org/
    
    # 01 - MLK Cultural Center: n/a 
    # notes - diff to access info, would want crowdsourced info here
    
    # 02 - Overbrook: n/a 
    # notes: not terribly active
    
    # 03 - Schenley Park Ice Rink - n/a 
    # notes: not offering community-based services we're interested in
    
    # 04 - Allegheny Northside Sr Center: n/a
    # notes: primarily a theatre center
    
    # 05 - Beechview Sr, Comm Ctr - food
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 06 - Brighton Heights - food
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 07 - Glen Hazel - food 
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 08 - Hazelwood Senior - food 
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 09 -  Homewood Senior Center - food 
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 10 - Lawrenceville - food
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 11 - Magee Rec Ctr - food 
    # after-school meals, 4-6pm (snack & dinner)
    # website: https://apps.pittsburghpa.gov/redtail/images/15894_MageePAGE.pdf
    
    # 12 - McKinley Park - n/a
    
    # 13 - Morningside - food 
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 14 - Mt Washington - food
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 15 -  Overbrook Senior Center - n/a
    
    # 16 - Sheraden - food 
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 17 - Southside Market House - n/a 
    # looks like reopened in 2019, not big web presence
    
    # 18 - West End Senior Center - food 
    # notes: free grab&go senior lunches, M, W, F from 11-1
    # healthy active living ctr for seniors
    
    # 19 - Morningside Crossing - housing
    # 46-unit mixed housing redevelopment, focus on seniors, most units for people making 20 - 60% median income
    # direct inquiries on open units here: https://cmshousing.com/properties/morningside-crossing/
    
    # 20 - Brookline Rec - n/a 
    # recreational facilities
    
    # 21 Chadwick Rec - n/a
    
    # 22 - Cowley Recreation Center - n/a 
    
    # 23 - Jefferson Recreation Center - food 
    # free after-school meals for kids, 4-6pm
    
    # 24 -  Paulson Recreation Center - food 
    # free after-school meals for kids, 4-6pm
    # link: https://www.afterschoolpgh.org/programs/paulson-community-recreation-center/
    
    # 25 - Robert E Williams Recreation Center - n/a 
    # currently in redevelopment
    
    # So, remove rows: 
        # 25, 22, 21, 20, 17, 15, 12, 4, 3, 2, 1
    """
    
    
    # drop the indices we don't want 
    new_pittSites = pittSites.copy()
    
    new_pittSites.drop([25, 22, 21, 20,
                    17, 15, 12, 4, 3, 2, 1], inplace=True)
    
    new_pittSites.reset_index(drop=True, inplace=True) # reset the index, get rid of old 
    
    
    # Add vicinity col so that matches API data 
    address1 = []
    for each in new_pittSites["address_number"]: 
        address1.append(each)
        
    address2 = []
    for each in new_pittSites["street"]: 
        address2.append(each)
        
    
    vicinity = [str(x + " " + y) for x, y in zip(address1, address2)] 
    
    # Add vicinity col to pittSites
    
    new_pittSites["Vicinity"] = vicinity
    
    # create lists for Tag Data 
    foodTag = [1 for x in range(12)]
    foodTag.append(0)
    foodTag.append(1)
    foodTag.append(1)
    
    housingTag = [0 for x in range(12)]
    housingTag.append(1)
    housingTag.append(0)
    housingTag.append(0)
    
    trainingTag = [1]
    for i in range(14):
        trainingTag.append(0)
    
    
    # Add cols to pittSites
    new_pittSites["Clothing"] = 0
    new_pittSites["Food"] = foodTag
    new_pittSites["Household"] = 0
    new_pittSites["Housing"] = housingTag
    new_pittSites["Training and other services"] = trainingTag
    new_pittSites["Notes"] = ""
    new_pittSites["Website"] = ""
    
    # Add in Notes data: 
    Notes = ["YMCA food bank (first Sat of month), life skills programming for youth",
             "free grab&go senior lunches, M, W, F from 11-1, healthy active living ctr for seniors", 
             "free grab&go senior lunches, M, W, F from 11-1, healthy active living ctr for seniors",
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors",
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors",
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors",
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors",
             "after-school meals, 4-6pm (snack & dinner)",
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors",
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors", 
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors",
             "free grab&go senior lunches, M, W, F from 11-1; healthy active living ctr for seniors",
            "46-unit mixed housing redevelopment, focus on seniors, most units for people making 20 - 60% median income", 
            "free after-school meals for kids, 4-6pm", 
            "free after-school meals for kids, 4-6pm" ] 
    
    new_pittSites["Notes"] = Notes
    
    Websites = ["https://www.spartancenter.org/",
                "",
                "",
                "",
                "",
                "",
                "",
                "https://apps.pittsburghpa.gov/redtail/images/15894_MageePAGE.pdf",
                "",
                "",
                "",
                "", 
                "https://cmshousing.com/properties/morningside-crossing/",
                "",
                "https://www.afterschoolpgh.org/programs/paulson-community-recreation-center/"]
    
    new_pittSites["Website"] = Websites
    
    pittCity_final = new_pittSites.copy() 
    pittCity_final.drop("type", axis=1, inplace=True) 
    pittCity_final.drop("zip", axis=1, inplace=True)
    pittCity_final.drop("street", axis=1, inplace=True)
    pittCity_final.drop("address_number", axis=1, inplace=True)
    
    pittCity_final.to_csv("pittCity_REALfinal.csv", index=False) 
