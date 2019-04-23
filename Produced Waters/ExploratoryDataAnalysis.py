# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:35:00 2019

@author: Shubham
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as pyplot


file = 'Texas Wells.xlsx'
df = pd.read_excel(file)

def fill_values_with_API(column):
    """
    Filling in missing values using similar API codes; column is a str
    The return value is the number of new entries in the main API dataframe
    """
    col_missing = APIm[APIm[column].isnull()]         
    prev_val = sum(APIm[column].isnull())

    for x,API_count in enumerate(col_missing['API']):
        slices = APIm[APIm.API.isin([API_count])]
        slices = slices.reset_index()
        #print(slices.head())
        s1 = 0
    
        if pd.notnull(slices[column]).any():            
            for i,val in enumerate(slices[column]):
            
        #if the block of wells with this particular API have any of latitudes/longitudes
        #filled in, then fill them up or down with that latitude and longitude
            
                s1 = np.nansum([val,s1])
                #print(APIm.loc[slices['index'][i],column])
                APIm.loc[slices['index'][i],column] = s1
                #print(APIm.loc[slices['index'][i],column])
    
    after_val = sum(APIm[column].isnull())           
    return prev_val - after_val


def fill_DEPTH_with_API(column):
    """
    Filling in missing values using similar API codes; column is a str
    The return value is the number of new entries in the main API dataframe
    """
    col_missing = APIm[APIm[column].isnull()]         
    prev_val = sum(APIm[column].isnull())

    for x,API_count in enumerate(col_missing['API']):
        slices = APIm[APIm.API.isin([API_count])]
        slices = slices.sort_values(by=[column]).reset_index()
        
        #print(slices.loc[:5,['index','DEPTHUPPER']])
    
        if pd.notnull(slices[column]).any(): 
            mean = slices[column].mean() 
            null_slice = slices[slices[column].isnull()].reset_index()
            for i,val in enumerate(null_slice[column]):
            
        #if the block of wells with this particular API have any of latitudes/longitudes
        #filled in, then fill them up or down with that latitude and longitude
            
                #s1 = np.nansum([val,s1])
                #print(APIm.loc[null_slice['index'][i],column])
                APIm.loc[null_slice['index'][i],column] = mean
                #print(APIm.loc[null_slice['index'][i],column])
    
    after_val = sum(APIm[column].isnull())           
    return prev_val - after_val
        
        
# deleting columns that are null values
df_drop = df.dropna(axis= 1, how='all')

formations = []
for formation in df_drop.FORMATION:
    if not formation in formations:
        formations.append(formation)

# selecting known wells with API numbers
APIm = df_drop[df_drop.API.notnull()]              #dropped from 19388 to 8208
APIm = APIm[['LATITUDE','LONGITUDE','API','BASIN','STATE','DATECOMP','DATESAMPLE','FORMATION','PERIOD','DEPTHUPPER','DEPTHLOWER','DEPTHWELL','LITHOLOGY','SG','SPGRAV','PH','TDSUSGS','TDS','HCO3','Ca','Cl','KNa','Mg','Na','SO4','H2S','cull_chargeb']]

# converting dates to datetime
APIm.DATECOMP = pd.to_datetime(APIm.DATECOMP)
APIm.DATESAMPLE = pd.to_datetime(APIm.DATESAMPLE)

# checking for duplicated wells, possibly looking at time-series data
API_dup = APIm[APIm.duplicated('API')]              #3448
API_orig = APIm[~APIm.duplicated('API')]            #4760

