# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:35:00 2019

@author: Shubham
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np

file = 'New Mexico Wells.xlsx'
df = pd.read_excel(file)
        
formations = []
for formation in df.FORMATION:
    if not formation in formations:
        formations.append(formation)
        
# deleting columns that are null values
df_drop = df.dropna(axis= 1, how='all')

# selecting known wells with API numbers
APIm = df_drop[df_drop.API.notnull()]              #dropped from 8055 to 6958
APIm = APIm[['LATITUDE','LONGITUDE','API','BASIN','STATE','DATECOMP','DATESAMPLE','FORMATION','PERIOD','DEPTHUPPER','DEPTHLOWER','DEPTHWELL','LITHOLOGY','SG','SPGRAV','PH','TDSUSGS','TDS','HCO3','Ca','Cl','KNa','Mg','Na','SO4','H2S','cull_chargeb']]

# converting dates to datetime
APIm.DATECOMP = pd.to_datetime(APIm.DATECOMP)
APIm.DATESAMPLE = pd.to_datetime(APIm.DATESAMPLE)

# checking for duplicated wells, possibly looking at time-series data
API_dup = APIm[APIm.duplicated('API')]              #4340
API_orig = APIm[~APIm.duplicated('API')]            #2618

# how many unique well names are there?
API_unique = APIm.groupby('API').nunique()         #2618 unique instances

# how did water TDS change geospatially and over time? USE TDSUSGS only
neg_Depth = API_orig.DEPTHUPPER * -1



"""
rng= np.random.RandomState(0)
colors = rng.rand(2618)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(API_orig.LONGITUDE, API_orig.LATITUDE, neg_Depth, c=colors, cmap='viridis',s=60)

plt.figure()
sns.scatterplot(x=API_orig.LONGITUDE, y=API_orig.LATITUDE, hue=API_orig.TDSUSGS)
plt.tight_layout()
plt.show()
"""



# there are 6 latitude and 6 longitude missing (rows 6163-7 and 8050)
lat_missing = APIm[APIm.LATITUDE.isnull()]
lon_missing = APIm[APIm.LONGITUDE.isnull()]

miss_well_fill_1 = APIm[APIm.API.isin([30015201790000])]
miss_well_fill_2 = APIm[APIm.API.isin([lat_missing.loc[8050,'API']])]

# need to add here a general method for adding the last well 8050's lat and long

# filling in the missing lat/lon data using previous data
scalar_lat = APIm.loc[1360,'LATITUDE']
scalar_lon = APIm.loc[1360,'LONGITUDE']
APIm['LATITUDE'].fillna(value=scalar_lat, inplace=True) 
APIm['LONGITUDE'].fillna(value=scalar_lon,inplace=True) 

# there are 4373 rows where DEPTHUPPER is missing 
du_missing = APIm[APIm.DEPTHUPPER.isnull()]

du_missing = du_missing.reindex(index=du_missing['API'])
i=0
# for checking if any of the depth_upper values correspond with same API numbers
for API_du in du_missing.index:
    miss_well_fill = APIm[APIm.API.isin([API_du])]
    list_upperd = []
    list_lowerd = []
    for eureka_upper, eureka_lower in zip(miss_well_fill['DEPTHUPPER'],miss_well_fill['DEPTHLOWER']):
        #print(eureka_lower,eureka_upper)
        
        if not math.isnan(eureka_upper):
            list_upperd.append(eureka_upper)
        
        if not math.isnan(eureka_lower):
            list_lowerd.append(eureka_lower)
            
    # filling in all the NaN values with mean of the remainder of the well depth values
    mean_upper = np.mean(list_upperd)
    mean_lower = np.mean(list_lowerd)
    print(APIm[APIm.API.isin([API_du])][['DEPTHUPPER','DEPTHLOWER']])
    APIm[APIm.API.isin([API_du])].DEPTHUPPER.fillna(4, inplace=True)
    APIm[APIm.API.isin([API_du])].DEPTHLOWER.fillna(value=mean_lower, inplace=True)
    print(APIm[APIm.API.isin([API_du])][['DEPTHUPPER','DEPTHLOWER']])
    i+= 1

    if i == 48:
        break        
    
    """
            miss_well_fill['DEPTHUPPER'] = eureka_upper
            miss_well_fill['DEPTHLOWER'] = eureka_lower
            print(miss_well_fill[['DEPTHUPPER','DEPTHLOWER']])
            
        """
# none of the values match on their well numbers
            




