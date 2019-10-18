import pandas as pd
import numpy as np
import datetime
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.geometry import Point
import geoplot as gplt

Uber2015=pd.read_csv('uber_trips_2015.csv')
Uber2014=pd.read_csv('uber_trips_2014.csv')
Demographics=pd.read_csv('demographics.csv')
Geographics=pd.read_csv('geographic.csv')
Green=pd.read_csv('green_trips_new_2.csv')
Subway=pd.read_csv('mta_trips.csv')
Weather=pd.read_csv('weather.csv') 
Yellow=pd.read_csv('yellow_trips_new.csv')
Zones=pd.read_csv('zones.csv')

TransportCols =['TransportType','PickDateTime','DropDateTime','PickNTA','DropNTA','Borough','Year','PickHour','DropHour',
                'Distance','DeltaTime','Cost','MaxTemp','MinTemp','AvgTemp','Precipitation','Snowfall','SnowDepth','WeekDay']

NTA=Geographics.copy()

## Make list of NTA columns

Boro=NTA.columns

# Create the GeoDataframe Object of each NTA polygon

NTAmap = gpd.GeoDataFrame()
c=0
for i in Boro:
    temp=NTA[i].dropna()
    m=temp.shape[0]
    l=[]
    for j in range(0,m,2):
        l.append((temp[j],temp[j+1]))
    
    poly = Polygon(l)
    
    NTAmap.loc[c, 'geometry'] = poly
    NTAmap.loc[c,'NTA']= i
    c= c+1

date=[]

#Uber 2014

for i in Uber2014['pickup_datetime']:
    try:
        temp=datetime.datetime.strptime(i, "%m/%d/%y %H:%M")
    except:
        temp=datetime.datetime.strptime(i, "%m/%d/%Y %H:%M:%S")
    
    date.append(temp)

Uber2014['PickDateTime']=date

Uber2014['PickHour']=Uber2014['PickDateTime'].apply(lambda x: x.hour)
Uber2014['Year']=Uber2014['PickDateTime'].apply(lambda x: x.year)
Uber2014['WeekDay']=Uber2014['PickDateTime'].apply(lambda x: x.weekday())
Uber2014['TransportType']='Uber'

Uber2014['PickGeoPoint']=Uber2014.apply(lambda row: Point(row['pickup_longitude'],row['pickup_latitude']),axis=1)
Uber2014PickPoints = gpd.GeoDataFrame()
Uber2014PickPoints['geometry']=Uber2014['PickGeoPoint'].copy()
UMergePoints=gpd.sjoin(Uber2014PickPoints,NTAmap, how="left",op='within')
Uber2014['PickNTA']=UMergePoints['NTA']

#Uber 2015
Uber2015['PickDateTime']=pd.to_datetime(Uber2015['pickup_datetime'], format='%Y-%m-%d %H:%M')

Uber2015['PickHour']=Uber2015['PickDateTime'].apply(lambda x: x.hour)
Uber2015['Year']=Uber2015['PickDateTime'].apply(lambda x: x.year)
Uber2015['WeekDay']=Uber2015['PickDateTime'].apply(lambda x: x.weekday())
Uber2015['TransportType']='Uber'
Uber2015=pd.merge(Uber2015,Zones[['location_id','nta_code']], how='left', left_on='pickup_location_id',right_on='location_id')
Uber2015.rename(columns={"nta_code": "PickNTA"})

#Green

Green['PickDateTime']=pd.to_datetime(Green['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
Green['DropDateTime']=pd.to_datetime(Green['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
Green['PickHour']=Green['PickDateTime'].apply(lambda x: x.hour)
Green['Year']=Green['PickDateTime'].apply(lambda x: x.year)
Green['WeekDay']=Green['PickDateTime'].apply(lambda x: x.weekday())
Green['TransportType']='Green'
Green['DeltaTime']=Green['DropDateTime']-Green['PickDateTime']

Green['PickGeoPoint']=Green.apply(lambda row: Point(row['pickup_longitude'],row['pickup_latitude']),axis=1)
GreenPickPoints = gpd.GeoDataFrame()
GreenPickPoints['geometry']=Green['PickGeoPoint'].copy()
GPMergePoints=gpd.sjoin(GreenPickPoints,NTAmap, how="left",op='within')
Green['PickNTA']=GPMergePoints['NTA']



Green['DropGeoPoint']=Green.apply(lambda row: Point(row['dropoff_longitude'],row['dropoff_latitude']),axis=1)
GreenDropPoints = gpd.GeoDataFrame()
GreenDropPoints['geometry']=Green['DropGeoPoint'].copy()
GDMergePoints=gpd.sjoin(GreenDropPoints,NTAmap, how="left",op='within')
Green['DropNTA']=GDMergePoints['NTA']

#Yellow

Yellow['PickDateTime']=pd.to_datetime(Yellow['pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
Yellow['DropDateTime']=pd.to_datetime(Yellow['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
Yellow['PickHour']=Yellow['PickDateTime'].apply(lambda x: x.hour)
Yellow['Year']=Yellow['PickDateTime'].apply(lambda x: x.year)
Yellow['WeekDay']=Yellow['PickDateTime'].apply(lambda x: x.weekday())
Yellow['DeltaTime']=Yellow['DropDateTime']-Yellow['PickDateTime']
Yellow['TransportType']='Yellow'

Yellow['PickGeoPoint']=Yellow.apply(lambda row: Point(row['pickup_longitude'],row['pickup_latitude']),axis=1)
YellowPickPoints = gpd.GeoDataFrame()
YellowPickPoints['geometry']=Yellow['PickGeoPoint'].copy()
YPMergePoints=gpd.sjoin(YellowPickPoints,NTAmap, how="left",op='within')
Yellow['PickNTA']=YPMergePoints['NTA']



Yellow['DropGeoPoint']=Yellow.apply(lambda row: Point(row['dropoff_longitude'],row['dropoff_latitude']),axis=1)
YellowDropPoints = gpd.GeoDataFrame()
YellowDropPoints['geometry']=Yellow['DropGeoPoint'].copy()
YDMergePoints=gpd.sjoin(YellowDropPoints,NTAmap, how="left",op='within')
Yellow['DropNTA']=YDMergePoints['NTA']



#Map
sfont=20
NTAmap.plot(alpha=0.5, figsize=(15,11.27), edgecolor='k')
plt.title("New York NTA Map",fontsize=sfont)

plt.xlabel("Longitude [°]",fontsize=sfont)
plt.ylabel("Latitude [°]",fontsize=sfont)