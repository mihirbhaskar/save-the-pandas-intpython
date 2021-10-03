import pandas as pd 

# import the pittCity data 
pittCity = pd.read_excel('C:/Users/smail/Desktop/Pitt City Facilities_copy.xlsx', index_col=0)
pd.set_option('display.max_columns', None)  # so that can see whole table 

# for row in pittCity: 
#    print(row) # gives us the col headings 

# parcel_id
# inactive
# name
# rentable
# type  --> tells us the type of facil, whom it serves, etc
# primary_user
# address_number
# street
# zip
# image
# neighborhood  6 decimals, comma 
# council_district
# ward
# tract
# public_works_division
# pli_division
# police_zone
# fire_zone
# latitude  --> need 
# longitude  --> need 

# from this, we need cols:  
# latitude, 
# longitude, 
# address_number,
#  street, 
# zip
# type 

# gives us the types of facilities 
pittCity.type.unique()
# print(type_facil) 

# we get: 
# ['Storage' 'Shelter' 'Senior' 'Pool' 'Utility' 'Activity' 'Restrooms'
#  'Service' 'Concession' 'Dugout' 'Pool/Rec' 'Rec Center' 'Office'
#  'Pool Closed' 'Firehouse' 'Community' 'Vacant' 'Cabin' 'Medic Station'
#  'Training' 'Police' 'Salt Dome' 'Recycling' 'SERVICE' 'STORAGE' 'POLICE'
#  'TRAINING' 'OFFICE' nan]
# we have a NaN val - let's code that to Community to see if useful 

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


# Add cols to pittSites
new_pittSites["Tag1"] = ""
new_pittSites["Tag2"] = ""
new_pittSites["Tag3"] = ""
new_pittSites["Tag4"] = ""
new_pittSites["Tag5"] = ""
new_pittSites["Notes"] = ""
new_pittSites["Website"] = ""


# create lists for Tag1 Data 
Tag1 = ["Food", "Food", "Food", "Food", "Food",
        "Food", "Food", "Food", "Food", "Food",
        "Food", "Food", "Housing", "Food", "Food"] 

new_pittSites["Tag1"] = Tag1 

# Add in data for Tag2 
Tag2 = ["Training and other services", "", "", "", 
        "", "", "", "", "", "", "", "", "", "", ""]

new_pittSites["Tag2"] = Tag2 


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

print(pittCity_final)
pittCity_final.to_csv("pittCity_REALfinal.csv", index=False) 