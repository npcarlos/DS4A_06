# Imports
import datetime
import matplotlib.dates as mdates
import os
import pandas as pd
import numpy as np

# Loading datasets
uber_2014_file = os.path.join(os.getcwd(),'Datathon/Dataset/Dataset/uber_trips_2014.csv') 
Uber2014 = pd.read_csv(uber_2014_file)

uber_2015_file = os.path.join(os.getcwd(),'Datathon/Dataset/Dataset/uber_trips_2015.csv') 
Uber2015 = pd.read_csv(uber_2015_file)

zones_file = os.path.join(os.getcwd(),'Datathon/Dataset/Dataset/zones.csv') 
zones = pd.read_csv(zones_file)


demographics_file = os.path.join(os.getcwd(),'Datathon/Dataset/Dataset/demographics.csv') 
demographics = pd.read_csv(demographics_file)

geographic_file = os.path.join(os.getcwd(),'Datathon/Dataset/Dataset/geographic.csv') 
geographic = pd.read_csv(geographic_file)


weather_file = os.path.join(os.getcwd(),'Datathon/Dataset/Dataset/weather.csv') 
weather = pd.read_csv(weather_file)
weather['date'] = weather['date'].apply(lambda row: datetime.datetime.strptime(row, "%m/%d/%y"))


# Cleaning scripts