# how many unique well names are there?
API_unique = APIm.groupby('API').nunique()         #4760 unique instances
"""
---------------------------------------------------------------------
lat_missing = APIm[APIm.LATITUDE.isnull()]         #36 missing
lon_missing = APIm[APIm.LONGITUDE.isnull()]        #34 missing

for x,API_count in enumerate(lat_missing['API']):
    lat_slices = APIm[APIm.API.isin([API_count])]
    lat_slices = lat_slices.reset_index()
    #print(lat_slices.head())
    l1 = 0
    
    if pd.notnull(lat_slices.LATITUDE).any():
        for i,lat in enumerate(lat_slices.LATITUDE):
            
        #if the block of wells with this particular API have any of latitudes/longitudes
        #filled in, then fill them up or down with that latitude and longitude
            
            l1 = np.nansum([lat,l1])
            print(APIm.loc[lat_slices['index'][i],'LATITUDE'])
            APIm.loc[lat_slices['index'][i],'LATITUDE'] = l1
            print(APIm.loc[lat_slices['index'][i],'LATITUDE'])
            
    #if x == 31:
        #break

print(sum(pd.notnull(APIm.LATITUDE)))           #only 2 got filled for latitudes
---------------------------------------------------------------------
"""

a = fill_values_with_API('LATITUDE')
print(a)

b = fill_values_with_API('LONGITUDE')
print(b)

c = fill_DEPTH_with_API('DEPTHUPPER')          #704 DEPTHUPPER filled
print(c)

d = fill_DEPTH_with_API('DEPTHLOWER')          #917 DEPTHLOWER filled
print(d)

fig = plt.figure()
ax = pyplot.subplots(figsize=(11.7,8.27))
ax.scatter(APIm.LONGITUDE, APIm.LATITUDE, APIm.DEPTHUPPER, cmap='viridis',s=60)

plt.figure()
sns.scatterplot(x=APIm.LONGITUDE, y=APIm.LATITUDE, hue=APIm.TDSUSGS)


plt.tight_layout()
plt.show()

"""
---------------------------------------------------------------------
# datesample analysis
column = 'DATESAMPLE'
col_missing = APIm[APIm[column].notnull()]         
prev_val = sum(APIm[column].notnull())

for x,API_count in enumerate(col_missing['API']):
    slices = APIm[APIm.API.isin([API_count])]
    slices = slices.sort_values(by=[column]).reset_index()
        
    print(slices.loc[:,['index','DATESAMPLE','TDSUSGS']])
    
    if x == 200:
        break
---------------------------------------------------------------------    
"""  

"""
---------------------------------------------------------------------
# how did water TDS change geospatially and over time? USE TDSUSGS only

Idea of implementation: fill in the missing dates (only 2456/6958 values are given, rest need to be filled in afterwards)
Maybe can check the dates of the different surveys under pdf files for more info;
or can check if the datesample times are regular?
or can it be machine-learned using the 2456 values?
---------------------------------------------------------------------



for API_time in API_orig.index:
    time_shots = APIm[APIm.API.isin([API_time])]
    time_shots.sort_values(by=['DATESAMPLE'])




rng= np.random.RandomState(0)
colors = rng.rand(2618)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(API_orig.LONGITUDE, API_orig.LATITUDE, neg_Depth, c=colors, cmap='viridis',s=60)

plt.figure()
sns.scatterplot(x=API_orig.LONGITUDE, y=API_orig.LATITUDE, hue=API_orig.TDSUSGS)
plt.tight_layout()
plt.show()



---------------------------------------------------------------------

miss_well_fill_1 = APIm[APIm.API.isin([lat_missing.iloc[0,2]])]
miss_well_fill_2 = APIm[APIm.API.isin([lat_missing.iloc[-1,2]])]

# need to add here a general method for adding the last well 8050's lat and long

# filling in the missing lat/lon data using previous data
scalar_lat = APIm.loc[1360,'LATITUDE']
scalar_lon = APIm.loc[1360,'LONGITUDE']
APIm['LATITUDE'].fillna(value=scalar_lat, inplace=True) 
APIm['LONGITUDE'].fillna(value=scalar_lon,inplace=True) 

# there are 4373 rows where DEPTHUPPER is missing, 2585 are present 

Idea of implementation: can the depths be guessed from previous data of similar APIs?
the rest of them can be machine-learned using formation name, lithology, TDS and previous data?


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
    
    
            miss_well_fill['DEPTHUPPER'] = eureka_upper
            miss_well_fill['DEPTHLOWER'] = eureka_lower
            print(miss_well_fill[['DEPTHUPPER','DEPTHLOWER']])
            
    
# none of the values match on their well numbers
---------------------------------------------------------------------            

"""


